-- =====================================================================
-- 수리 프로세스 데이터 분석 마스터 스크립트 (repair_db.repair_logs)
-- =====================================================================
-- 본 스크립트는 네덜란드 임대 주택 수리 프로세스 데이터(repair_cleaned.csv)의
-- 전수 EDA, 데이터 정합성 검증, 비즈니스 가설 검증, n차 수리 공정 분석,
-- 그리고 케이스별 1행 원천 타임라인 마스터 뷰(case_master_view) 생성을 포함합니다.
-- =====================================================================

USE `repair_db`;

-- ---------------------------------------------------------------------
-- 1. 데이터 정상 적재 및 기본 볼륨 검증
-- ---------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT caseID) AS total_cases,
    MIN(clean_timestamp) AS first_event,
    MAX(clean_timestamp) AS last_event
FROM repair_logs;


-- ---------------------------------------------------------------------
-- 2. [데이터 정합성 검증] 작업별 피벗 및 소요시간(Complete - Start) 음수 탐색
--    각 작업의 시작(start)과 종료(complete) 시각을 피벗하여 소요시간을 계산하고,
--    시간 역전(complete < start) 등 정합성 위배 음수 케이스가 존재하는지 검증
-- ---------------------------------------------------------------------
WITH NumberedEvents AS (
    SELECT 
        caseID,
        taskID,
        eventtype,
        clean_timestamp,
        -- 동일 작업 재작업 시 1:1 회차(attempt) 매핑
        ROW_NUMBER() OVER (
            PARTITION BY caseID, taskID, eventtype
            ORDER BY clean_timestamp, seq, sub_seq
        ) AS attempt
    FROM repair_logs
    WHERE eventtype IN ('start', 'complete')
),
TaskPivot AS (
    SELECT 
        caseID,
        taskID,
        attempt,
        MAX(CASE WHEN eventtype = 'start' THEN clean_timestamp END) AS start_time,
        MAX(CASE WHEN eventtype = 'complete' THEN clean_timestamp END) AS complete_time
    FROM NumberedEvents
    GROUP BY caseID, taskID, attempt
    HAVING start_time IS NOT NULL 
       AND complete_time IS NOT NULL
)
SELECT 
    caseID,
    taskID,
    attempt,
    start_time,
    complete_time,
    TIMESTAMPDIFF(MINUTE, start_time, complete_time) AS duration_minutes,
    ROUND(TIMESTAMPDIFF(SECOND, start_time, complete_time) / 3600.0, 2) AS duration_hours,
    CASE
        WHEN complete_time < start_time THEN '시간 역전(오류)'
        WHEN complete_time = start_time THEN '동시 발생'
        ELSE '정상'
    END AS validation_status
FROM TaskPivot
ORDER BY validation_status DESC;


-- ---------------------------------------------------------------------
-- 3. 3대 업무 그룹(접수/현장/정산) 및 수행 주체(사람 vs 시스템)별 업무 비중
-- ---------------------------------------------------------------------
SELECT 
    task_group,
    SUBJECT,
    taskID,
    COUNT(*) AS event_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY task_group), 
        1
    ) AS group_ratio_pct
FROM repair_logs
GROUP BY task_group, SUBJECT, taskID
ORDER BY FIELD(task_group, '접수', '현장', '정산'), event_count DESC;


-- ---------------------------------------------------------------------
-- 4. [접수 단계 심층 분석] 접수 담당자별 현황 및 '지역 전담제' 가설 검증
-- ---------------------------------------------------------------------
-- [1차 관찰 및 가설 제기]:
-- - 정상 접수 927건, 전체 고유 주택 890채
-- - 접수 담당자별 단순 주택 집계: Dian 431채 + Monica 482채 = 913채 (중복 23채, 2.5% 미만)
-- - 수치상 중복이 매우 적어 초기에는 "특정 지역/주택 전담제로 의심"할 수 있음.
--
-- [심층 검증 (통계적 착시 규명)]:
-- 1) 전체 890채 중 855채(96.1%)는 수리가 단 1회만 발생하여 담당자가 겹칠 기회 자체가 없었음.
-- 2) 2회 이상 발생한 35채 중 무려 65.7%(23채)가 타 상담원에게 교차 접수됨 (전담제 가설 기각).
-- 3) 주택 식별 Key(0~10,000) 분포도 두 사람 모두 전 구간에 균등 분포 (평균 5,018 vs 5,143).
-- => [결론]: 전담 구역제가 아니며, 단일 접수 풀(Shared Pool)에서 순번 배분(Round-Robin) 방식으로 운영되는 통합 콜센터 체제로 규명됨.

