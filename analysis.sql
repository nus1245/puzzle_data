-- =====================================================================
-- 수리 프로세스 데이터 분석 마스터 스크립트 (repair_db.repair_logs)
-- =====================================================================
-- 본 스크립트는 네덜란드 임대 주택 수리 프로세스 데이터(repair_cleaned.csv)의
-- 전수 EDA, 데이터 정합성 검증, 비즈니스 가설 검증, n차 수리 공정 분석,
-- 그리고 케이스별 1행 원천 타임라인 마스터 뷰(case_master_view) 생성을 포함합니다.
-- =====================================================================
USE `repair_db`;
-- ---------------------------------------------------------------------
--  데이터 정상 적재 및 기본 볼륨 검증
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS total_rows,
    COUNT(DISTINCT caseID) AS total_cases,
    MIN(clean_timestamp) AS first_event,
    MAX(clean_timestamp) AS last_event,
    COUNT(DISTINCT objectKey) AS distinct_houses,
    (
        SELECT COUNT(DISTINCT caseID)
        FROM repair_logs
        WHERE objectKey IS NOT NULL
    ) AS CNT
FROM repair_logs;
-- ---------------------------------------------------------------------
-- [데이터 정합성 검증] 작업별 피벗 및 소요시간(Complete - Start) 음수 탐색
--    각 작업의 시작(start)과 종료(complete) 시각을 피벗하여 소요시간을 계산하고,
--    시간 역전(complete < start) 등 정합성 위배 음수 케이스가 존재하는지 검증
-- ---------------------------------------------------------------------
WITH NumberedEvents AS (
    SELECT caseID,
        taskID,
        eventtype,
        clean_timestamp,
        -- 동일 작업 재작업 시 1:1 회차(attempt) 매핑
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
    TIMESTAMPDIFF(MINUTE, start_time, complete_time) AS duration_minutes,
    ROUND(
        TIMESTAMPDIFF(SECOND, start_time, complete_time) / 3600.0,
        2
    ) AS duration_hours,
    CASE
        WHEN complete_time < start_time THEN '시간 역전(오류)'
        WHEN complete_time = start_time THEN '동시 발생'
        ELSE '정상'
    END AS validation_status
FROM TaskPivot
ORDER BY validation_status DESC;
-- ---------------------------------------------------------------------
-- 7. [케이스 마스터 피벗 뷰] 케이스(caseID)별 1행 타임라인 뷰(피벗 처리) 생성
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW case_master_view AS WITH RepairTaskEvents AS (
        -- 1. 수리 작업별 시작 및 완료 시각 정돈 (외주수리는 RepairReady 완료 시점 매핑)
        SELECT r.caseID,
            r.taskID,
            r.originator,
            r.seq,
            MIN(r.clean_timestamp) AS start_time,
            CASE
                WHEN r.taskID = 'ExternRepair' THEN (
                    SELECT MIN(rr.clean_timestamp)
                    FROM repair_logs rr
                    WHERE rr.caseID = r.caseID
                        AND rr.taskID = 'RepairReady'
                )
                ELSE MAX(r.clean_timestamp)
            END AS end_time
        FROM repair_logs r
        WHERE r.taskID IN (
                'InternRepair',
                'ExternRepair',
                'ImmediateRepair'
            )
        GROUP BY r.caseID,
            r.taskID,
            r.originator,
            r.seq
    ),
    RankedRepairs AS (
        -- 2. 케이스 내 수리 순번(1차, 2차, 3차 수리) 부여
        SELECT caseID,
            taskID,
            originator,
            start_time,
            end_time,
            DENSE_RANK() OVER (
                PARTITION BY caseID
                ORDER BY start_time,
                    seq
            ) AS repair_order
        FROM RepairTaskEvents
    ),
    PivotedRepairs AS (
        -- 3. 1~3차 수리 공정을 케이스당 1행으로 사전 피벗 (담당자 충돌 회피 및 1:1 조인 보장)
        SELECT caseID,
            -- 1차 수리 공정 (모든 수리 케이스 927건 전수 존재)
            MAX(
                CASE
                    WHEN repair_order = 1 THEN taskID
                END
            ) AS rep1_task,
            MAX(
                CASE
                    WHEN repair_order = 1 THEN originator
                END
            ) AS rep1_worker,
            MAX(
                CASE
                    WHEN repair_order = 1 THEN start_time
                END
            ) AS rep1_start,
            MAX(
                CASE
                    WHEN repair_order = 1 THEN end_time
                END
            ) AS rep1_complete,
            -- 2차 수리 공정 (외주전환/재작업 117건만 값 존재, 나머지는 NULL)
            MAX(
                CASE
                    WHEN repair_order = 2 THEN taskID
                END
            ) AS rep2_task,
            MAX(
                CASE
                    WHEN repair_order = 2 THEN originator
                END
            ) AS rep2_worker,
            MAX(
                CASE
                    WHEN repair_order = 2 THEN start_time
                END
            ) AS rep2_start,
            MAX(
                CASE
                    WHEN repair_order = 2 THEN end_time
                END
            ) AS rep2_complete,
            -- 3차 수리 공정 (3단계 장기 에스컬레이션 6건만 값 존재, 나머지는 NULL)
            MAX(
                CASE
                    WHEN repair_order = 3 THEN taskID
                END
            ) AS rep3_task,
            MAX(
                CASE
                    WHEN repair_order = 3 THEN originator
                END
            ) AS rep3_worker,
            MAX(
                CASE
                    WHEN repair_order = 3 THEN start_time
                END
            ) AS rep3_start,
            MAX(
                CASE
                    WHEN repair_order = 3 THEN end_time
                END
            ) AS rep3_complete
        FROM RankedRepairs
        GROUP BY caseID
    )
SELECT l.caseID,
    -- -----------------------------------------------------------------
    -- 1. [인입 및 접수 섹션]
    -- -----------------------------------------------------------------
    MAX(l.contact) AS contact_channel,
    -- 고객 인입 채널 (Phone, Web, Letter, Personal)
    MAX(l.objectKey) AS objectKey,
    -- 수리 대상 주택 번호 (890채)
    MAX(l.RepairType) AS planned_repair_type,
    -- 티켓 발행 시 상담원의 1차 계획 코드 (P, E, B)
    -- 최초 응대 (FirstContact)
    MAX(
        CASE
            WHEN l.taskID = 'FirstContact' THEN l.originator
        END
    ) AS contact_worker,
    -- 최초 접수 상담원 (Dian, Monica)
    MIN(
        CASE
            WHEN l.taskID = 'FirstContact' THEN l.clean_timestamp
        END
    ) AS contact_time,
    -- 최초 인입 접수 시각
    -- 티켓 발행 (MakeTicket)
    MAX(
        CASE
            WHEN l.taskID = 'MakeTicket' THEN l.originator
        END
    ) AS ticket_worker,
    -- 전산 티켓 발행자
    MAX(
        CASE
            WHEN l.taskID = 'MakeTicket'
            AND l.eventtype = 'start' THEN l.clean_timestamp
        END
    ) AS ticket_start,
    MAX(
        CASE
            WHEN l.taskID = 'MakeTicket'
            AND l.eventtype = 'complete' THEN l.clean_timestamp
        END
    ) AS ticket_complete,
    -- 방문 일정 조율 (ArrangeSurvey)
    MAX(
        CASE
            WHEN l.taskID = 'ArrangeSurvey' THEN l.originator
        END
    ) AS survey_arrange_worker,
    -- 점검 일정 조율 담당자
    MAX(
        CASE
            WHEN l.taskID = 'ArrangeSurvey'
            AND l.eventtype = 'start' THEN l.clean_timestamp
        END
    ) AS survey_arrange_start,
    MAX(
        CASE
            WHEN l.taskID = 'ArrangeSurvey'
            AND l.eventtype = 'complete' THEN l.clean_timestamp
        END
    ) AS survey_arrange_complete,
    -- 고객 일정 통보 및 오접수 취소 알림
    MAX(
        CASE
            WHEN l.taskID = 'InformClientSurvey' THEN l.clean_timestamp
        END
    ) AS inform_survey_time,
    -- 고객에게 확정 일정 안내 시각
    MAX(
        CASE
            WHEN l.taskID = 'InformClientWrongPlace' THEN l.clean_timestamp
        END
    ) AS wrong_place_time,
    -- 오접수 조기 종료 안내 시각 (73건)
    -- -----------------------------------------------------------------
    -- 2. [현장 점검 및 n차 수리 공정 섹션]
    -- -----------------------------------------------------------------
    -- 현장 실사 및 점검 (Survey)
    MAX(
        CASE
            WHEN l.taskID = 'Survey' THEN l.originator
        END
    ) AS survey_worker,
    -- 현장 실사 기사 (Anne, Cindy 등)
    MIN(
        CASE
            WHEN l.taskID = 'Survey' THEN l.clean_timestamp
        END
    ) AS survey_start,
    -- 현장 점검 시작 시각
    MAX(
        CASE
            WHEN l.taskID = 'Survey' THEN l.clean_timestamp
        END
    ) AS survey_complete,
    -- 현장 점검 완료 시각
    MAX(l.RepairInternally) AS repair_internally,
    -- 기사 실사 후 사내수리 가능 여부 판정 (1: 사내, 0: 외주)
    MAX(l.RepairCode) AS repair_code,
    -- 고장 부위/유형 코드
    MAX(l.EstimatedRepairTime) AS estimated_hours,
    -- 기사 실측 예상 소요시간
    -- 1차 수리 공정
    r.rep1_task,
    -- 1차 수리 종류 (Immediate, Intern, Extern)
    r.rep1_worker,
    -- 1차 수리 기사/업체
    r.rep1_start,
    -- 1차 수리 시작 시각
    r.rep1_complete,
    -- 1차 수리 완료 시각
    -- 2차 수리 공정 (외주전환/재작업 117건만 값 존재, 나머지는 NULL)
    r.rep2_task,
    -- 2차 수리 종류
    r.rep2_worker,
    -- 2차 수리 기사/업체
    r.rep2_start,
    -- 2차 수리 시작 시각
    r.rep2_complete,
    -- 2차 수리 완료 시각
    -- 3차 수리 공정 (3단계 장기 에스컬레이션 6건만 값 존재, 나머지는 NULL)
    r.rep3_task,
    -- 3차 수리 종류
    r.rep3_worker,
    -- 3차 수리 기사/업체
    r.rep3_start,
    -- 3차 수리 시작 시각
    r.rep3_complete,
    -- 3차 수리 완료 시각
    -- 최종 현장 수리 마감 (RepairReady)
    MAX(
        CASE
            WHEN l.taskID = 'RepairReady' THEN l.clean_timestamp
        END
    ) AS repair_ready_time,
    -- 현장 수리 작업 완전 마감 시각
    -- -----------------------------------------------------------------
    -- 3. [비용 결제 및 티켓 마감 섹션 (Billing)]
    -- -----------------------------------------------------------------
    -- 수리 완료 직후 시스템이 비동기 병렬로 처리하는 전산 자동화 공정
    MAX(
        CASE
            WHEN l.task_group = '정산' THEN l.originator
        END
    ) AS billing_worker,
    -- 자동화 수행 주체 (System)
    MAX(
        CASE
            WHEN l.taskID = 'ReadyInformClient' THEN l.clean_timestamp
        END
    ) AS client_inform_time,
    -- 고객 완료 알림 시각
    MAX(
        CASE
            WHEN l.taskID = 'SendTicketToFinAdmin' THEN l.clean_timestamp
        END
    ) AS fin_commit_time,
    -- 재무부 전송 시각
    MAX(
        CASE
            WHEN l.taskID = 'TicketReady' THEN l.clean_timestamp
        END
    ) AS ticket_ready_time,
    -- 두 조건 완료(AND-Join) 후 최종 티켓 종결 시각
    -- 병렬작업 선행 관계 판별 (고객 알림이 먼저 끝났는가 vs 재무 승인이 먼저 끝났는가)
    CASE
        WHEN MAX(
            CASE
                WHEN l.taskID = 'ReadyInformClient' THEN l.clean_timestamp
            END
        ) < MAX(
            CASE
                WHEN l.taskID = 'SendTicketToFinAdmin' THEN l.clean_timestamp
            END
        ) THEN '고객 선행'
        WHEN MAX(
            CASE
                WHEN l.taskID = 'SendTicketToFinAdmin' THEN l.clean_timestamp
            END
        ) < MAX(
            CASE
                WHEN l.taskID = 'ReadyInformClient' THEN l.clean_timestamp
            END
        ) THEN '승인 선행'
        WHEN MAX(
            CASE
                WHEN l.taskID = 'ReadyInformClient' THEN l.clean_timestamp
            END
        ) = MAX(
            CASE
                WHEN l.taskID = 'SendTicketToFinAdmin' THEN l.clean_timestamp
            END
        ) THEN '동일'
        ELSE NULL
    END AS billing_precedence,
    -- -----------------------------------------------------------------
    -- 4. [케이스 전체 요약 타임라인]
    -- -----------------------------------------------------------------
    MIN(l.clean_timestamp) AS case_start_time,
    -- 케이스 최초 유입 시각
    MAX(l.clean_timestamp) AS case_end_time,
    -- 케이스 최종 종결 시각
    COUNT(*) AS total_events -- 케이스 내 총 이벤트 수
FROM repair_logs l
    LEFT JOIN PivotedRepairs r ON l.caseID = r.caseID
GROUP BY l.caseID,
    r.rep1_task,
    r.rep1_worker,
    r.rep1_start,
    r.rep1_complete,
    r.rep2_task,
    r.rep2_worker,
    r.rep2_start,
    r.rep2_complete,
    r.rep3_task,
    r.rep3_worker,
    r.rep3_start,
    r.rep3_complete
ORDER BY l.caseID;
-- ---------------------------------------------------------------------
-- 1. [접수 단계 분석] 접수 담당자별 현황 및 '지역 전담제' 가정 검증
-- ---------------------------------------------------------------------
-- [1차 관찰 및 가정 제기]:
-- - 정상 접수 927건, 전체 고유 주택 890채
-- - 접수 담당자별 단순 주택 집계: Dian 431채 + Monica 482채 = 913채 (중복 23채, 2.5% 미만)
-- - 주택 중복 수치상 중복이 매우 적으므로, "특정 지역 전담제"로 경계선 주위 주택이 접수되면 인계과정이 발생 의심
--
SELECT originator,
    COUNT(distinct objectKey) AS total_houses
FROM repair_logs
WHERE objectKey IS NOT NULL
    AND task_group = '접수'
GROUP BY originator;
WITH HouseCaseCounts AS (
    SELECT objectKey,
        COUNT(DISTINCT caseID) AS case_cnt
    FROM repair_logs
    WHERE objectKey IS NOT NULL
        AND task_group = '접수'
    GROUP BY objectKey
)
SELECT CASE
        WHEN case_cnt = 1 THEN '1회 접수 (단발성)'
        WHEN case_cnt >= 2 THEN '2회 이상 접수 (재발/중복)'
    END AS category,
    COUNT(objectKey) AS total_houses,
    ROUND(
        COUNT(objectKey) * 100.0 / (
            SELECT COUNT(DISTINCT objectKey)
            FROM repair_logs
            WHERE objectKey IS NOT NULL
        ),
        1
    ) AS ratio_pct
FROM HouseCaseCounts
GROUP BY CASE
        WHEN case_cnt = 1 THEN '1회 접수 (단발성)'
        WHEN case_cnt >= 2 THEN '2회 이상 접수 (재발/중복)'
    END;
SELECT COUNT(DISTINCT caseID) AS total_cases,
    COUNT(DISTINCT objectKey) AS total_distinct_houses
FROM repair_logs
WHERE task_group = '접수'
    AND SUBJECT = '사람'
    AND objectKey IS NOT NULL
    AND caseID IN (
        SELECT caseID
        FROM repair_logs
        WHERE task_group = '접수'
            AND SUBJECT = '사람'
        GROUP BY caseID
        HAVING COUNT(DISTINCT originator) = 1
    );
SELECT originator,
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
-- - 순수 단독 접수: 804건 (고유 주택 775채, Dian 377건 / Monica 427건)
--   * Dian과 Monica 양쪽에서 각각 1회씩 단독 접수된 중복 주택 18채 존재 (실질 793채 관여)
WITH CaseSummary AS (
    -- 1. 케이스별 주택(objectKey) 및 접수 담당자 수(단독 vs 인계) 판별
    SELECT caseID,
        MAX(objectKey) AS objectKey,
        COUNT(DISTINCT originator) AS orig_cnt,
        CASE
            WHEN COUNT(DISTINCT originator) = 1 THEN '단독 접수'
            ELSE '핸드오버(인계)'
        END AS handover_type
    FROM repair_logs
    WHERE task_group = '접수'
        AND SUBJECT = '사람'
    GROUP BY caseID
    HAVING MAX(objectKey) IS NOT NULL
),
HouseFrequency AS (
    -- 2. 주택별 누적 접수 횟수 (1회 vs 2회 이상)
    SELECT objectKey,
        COUNT(caseID) AS house_total_cases,
        CASE
            WHEN COUNT(caseID) = 1 THEN '1회 접수 주택 (855채)'
            ELSE '2회 이상 접수 주택 (35채)'
        END AS house_category
    FROM CaseSummary
    GROUP BY objectKey
)
SELECT h.house_category AS `주택 접수 빈도`,
    COUNT(c.caseID) AS `총 케이스(건)`,
    SUM(
        CASE
            WHEN c.handover_type = '단독 접수' THEN 1
            ELSE 0
        END
    ) AS `단독접수(건)`,
    ROUND(
        SUM(
            CASE
                WHEN c.handover_type = '단독 접수' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(c.caseID),
        1
    ) AS `단독접수 비율(%)`,
    SUM(
        CASE
            WHEN c.handover_type = '핸드오버(인계)' THEN 1
            ELSE 0
        END
    ) AS `핸드오버(건)`,
    ROUND(
        SUM(
            CASE
                WHEN c.handover_type = '핸드오버(인계)' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(c.caseID),
        1
    ) AS `핸드오버 비율(%)`
FROM CaseSummary c
    JOIN HouseFrequency h ON c.objectKey = h.objectKey
GROUP BY h.house_category;
--  2회 이상 접수된 주택 수(35채)와 총 발생 건수(72건) 집계
SELECT COUNT(DISTINCT objectKey) AS `2회이상 접수 주택수(채)`,
    COUNT(DISTINCT caseID) AS `총 발생 케이스(건)`
FROM repair_logs
WHERE task_group = '접수'
    AND SUBJECT = '사람'
    AND objectKey IS NOT NULL
    AND objectKey IN (
        SELECT objectKey
        FROM repair_logs
        WHERE task_group = '접수'
            AND SUBJECT = '사람'
            AND objectKey IS NOT NULL
        GROUP BY objectKey
        HAVING COUNT(DISTINCT caseID) >= 2
    );
-- [가정 검증 요약]:
-- 1) 단발성 접수 주택 (전체의 96.1%):
--    - 전체 890채 중 855채는 수리가 평생 딱 1번만 발생함.
--    - 이 중 115건(13.5%)에서 상담원 간 인계(핸드오버)가 발생함.
--
-- 2) 반복 접수 주택 (전체의 3.9%):
--    - 2회 이상 수리가 발생한 주택은 총 35채이며, 여기서 발생한 총 접수는 72건임.
--    - 이 72건 중에서도 인계가 발생한 건은 8건(11.1%)에 불과함.
--
-- [해석]:
--  1회 접수 주택의 인계율(13.5%)과 2회 이상 주택의 인계율(11.1%)이 약 11~13%대로 큰 차이가 없음.
-- 만약, 첫 접수 담당자와 두번째 접수 담당자 간 차이로 인계 발생 인지 재접수 건의 담당자 매칭을 통해 확인
-- 1 주택 - 담당자 고정 매칭 여부
WITH ReceiptEvents AS (
    -- 1. 케이스 내 접수 단계(사람) 이벤트의 시간순 번호 부여
    SELECT r.caseID,
        r.originator,
        r.clean_timestamp,
        r.seq,
        r.sub_seq,
        ROW_NUMBER() OVER (
            PARTITION BY r.caseID
            ORDER BY r.clean_timestamp,
                r.seq,
                r.sub_seq
        ) AS rn_asc,
        ROW_NUMBER() OVER (
            PARTITION BY r.caseID
            ORDER BY r.clean_timestamp DESC,
                r.seq DESC,
                r.sub_seq DESC
        ) AS rn_desc
    FROM repair_logs r
    WHERE r.task_group = '접수'
        AND r.SUBJECT = '사람'
),
CaseReceiptWorker AS (
    -- 2. 케이스별 주택(objectKey) 매핑 및 최초/최종 접수 담당자 추출
    SELECT e.caseID,
        MAX(r.objectKey) AS objectKey,
        MIN(e.clean_timestamp) AS receipt_start_time,
        MAX(
            CASE
                WHEN e.rn_asc = 1 THEN e.originator
            END
        ) AS first_worker,
        MAX(
            CASE
                WHEN e.rn_desc = 1 THEN e.originator
            END
        ) AS last_worker,
        COUNT(DISTINCT e.originator) AS worker_count
    FROM ReceiptEvents e
        JOIN repair_logs r ON e.caseID = r.caseID
        AND r.objectKey IS NOT NULL
    GROUP BY e.caseID
),
HouseVisits AS (
    -- 3. 주택별 접수 발생 순서(1차, 2차...) 매기기
    SELECT caseID,
        objectKey,
        receipt_start_time,
        first_worker,
        last_worker,
        worker_count,
        ROW_NUMBER() OVER (
            PARTITION BY objectKey
            ORDER BY receipt_start_time,
                caseID
        ) AS visit_order,
        COUNT(*) OVER (PARTITION BY objectKey) AS total_visits
    FROM CaseReceiptWorker
) -- 4. 2회 이상 접수 주택의 1차 접수와 2차 접수 매칭
SELECT v1.objectKey AS `주택번호`,
    v1.total_visits AS `총접수건수`,
    -- [1차 접수]
    v1.caseID AS `1차 caseID`,
    DATE_FORMAT(v1.receipt_start_time, '%m-%d %H:%i') AS `1차 접수일시`,
    v1.first_worker AS `1차 최초담당자`,
    v1.last_worker AS `1차 최종담당자`,
    CASE
        WHEN v1.worker_count > 1 THEN '인계(O)'
        ELSE '단독'
    END AS `1차 인계여부`,
    -- [2차 접수]
    v2.caseID AS `2차 caseID`,
    DATE_FORMAT(v2.receipt_start_time, '%m-%d %H:%i') AS `2차 접수일시`,
    v2.first_worker AS `2차 최초담당자`,
    v2.last_worker AS `2차 최종담당자`,
    CASE
        WHEN v2.worker_count > 1 THEN '인계(O)'
        ELSE '단독'
    END AS `2차 인계여부`,
    -- [담당자 승계 분석]
    CASE
        WHEN v1.last_worker = v2.first_worker THEN '동일인 시작 (유지)'
        ELSE '타담당자 시작 (교차)'
    END AS `접수 시작 승계`,
    CASE
        WHEN v1.last_worker = v2.last_worker THEN '최종담당 일치'
        ELSE '최종담당 불일치'
    END AS `최종 처리자 일치여부`
FROM HouseVisits v1
    JOIN HouseVisits v2 ON v1.objectKey = v2.objectKey
    AND v2.visit_order = 2
WHERE v1.visit_order = 1
ORDER BY v1.objectKey;


-- CNT 및 RATIO
WITH ReceiptEvents AS (
    SELECT r.caseID,
        r.originator,
        r.clean_timestamp,
        r.seq,
        r.sub_seq,
        ROW_NUMBER() OVER (
            PARTITION BY r.caseID
            ORDER BY r.clean_timestamp,
                r.seq,
                r.sub_seq
        ) AS rn_asc,
        ROW_NUMBER() OVER (
            PARTITION BY r.caseID
            ORDER BY r.clean_timestamp DESC,
                r.seq DESC,
                r.sub_seq DESC
        ) AS rn_desc
    FROM repair_logs r
    WHERE r.task_group = '접수'
        AND r.SUBJECT = '사람'
),
CaseReceiptWorker AS (
    SELECT e.caseID,
        MAX(r.objectKey) AS objectKey,
        MIN(e.clean_timestamp) AS receipt_start_time,
        MAX(
            CASE
                WHEN e.rn_asc = 1 THEN e.originator
            END
        ) AS first_worker,
        MAX(
            CASE
                WHEN e.rn_desc = 1 THEN e.originator
            END
        ) AS last_worker,
        COUNT(DISTINCT e.originator) AS worker_count
    FROM ReceiptEvents e
        JOIN repair_logs r ON e.caseID = r.caseID
        AND r.objectKey IS NOT NULL
    GROUP BY e.caseID
),
HouseVisits AS (
    SELECT caseID,
        objectKey,
        receipt_start_time,
        first_worker,
        last_worker,
        worker_count,
        ROW_NUMBER() OVER (
            PARTITION BY objectKey
            ORDER BY receipt_start_time,
                caseID
        ) AS visit_order
    FROM CaseReceiptWorker
),
MatchedVisits AS (
    SELECT v1.objectKey AS house_id,
        v1.first_worker AS c1_first,
        v1.last_worker AS c1_last,
        v2.first_worker AS c2_first,
        v2.last_worker AS c2_last,
        -- 일치 여부 판별 플래그
        CASE
            WHEN v1.first_worker = v2.first_worker THEN 1
            ELSE 0
        END AS is_first_matched,
        CASE
            WHEN v1.last_worker = v2.last_worker THEN 1
            ELSE 0
        END AS is_last_matched,
        -- 2차에서 타 상담원이 최초 수신했으나, 인계를 통해 1차 최종 담당자로 복귀된 건
        CASE
            WHEN v1.last_worker != v2.first_worker
            AND v1.last_worker = v2.last_worker THEN 1
            ELSE 0
        END AS is_recovered_by_handover
    FROM HouseVisits v1
        JOIN HouseVisits v2 ON v1.objectKey = v2.objectKey
        AND v2.visit_order = 2
    WHERE v1.visit_order = 1
)
SELECT COUNT(*) AS `2회이상 접수 주택수(채)`,
    -- 1. 최초 전화 수신자 일치율
    SUM(is_first_matched) AS `최초 수신자 일치`,
    ROUND(SUM(is_first_matched) * 100.0 / COUNT(*), 1) AS `최초 수신 일치율(%)`,
    -- 2. 최종 처리자 일치율
    SUM(is_last_matched) AS `최종 처리자 일치`,
    ROUND(SUM(is_last_matched) * 100.0 / COUNT(*), 1) AS `최종 처리 일치율(%)`,
    -- 3. 인계를 통해 이전 담당자에게 복귀된 주택 수
    SUM(is_recovered_by_handover) AS `인계로 이전담당자 복귀`,
    ROUND(
        SUM(is_recovered_by_handover) * 100.0 / COUNT(*),
        1
    ) AS `인계 복귀율(%)`
FROM MatchedVisits;
-- [가정 검증 요약 (재접수 35채 분석)]:
-- 1) 전화 최초 인입: 35채 중 13채(37.1%)만 1차와 동일인이 받았고, 22채(62.9%)는 타 상담원에게 무작위 연결됨.
-- 2) 인계 및 처리: 타인이 받은 22채 중 이전 담당자에게 인계된 주택은 단 3채(8.6%)에 불과하며,
--    나머지 19채(54.3%)는 이전 담당자와 무관하게 새 상담원이 그대로 접수 처리를 완료함.
-- => [결론]: 재접수 시에도 고객/주택별 담당자 지정이 없음. 지역담당제 부분 해소,
-- ---------------------------------------------------------------------
-- 1-2. [지역 분담 가정 확인] 접수 담당자 구분에 따른 현장 인력 배정 편향 
-- 담당구역
-- ---------------------------------------------------------------------
-- 접수자가 Dian/Monica로 갈리더라도, 현장 기사들의 출동 구역 편향이 존재하는지 확인
WITH SingleReceiptCases AS (
    -- 단독 접수한 케이스와 해당 접수 담당자 매핑
    SELECT caseID,
        MAX(originator) AS receipt_worker -- Dian 또는 Monica
    FROM repair_logs
    WHERE task_group = '접수'
        AND SUBJECT = '사람'
    GROUP BY caseID
    HAVING COUNT(DISTINCT originator) = 1
)
SELECT COALESCE(f.originator, '전체 총계') AS field_worker,
    -- Dian 접수 구역 출동 케이스 수
    COUNT(
        DISTINCT CASE
            WHEN r.receipt_worker = 'Dian' THEN f.caseID
        END
    ) AS dian_area_cases,
    -- Monica 접수 구역 출동 케이스 수
    COUNT(
        DISTINCT CASE
            WHEN r.receipt_worker = 'Monica' THEN f.caseID
        END
    ) AS monica_area_cases,
    -- 전체 출동 케이스 수
    COUNT(DISTINCT f.caseID) AS total_cases,
    -- Dian 구역 출동 비율 (%)
    ROUND(
        COUNT(
            DISTINCT CASE
                WHEN r.receipt_worker = 'Dian' THEN f.caseID
            END
        ) * 100.0 / COUNT(DISTINCT f.caseID),
        1
    ) AS dian_ratio_pct
