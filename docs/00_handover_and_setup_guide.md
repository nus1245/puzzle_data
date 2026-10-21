# 📌 프로젝트 인수인계 및 노트북 환경 세팅 가이드 (Handover & Setup Guide)

> **문서 목적**: 다른 PC나 노트북(새로 설치된 Antigravity IDE 환경)에서 이어서 분석을 진행할 때, 프로젝트 맥락을 놓치지 않고 3분 내에 동일한 환경을 세팅하고 다음 단계를 진행할 수 있도록 작성된 가이드입니다.  
> **최종 수정일**: 2026-10-22  
> **현재 브랜치**: `main`

---

## 1. 프로젝트 개요 및 현재 진행 현황 (Current Progress)

- **분석 파일**: [analysis.ipynb](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/analysis.ipynb)
- **원본 데이터**: [repair2.csv](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/repair2.csv) (1,000건 caseID, 13,262행 이벤트 로그)
- **현재 완료된 작업 (Cell 1 ~ 53)**:
  1. **용어 및 컬럼 표준화**:
     - `task_group`: '접수', '현장', '정산' (영문 snake_case)
     - `seq`: 1~13 (작업 대분류 순서)
     - `sub_seq`: 1~2 (start=1, complete=2)
     - `작업단계`: `[seq-sub_seq] taskID_eventtype` 형태
  2. **날짜 이상치(873건) 100% 복원**:
     - 엑셀 드래그 오류(860건) 및 NaT(13건)을 케이스별 정상 날짜 기준 `re_date`로 복원 완료.
  3. **접수 시간 더미값(`0:00`) 순차 보정**:
     - `0:00`은 실제 자정이 아닌 누락/기본값(Placeholder)으로 판명.
     - **3번 시작(`MakeTicket start`, 5건)**: `MakeTicket complete` 시각에서 중앙값 **4.0분**을 감산하여 보정.
     - **1번(`FirstContact`, 6건)**: 정상 케이스에서 3번 시작과 100% 동일(시차 0.0분)하므로 복원된 3번 시작 시각으로 매핑 대체 완료.

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

## 3. 내일 이어갈 다음 분석 과제 (Next Roadmap)

1. **잔여 시간 결측치(7건 NaT) 처리**:
   - 현장(`task_group == '현장'`, seq 6~10) 및 정산(`task_group == '정산'`, seq 11~13)에 존재하는 7건의 time 결측치 확인 및 업무 규칙 기반 대체.
2. **Stage 2: AS-IS 프로세스 마이닝 도출**:
   - **Happy Path 분석**: 가장 빈번한 정상 수리 경로(전체 케이스의 몇 %를 차지하는지) 도출
   - **DFG (Directly-Follows Graph)**: 작업 간 전이 관계 및 시각화
   - **병목 및 재작업(루프) 분석**: 이동 시간 및 수리 지연, 재작업이 일어나는 특정 병목 지점 탐색

---

## 4. 🤖 새로운 세션의 AI 어시스턴트(Antigravity)를 위한 지침

> 사용자가 노트북 환경에서 질문할 경우, 위 세팅 가이드와 현재 완료된 Cell 53 상태를 기반으로 친절하고 직관적으로 지원할 것. 복잡한 추상화(`locals()` 등)를 지양하고 직관적이고 깔끔한 코드를 유지할 것.