-- 4-1. 담당자별 순수 단독 접수 vs 인계 접수 현황 집계
SELECT 
    originator,
    COUNT(DISTINCT objectKey) AS total_houses,
    COUNT(DISTINCT caseID) AS total_cases
FROM repair_logs
WHERE task_group = '접수'
  AND SUBJECT = '사람'
  AND objectKey IS NOT NULL
  AND caseID IN (
      -- 순수 1명만 참여한 caseID 목록
      SELECT caseID
      FROM repair_logs
      WHERE task_group = '접수' 
        AND SUBJECT = '사람'
      GROUP BY caseID
      HAVING COUNT(DISTINCT originator) = 1
  )
GROUP BY originator;

-- [접수 방식 요약]
-- - 순수 단독 접수: 804건 (고유 775채의 주택, Dian 377건 / Monica 427건)
-- - 담당자 간 인계 접수: 123건 (총 123채의 주택에서 발생, 인계 시 일정 조율 병목으로 대기시간 7배 급증)


-- ---------------------------------------------------------------------
-- 5. [현장 단계 심층 분석] 접수 담당자 구분에 따른 현장 인력 배정 편향 분석
-- ---------------------------------------------------------------------
-- 접수자가 Dian/Monica로 갈리더라도, 현장 기사들의 출동 구역 편향이 존재하는지 확인
WITH SingleReceiptCases AS (
    -- 단독 접수한 케이스와 해당 접수 담당자 매핑
    SELECT 
        caseID,
        MAX(originator) AS receipt_worker -- Dian 또는 Monica
    FROM repair_logs
    WHERE task_group = '접수' 
      AND SUBJECT = '사람'
    GROUP BY caseID
    HAVING COUNT(DISTINCT originator) = 1
)
SELECT 
    -- 롤업(Rollup) 총합 행의 이름을 '전체 총계'로 표기
    COALESCE(f.originator, '전체 총계') AS field_worker,
    -- Dian 접수 구역 출동 케이스 수
    COUNT(DISTINCT CASE WHEN r.receipt_worker = 'Dian' THEN f.caseID END) AS dian_area_cases,
    -- Monica 접수 구역 출동 케이스 수
    COUNT(DISTINCT CASE WHEN r.receipt_worker = 'Monica' THEN f.caseID END) AS monica_area_cases,
    -- 전체 출동 케이스 수
    COUNT(DISTINCT f.caseID) AS total_cases,
    -- Dian 구역 출동 비율 (%)
    ROUND(
        COUNT(DISTINCT CASE WHEN r.receipt_worker = 'Dian' THEN f.caseID END) * 100.0 / COUNT(DISTINCT f.caseID), 
        1
    ) AS dian_ratio_pct
FROM repair_logs f
JOIN SingleReceiptCases r ON f.caseID = r.caseID
WHERE f.task_group = '현장'
  AND f.SUBJECT = '사람'
GROUP BY f.originator WITH ROLLUP
ORDER BY GROUPING(f.originator) ASC, total_cases DESC;

-- [현장 배정 분석 결론]
-- - 현장 작업자들의 Dian 구역 출동 비율이 38% ~ 55%로 전체 평균(46.9%)에 수렴.
-- - 특정 기사가 특정 접수 건에 편향되지 않음 (Anne 50:50, Edd 51.8:48.2, John 46.2:53.8 등 균등 출동).
-- => 현장 기사 및 외주업체(FixIt, DoIt)는 구역 제한 없이 전 지역을 담당하는 완전 통합 풀링(Resource Pooling) 체제로 운영됨.