FROM repair_logs f
    JOIN SingleReceiptCases r ON f.caseID = r.caseID
WHERE f.task_group = '현장'
    AND f.SUBJECT = '사람'
GROUP BY f.originator WITH ROLLUP
ORDER BY GROUPING(f.originator) ASC,
    total_cases DESC;
-- [현장 배정 분석 결론]
-- - 현장 작업자들의 Dian 구역 출동 비율이 38% ~ 55%로 전체 평균(46.9%)에 수렴.
-- - 특정 기사가 특정 접수 건에 편향되지 않음 (Anne 50:50, Edd 51.8:48.2, John 46.2:53.8 등 균등 출동).
-- [가정 결론]
-- => 현장 기사 및 외주업체(FixIt, DoIt)는 구역 제한 없이 전 지역을 담당하는 완전 통합 체제로 운영됨.
-- => 접수와 현장간의 비편향적인 모습과 이관처리 없이 접수 작업을 이어가는 측면에서 접수 역시 지역 담당이 아닌 통합 체제로 추정
-- 2-1 [접수 단계] 채널별 정상/오류 접수 분포
-- 1) 접수 오류 그룹
SELECT 'is_null' AS obj_type,
    contact_channel,
    COUNT(*) AS cnt,
    ROUND(
        COUNT(*) * 100.0 / (
            SELECT COUNT(*)
            FROM case_master_view
            WHERE objectKey IS NULL
        ),
        2
    ) AS pct
