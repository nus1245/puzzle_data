# 📌 프로젝트 인수인계 및 노트북 환경 세팅 가이드 (Handover & Setup Guide)

> **문서 목적**: 다른 PC나 노트북(새로 설치된 Antigravity IDE 환경)에서 이어서 분석을 진행할 때, 프로젝트 맥락 유지 및 3분 내 동일 환경 세팅 후 후속 분석을 재개하기 위한 인수인계 가이드.  
> **최종 수정일**: 2026-10-22  
> **현재 브랜치**: `main`

---

## 1. 프로젝트 개요 및 현재 진행 현황 (Current Progress)

- **분석 파일**: [analysis.ipynb](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/analysis.ipynb)
- **원본 데이터**: [repair2.csv](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/repair2.csv) (1,000건 caseID, 13,262행 이벤트 로그)
- **전처리 완료 데이터**: [repair_cleaned.csv](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/repair_cleaned.csv) (1,000건 caseID, 13,262행 x 24열, SQL 집계용)
- **현재 완료된 작업 (Cell 0 ~ 84, 총 85개 셀)**:
  1. **CASE 1 (`taskID` 2건 결측치 복원)**: FirstContact(7124행), InformClientSurvey(7785행) 복원 완료
  2. **CASE 2 (`originator` 2건 결측치 복원)**: 1:1 시작-완료 짝 매칭으로 Anne(8217행, Survey), Paul(12880행, InternRepair) 복원 완료
  3. **CASE 3 (`eventtype` 5건 결측치 복원)**: Pair(start 2건, complete 1건) 및 단일 마일스톤(complete 2건) 100% 매칭 복원 완료
  4. **CASE 4 (`DATE` 873건 결측치 및 연도 이상치 복원)**: 1905년(6건) 및 2020~2022년(860건), NaT(13건)을 그룹 기준 일자 `re_date`로 100% 복원 완료
  5. **CASE 5 (`TIME` 결측치 및 시간 이상치 정밀 추정 - 28건 전수 100% 완료)**:
     - **[CASE 5 의심군 전수 추출 (Cell 55~56)]**: 결측(13건) + `0:00`(15건) = **총 28건 의심군 전수 추출 (`anom_time_rows`)**
     - **5-1 ~ 5-4 (`접수 공정 16건 100% 완료`, Cell 57~64)**: 1번 FC ➔ 3번 MT 착수 0.0분 동시성 입증, 3번 소요시간 중앙값(4분) 및 자정 실측 선별, 1번 동기화 완료
     - **5-5 ~ 5-6 (`현장조사 공정 2건 100% 완료`, Cell 67~70)**: 4·5번 즉시/동시 트리거, 6번 Survey 완료 앵커 기준 소요시간 중앙값(41분) 역산 대체 완료
     - **5-7 (`수리 공정 4건 100% 완료`, Cell 71~72)**: 외주수리 3대 진입 경로 0분 즉시 인계 입증, RepairReady 0분 동시 알림 및 전진 교정 완료
     - **5-8 (`정산 공정 6건 100% 완료`, Cell 73~74)**:
       - **병렬 진행성 및 TicketReady 막단 행동 실측 입증**: TicketReady 막단율 100.0%, 재무 51.18% vs 고객 48.82% 대등 비율 규명
       - **4대 대체 규칙 적용**: TicketReady 결측 2건(마지막 완료 작업 매핑), 정산 작업 결측 4건(TicketReady 시점 끝행동 매핑)
     - **최종 무결성 달성**: `anom_time_rows` 28건 전수 처리 완료 (잔여 0건), `df_clean['re_time']` 결측치 0건 (100% 무결성 확인)
  6. **기본 분석 및 전처리 성과 종합 검증 (Cell 75~82)**:
     - **통합 정밀 타임스탬프(`clean_timestamp`) 생성**: 13,262건 전수 결측 0건 (1970-01-01 ~ 1970-01-20 정상화)
     - **전처리 종합 성과표(Scorecard)**: 5대 핵심 컬럼 결측/이상치 100% 복원, 데이터 보존율 100.0% (임의 행 삭제 0건)
     - **케이스 리드타임 정상화**: 리드타임 산출 가능 비율 40.5% ➔ 100.0% (+59.5%p 향상, 왜곡 케이스 0건 달성)
     - **프로세스 마이닝 준비도(PM Ready)**: Case ID(100%), Activity(100%), Timestamp(100%) 완결도 확보
     - **5대 CASE 대표 샘플 1:1 대조표 구현**: 주요 이상치 행 원본 vs 전처리 결과 시각적 검증 완료
  7. **최종 데이터셋 CSV 내보내기 및 SQL 가이드 (Cell 83~84)**:
     - **`repair_cleaned.csv` 저장 완료**: 13,262행 x 24열, 2.18 MB, `utf-8-sig` 인코딩 적용 (한글 컬럼 깨짐 방지)
     - **SQL 스키마 매핑 가이드 제공**: DBeaver, SQLite, PostgreSQL 등 SQL DBMS 집계 분석 최적화 스키마 수립