-- ---------------------------------------------------------------------
-- 6. [수리 공정 심층 분석] 1차 ➔ 2차 ➔ 3차 수리 에스컬레이션 및 재작업(Rework) 분석
-- ---------------------------------------------------------------------
-- 수리 공정 차수(1차, 2차, 3차)별 작업 유형 분석
SELECT 
    taskID,
    repair_order,
    COUNT(*) AS cnt,
    ROUND(COUNT(*) * 100.0 / 927.0, 1) AS pct_of_total_repairs
FROM (
    SELECT 
        caseID,
        taskID,
        originator,
        MIN(clean_timestamp) AS task_start,
        MAX(clean_timestamp) AS task_complete,
        DENSE_RANK() OVER (
            PARTITION BY caseID 
            ORDER BY MIN(clean_timestamp), seq
        ) AS repair_order
    FROM repair_logs
    WHERE taskID IN ('InternRepair', 'ExternRepair', 'ImmediateRepair')
    GROUP BY caseID, taskID, originator, seq
) t
GROUP BY taskID, repair_order
ORDER BY taskID DESC, repair_order;

-- [수리 에스컬레이션 결론]
-- 1. 1차 수리 종결률 87.4% (810건): 대부분 1차에서 완료 (즉시 383건, 사내 485건, 외주 59건)
-- 2. 2차 수리 전환율 12.6% (117건):
--    - 사내 재수리 49건: 즉시수리 후 사내연계(23건) + 사내 재방문 품질 하자 재작업(26건)
--    - 외주 전환 68건: 즉시수리 실패(38건) + 사내수리 실패(30건) 후 외주 이관
-- 3. 3차 수리 전환율 0.6% (6건): 2차 수리 건 중 5.1%가 3차까지 장기화 (외주 5건, 사내재수리 1건)