FROM case_master_view
WHERE objectKey IS NULL
GROUP BY contact_channel
UNION ALL
-- 2) 정상 진행 그룹
SELECT 'is_not_null' AS obj_type,
    contact_channel,
    COUNT(*) AS cnt,
    ROUND(
        COUNT(*) * 100.0 / (
            SELECT COUNT(*)
            FROM case_master_view
            WHERE objectKey IS NOT NULL
        ),
        2
    ) AS pct
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY contact_channel;
-- 특정 채널에 유의미한 오접수는 보이지 않음
-- 3-1 [접수 단계] 접수구간 병목 현상 구체적 도출
SELECT avg(
        TIMESTAMPDIFF(MINUTE, contact_time, inform_survey_time)
    ) AS avg_contact_duration_minutes,
    min(
        TIMESTAMPDIFF(MINUTE, contact_time, inform_survey_time)
    ) AS min_contact_duration_minutes,
    max(
        TIMESTAMPDIFF(MINUTE, contact_time, inform_survey_time)
    ) / 60 AS max_contact_duration_hour
FROM case_master_view
WHERE objectKey IS NOT NULL;
-- [접수 구간 소요시간 통계치]
-- - 전체 평균 접수 소요시간: 125.0분 (약 2.08시간)
-- - 최소: 4.0분 / 최대: 36.5시간 (2,191분)
-- 월별 접수 건수와 평균 접수 소요 시간
SELECT DATE_FORMAT(contact_time, '%Y-%m') AS month,
    COUNT(*) AS ticket_count,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, contact_time, inform_survey_time)
        ) / 60,
        2
    ) AS avg_duration_hours
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY month
ORDER BY month;
-- 일별 접수 건수와 평균 접수 소요 시간
SELECT DATE_FORMAT(contact_time, '%Y-%m-%d') AS day,
    COUNT(*) AS ticket_count,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, contact_time, inform_survey_time)
        ) / 60,
        2
    ) AS avg_duration_hours
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY day
ORDER BY day;
-- 일별 접수량과 접수구간 소요시간 공변하지 않음
-- 일별 인계 발생 건수, 접수 건 소요시간 비교
SELECT DATE(m.contact_time) AS contact_date,
    COUNT(*) AS total_tickets,
    -- 접수 단계 참여자가 2명 이상인 인계 케이스 카운트
    SUM(
        CASE
            WHEN h.caseID IS NOT NULL THEN 1
            ELSE 0
        END
    ) AS handover_count,
    ROUND(
        SUM(
            CASE
                WHEN h.caseID IS NOT NULL THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        1
    ) AS handover_rate_pct,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, m.contact_time, m.inform_survey_time)
        ) / 60.0,
        2
    ) AS avg_duration_hours
