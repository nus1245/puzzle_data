# 5. 전처리 완료 데이터셋 딕셔너리 및 SQL 집계 참조 가이드 (Cleaned Data Dictionary & SQL Reference)

> **문서 목적**: 전처리 완료 데이터셋(`repair_cleaned.csv`)의 24개 전체 열 명세, 속성 정의, 결측 특성 및 SQL 환경에서의 집계·프로세스 마이닝 분석 참조 기준 제공.  
> **기준 파일**: [repair_cleaned.csv](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/repair_cleaned.csv) (13,262행 x 24열, 2.18 MB, UTF-8-SIG)  
> **연계 노트북**: [analysis.ipynb](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/analysis.ipynb) (Cell 75~84 종합 성과 검증 및 CSV 내보내기)  
> **시각화 구성표**: [고해상도 슬라이드용 다이어그램 PNG](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/01_cleaned_data_schema.png)  |  [인터랙티브 웹 스키마 뷰어 HTML](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/data_schema_viewer.html)

---

## 1. 전처리 완료 데이터셋 24개 열(Columns) 종합 명세서

전체 24개 열을 기능 및 분석 목적에 따라 **4대 그룹**으로 분류.

### [그룹 1] 프로세스 마이닝 및 시계열 분석 핵심 정제 컬럼 (★ SQL 주력 활용)
모든 결측치와 이상치가 100% 해소된 컬럼군으로, SQL 집계 쿼리 및 리드타임 계산의 절대적 기준축으로 활용.

| 열 순번 | 컬럼명 | 데이터 타입 | 결측치 건수 (비율) | 샘플 데이터 | 정의 및 SQL 분석 역할 |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **24** | **`clean_timestamp`** | `TIMESTAMP` | **0건 (0.0%)** | `1970-01-02 08:08:00` | **최종 정제 타임스탬프**. `re_date`와 `re_time`을 결합한 일시. 리드타임 계산, 대기시간 산출, 윈도우 함수 정렬의 필수 기준축. |
| **22** | **`re_date`** | `DATE` | **0건 (0.0%)** | `1970-01-02` | **정제된 일자** (`YYYY-MM-DD`). 1905년 및 2020~2022년 이상치 879건을 전수 교정하여 13,262건 전체가 1970년 정상 수리 기간으로 귀속됨. |
| **23** | **`re_time`** | `TIME` | **0건 (0.0%)** | `08:08` | **정제된 시각** (`HH:MM`). 결측(13건) 및 더미 '0:00'(15건) 총 28건 의심군을 인과관계 및 통계적 모수 추정으로 100% 복원 완료. |
| **19** | **`seq`** | `INTEGER` | **0건 (0.0%)** | `1` | **13대 표준 프로세스 대분류 순서** (`1~13`). 시간 결측이나 동일 시각 이벤트 간 비즈니스 인과 정렬 축 (`ORDER BY seq`). |
| **20** | **`sub_seq`** | `INTEGER` | **0건 (0.0%)** | `1` | **작업 내 상세 단계 순서** (`start` = 1, `complete` = 2, 단일 마일스톤 = 1). |
| **21** | **`작업단계`** | `VARCHAR(50)`| **0건 (0.0%)** | `[1-1] FirstContact_complete` | 시퀀스와 작업명, 이벤트유형을 결합한 가독성 복합 라벨. |

---

### [그룹 2] 프로세스 필수 식별자 및 비즈니스 분류 컬럼
단일 프로세스 인스턴스 추적 및 부서/주체별 다차원 세그먼트 집계에 활용.

