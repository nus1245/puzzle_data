# 📌 프로젝트 인수인계 및 노트북 환경 세팅 가이드 (Handover & Setup Guide)

> **문서 목적**: 다른 PC나 노트북(새로 설치된 Antigravity IDE 환경)에서 이어서 분석을 진행할 때, 프로젝트 맥락을 놓치지 않고 3분 내에 동일한 환경을 세팅하고 다음 단계를 진행할 수 있도록 작성된 가이드입니다.  
> **최종 수정일**: 2026-10-22  
> **현재 브랜치**: `main`

---

## 1. 프로젝트 개요 및 현재 진행 현황 (Current Progress)

- **분석 파일**: [analysis.ipynb](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/analysis.ipynb)
- **원본 데이터**: [repair2.csv](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/repair2.csv) (1,000건 caseID, 13,262행 이벤트 로그)
- **현재 완료된 작업 (Cell 1 ~ 63)**:
- **현재 완료된 작업 (5대 CASE 전처리 체계)**:
  1. **CASE 1 (`taskID` 2건 결측치 복원)**: FirstContact(7124행), InformClientSurvey(7785행) 복원 완료
  2. **CASE 2 (`originator` 2건 결측치 복원)**: 1:1 시작-완료 짝 매칭으로 Anne(8217행, Survey), Paul(12880행, InternRepair) 복원 완료
  3. **CASE 3 (`eventtype` 5건 결측치 복원)**: Pair(start 2건, complete 1건) 및 단일 마일스톤(complete 2건) 100% 매칭 복원 완료
  4. **CASE 4 (`DATE` 873건 결측치 및 연도 이상치 복원)**: 1905년(6건) 및 2020~2022년(860건), NaT(13건)을 그룹 기준 일자 `re_date`로 100% 복원 완료
  5. **CASE 5 (`TIME` 결측치 및 시간 이상치 정밀 추정)**:
     - **[기준 표본 정의 1]**: 접수 공정(1·3번) 전용 무결점 기준 모수 `df_baseline_receipt`(751건, 75.1%) 구축
     - **5-1 (`FirstContact`)**: 3번 start와의 시차 0.0분 완전 일치 규칙(명분) 확립 (실제 대체는 5-2 일괄 동기화)
     - **5-2 (`MakeTicket start`)**: `MakeTicket complete` 앵커 무결성 확인 ➔ 중앙값(4.0분) 역산 대체 ➔ 1번 FirstContact 0분 일괄 동기화
     - **[기준 표본 정의 2]**: 현장/조사 공정(4·5·6번) 전용 무결점 기준 모수 `df_baseline_survey`(655건, 65.5%) 구축
     - **5-3 (`현장/조사 공정 7건`)**: 4·5번 동시 트리거(0.0분) 및 6번 Survey 현장조사(중앙값 40.0분) 역산 대체 완료
     - *(잔여 과제: 5-4 수리 공정 4건, 5-5 정산 공정 6건)*

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
이후 Antigravity IDE에서 해당 폴더를 엽니다.

---

### 필수 확장 프로그램 (Extensions)
Antigravity IDE 좌측 메뉴의 확장 아이콘(`Ctrl + Shift + X`)에서 확인 및 설치:
- **Python** (Microsoft)
- **Jupyter** (Microsoft)

---

### 환경 패키지 설치
Antigravity IDE 내장 터미널(`Ctrl + ~`)을 열고 아래 명령어를 입력합니다:
```bash
pip install -r requirements.txt
```
*(requirements.txt에 pandas, numpy, matplotlib, seaborn, jupyter, ipykernel이 모두 포함되어 있습니다.)*

---

### 분석 노트북 재개
1. 좌측 탐색기에서 [analysis.ipynb](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/analysis.ipynb) 열기
2. 우측 상단 **`Select Kernel`** 클릭 ➔ 위에서 설치한 파이썬 환경 선택
3. 상단 **`Run All` (모두 실행)** 클릭 ➔ 오늘 완료한 53개 셀이 30초 내에 메모리에 복원됨

---

## 3. 이어갈 다음 분석 과제 (Stage 2 Roadmap)

1. **Stage 2: AS-IS 프로세스 마이닝 도출 (Happy Path & DFG)**:
   - **Happy Path 분석**: 가장 빈번한 정상 수리 경로(전체 1,000개 케이스 중 점유율 %) 도출
   - **DFG (Directly-Follows Graph)**: 작업 간 전이 매트릭스 및 빈도/시간 기반 시각화
   - **병목 및 재작업(루프) 분석**: 이동 시간 및 수리 지연, 재작업이 일어나는 특정 병목 지점 탐색
2. **수리 유형별 리드타임 편차 분석**:
   - 내부수리(`InternRepair`) vs 외주수리(`ExternRepair`) vs 즉시수리(`ImmediateRepair`) 리드타임 비교 및 성능 분석

---

## 4. 🤖 새로운 세션의 AI 어시스턴트(Antigravity)를 위한 지침

> 사용자가 노트북 환경에서 질문할 경우, 위 세팅 가이드와 현재 완료된 Cell 53 상태를 기반으로 친절하고 직관적으로 지원할 것. 복잡한 추상화(`locals()` 등)를 지양하고 직관적이고 깔끔한 코드를 유지할 것.