FROM case_master_view m
    LEFT JOIN (
        -- 접수 단계에 2명 이상의 상담원이 관여한 123건 추출
        SELECT caseID
        FROM repair_logs
        WHERE task_group = '접수'
            AND SUBJECT = '사람'
        GROUP BY caseID
        HAVING COUNT(DISTINCT originator) > 1
    ) h ON m.caseID = h.caseID
WHERE m.objectKey IS NOT NULL
GROUP BY DATE(m.contact_time) WITH ROLLUP
ORDER BY contact_date;
-- 인계비중이 높아질수록 늘어나는 지연시간 관측
-- [병목 가정] 인계작업 시 접수 프로세스 시간 지연 현상
-- 심층 추적 인계 발생군(13.3%) vs 단독 처리군(86.7%) 소요시간 비교
SELECT CASE
        WHEN h.caseID IS NOT NULL THEN '인계 발생군 (Handover)'
        ELSE '단독 처리군 (Single)'
    END AS receipt_group,
    COUNT(*) AS case_count,
    ROUND(
        COUNT(*) * 100.0 / (
            SELECT COUNT(*)
            FROM case_master_view
            WHERE objectKey IS NOT NULL
        ),
        1
    ) AS case_ratio_pct,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, m.contact_time, m.inform_survey_time)
        ),
        1
    ) AS avg_duration_minutes,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, m.contact_time, m.inform_survey_time)
        ) / 60.0,
        2
    ) AS avg_duration_hours,
    MIN(
        TIMESTAMPDIFF(MINUTE, m.contact_time, m.inform_survey_time)
    ) AS min_duration_minutes,
    ROUND(
        MAX(
            TIMESTAMPDIFF(MINUTE, m.contact_time, m.inform_survey_time)
        ) / 60.0,
        2
    ) AS max_duration_hours
FROM case_master_view m
    LEFT JOIN (
        -- 접수 단계에 2명 이상의 상담원이 관여한 123건
        SELECT caseID
        FROM repair_logs
        WHERE task_group = '접수'
            AND SUBJECT = '사람'
        GROUP BY caseID
        HAVING COUNT(DISTINCT originator) > 1
    ) h ON m.caseID = h.caseID
WHERE m.objectKey IS NOT NULL
GROUP BY CASE
        WHEN h.caseID IS NOT NULL THEN '인계 발생군 (Handover)'
        ELSE '단독 처리군 (Single)'
    END;
-- [가정 검증 요약]
-- - 단독 처리군 (804건, 86.7%): 평균 71.9분 (1.20시간), 최소 4.0분, 최대 36.5시간
-- - 인계 발생군 (123건, 13.3%): 평균 472.1분 (7.87시간), 최소 72.0분, 최대 34.6시간
-- => 인계 발생 시 평균 접수 소요시간이 1.20시간에서 7.87시간으로 약 6.5배 폭증 확인
-- 인계 작업 case 상세 과정 확인
SELECT contact_channel,
    count(*)
from case_master_view
where caseID in (
        SELECT caseID
        from repair_logs
        where task_group = '접수'
            and SUBJECT = '사람'
        group by caseID
        HAVING count(DISTINCT originator) > 1
    )
group by contact_channel;
-- [인계 작업 발생 채널 특성]
-- - 인계 발생 채널: Web 69건, Letter 54건 (총 123건 100% 비실시간 채널)
-- - 실시간 채널(Phone, Personal)은 인계 0건 (100% 단독 완결)
-- - Letter, Web의 경우 접수원이 정보 수용 후 고객과 추가 일정 재조율을 거치며 인계 발생
-- [채널별 동시성 심층 확인] 채널별 접수 구간 시간 차이
SELECT contact_channel,
    COUNT(*) AS ticket_count,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, contact_time, ticket_complete)
        ),
        1
    ) AS avg_time1_minutes,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete)
        ),
        1
    ) AS avg_time2_minutes,
    ROUND(
        max(
            TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete)
        ),
        1
    ) AS max_time2_minutes,
    ROUND(
        min(
            TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete)
        ),
        1
    ) AS min_time2_minutes
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY contact_channel;
-- -------------------------------------------------------------
-- 채널별 time2(접수~일정조율완료) 구간별 분포 검증 (이봉 분포 / 양극화 구조 확인)
-- 15분 이하(즉시 완료), 15분~60분(중간 공백), 60분 초과(지연) 집단 비율 및 평균 소요시간
-- -------------------------------------------------------------
SELECT contact_channel,
    COUNT(*) AS total_cases,
    -- 15분 이내 즉시 완료 집단 (Fast Cohort)
    SUM(
        CASE
            WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) <= 15 THEN 1
            ELSE 0
        END
    ) AS fast_cases_le_15m,
    ROUND(
        SUM(
            CASE
                WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) <= 15 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        1
    ) AS fast_pct,
    ROUND(
        AVG(
            CASE
                WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) <= 15 THEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete)
            END
        ),
        1
    ) AS avg_fast_time_m,
    -- 15분 ~ 60분 사이 구간 (0건 확인용)
    SUM(
        CASE
            WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) > 15
            AND TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) <= 60 THEN 1
            ELSE 0
        END
    ) AS mid_cases_15_to_60m,
    -- 60분 초과 지연 집단 (Slow Cohort)
    SUM(
        CASE
            WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) > 60 THEN 1
            ELSE 0
        END
    ) AS slow_cases_gt_60m,
    ROUND(
        SUM(
            CASE
                WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) > 60 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        1
    ) AS slow_pct,
    ROUND(
        min(
            CASE
                WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) > 60 THEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete)
            END
        ),
        1
    ) AS min_slow_time_m,
    ROUND(
        max(
            CASE
                WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) > 60 THEN TIMESTAMPDIFF(hour, contact_time, survey_arrange_complete)
            END
        ),
        1
    ) AS max_slow_time_h,
    ROUND(
        AVG(
            CASE
                WHEN TIMESTAMPDIFF(MINUTE, contact_time, survey_arrange_complete) > 60 THEN TIMESTAMPDIFF(hour, contact_time, survey_arrange_complete)
            END
        ),
        1
    ) AS avg_slow_time_h
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY contact_channel;
-- [채널별 소요시간 양극화 및 이봉 분포 분석 결과]
-- 1) FAST 코호트 (15분 이내 완결):
--    - Phone: 100%(251건)가 FAST (평균 8.2분)
--    - Personal: 99.6%(227건)가 FAST (평균 8.5분, 15.0분 경계값 1건)
--    - Letter: 51.7%(107건)가 FAST (평균 8.4분)
--    - Web: 47.3%(114건)가 FAST (평균 6.8분 - 전 채널 최단!)
-- 2) SLOW 코호트 (60분 초과 장기 지연):
--    - Letter: 47.8%(99건)가 SLOW (평균 7.5시간, 최대 26.0시간)
--    - Web: 52.7%(127건)가 SLOW (평균 8.6시간, 최대 36.5시간)
-- 3) 중간 공백 (15분~60분): 0건 (15.0분 경계값 2건 제외 시 공백) ➔ 완전한 이봉(양극화) 구조 형성
-- - 시사점: 실시간 채널은 즉시 연결 이점으로 빠르고, Web 채널은 정형 양식 덕분에 정상 접수 시 최단 시간(6.8분)을 기록하나, 비실시간 채널의 약 50%는 일정 재조율 대기 큐로 인해 장기 지연됨
-- -------------------------------------------------------------
-- [가정 검증] 접수 구간의 24시간(야간 포함) 활동 여부 및 담당자(Dian, Monica) 근무 형태 확인
-- -------------------------------------------------------------
-- 1) 접수 단계(task_group='접수') 시간대별(0~23시) 담당자별 이벤트 건수
SELECT HOUR(clean_timestamp) AS active_hour,
    COUNT(*) AS total_intake_events,
    SUM(
        CASE
            WHEN originator = 'Dian' THEN 1
            ELSE 0
        END
    ) AS dian_events,
    SUM(
        CASE
            WHEN originator = 'Monica' THEN 1
            ELSE 0
        END
    ) AS monica_events,
    SUM(
        CASE
            WHEN originator = 'System' THEN 1
            ELSE 0
        END
    ) AS system_events