| 열 순번 | 컬럼명 | 데이터 타입 | 결측치 건수 (비율) | 샘플 데이터 | 정의 및 SQL 분석 역할 |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **1** | **`caseID`** | `INTEGER` | **0건 (0.0%)** | `1` | **수리 요청 접수 번호** (1 ~ 1,000). 단일 수리 사건(Process Instance) 식별자 (`GROUP BY caseID`). |
| **2** | **`taskID`** | `VARCHAR(50)`| **0건 (0.0%)** | `FirstContact` | **수행 액티비티 업무명** (CASE 1 결측 2건 복원 완료, 총 13개 고유 작업). 프로세스 노드(Node) 구성 요소. |
| **3** | **`originator`** | `VARCHAR(50)`| **0건 (0.0%)** | `Dian` | **업무 수행 담당자** (CASE 2 결측 2건 복원 완료, Anne·Paul 등 실무자 13명 + System). 리소스 분석 활용. |
| **4** | **`eventtype`** | `VARCHAR(20)`| **0건 (0.0%)** | `complete` | **이벤트 라이프사이클** (`start` / `complete`, CASE 3 결측 5건 복원 완료). 순수 작업시간과 대기시간 분리 기준. |
| **15** | **`task_group`** | `VARCHAR(20)`| **0건 (0.0%)** | `접수` | **3대 업무 그룹** (`접수`, `현장`, `정산`). 대분류 단계별 소요시간 및 병목 분석 축. |
| **16** | **`SUBJECT`** | `VARCHAR(20)`| **0건 (0.0%)** | `사람` | **수행 주체 구분** (`사람`, `시스템`). 자동화 업무와 인적 업무 간 생산성 비교 지표. |
| **17** | **`외주여부`** | `VARCHAR(20)`| **0건 (0.0%)** | `내부` | **현장 작업 외주 여부** (`내부`, `외부`, `-`). 사내 수리 vs 외주 위탁 수리 성과 대조 지표. |

---

### [그룹 3] 도메인 수리 속성 컬럼 (구조적 결측치)
수리 실행 task 이벤트 발생 시점에만 로깅되는 업무 도메인 속성 (행 삭제 금지 대상).

| 열 순번 | 컬럼명 | 데이터 타입 | 결측치 건수 (비율) | 샘플 데이터 | 정의 및 특성 설명 |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **5** | **`contact`** | `VARCHAR(20)`| 12,262건 (92.5%) | `Phone` | 최초 고객 접수 채널 (`Web`, `Phone`). FirstContact 시점에만 발생. |
| **6** | **`RepairType`** | `VARCHAR(20)`| 12,335건 (93.0%) | `E` | 수리 방식 코드 (`P`, `E` 등). 수리 task 실행 시점에 기록. |
| **7** | **`objectKey`** | `FLOAT` | 12,335건 (93.0%) | `1340.0` | 수리 대상 주택/부품 고유 식별 번호. 동일 주택 반복 수리 분석 활용. |
| **8** | **`RepairInternally`** | `BOOLEAN` | 12,335건 (93.0%) | `True` | 사내 직접 수리 여부 (`True` / `False`). 외주 위탁 여부의 도메인 플래그. |
| **9** | **`EstimatedRepairTime`**| `FLOAT` | 12,335건 (93.0%) | `240.0` | 작업 전 산정된 예상 수리 시간 (분 단위). 계획 대비 실적 오차 분석 활용. |
| **10** | **`RepairCode`** | `FLOAT` | 12,335건 (93.0%) | `1.0` | 수리 난이도 및 작업 유형 카테고리 분류 코드. |
| **11** | **`RepairOK`** | `BOOLEAN` | 11,408건 (86.0%) | `True` | 수리 정상 종료 여부 (`True` / `False`). 재수리 및 재작업(Rework) 유발 판별 지표. |

---

### [그룹 4] 원본 추적 및 정제 전 이력 컬럼 (검증 및 감사용)
전처리 전 최초 수집 상태 데이터 보존용 컬럼군.

| 열 순번 | 컬럼명 | 데이터 타입 | 결측치 건수 (비율) | 샘플 데이터 | 설명 및 유의사항 |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **12** | **`date`** | `VARCHAR(20)`| 13건 (0.1%) | `1970-01-02` | 원본 일자 컬럼 (2020~2022년 드래그 오염 보존, SQL 분석 시 `re_date` 사용 권장). |
| **13** | **`time`** | `VARCHAR(20)`| 13건 (0.1%) | `0:00` | 원본 시각 컬럼 (초기 NaN 및 더미 0:00 상태, SQL 분석 시 `re_time` 사용 권장). |
| **14** | **`timestamp`** | `VARCHAR(30)`| 13건 (0.1%) | `1970-01-02 00:00:00` | 원본 `date` + `time` 결합 일시 (SQL 분석 시 `clean_timestamp` 필수 사용). |
| **18** | **`수정된연도`** | `FLOAT` | 13건 (0.1%) | `1970.0` | 1905년 이상치(6건) 판정 과정에서 생성된 보조 컬럼. |