-- ---------------------------------------------------------------------
-- 7. [케이스 마스터 피벗 뷰] 케이스(caseID)별 1행 원천 타임라인 뷰 생성
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW case_master_view AS
WITH RepairTaskEvents AS (
    -- 1. 수리 작업별 시작 및 완료 시각 정돈 (외주수리는 RepairReady 완료 시점 매핑)
    SELECT 
        r.caseID,
        r.taskID,
        r.originator,
        r.seq,
        MIN(r.clean_timestamp) AS start_time,
        CASE 
            WHEN r.taskID = 'ExternRepair' THEN (
                SELECT MIN(rr.clean_timestamp) 
                FROM repair_logs rr 
                WHERE rr.caseID = r.caseID AND rr.taskID = 'RepairReady'
            )
            ELSE MAX(r.clean_timestamp)
        END AS end_time
    FROM repair_logs r
    WHERE r.taskID IN ('InternRepair', 'ExternRepair', 'ImmediateRepair')
    GROUP BY r.caseID, r.taskID, r.originator, r.seq
),
RankedRepairs AS (
    -- 2. 케이스 내 수리 순번(1차, 2차, 3차 수리) 부여
    SELECT 
        caseID,
        taskID,
        originator,
        start_time,
        end_time,
        DENSE_RANK() OVER (
            PARTITION BY caseID 
            ORDER BY start_time, seq
        ) AS repair_order
    FROM RepairTaskEvents
),
PivotedRepairs AS (
    -- 3. 1~3차 수리 공정을 케이스당 1행으로 사전 피벗 (담당자 충돌 회피 및 1:1 조인 보장)
    SELECT 
        caseID,
        -- 1차 수리 공정 (모든 수리 케이스 927건 전수 존재)
        MAX(CASE WHEN repair_order = 1 THEN taskID END)     AS rep1_task,
        MAX(CASE WHEN repair_order = 1 THEN originator END) AS rep1_worker,
        MAX(CASE WHEN repair_order = 1 THEN start_time END) AS rep1_start,
        MAX(CASE WHEN repair_order = 1 THEN end_time END)   AS rep1_complete,
        
        -- 2차 수리 공정 (외주전환/재작업 117건만 값 존재, 나머지는 NULL)
        MAX(CASE WHEN repair_order = 2 THEN taskID END)     AS rep2_task,
        MAX(CASE WHEN repair_order = 2 THEN originator END) AS rep2_worker,
        MAX(CASE WHEN repair_order = 2 THEN start_time END) AS rep2_start,
        MAX(CASE WHEN repair_order = 2 THEN end_time END)   AS rep2_complete,

        -- 3차 수리 공정 (3단계 장기 에스컬레이션 6건만 값 존재, 나머지는 NULL)
        MAX(CASE WHEN repair_order = 3 THEN taskID END)     AS rep3_task,
        MAX(CASE WHEN repair_order = 3 THEN originator END) AS rep3_worker,
        MAX(CASE WHEN repair_order = 3 THEN start_time END) AS rep3_start,
        MAX(CASE WHEN repair_order = 3 THEN end_time END)   AS rep3_complete
    FROM RankedRepairs
    GROUP BY caseID
)
SELECT 
    l.caseID,
    
    -- -----------------------------------------------------------------
    -- 1. [인입 및 접수 섹션]
    -- -----------------------------------------------------------------
    MAX(l.contact)                                                      AS contact_channel,        -- 고객 인입 채널 (Phone, Web, Letter, Personal)
    MAX(l.objectKey)                                                    AS objectKey,              -- 수리 대상 주택 번호 (890채)
    MAX(l.RepairType)                                                   AS planned_repair_type,    -- 티켓 발행 시 상담원의 1차 계획 코드 (P, E, B)
    
    -- 최초 응대 (FirstContact)
    MAX(CASE WHEN l.taskID = 'FirstContact' THEN l.originator END)      AS contact_worker,         -- 최초 접수 상담원 (Dian, Monica)
    MIN(CASE WHEN l.taskID = 'FirstContact' THEN l.clean_timestamp END)  AS contact_time,           -- 최초 인입 접수 시각
    
    -- 티켓 발행 (MakeTicket)
    MAX(CASE WHEN l.taskID = 'MakeTicket' THEN l.originator END)        AS ticket_worker,          -- 전산 티켓 발행자
    MAX(CASE WHEN l.taskID = 'MakeTicket' AND l.eventtype = 'start'    THEN l.clean_timestamp END) AS ticket_start,
    MAX(CASE WHEN l.taskID = 'MakeTicket' AND l.eventtype = 'complete' THEN l.clean_timestamp END) AS ticket_complete,
    
    -- 방문 일정 조율 (ArrangeSurvey)
    MAX(CASE WHEN l.taskID = 'ArrangeSurvey' THEN l.originator END)      AS survey_arrange_worker,  -- 점검 일정 조율 담당자
    MAX(CASE WHEN l.taskID = 'ArrangeSurvey' AND l.eventtype = 'start'    THEN l.clean_timestamp END) AS survey_arrange_start,
    MAX(CASE WHEN l.taskID = 'ArrangeSurvey' AND l.eventtype = 'complete' THEN l.clean_timestamp END) AS survey_arrange_complete,
    
    -- 고객 일정 통보 및 오접수 취소 알림
    MAX(CASE WHEN l.taskID = 'InformClientSurvey'     THEN l.clean_timestamp END) AS inform_survey_time, -- 고객에게 확정 일정 안내 시각
    MAX(CASE WHEN l.taskID = 'InformClientWrongPlace' THEN l.clean_timestamp END) AS wrong_place_time,   -- 오접수 조기 종료 안내 시각 (73건)

    -- -----------------------------------------------------------------
    -- 2. [현장 점검 및 n차 수리 공정 섹션]
    -- -----------------------------------------------------------------
    -- 현장 실사 및 점검 (Survey)
    MAX(CASE WHEN l.taskID = 'Survey' THEN l.originator END)            AS survey_worker,          -- 현장 실사 기사 (Anne, Cindy 등)
    MIN(CASE WHEN l.taskID = 'Survey' THEN l.clean_timestamp END)        AS survey_start,           -- 현장 점검 시작 시각
    MAX(CASE WHEN l.taskID = 'Survey' THEN l.clean_timestamp END)        AS survey_complete,        -- 현장 점검 완료 시각
    MAX(l.RepairInternally)                                             AS repair_internally,      -- 기사 실사 후 사내수리 가능 여부 판정 (1: 사내, 0: 외주)
    MAX(l.RepairCode)                                                   AS repair_code,            -- 고장 부위/유형 코드
    MAX(l.EstimatedRepairTime)                                          AS estimated_hours,        -- 기사 실측 예상 소요시간
    
    -- 1차 수리 공정
    r.rep1_task,                                                                                   -- 1차 수리 종류 (Immediate, Intern, Extern)
    r.rep1_worker,                                                                                 -- 1차 수리 기사/업체
    r.rep1_start,                                                                                  -- 1차 수리 시작 시각
    r.rep1_complete,                                                                               -- 1차 수리 완료 시각
    
    -- 2차 수리 공정 (외주전환/재작업 117건만 값 존재, 나머지는 NULL)
    r.rep2_task,                                                                                   -- 2차 수리 종류
    r.rep2_worker,                                                                                 -- 2차 수리 기사/업체
    r.rep2_start,                                                                                  -- 2차 수리 시작 시각
    r.rep2_complete,                                                                               -- 2차 수리 완료 시각

    -- 3차 수리 공정 (3단계 장기 에스컬레이션 6건만 값 존재, 나머지는 NULL)
    r.rep3_task,                                                                                   -- 3차 수리 종류
    r.rep3_worker,                                                                                 -- 3차 수리 기사/업체
    r.rep3_start,                                                                                  -- 3차 수리 시작 시각
    r.rep3_complete,                                                                               -- 3차 수리 완료 시각
    
    -- 최종 현장 수리 마감 (RepairReady)
    MAX(CASE WHEN l.taskID = 'RepairReady' THEN l.clean_timestamp END)  AS repair_ready_time,      -- 현장 수리 작업 완전 마감 시각

    -- -----------------------------------------------------------------
    -- 3. [비용 결제 및 티켓 마감 섹션 (Billing)]
    -- -----------------------------------------------------------------
    -- 수리 완료 직후 시스템이 비동기 병렬로 처리하는 전산 자동화 공정
    MAX(CASE WHEN l.task_group = '정산' THEN l.originator END)         AS billing_worker,         -- 자동화 수행 주체 (System)
    MAX(CASE WHEN l.taskID = 'ReadyInformClient'     THEN l.clean_timestamp END) AS client_inform_time, -- 고객 완료 알림 시각
    MAX(CASE WHEN l.taskID = 'SendTicketToFinAdmin' THEN l.clean_timestamp END) AS fin_commit_time,     -- 재무부 전송 시각
    MAX(CASE WHEN l.taskID = 'TicketReady'          THEN l.clean_timestamp END) AS ticket_ready_time,   -- 두 조건 완료(AND-Join) 후 최종 티켓 종결 시각
    
    -- 병렬작업 선행 관계 판별 (고객 알림이 먼저 끝났는가 vs 재무 승인이 먼저 끝났는가)
    CASE 
        WHEN MAX(CASE WHEN l.taskID = 'ReadyInformClient' THEN l.clean_timestamp END) < 
             MAX(CASE WHEN l.taskID = 'SendTicketToFinAdmin' THEN l.clean_timestamp END) THEN '고객 선행'
        WHEN MAX(CASE WHEN l.taskID = 'SendTicketToFinAdmin' THEN l.clean_timestamp END) < 
             MAX(CASE WHEN l.taskID = 'ReadyInformClient' THEN l.clean_timestamp END) THEN '승인 선행'
        WHEN MAX(CASE WHEN l.taskID = 'ReadyInformClient' THEN l.clean_timestamp END) = 
             MAX(CASE WHEN l.taskID = 'SendTicketToFinAdmin' THEN l.clean_timestamp END) THEN '동일'
        ELSE NULL 
    END AS billing_precedence,

    -- -----------------------------------------------------------------
    -- 4. [케이스 전체 요약 타임라인]
    -- -----------------------------------------------------------------
    MIN(l.clean_timestamp)                                              AS case_start_time,        -- 케이스 최초 유입 시각
    MAX(l.clean_timestamp)                                              AS case_end_time,          -- 케이스 최종 종결 시각
    COUNT(*)                                                            AS total_events            -- 케이스 내 총 이벤트 수