FROM repair_logs
WHERE task_group = '접수'
GROUP BY HOUR(clean_timestamp)
ORDER BY active_hour;
-- 2) 최초 접수 시간(contact_time)의 채널별 24시간 분포 확인 (야간 대면/전화 접수 존재 여부)
SELECT HOUR(contact_time) AS contact_hour,
    COUNT(*) AS total_cases,
    SUM(
        CASE
            WHEN contact_channel = 'Personal' THEN 1
            ELSE 0
        END
    ) AS personal_cnt,
    SUM(
        CASE
            WHEN contact_channel = 'Phone' THEN 1
            ELSE 0
        END
    ) AS phone_cnt,
    SUM(
        CASE
            WHEN contact_channel = 'Letter' THEN 1
            ELSE 0
        END
    ) AS letter_cnt,
    SUM(
        CASE
            WHEN contact_channel = 'Web' THEN 1
            ELSE 0
        END
    ) AS web_cnt
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY HOUR(contact_time)
ORDER BY contact_hour;
-- [근무 형태 검증 및 인계 병목 메커니즘 결론]
-- 1) 24시간 상시 활동 확인:
--    - 야간 시간대(0~23시)에도 접수 담당자(Dian, Monica) 및 채널이 상시 운영됨 ➔ '업무시간 외(야간) 방치' 가설 기각
-- 2) 대기 큐 적체 및 인계 메커니즘:
--    - 비실시간 접수 시 초기 정보 누락 또는 고객 비동기 조율로 인해 대기 큐(Pending) 형성
--    - 대기 큐에 묶여 있는 동안, 먼저 손이 빈 타 상담원이 응답을 이어받아 처리하면서 인계(Handover)와 장기 지연이 동시 발현됨
-- ---------------------------------------------------------------------
-- 2. [현장 단계 분석] 공정별 소요시간 구조 분해 및 핵심 병목 규명
-- ---------------------------------------------------------------------
-- ---------------------------------------------------------------------
-- 2-1. [거시 진단] 전체 리드타임 중 현장 공정(방문~수리완료)의 비중
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 전체 수리 사이클(접수~정산준비) 중 현장 공정이 차지하는 시간적 비중 정량 산출
SELECT -- 1) 현장 과정 평균 소요 시간 및 일수 (약 97.8시간 / 24 = 약 4.07일)
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time) / 60.0
        ),
        1
    ) AS avg_field_hours,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time) / 1440.0
        ),
        2
    ) AS avg_field_days,
    -- 2) 전체 프로세스 평균 소요 시간 (약 105.4시간)
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, contact_time, ticket_ready_time) / 60.0
        ),
        1
    ) AS total_case_hours,
    -- 3) 현장 공정 비중 (%)
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time)
        ) * 100.0 / AVG(
            TIMESTAMPDIFF(MINUTE, contact_time, ticket_ready_time)
        ),
        1
    ) AS field_ratio_pct
FROM case_master_view
WHERE objectKey IS NOT NULL;
-- [거시 진단 요약]:
-- - 전체 프로세스 리드타임: 평균 105.9시간 (약 4.4일)
-- - 현장 공정 소요시간  : 평균 98.3시간 (약 4.1일, 전체의 92.8% 차지)
-- => 수리 프로세스 지연의 핵심은 접수 이후의 현장 공정임이 입증됨.
-- ---------------------------------------------------------------------
-- 2-2. [구조 분해] 실작업 시간 vs 대기시간 비중 분해 (기사 생산성 검증)
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 현장 지연이 기사의 실제 작업 시간 과다인지, 공정 간 대기시간 적체인지 검증
SELECT -- 현장 총 리드타임 (평균 98.3시간)
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time) / 60.0
        ),
        1
    ) AS total_field_hours,
    -- 1) 순수 실작업 시간 합계 (실사 40분 + 1차수리 3.5h + 추가수리 23분 = 약 4.6시간)
    ROUND(
        AVG(
            (
                TIMESTAMPDIFF(MINUTE, survey_start, survey_complete) + TIMESTAMPDIFF(MINUTE, rep1_start, rep1_complete) + COALESCE(
                    TIMESTAMPDIFF(MINUTE, rep2_start, rep2_complete),
                    0
                ) + COALESCE(
                    TIMESTAMPDIFF(MINUTE, rep3_start, rep3_complete),
                    0
                )
            ) / 60.0
        ),
        1
    ) AS pure_work_hours,
    -- 2) 순수 실작업 비중 (4.7%)
    ROUND(
        AVG(
            (
                TIMESTAMPDIFF(MINUTE, survey_start, survey_complete) + TIMESTAMPDIFF(MINUTE, rep1_start, rep1_complete) + COALESCE(
                    TIMESTAMPDIFF(MINUTE, rep2_start, rep2_complete),
                    0
                ) + COALESCE(
                    TIMESTAMPDIFF(MINUTE, rep3_start, rep3_complete),
                    0
                )
            ) / 60.0
        ) * 100.0 / AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time) / 60.0
        ),
        1
    ) AS pure_work_ratio_pct,
    -- 3) 순수 대기시간 합계 (약 93.7시간, 약 3.9일)
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time) / 60.0 - (
                (
                    TIMESTAMPDIFF(MINUTE, survey_start, survey_complete) + TIMESTAMPDIFF(MINUTE, rep1_start, rep1_complete) + COALESCE(
                        TIMESTAMPDIFF(MINUTE, rep2_start, rep2_complete),
                        0
                    ) + COALESCE(
                        TIMESTAMPDIFF(MINUTE, rep3_start, rep3_complete),
                        0
                    )
                ) / 60.0
            )
        ),
        1
    ) AS pure_wait_hours,
    -- 4) 순수 대기시간 비중 (95.3%)
    ROUND(
        (
            1.0 - (
                AVG(
                    (
                        TIMESTAMPDIFF(MINUTE, survey_start, survey_complete) + TIMESTAMPDIFF(MINUTE, rep1_start, rep1_complete) + COALESCE(
                            TIMESTAMPDIFF(MINUTE, rep2_start, rep2_complete),
                            0
                        ) + COALESCE(
                            TIMESTAMPDIFF(MINUTE, rep3_start, rep3_complete),
                            0
                        )
                    ) / 60.0
                ) / AVG(
                    TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time) / 60.0
                )
            )
        ) * 100.0,
        1
    ) AS pure_wait_ratio_pct
FROM case_master_view
WHERE objectKey IS NOT NULL;
-- [구조 분해 요약]:
-- - 순수 실작업 시간: 평균 4.6시간 (4.7%) ➔ 실사 40.5분, 1차 수리 3.51시간, 추가 수리 23.5분
-- - 순수 대기 시간  : 평균 93.7시간 (95.3%) ➔ 전체 현장 시간의 95% 이상이 단순 대기 상태
-- => 기사의 작업 속도가 느린 것이 아니라, '공정 간 대기시간 관리 부재'가 핵심 원인임.
-- ---------------------------------------------------------------------
-- 2-3. [병목 타겟팅] 핵심 대기구간 정밀 분해 (Wait 1 vs Wait 2)
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 94시간 대기시간이 '실사 방문 전(Wait 1)'과 '수리 출동 전(Wait 2)' 중 어디에 집중되는지 분해
SELECT ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time) / 60.0
        ),
        1
    ) AS total_field_hours,
    -- 1) [병목 1위] 실사 전 방문 대기시간 (Wait 1) 및 비중
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, survey_start) / 60.0
        ),
        1
    ) AS wait1_survey_hours,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, survey_start) / 1440.0
        ),
        2
    ) AS wait1_survey_days,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, survey_start)
        ) * 100.0 / AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time)
        ),
        1
    ) AS wait1_ratio_pct,
    -- 2) [병목 2위] 실사 완료 후 1차 수리 전 대기시간 (Wait 2) 및 비중
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, survey_complete, rep1_start) / 60.0
        ),
        1
    ) AS wait2_repair_hours,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, survey_complete, rep1_start)
        ) * 100.0 / AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time)
        ),
        1
    ) AS wait2_ratio_pct,
    -- 3) 총 대기시간 비중 합계 (Wait 1 + Wait 2 = 94.4%)
    ROUND(
        (
            AVG(
                TIMESTAMPDIFF(MINUTE, inform_survey_time, survey_start)
            ) + AVG(
                TIMESTAMPDIFF(MINUTE, survey_complete, rep1_start)
            )
        ) * 100.0 / AVG(
            TIMESTAMPDIFF(MINUTE, inform_survey_time, repair_ready_time)
        ),
        1
    ) AS total_waiting_ratio_pct
FROM case_master_view
WHERE objectKey IS NOT NULL;
-- [병목 타겟팅 요약]:
-- 1) [압도적 1위 병목]: '실사 전 방문 대기(Wait 1)' 76.8시간(약 3.2일, 78.2% 차지)
--    - 접수 완료 후 실제 조사원이 방문하기까지 3일 이상 지연 (접수 단계의 '일정 조율 핑퐁'과 직결)
-- 2) [2위 병목]: '실사 완료 후 수리 출동 대기(Wait 2)' 15.9시간(약 0.7일, 16.2% 차지)
-- => 현장 대기의 약 80%가 '실사 방문 전 대기'에 편중됨을 확증.
-- ---------------------------------------------------------------------
-- 2-4. [품질 및 재작업 진단] 수리 차수별 에스컬레이션 및 재작업 지연
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 1차 수리 원샷 종결률 및 실패 시 2차/3차 전환에 따른 추가 대기시간 산출
-- 0) [수리 메커니즘 정합성 검증] 단방향 에스컬레이션 및 RepairInternally 판정 일치성 검증
--    • 외주수리(ExternRepair) 이후 사내수리/즉시수리로 역류(Rollback)한 케이스가 존재하는가?
--    • 실사(Survey) 시점의 RepairInternally 속성 판정과 1차 실행 수리작업 간의 100% 정합성 검증
-- ---------------------------------------------------------------------
-- [검증 1] 외주수리 이후 후속 수리 역류 탐색 (0건 확인 -> 외주는 최종 종결)
SELECT 
    caseID,
    rep1_task,
    rep2_task,
    rep3_task
FROM case_master_view
WHERE (rep1_task = 'ExternRepair' AND rep2_task IS NOT NULL)
   OR (rep2_task = 'ExternRepair' AND rep3_task IS NOT NULL);

-- [검증 2] Survey 시점 RepairInternally 판정과 1차 실행 수리작업 일치성 검증
-- (False 59건 전원 외주 직행 / True 868건 전원 즉시/사내 착수 확인)
SELECT 
    CASE 
        WHEN l.RepairInternally = 1 THEN 'True (사내 수리 판정)'
        WHEN l.RepairInternally = 0 THEN 'False (외주 위탁 판정)'
        ELSE '기타/결측'
    END AS planned_internally_flag,
    c.rep1_task AS actual_rep1_task,
    COUNT(*) AS case_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY l.RepairInternally), 1) AS match_ratio_pct
FROM repair_logs l
JOIN case_master_view c ON l.caseID = c.caseID
WHERE l.taskID = 'Survey'
GROUP BY l.RepairInternally, c.rep1_task
ORDER BY l.RepairInternally, case_count DESC;

-- [수리 메커니즘 검증 결론]:
-- 1) 외주수리(ExternRepair) 이후 사내/즉시수리 역류 0건 (완벽한 단방향 에스컬레이션: 즉시 ➔ 사내 ➔ 외주)
-- 2) RepairInternally 판정 정합도: False(59건) 100.0% 외주 직행 / True(868건) 100.0% 사내/즉시 착수 (정합도 100%)
-- ---------------------------------------------------------------------
-- 1) 수리 차수별 작업 유형 분포
SELECT taskID,
    repair_order,
    COUNT(*) AS cnt,
    ROUND(COUNT(*) * 100.0 / 927.0, 1) AS pct_of_total_repairs