---

## 2. 범주형 변수 허용값 및 세부 비즈니스 매핑 기준

### ① `taskID` (13대 업무) 및 시퀀스 매핑
| seq | sub_seq | taskID | 국문 명칭 | task_group | SUBJECT | 외주여부 | 페어(Pair) 구조 |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | 1 | `FirstContact` | 최초 접수 | 접수 | 사람 | 내부 | 단일 마일스톤 (`complete`) |
| **2** | 1 | `InformClientWrongPlace`| 오접수 안내/종료 | 접수 | 사람 | 내부 | 단일 마일스톤 (`complete`) |
| **3** | 1, 2 | `MakeTicket` | 티켓 발행 | 접수 | 사람 | 내부 | 1:1 페어 (`start` ➔ `complete`) |
| **4** | 1, 2 | `ArrangeSurvey` | 방문일정 조율 | 접수 | 사람 | 내부 | 1:1 페어 (`start` ➔ `complete`) |
| **5** | 1 | `InformClientSurvey` | 조율완료 알림 | 접수 | 시스템 | - | 단일 마일스톤 (`complete`) |
| **6** | 1, 2 | `Survey` | 현장 방문 조사 | 현장 | 사람 | 내부 | 1:1 페어 (`start` ➔ `complete`) |
| **7** | 1, 2 | `ImmediateRepair` | 당일 경미 즉시수리 | 현장 | 사람 | 내부 | 1:1 페어 (`start` ➔ `complete`) |
| **8** | 1, 2 | `InternRepair` | 사내 전문 수리 | 현장 | 사람 | 내부 | 1:1 페어 (`start` ➔ `complete`) |
| **9** | 1 | `ExternRepair` | 외주 위탁 수리 | 현장 | 사람 | 외부 | 단일 착수 (`start`) |
| **10** | 1 | `RepairReady` | 수리완료 등록 | 현장 | 시스템 | - | 단일 마일스톤 (`complete`) |
| **11** | 1 | `ReadyInformClient` | 고객 완료 안내 | 정산 | 시스템 | - | 단일 마일스톤 (`complete`, 병렬) |
| **12** | 1 | `SendTicketToFinAdmin` | 재무팀 이관 | 정산 | 시스템 | - | 단일 마일스톤 (`complete`, 병렬) |
| **13** | 1 | `TicketReady` | 티켓 최종 종결 | 정산 | 시스템 | - | 단일 마일스톤 (`complete`, 최종) |

### ② `originator` (작업자) 구분
- **사람 실무자 (13명)**:
  - 접수/조사 담당: `Dian`, `Monica`, `Anne`, `Jane`, `John`, `Kevin` 등
  - 수리 전문 기술자: `Paul`, `Barbara`, `Bert` 등
  - 외주 협력업체: `DoIt`, `FixIt`
- **시스템 자동화 (1개)**:
  - `System`: 고객 알림 발송 및 정산/마감 자동화 처리

---

## 3. SQL 테이블 생성(DDL) 및 임포트 구문

### PostgreSQL / MySQL / DuckDB 공용 DDL
```sql
CREATE TABLE repair_logs (
    caseID              INTEGER NOT NULL,
    taskID              VARCHAR(50) NOT NULL,
    originator          VARCHAR(50) NOT NULL,
    eventtype           VARCHAR(20) NOT NULL,
    contact             VARCHAR(20),
    RepairType          VARCHAR(20),
    objectKey           FLOAT,
    RepairInternally    BOOLEAN,
    EstimatedRepairTime FLOAT,
    RepairCode          FLOAT,
    RepairOK            BOOLEAN,
    date                VARCHAR(20),
    time                VARCHAR(20),
    timestamp           VARCHAR(30),
    task_group          VARCHAR(20) NOT NULL,
    SUBJECT             VARCHAR(20) NOT NULL,
    외주여부            VARCHAR(20) NOT NULL,
    수정된연도          FLOAT,
    seq                 INTEGER NOT NULL,
    sub_seq             INTEGER NOT NULL,
    작업단계            VARCHAR(50) NOT NULL,
    re_date             DATE NOT NULL,
    re_time             TIME NOT NULL,
    clean_timestamp     TIMESTAMP NOT NULL
);

-- 인덱스 생성 권장 (조회 속도 최적화)
CREATE INDEX idx_repair_case_time ON repair_logs (caseID, clean_timestamp, seq, sub_seq);
CREATE INDEX idx_repair_task_group ON repair_logs (task_group, taskID);
```