FROM repair_logs l
LEFT JOIN PivotedRepairs r ON l.caseID = r.caseID
GROUP BY l.caseID, 
    r.rep1_task, r.rep1_worker, r.rep1_start, r.rep1_complete,
    r.rep2_task, r.rep2_worker, r.rep2_start, r.rep2_complete,
    r.rep3_task, r.rep3_worker, r.rep3_start, r.rep3_complete
ORDER BY l.caseID;


-- ---------------------------------------------------------------------
-- 8. [마스터 뷰 활용 예시] 주요 공정별 소요시간 및 병목 분석 쿼리들
-- ---------------------------------------------------------------------

-- 8-1. 주요 공정별 순수 소요시간 및 대기시간 산출
SELECT 
    caseID,
    contact_channel,
    planned_repair_type,
    rep1_task,
    -- 1) 티켓 발행 소요시간 (분)
    TIMESTAMPDIFF(MINUTE, ticket_start, ticket_complete) AS ticket_duration_min,
    -- 2) 방문 일정 조율 소요시간 (분)
    TIMESTAMPDIFF(MINUTE, survey_arrange_start, survey_arrange_complete) AS arrange_duration_min,
    -- 3) 접수 완료 ➔ 현장 점검 시작까지 대기시간 (시간)
    ROUND(TIMESTAMPDIFF(MINUTE, inform_survey_time, survey_start) / 60.0, 1) AS wait_until_survey_hours,
    -- 4) 현장 점검 소요시간 (분)
    TIMESTAMPDIFF(MINUTE, survey_start, survey_complete) AS survey_duration_min,
    -- 5) 1차 수리 순수 소요시간 (시간)
    ROUND(TIMESTAMPDIFF(MINUTE, rep1_start, rep1_complete) / 60.0, 1) AS rep1_duration_hours,
    -- 6) 케이스 전체 총 소요시간 (Lead Time 일수)
    ROUND(TIMESTAMPDIFF(MINUTE, case_start_time, case_end_time) / 1440.0, 2) AS total_lead_days
FROM case_master_view
LIMIT 20;

-- 8-2. 1차 수리 실패 후 2차 수리 전환 대기시간(Waiting Time) 분석 (117건 대상)
SELECT 
    rep1_task,
    rep2_task,
    COUNT(*) AS case_count,
    ROUND(AVG(TIMESTAMPDIFF(MINUTE, rep1_complete, rep2_start) / 60.0), 1) AS avg_handover_wait_hours,
    ROUND(MAX(TIMESTAMPDIFF(MINUTE, rep1_complete, rep2_start) / 60.0), 1) AS max_handover_wait_hours
FROM case_master_view
WHERE rep2_task IS NOT NULL
GROUP BY rep1_task, rep2_task
ORDER BY case_count DESC;

-- 8-3. 비용결제(Billing) 병렬 처리 선행 유형별 케이스 비중
SELECT 
    billing_precedence,
    COUNT(*) AS case_count,
    ROUND(COUNT(*) * 100.0 / 927.0, 1) AS ratio_pct
FROM case_master_view
WHERE billing_precedence IS NOT NULL
GROUP BY billing_precedence;