FROM (
        SELECT caseID,
            taskID,
            originator,
            DENSE_RANK() OVER (
                PARTITION BY caseID
                ORDER BY MIN(clean_timestamp),
                    seq
            ) AS repair_order
        FROM repair_logs
        WHERE taskID IN (
                'InternRepair',
                'ExternRepair',
                'ImmediateRepair'
            )
        GROUP BY caseID,
            taskID,
            originator,
            seq
    ) t
GROUP BY taskID,
    repair_order
ORDER BY repair_order,
    cnt DESC;
-- 2) 1차 수리 실패 후 2차 수리 전환 대기시간 (117건 대상)
SELECT rep1_task,
    rep2_task,
    COUNT(*) AS case_count,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, rep1_complete, rep2_start) / 60.0
        ),
        1
    ) AS avg_handover_wait_hours,
    ROUND(
        MAX(
            TIMESTAMPDIFF(MINUTE, rep1_complete, rep2_start) / 60.0
        ),
        1
    ) AS max_handover_wait_hours
FROM case_master_view
WHERE rep2_task IS NOT NULL
GROUP BY rep1_task,
    rep2_task
ORDER BY case_count DESC;
-- [수리 품질 및 재작업 요약 (전수 검증 완료)]:
-- - 1차 수리 완결률: 87.4% (810건) ➔ 사내 429건, 즉시 322건, 외주 59건 종결
-- - 2차 수리 전환율: 12.6% (117건) ➔ 1차 실패 후 재작업 및 외주 이관 발생
--   • 사내 하자 재방문(26건): 평균 32.9시간(최대 10.1일) 대기 발생 ➔ 핵심 품질 리스크
--   • 즉시수리 후 사내연계(23건): 평균 0.9시간(최대 6.0시간) 대기 발생
--   • 1차 실패 후 외주 이관(68건): 즉시수리 실패 38건 + 사내수리 실패 30건 (대기 0.0h, 즉시 외주 접수)
-- 3) [핵심 진단] 사내 하자 재방문(26건)의 현장 실사 수리코드(RepairCode) 및 사전분류(RepairType) 심층 조회
-- [목적]: 32.9시간 추가 대기를 초래하는 26건의 원인 고장유형을 식별하여 '정밀검사 및 사전 패키징' 집중 대상 도출
SELECT 
    c.repair_code AS `현장 실사 수리코드(RepairCode)`,
    c.planned_repair_type AS `접수 사전분류(RepairType)`,
    COUNT(*) AS `리워크 발생건수(건)`,
    ROUND(COUNT(*) * 100.0 / 26.0, 1) AS `26건 내 비중(%)`,
    -- 해당 수리코드 전체 1차 사내수리 모수 대비 리워크 발생률
    ROUND(
        COUNT(*) * 100.0 / (
            SELECT COUNT(*) 
            FROM case_master_view sub 
            WHERE sub.rep1_task = 'InternRepair' 
              AND sub.repair_code = c.repair_code
        ), 1
    ) AS `해당코드 사내수리 대비 리워크율(%)`
FROM case_master_view c
WHERE c.rep1_task = 'InternRepair' 
  AND c.rep2_task = 'InternRepair'
GROUP BY c.repair_code, c.planned_repair_type WITH ROLLUP
ORDER BY GROUPING(c.repair_code), c.repair_code, `리워크 발생건수(건)` DESC;

-- 4) 사내 하자 재방문 26건 상세 케이스 원천 추적 (기사, 대기시간, 주택번호)
SELECT 
    c.caseID,
    c.objectKey AS `주택번호`,
    c.contact_channel AS `접수채널`,
    c.planned_repair_type AS `접수코드`,
    c.repair_code AS `실사코드`,
    c.rep1_worker AS `1차수리기사`,
    c.rep2_worker AS `2차재수리기사`,
    ROUND(TIMESTAMPDIFF(MINUTE, c.rep1_complete, c.rep2_start) / 60.0, 1) AS `재출하_추가대기(시간)`,
    ROUND(TIMESTAMPDIFF(MINUTE, c.contact_time, c.ticket_ready_time) / 60.0, 1) AS `총리드타임(시간)`
FROM case_master_view c
WHERE c.rep1_task = 'InternRepair' 
  AND c.rep2_task = 'InternRepair'
ORDER BY `재출하_추가대기(시간)` DESC;

-- [26건 리워크 수리코드 분석 결론 및 TO-BE 방안]:
-- 1) 현장 실사 수리코드(RepairCode) 편중:
--    • Code 1 (16건, 61.5%): 26건 중 과반 이상이 1번 코드에 집중! (사내 1번 코드 234건 중 6.8% 리워크 발생)
--    • Code 2 (9건, 34.6%): 사내 2번 코드 224건 중 4.0% 리워크 발생
--    • Code 3 (1건, 3.8%): 사내 3번 코드 27건 중 3.7% 리워크 발생
--    • Code 4 (0건, 0.0%): 외주 전담 코드이므로 사내 리워크 0건
-- 2) 접수 사전분류와의 연계:
--    • E-1 조합(접수 E형 + 실사 1번 코드)이 16건으로 26건 전체의 61.5%를 독점.
-- 3) 비즈니스 액션 플랜 (TO-BE 전략 연계):
--    • 현장 실사에서 '수리코드 1번(특히 E-1)'이 확정되는 즉시,
--      단순 부품 교체로 끝내지 않고 '배관/전기 연계부품 2차 체크리스트 정밀검사'를 의무화.
--    • 1번 코드 전용 '사전 패키징 예비 부품 키트'를 기사에게 동봉 출고하여 부품 재주문으로 인한 32.9시간 지연을 원천 차단.
-- ---------------------------------------------------------------------

-- 3. [심층 대기행렬 분석] 접수-현장 간 이월(Spillover) 및 대기열 적체(WIP) 동역학 검증
-- ---------------------------------------------------------------------
-- [분석 가설]:
-- 1) 접수 지연(익일 이월 등)이 현장 대기열 큐를 팽창시켜 현장 실사 대기시간(Wait 1)에 영향을 미치는가?
-- 2) 초기 8일간 집중 유입(135건/일)과 현장 실사 처리 한계(69건/일)의 불균형이 대기열 적체와 대기시간 폭증의 본질인가?
-- ---------------------------------------------------------------------
-- 3-1. [파이프라인 타임라인] 일자별 3대 공정 유입·소화 흐름 및 현장 대기열(WIP) 적체 추적
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 1/1~1/18 전체 기간 동안 접수 유입(Inflow), 현장 이관(Handoff), 실사 착수(Outflow)의 일일 수치와
-- - 윈도우 함수를 통한 누적 대기열(Field Queue WIP) 및 당일 유입건의 평균 실사 대기시간(Wait 1) 산출
WITH IntakeDaily AS (
    SELECT DATE(contact_time) AS dt,
        COUNT(*) AS intake_cnt
    FROM case_master_view
    WHERE objectKey IS NOT NULL
    GROUP BY DATE(contact_time)
),
HandoffDaily AS (
    SELECT DATE(inform_survey_time) AS dt,
        COUNT(*) AS handoff_cnt,
        ROUND(
            AVG(
                TIMESTAMPDIFF(MINUTE, inform_survey_time, survey_start) / 60.0
            ),
            1
        ) AS avg_wait1_h
    FROM case_master_view
    WHERE objectKey IS NOT NULL
    GROUP BY DATE(inform_survey_time)
),
SurveyDaily AS (
    SELECT DATE(survey_start) AS dt,
        COUNT(*) AS survey_cnt
    FROM case_master_view
    WHERE objectKey IS NOT NULL
    GROUP BY DATE(survey_start)
),
AllDates AS (
    SELECT dt
    FROM IntakeDaily
    UNION
    SELECT dt
    FROM HandoffDaily
    UNION
    SELECT dt
    FROM SurveyDaily
)
SELECT d.dt AS `일자`,
    -- 1) [접수 국면] 당일 인입 vs 누적 접수
    COALESCE(i.intake_cnt, 0) AS `접수인입(건)`,
    SUM(COALESCE(i.intake_cnt, 0)) OVER (
        ORDER BY d.dt
    ) AS `누적접수인입(건)`,
    -- 2) [현장 이관 국면] 당일 이관 vs 누적 이관
    COALESCE(h.handoff_cnt, 0) AS `현장이관(건)`,
    SUM(COALESCE(h.handoff_cnt, 0)) OVER (
        ORDER BY d.dt
    ) AS `누적현장이관(건)`,
    (
        SUM(COALESCE(i.intake_cnt, 0)) OVER (
            ORDER BY d.dt
        ) - SUM(COALESCE(h.handoff_cnt, 0)) OVER (
            ORDER BY d.dt
        )
    ) AS `접수미이관_WIP(건)`,
    -- 3) [현장 실사 국면] 당일 실사 vs 누적 실사
    COALESCE(s.survey_cnt, 0) AS `실사착수(건)`,
    SUM(COALESCE(s.survey_cnt, 0)) OVER (
        ORDER BY d.dt
    ) AS `누적실사착수(건)`,
    (
        SUM(COALESCE(h.handoff_cnt, 0)) OVER (
            ORDER BY d.dt
        ) - SUM(COALESCE(s.survey_cnt, 0)) OVER (
            ORDER BY d.dt
        )
    ) AS `현장적체대기열_WIP(건)`,
    -- 4) 당일 이관건의 실측 실사 방문 대기시간
    h.avg_wait1_h AS `당일이관건_평균실사대기(h)`
FROM AllDates d
    LEFT JOIN IntakeDaily i ON d.dt = i.dt
    LEFT JOIN HandoffDaily h ON d.dt = h.dt
    LEFT JOIN SurveyDaily s ON d.dt = s.dt
