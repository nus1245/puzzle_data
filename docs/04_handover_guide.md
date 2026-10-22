# 🤝 4. 프로젝트 인수인계 및 실행 가이드 (Handover Guide)

타 담당자의 분석 재현 및 확장을 위한 개발 환경 설정, 디렉토리 구조, 실행 절차 정리 인수인계 문서.

---

## 1. 프로젝트 디렉토리 구조

```text
puzzle_data/
├── docs/                       # 📄 기획, 인사이트, PPT 스토리보드, 인수인계 문서
│   ├── README.md               # 문서 폴더 안내
│   ├── 01_project_overview.md  # 프로젝트 개요 및 컬럼 데이터 딕셔너리
│   ├── 02_analysis_insights.md # 분석 진행 경과 및 핵심 인사이트 누적
│   ├── 03_ppt_storyboard.md    # PPT 발표자료 제작용 스토리보드
│   └── 04_handover_guide.md    # 인수인계 및 실행 가이드 (본 문서)
├── outputs/                    # 📊 생성된 그래프 이미지, 보고서 등 산출물 저장
│   └── figures/                # (차트 이미지 저장용)
├── analysis.ipynb              # 📓 대화형 분석용 주피터 노트북
├── main.py                     # 🐍 파이썬 일괄 실행 스크립트
├── repair2.csv                 # 💾 원본 데이터 파일 (13,262행 x 13열)
├── repair_cleaned.csv          # 💾 전처리 완료 데이터 파일 (13,262행 x 24열, SQL 집계용)
├── requirements.txt            # 📦 필요한 파이썬 패키지 목록
└── README.md                   # 저장소 최상위 안내
```

---

## 2. 개발 및 실행 환경
* **기본 파이썬 버전**: `Python 3.14.7`
* **필수 라이브러리**:
  * `pandas` (3.0.5)
  * `numpy`
  * `matplotlib`
  * `seaborn`
  * `jupyter` / `ipykernel` (7.4.0)

### 패키지 설치 방법 (새로운 PC/가상환경에서 설정 시)
```powershell
pip install -r requirements.txt
```

---

## 3. 분석 작업 실행 방법

### 방법 A: 주피터 노트북에서 실행 (추천)
1. IDE에서 `analysis.ipynb` 파일 열기.
2. 커널을 Python 환경으로 선택.
3. 셀 단위로 `Shift + Enter` 또는 `Run All`을 통해 데이터 전처리 및 시각화 대화형 수행.

### 방법 B: 파이썬 스크립트로 일괄 실행
터미널에서 아래 명령어 실행 시 데이터 무결성 검증 및 기본 현황 출력:
```powershell
python main.py
```

---

## 4. 인수인계 담당자를 위한 핵심 체크포인트
1. **데이터 업데이트 시**:
   * 신규 데이터 인입 시 `repair2.csv` 교체 또는 경로 지정 후 실행.
   * 5대 결측치 및 이상치 처리 체계(CASE 1~5) 우선 점검 필수.
2. **시각화 결과 저장 위치**:
   * PPT용 고해상도 차트는 `outputs/figures/`에 `.png` 형식으로 자동 저장 (`plt.savefig(...)` 활용).
3. **분석 내용 전달 시**:
   * 보고 전 `docs/02_analysis_insights.md` 및 `docs/03_ppt_storyboard.md` 정독을 통한 프로젝트 맥락 5분 내 파악 가능.