---

## 4. 실전 SQL 집계 및 프로세스 분석 쿼리 템플릿

### 쿼리 1. 케이스별 총 소요시간(Lead Time) 및 기본 현황 산출
```sql
SELECT 
    caseID,
    MIN(clean_timestamp) AS case_start,
    MAX(clean_timestamp) AS case_end,
    COUNT(*) AS total_events,
    ROUND((JULIANDAY(MAX(clean_timestamp)) - JULIANDAY(MIN(clean_timestamp))), 2) AS lead_time_days,
    ROUND((JULIANDAY(MAX(clean_timestamp)) - JULIANDAY(MIN(clean_timestamp))) * 24, 1) AS lead_time_hours
FROM repair_logs
GROUP BY caseID
ORDER BY lead_time_days DESC;
```

### 쿼리 2. 3대 업무 그룹(접수/현장/정산) 및 주체별 작업 건수 집계
```sql
SELECT 
    task_group,
    SUBJECT,
    taskID,
    originator,
    COUNT(*) AS event_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY task_group), 1) AS group_ratio_pct
FROM repair_logs
GROUP BY task_group, SUBJECT, taskID, originator
ORDER BY task_group, event_count DESC;
```

### 쿼리 3. 수리 유형별(사내수리 vs 외주수리) 평균 리드타임 비교
```sql
WITH CaseRepairSummary AS (
    SELECT 
        caseID,
        MAX(CASE WHEN taskID = 'ExternRepair' THEN '외주수리(Extern)'
                 WHEN taskID = 'InternRepair' THEN '사내수리(Intern)'
                 WHEN taskID = 'ImmediateRepair' THEN '즉시수리(Immediate)'
                 ELSE '기타' END) AS repair_mode,
        ROUND((JULIANDAY(MAX(clean_timestamp)) - JULIANDAY(MIN(clean_timestamp))), 2) AS lead_time_days
    FROM repair_logs
    GROUP BY caseID
)
SELECT 
    repair_mode,
    COUNT(*) AS case_count,
    ROUND(AVG(lead_time_days), 2) AS avg_lead_time_days,
    ROUND(MIN(lead_time_days), 2) AS min_lead_time_days,
    ROUND(MAX(lead_time_days), 2) AS max_lead_time_days
FROM CaseRepairSummary
GROUP BY repair_mode
ORDER BY avg_lead_time_days DESC;
```

### 쿼리 4. 단계 간 이동 시간 및 병목(대기시간) 탐색 윈도우 쿼리
```sql
WITH EventTransitions AS (
    SELECT 
        caseID,
        taskID AS current_task,
        clean_timestamp AS current_time,
        LEAD(taskID) OVER (PARTITION BY caseID ORDER BY clean_timestamp, seq, sub_seq) AS next_task,
        LEAD(clean_timestamp) OVER (PARTITION BY caseID ORDER BY clean_timestamp, seq, sub_seq) AS next_time
    FROM repair_logs
)
SELECT 
    current_task,
    next_task,
    COUNT(*) AS transition_count,
    ROUND(AVG((JULIANDAY(next_time) - JULIANDAY(current_time)) * 24), 2) AS avg_waiting_hours,
    ROUND(MAX((JULIANDAY(next_time) - JULIANDAY(current_time)) * 24), 2) AS max_waiting_hours
FROM EventTransitions
WHERE next_task IS NOT NULL
GROUP BY current_task, next_task
HAVING COUNT(*) >= 10
ORDER BY avg_waiting_hours DESC;
```