ORDER BY d.dt;
-- [파이프라인 분석 요약]:
-- 1) 접수 집중: 1/1~1/8 단 8일간 927건 전수 유입 (일평균 135건 유입 ➔ 매일 120~141건 현장 이관)
-- 2) 실사 착수 지체: 현장 실사 착수는 일평균 69건(최저 45건 ~ 최고 78건) 수준에 머무름
-- 3) 대기열 폭증: 1/1 적체 20건(대기 10.7h) ➔ 1/7 적체 403건(대기 82.5h, 1/4~6 피크 93h대)으로 대기열 20배 폭증!
-- => 핵심 질문 도출: 현장 실사 착수는 왜 하루 69건 수준에 머물렀는가? (기사 CAPA 한계 진단 필요 ➔ 3-2로 연결)
-- ---------------------------------------------------------------------
-- 3-2. [현장 실사 CAPA 진단] 일자별 실사 처리량, 가동 인력 및 기술자 1인당 소화량 한계 검증
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 3-1에서 확인된 '일일 실사 69건 착수'의 원인을 규명하기 위해,
-- - 현장 기술자(11명)의 가동 현황과 1인당 실사 소화 능력(CAPA Ceiling)을 실측
SELECT DATE(survey_start) AS survey_date,
    COUNT(*) AS daily_survey_cnt,
    COUNT(DISTINCT survey_worker) AS active_tech_cnt,
    ROUND(
        COUNT(*) * 1.0 / COUNT(DISTINCT survey_worker),
        1
    ) AS surveys_per_tech,
    ROUND(
        SUM(
            TIMESTAMPDIFF(MINUTE, survey_start, survey_complete) / 60.0
        ),
        1
    ) AS total_survey_hours,
    ROUND(
        AVG(
            TIMESTAMPDIFF(MINUTE, survey_start, survey_complete)
        ),
        1
    ) AS avg_survey_dur_min
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY DATE(survey_start)
ORDER BY survey_date;
-- [실사 CAPA 분석 요약]:
-- 1) 가동 인력 및 일일 실사 한계: 1/2~1/8 집중 인입기 동안 10~11명의 기술자가 일평균 69.2건(최대 78건) 실사 소화
-- 2) 기술자 1인당 한계: 1인당 일평균 6.0~7.1건(순수 실사 소요 4.1~4.8시간) 소화 (본 수리 작업 및 가구 간 이동 시간 병행으로 인한 물리적 상한선)
-- 3) 병목의 메커니즘: 일일 접수 인계량(135건/일) 대비 현장 실사 소화량(평균 69건/일)은 51.1%에 불과하여, 매일 66건씩 적체(WIP)가 누적되며 76.8h 대기 발생
-- ---------------------------------------------------------------------
-- 3-3. [접수 이월 진단] 접수 부서의 일자별 당일 처리 vs 익일 이월(Spillover) 매트릭스
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 대기열 적체의 원인이 혹시 접수 부서가 유입량을 다음 날로 미루었기 때문인지(이월률) 정량 검증
SELECT DATE(contact_time) AS contact_date,
    COUNT(*) AS total_intake,
    -- 당일 이관 건수 및 비율
    SUM(
        CASE
            WHEN DATE(contact_time) = DATE(inform_survey_time) THEN 1
            ELSE 0
        END
    ) AS same_day_handoff,
    ROUND(
        SUM(
            CASE
                WHEN DATE(contact_time) = DATE(inform_survey_time) THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        1
    ) AS same_day_pct,
    -- 익일(이후) 이월 건수 및 비율
    SUM(
        CASE
            WHEN DATE(contact_time) != DATE(inform_survey_time) THEN 1
            ELSE 0
        END
    ) AS spillover_handoff,
    ROUND(
        SUM(
            CASE
                WHEN DATE(contact_time) != DATE(inform_survey_time) THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        1
    ) AS spillover_pct,
    -- 당일 처리군 vs 이월군 접수 소요시간 비교
    ROUND(
        AVG(
            CASE
                WHEN DATE(contact_time) = DATE(inform_survey_time) THEN TIMESTAMPDIFF(MINUTE, contact_time, inform_survey_time) / 60.0
            END
        ),
        2
    ) AS same_day_avg_intake_h,
    ROUND(
        AVG(
            CASE
                WHEN DATE(contact_time) != DATE(inform_survey_time) THEN TIMESTAMPDIFF(MINUTE, contact_time, inform_survey_time) / 60.0
            END
        ),
        2
    ) AS spillover_avg_intake_h
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY DATE(contact_time)
ORDER BY contact_date;
-- [접수 이월 분석 요약]:
-- 1) 전체 927건 중 844건(91.0%)은 당일 이관 완료 (평균 접수 0.76~1.95시간)
-- 2) 익일(이후) 이월은 83건(9.0%, 일평균 8~16건)에 불과 (평균 접수 9.7~14.2시간)
-- => 접수 부서 자체가 대량으로 물량을 미룬 것(이월 파동)이 아니라, 들어오는 족족 91%를 당일 털어내며 현장으로 밀어넣음! (접수 책임론 기각)
-- ---------------------------------------------------------------------
-- 3-4. [전이 효과 검증] 동일 접수일자 내 "당일 이관군" vs "익일 이월군"의 현장 대기시간 비교
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 접수 단계에서 지연되어 익일로 이월된 건이 실제로 현장 대기시간(Wait 1)과 고객 총 대기시간(Total to Survey)에 미치는 영향 추적
SELECT DATE(contact_time) AS contact_date,
    COUNT(*) AS total_cases,
    -- 1) 당일 이관군
    SUM(
        CASE
            WHEN DATE(contact_time) = DATE(inform_survey_time) THEN 1
            ELSE 0
        END
    ) AS same_day_cnt,
    ROUND(
        AVG(
            CASE
                WHEN DATE(contact_time) = DATE(inform_survey_time) THEN TIMESTAMPDIFF(MINUTE, inform_survey_time, survey_start) / 60.0
            END
        ),
        1
    ) AS same_wait1_h,
    ROUND(
        AVG(
            CASE
                WHEN DATE(contact_time) = DATE(inform_survey_time) THEN TIMESTAMPDIFF(MINUTE, contact_time, survey_start) / 60.0
            END
        ),
        1
    ) AS same_total_survey_h,
    -- 2) 익일 이월군
    SUM(
        CASE
            WHEN DATE(contact_time) != DATE(inform_survey_time) THEN 1
            ELSE 0
        END
    ) AS spillover_cnt,
    ROUND(
        AVG(
            CASE
                WHEN DATE(contact_time) != DATE(inform_survey_time) THEN TIMESTAMPDIFF(MINUTE, inform_survey_time, survey_start) / 60.0
            END
        ),
        1
    ) AS spill_wait1_h,
    ROUND(
        AVG(
            CASE
                WHEN DATE(contact_time) != DATE(inform_survey_time) THEN TIMESTAMPDIFF(MINUTE, contact_time, survey_start) / 60.0
            END
        ),
        1
    ) AS spill_total_survey_h
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY DATE(contact_time)
ORDER BY contact_date;
-- [전이 효과 요약]:
-- 1) 1/1 초기: 당일 이관군 Wait 1은 10.7시간, 익일 이월군은 14.4시간(총 대기 24.1시간)으로 대기열 팽창 전에는 빠르게 소화됨
-- 2) 1/3~1/5 피크: 이미 현장 큐에 150~270건이 적체되어 있어 당일 이관(82~92h)이나 이월(67~125h) 모두 극심한 대기 늪에 빠짐
-- => 결론: 접수 이월 자체보다 '일별 현장 조사 가능 규모(CAPA 69건)가 접수 적재 규모(135건)'를 따라가지 못해서 현장 대기시간이 증가하는 것이 핵심 병목
-- ---------------------------------------------------------------------
-- 3-5. [종합 실사 CAPA 정량화] 현장 일일 실사 처리능력(CAPA) 및 인입 과부하율 단일 집계
-- ---------------------------------------------------------------------
-- [분석 의도]:
-- - 3-2의 일자별 수치를 바탕으로, 전체 실사의 96.2%(892건)가 집중 처리된 실질 가동 기간(1/1~1/14, 14일) 동안
-- - 현장 기술팀의 '지속 실사 CAPA(일평균 63.7건, 피크 71.3건)'와 1인당 소화량, 그리고 일일 접수량(135건) 대비 과부하율 산출
WITH DailySurveyStats AS (
    SELECT DATE(survey_start) AS survey_date,
        COUNT(*) AS daily_cnt,
        COUNT(DISTINCT survey_worker) AS active_tech_cnt,
        SUM(
            TIMESTAMPDIFF(MINUTE, survey_start, survey_complete) / 60.0
        ) AS daily_hours
    FROM case_master_view
    WHERE objectKey IS NOT NULL
        AND DATE(survey_start) BETWEEN '1970-01-01' AND '1970-01-14'
    GROUP BY DATE(survey_start)
)
SELECT COUNT(*) AS `실질가동분석일수(일)`,
    SUM(daily_cnt) AS `기간총실사소화(건)`,
    -- 1) 현장 일일 실사 지속 CAPA (14일간 지속 소화량 63.7건/일)
    ROUND(AVG(daily_cnt), 1) AS `일평균_실사CAPA(건/일)`,
    -- 2) 기술자 조직 규모
    MAX(active_tech_cnt) AS `총가동기술자수(명)`,
    -- 3) 기술자 1인당 일일 실사 소화량
    ROUND(AVG(daily_cnt) / MAX(active_tech_cnt), 1) AS `기술자1인당_일일실사CAPA(건/인)`,
    -- 4) 현장 기술팀의 하루 순수 실사 투입 공수
    ROUND(AVG(daily_hours), 1) AS `일평균_실사투입공수(h/일)`,
    -- 5) 일일 인입량(135건) 대비 실사 소화율 및 과부하율
    ROUND(AVG(daily_cnt) * 100.0 / 135.0, 1) AS `접수인입대비_실사소화율(%)`,
    ROUND(135.0 * 100.0 / AVG(daily_cnt), 1) AS `현장CAPA대비_인입과부하율(%)`
FROM DailySurveyStats;
-- [종합 실사 CAPA 요약]:
-- 1) 실질 가동 모수: 1/1~1/14(14일간) 전체 실사의 96.2%(892건)를 소화 (1/15 이후는  잔여 물량으로 급감)
-- 2) 현장 일일 실사 지속 CAPA: 14일 지속 운영 평균 63.7건/일 ( 잔여 적체 소화기 60건 안팎 유지)
-- 3) 1인당 소화량: 기사 1인당 일평균 5.8~6.9건(약 4.0~4.5시간) 소화 (수리 작업과 병행 투입되므로 이것이 물리적 상한선)
-- 4) 과부하율: 접수부서가 하루 135건을 쏟아낼 때 현장 CAPA는 63.7건(소화율 47.2%)에 불과하여, CAPA 대비 211.9%의 극심한 과부하 발생
-- ---------------------------------------------------------------------
-- 4. [사전 접수 분류 vs 현장 수리 정합성 심층 검증 (TO-BE 우회 타당성)]
-- ---------------------------------------------------------------------
-- [분석 가설]:
-- 1) 접수 단계에서 부여된 사전 수리 유형(P, B, E)이 현장 실사 후 결정된 실제 수리 방식과 얼마나 일치하는가?
-- 2) 접수 단계의 사전 분류를 신뢰하고 현장 실사를 우회(Bypass)시킬 수 있는 정량적 타당성이 존재하는가?
-- 4-1. 접수 시점 속성(Repairtype) 및 현장 실사 확정 속성(RepairCode) 부여 시점 확인
-- 1) 접수 단계: 티켓 발행 완료 시점에 접수원의 고객 상담을 기반으로 사전 수리 방식(P, B, E) 확정
SELECT taskid,
    eventtype,
    Repairtype
FROM repair_logs
WHERE Repairtype IS NOT NULL;
-- 2) 현장 단계: 40분간의 현장 실사(Survey) 완료 시점에 기술자가 실사 수리코드(1, 2, 3, 4) 최종 확정
SELECT taskid,
    eventtype,
    RepairCode
