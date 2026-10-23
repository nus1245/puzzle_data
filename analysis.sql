-- =====================================================================
-- 수리 프로세스 데이터 분석 (repair_db.repair_logs)
-- IDE 내 SQLTools 확장 프로그램을 통해 상단의 [Run on active connection]을
-- 클릭하여 쿼리를 즉시 실행할 수 있습니다.
-- =====================================================================
USE `repair_db`;
-- ---------------------------------------------------------------------
-- 1. 데이터 정상 적재 및 기본 볼륨 검증
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS total_rows,
    COUNT(DISTINCT caseID) AS total_cases,
    MIN(clean_timestamp) AS first_event,
    MAX(clean_timestamp) AS last_event
FROM repair_logs;
-- ---------------------------------------------------------------------
-- 1-1. [데이터 정합성 검증] 작업별 피벗(Pivot) 및 소요시간(Complete - Start) 음수 탐색
--      각 작업의 시작(start)과 종료(complete) 시각을 피벗하여 소요시간을 계산하고,
--      시간 역전(complete < start) 등 정합성 위배 음수 케이스가 존재하는지 검증
-- ---------------------------------------------------------------------
WITH NumberedEvents AS (
    SELECT caseID,
        taskID,
        eventtype,
        clean_timestamp,
        -- 동일 작업이 재작업(Rework)된 경우를 고려하여 1:1 회차(attempt) 번호 매핑
        ROW_NUMBER() OVER (
            PARTITION BY caseID,
            taskID,
            eventtype
            ORDER BY clean_timestamp,
                seq,
                sub_seq
        ) AS attempt
    FROM repair_logs
    WHERE eventtype IN ('start', 'complete')
),
TaskPivot AS (
    SELECT caseID,
        taskID,
        attempt,
        -- 피벗(Pivot): start 시각과 complete 시각을 컬럼으로 회전
        MAX(
            CASE
                WHEN eventtype = 'start' THEN clean_timestamp
            END
        ) AS start_time,
        MAX(
            CASE
                WHEN eventtype = 'complete' THEN clean_timestamp
            END
        ) AS complete_time
    FROM NumberedEvents
    GROUP BY caseID,
        taskID,
        attempt
    HAVING start_time IS NOT NULL
        AND complete_time IS NOT NULL
)
SELECT caseID,
    taskID,
    attempt,
    start_time,
    complete_time,
    -- COMPLETE - START 소요시간 (분 및 시간 단위)
    TIMESTAMPDIFF(MINUTE, start_time, complete_time) AS duration_minutes,
    ROUND(
        TIMESTAMPDIFF(SECOND, start_time, complete_time) / 3600.0,
        2
    ) AS duration_hours,
    CASE
        WHEN complete_time < start_time THEN '❌ 음수 (시간 역전)'
        WHEN complete_time = start_time THEN '⚡ 0분 (동시 발생)'
        ELSE '✅ 정상'
    END AS validation_status
FROM TaskPivot
ORDER BY validation_status DSEC;
-- ---------------------------------------------------------------------
-- 2. 케이스별 총 소요시간(Lead Time) 상위 지연 케이스 분석
-- ---------------------------------------------------------------------
SELECT caseID,
    MIN(clean_timestamp) AS case_start,
    MAX(clean_timestamp) AS case_end,
    COUNT(*) AS total_events,
    ROUND(
        TIMESTAMPDIFF(DAY, MIN(clean_timestamp), MAX(clean_timestamp))
    ) AS lead_time_days,
    ROUND(
        TIMESTAMPDIFF(
            MINUTE,
            MIN(clean_timestamp),
            MAX(clean_timestamp)
        ) / 60.0,
        1
    ) AS lead_time_hours
FROM repair_logs
GROUP BY caseID
ORDER BY lead_time_days DESC,
    lead_time_hours DESC
LIMIT 20;
-- ---------------------------------------------------------------------
-- 3. 3대 업무 그룹(접수/현장/정산) 및 수행 주체(사람 vs 시스템)별 업무 비중
-- ---------------------------------------------------------------------
SELECT task_group,
    SUBJECT,
    taskID,
    COUNT(*) AS event_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY task_group),
        1
    ) AS group_ratio_pct
FROM repair_logs
GROUP BY task_group,
    SUBJECT,
    taskID
ORDER BY FIELD(task_group, '접수', '현장', '정산'),
    event_count DESC;
-- ---------------------------------------------------------------------
-- 4. 수리 방식별(사내 수리 vs 외주 위탁 vs 즉시 수리) 리드타임 비교
-- ---------------------------------------------------------------------
WITH CaseRepairSummary AS (
    SELECT caseID,
        MAX(
            CASE
                WHEN taskID = 'ExternRepair' THEN '외주수리(Extern)'
                WHEN taskID = 'InternRepair' THEN '사내수리(Intern)'
                WHEN taskID = 'ImmediateRepair' THEN '즉시수리(Immediate)'
                ELSE '기타'
            END
        ) AS repair_mode,
        TIMESTAMPDIFF(
            DAY,
            MIN(clean_timestamp),
            MAX(clean_timestamp)
        ) AS lead_time_days,
        TIMESTAMPDIFF(
            HOUR,
            MIN(clean_timestamp),
            MAX(clean_timestamp)
        ) / 24 AS lead_time_TIMES
    FROM repair_logs
    WHERE taskID = '현장'
    GROUP BY caseID
)
SELECT repair_mode,
    COUNT(*) AS case_count,
    ROUND(AVG(lead_time_days), 2) AS avg_lead_days,
    ROUND(MIN(lead_time_days), 2) AS min_lead_days,
    ROUND(MAX(lead_time_days), 2) AS max_lead_days
FROM CaseRepairSummary
GROUP BY repair_mode
ORDER BY avg_lead_days DESC;
-- ---------------------------------------------------------------------
-- 5. [병목 탐색] 단계 간 이동 시간 및 대기시간(Waiting Time) 분석
-- ---------------------------------------------------------------------
WITH EventTransitions AS (
    SELECT caseID,
        taskID AS current_task,
        clean_timestamp AS current_time,
        LEAD(taskID) OVER (
            PARTITION BY caseID
            ORDER BY clean_timestamp,
                seq,
                sub_seq
        ) AS next_task,
        LEAD(clean_timestamp) OVER (
            PARTITION BY caseID
            ORDER BY clean_timestamp,
                seq,
                sub_seq
        ) AS next_time
    FROM repair_logs
)
SELECT current_task,
    next_task,
    COUNT(*) AS transition_count,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, current_time, next_time) / 60.0
        ),
        2
    ) AS avg_waiting_hours,
    ROUND(
        MAX(
            TIMESTAMPDIFF(MINUTE, current_time, next_time) / 60.0
        ),
        2
    ) AS max_waiting_hours
FROM EventTransitions
WHERE next_task IS NOT NULL
GROUP BY current_task,
    next_task
HAVING COUNT(*) >= 10
ORDER BY avg_waiting_hours DESC;
-- ---------------------------------------------------------------------
-- 6. 담당자(originator)별 처리 건수 및 고유 케이스 수 집계
-- ---------------------------------------------------------------------
SELECT originator,
    task_group,
    COUNT(DISTINCT caseID) AS handled_cases,
    COUNT(*) AS total_actions
FROM repair_logs
WHERE SUBJECT = '사람'
GROUP BY originator,
    task_group
ORDER BY handled_cases DESC;