---

## 2. 새 노트북(새로운 환경)에서 바로 시작하는 법

### [방법 A] 깃(Git)이 설치되어 있지 않은 경우 (가장 간편한 방법)
1. 브라우저에서 저장소 접속: [https://github.com/nus1245/puzzle_data](https://github.com/nus1245/puzzle_data)
2. 초록색 **`<> Code`** 버튼 ➔ **`Download ZIP`** 클릭
3. 다운로드된 ZIP 파일 압축 해제
4. Antigravity IDE 실행 후 **`File > Open Folder...`** (단축키: `Ctrl + K, Ctrl + O`) 로 압축 푼 폴더 열기

### [방법 B] 깃(Git)이 설치되어 있는 경우
```bash
git clone https://github.com/nus1245/puzzle_data.git
```
이후 Antigravity IDE에서 해당 폴더 열기.

---

### 필수 확장 프로그램 (Extensions)
Antigravity IDE 좌측 메뉴의 확장 아이콘(`Ctrl + Shift + X`)에서 확인 및 설치:
- **Python** (Microsoft)
- **Jupyter** (Microsoft)

---

### 환경 패키지 설치
Antigravity IDE 내장 터미널(`Ctrl + ~`) 열고 아래 명령어 입력:
```bash
pip install -r requirements.txt
```
*(requirements.txt에 pandas, numpy, matplotlib, seaborn, jupyter, ipykernel 포함)*

---

### 분석 노트북 재개
1. 좌측 탐색기에서 [analysis.ipynb](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/analysis.ipynb) 열기
2. 우측 상단 **`Select Kernel`** 클릭 ➔ 위에서 설치한 파이썬 환경 선택
3. 상단 **`Run All` (모두 실행)** 클릭 ➔ 완료된 전체 85개 셀(전처리·성과검증·CSV저장 100% 무결성) 일괄 실행 및 메모리 복원

---

## 3. 이어갈 다음 분석 과제 (Stage 2 Roadmap)

1. **Stage 2: AS-IS 프로세스 마이닝 도출 (Happy Path & DFG)**:
   - **Happy Path 분석**: 가장 빈번한 정상 수리 경로(전체 1,000개 케이스 중 점유율 %) 도출
   - **DFG (Directly-Follows Graph)**: 작업 간 전이 매트릭스 및 빈도/시간 기반 시각화
   - **병목 및 재작업(루프) 분석**: 이동 시간 및 수리 지연, 재작업이 일어나는 특정 병목 지점 탐색
2. **수리 유형별 리드타임 편차 분석**:
   - 내부수리(`InternRepair`) vs 외주수리(`ExternRepair`) vs 즉시수리(`ImmediateRepair`) 리드타임 비교 및 성능 분석
3. **SQL 환경 기반 집계 쿼리 분석**:
   - `repair_cleaned.csv`를 기반으로 한 부서/담당자/작업별 집계 쿼리 및 성능 분석

---

## 4. 🤖 새로운 세션의 AI 어시스턴트(Antigravity)를 위한 지침

> 사용자가 노트북 환경에서 질문할 경우, 위 세팅 가이드와 현재 완료된 전체 85개 셀(CASE 1~5, 성과 검증, CSV 내보내기 완료) 상태를 기반으로 직관적이고 가독성 높은 지원 유지. 복잡한 추상화(`locals()` 등)를 지양하고 직관적이고 깔끔한 코드 형태 견지.