FROM repair_logs
WHERE RepairCode IS NOT NULL;
-- 4-2. 사전 분류(planned_repair_type) × 실사 수리코드(repair_code) 교차 분포
SELECT planned_repair_type,
    repair_code,
    COUNT(*) AS cnt
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY planned_repair_type,
    repair_code WITH ROLLUP;
-- 4-3. 사전 분류(planned_repair_type) × 첫 실행 수리작업(rep1_task) 교차 분포
SELECT planned_repair_type,
    rep1_task,
    COUNT(*) AS cnt
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY planned_repair_type,
    rep1_task WITH ROLLUP;
-- 4-4. [핵심 교차 분석] 사전 분류 × 실사 수리코드 × 1차 수리 작업 3단 정합성 검증
SELECT planned_repair_type,
    repair_code,
    rep1_task,
    COUNT(*) AS cnt,
    -- 1) 해당 카테고리(P, B, E) 그룹 내 비중 (%)
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY planned_repair_type),
        1
    ) AS category_ratio_pct,
    -- 2) 전체 927건 대비 비중 (%)
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS total_ratio_pct
FROM case_master_view
WHERE objectKey IS NOT NULL
GROUP BY planned_repair_type,
    repair_code,
    rep1_task
ORDER BY planned_repair_type,
    repair_code,
    cnt DESC;
-- [사전 분류 정합성 분석 요약]:
-- 1) E형 (사내수리 370건, 전체의 39.9%):
--    • E-1(234건) + E-2(136건) = 100.0% 전원 사내수리(InternRepair)로 완결 ➔ 접수-현장 정합도 100%
-- 2) P형 (즉시/사내 439건, 전체의 47.4%):
--    • P-1(298건) + P-3(67건) = 365건(83.1%) 현장 즉시수리(ImmediateRepair) 완결
--    • P-2(36건, 8.2%) 사내수리 완결 ➔ 사내 자체 역량으로 총 401건(91.3%) 완결
--    • P-4(38건, 8.7%)만 전문 외주수리(ExternRepair)로 전환
-- 3) B형 (복합진단 118건, 전체의 12.7%):
--    • B-1(즉시 18건, 15.3%), B-2/3(사내 79건, 66.9%), B-4(외주 21건, 17.8%)로 분산
--    • 사전 판단이 어려워 현장 전문 인력의 방문 실사가 필수적인 유일한 영역
-- 4) 정량 종합:
--    • 접수원 사전 분류의 사내 완결 정합도는 87.3%(낙관적 809건) ~ 83.2%(외주 제외 보수적 771건)에 달함
--    • 즉, 접수 매뉴얼의 분류 방향성은 이미 현장과 일치하며, 실사 대기열 우회(Bypass) 전략의 수학적 타당성이 완벽히 입증됨
-- =========================================================================================
-- [비즈니스 인사이트 및 TO-BE 프로세스 개선 가설]
-- =========================================================================================
-- 1. 접수원 사전 판단의 높은 정합성과 이론적 극단 가설:
--    - 사측 접수원의 사전 접수 매뉴얼 방향성은 실제 수리 방향과 상당 부분 일치한다.
--      (E형은 100% 사내수리, P형은 91.3%가 사내 자체 종결: 즉시 365건 + 사내 36건)
--    - 극단적인 대안으로, E형(사내수리)과 P형(즉시수리)을 현장 실사 대기열에 세우지 않고 
--      해당 수리팀으로 직행시킨다면, 실사 대기열 유입량을 83.2% ~ 87.3% 원천 감축할 수 있다:
--      * 낙관적(87.3%): E형 전체(370건) + P형 전체(439건) = 총 809건 실사 제외
--      * 보수적(83.2%): 외주로 빠질 리스크가 있는 P-4(38건)는 제외하고 사내 완결 확정 771건만 실사 제외
--    - 결과적으로 일일 실사 유입량이 기사 일일 CAPA(69건)를 훨씬 밑돌게 되어(14.8~19.5건/일), 
--      76.8시간에 달하는 실사 병목 적체는 구조적으로 즉시 소멸된다.
--
-- 2. 그럼에도 AS-IS가 이중 출장 구조를 유지할 수밖에 없었던 원인 (정보 해상도의 한계):
--    - 이러한 높은 사전 적중률에도 불구하고 현장이 '선 실사 ➔ 후 수리' 방식을 고수한 이유는,
--    - 기존 매뉴얼의 정보 수집 해상도가 단순 알파벳 대분류(E, P)에 불과했기 때문이라고 생각한다.
--    - 현장 기술자 입장에서는 알파벳 코드로 차에 실어갈 구체적인 자재/규격을 특정할 수 없어, 
--      결국 40분짜리 현장 실사를 통해 부품을 직접 확인해야만 했다.

-- 3. 현실적 해결책: '사전 접수 매뉴얼의 고도화 (부품 특정화)'
--    - 실사를 억지로 생략하는 것이 아니라, 현장 기술자가 신뢰할 수 있도록 접수 단계의 정보 해상도를 끌어올려 즉시 1회 방문 수리로 전향한다:
--    - 1) E형 (사내수리 370건): 모바일 사진/라벨 확인 ➔ 사전 부품 별도 챙긴 후 1회 방문 수리 직행 (실사 40분 + 자재대기 38.7h 제거).
--    - 2) P형 (즉시수리 365건): 단순 고장 사진 확인 ➔ 범용 부품 적재 차량 출동으로 당일 1회 원샷 완결.
--    - 3) B형 (복합진단 118건): 사진 식별 불가 건(12.7%)만 전문 실사 큐 배정 (실사 큐 927건 ➔ 118건으로 87.3% 원천 감축).
--    - 4) 채널별 인프라 고도화:
--         * 웹 접수(241건, 26%): 온라인 접수 양식의 질문 체크리스트 고도화(사진/라벨 필수 첨부, 증상 세분화)로 초기 인입 해상도 극대화.
--         * 전화/대면 접수(479건, 52%): 접수원 표준 질의 스크립트 적용 및 통화 중 '모바일 사진 등록 링크(SMS)' 발송 연계.
--         ➔ 이를 통해 접수원의 P, B, E 코드를 세부 자재/수리 하위 코드 수준으로 정밀화하여 현장 수리팀으로 다이렉트 인계.

-- -----------------------------------------------------------------------------------------
-- 5. [TO-BE 정량 검증] 패스트트랙 시나리오별 실사 CAPA 부하 경감 및 OLS 리드타임 단축 시뮬레이션
-- -----------------------------------------------------------------------------------------
-- [목적]: 접수 신뢰 수준에 따른 4단계 시나리오(극보수 E형만 ~ 낙관적 전체)별 
--         일일 실사 유입량, 기사 11인 CAPA(68건) 대비 부하율, 그리고 OLS(+1.12h/h) 리드타임 단축치 산출
WITH ScenarioBase AS (
    SELECT 
        caseID,
        planned_repair_type,
        repair_code,
        rep1_task
    FROM case_master_view
    WHERE objectKey IS NOT NULL
),
ScenarioMetrics AS (
    SELECT 
        -- 시나리오 1: [극보수] E형만 신뢰 (실패 리스크 0%, E형 100% 직행)
        '1. 극보수 (E형만 직행)' AS scenario_name,
        SUM(CASE WHEN planned_repair_type = 'E' THEN 1 ELSE 0 END) AS bypass_cases,
        COUNT(*) - SUM(CASE WHEN planned_repair_type = 'E' THEN 1 ELSE 0 END) AS remaining_survey_cases
    FROM ScenarioBase
    UNION ALL
    SELECT 
        -- 시나리오 2: [보수 1안] E형 + P-1, P-3(즉시수리 완결) 직행
        '2. 보수 1안 (E형 + P-1,3 즉시 직행)' AS scenario_name,
        SUM(CASE WHEN planned_repair_type = 'E' OR (planned_repair_type = 'P' AND repair_code IN (1, 3)) THEN 1 ELSE 0 END) AS bypass_cases,
        COUNT(*) - SUM(CASE WHEN planned_repair_type = 'E' OR (planned_repair_type = 'P' AND repair_code IN (1, 3)) THEN 1 ELSE 0 END) AS remaining_survey_cases
    FROM ScenarioBase
    UNION ALL
    SELECT 
        -- 시나리오 3: [보수 2안] 외주 리스크 제외 E형 + P형 사내종결(401건) 직행
        '3. 보수 2안 (E형 + P형 사내자체 완결)' AS scenario_name,
        SUM(CASE WHEN planned_repair_type = 'E' OR (planned_repair_type = 'P' AND rep1_task IN ('ImmediateRepair', 'InternRepair')) THEN 1 ELSE 0 END) AS bypass_cases,
        COUNT(*) - SUM(CASE WHEN planned_repair_type = 'E' OR (planned_repair_type = 'P' AND rep1_task IN ('ImmediateRepair', 'InternRepair')) THEN 1 ELSE 0 END) AS remaining_survey_cases
    FROM ScenarioBase
    UNION ALL
    SELECT 
        -- 시나리오 4: [낙관적] E형 전체 + P형 전체 (809건) 직행
        '4. 낙관적 (E형 + P형 전체 직행)' AS scenario_name,
        SUM(CASE WHEN planned_repair_type IN ('E', 'P') THEN 1 ELSE 0 END) AS bypass_cases,
        COUNT(*) - SUM(CASE WHEN planned_repair_type IN ('E', 'P') THEN 1 ELSE 0 END) AS remaining_survey_cases
    FROM ScenarioBase
)
SELECT 
    scenario_name AS `패스트트랙 시나리오`,
    bypass_cases AS `실사우회 건수(건)`,
    ROUND(bypass_cases * 100.0 / 927.0, 1) AS `우회비율(%)`,
    remaining_survey_cases AS `실사큐 잔여(건)`,
    -- 일일 실사 유입량 (8일 피크 일평균 134.3건 기준)
    ROUND(134.3 * (remaining_survey_cases / 927.0), 1) AS `일일 실사유입(건/일)`,
    -- 현장 기사 11인 일일 CAPA(68.0건) 대비 부하율 (%)
    ROUND((134.3 * (remaining_survey_cases / 927.0) / 68.0) * 100.0, 1) AS `기사CAPA 부하율(%)`,
    -- 보수적 대기 20% 단축 시 절감시간 (76.8h 기준)
    ROUND(76.81 * 0.20, 1) AS `보수적20%_실사대기절감(h)`,
    -- OLS 회귀계수(+1.12h/h) 적용 전체 리드타임 순단축 효과
    ROUND(76.81 * 0.20 * 1.12, 1) AS `OLS_리드타임_순단축(h)`
FROM ScenarioMetrics;