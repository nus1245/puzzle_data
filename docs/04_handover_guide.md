# 🤝 4. 프로젝트 인수인계 및 실행 가이드 (Handover Guide)

이 문서는 다른 담당자가 본 프로젝트를 이어받아 분석을 재현하거나 확장할 때 필요한 환경 설정 및 실행 절차를 정리한 문서입니다.

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
1. VS Code 또는 IDE에서 `analysis.ipynb` 파일을 엽니다.
2. 커널을 `Python 3.14.7`로 선택합니다.
3. 셀 단위로 `Shift + Enter`를 눌러 데이터 전처리 및 시각화를 대화형으로 수행합니다.

### 방법 B: 파이썬 스크립트로 일괄 실행
터미널에서 아래 명령어를 실행하면 데이터 무결성 검증 및 기본 현황이 출력됩니다:
```powershell
python main.py
```

---

## 4. 인수인계 담당자를 위한 핵심 체크포인트
1. **데이터 업데이트 시**:
   * 새로운 기간의 수리 데이터가 들어오면 `repair2.csv`를 교체하거나 경로를 지정하여 실행합니다.
   * `date`, `time` 결측치(약 13건) 처리 로직을 항상 먼저 점검해야 합니다.
2. **시각화 결과 저장 위치**:
   * PPT에 들어갈 고해상도 차트는 `outputs/figures/` 폴더에 `.png` 형식으로 저장하도록 코드가 구성되어 있습니다 (`plt.savefig(...)` 활용).
3. **분석 내용 전달 시**:
   * 회의나 보고 전 `docs/02_analysis_insights.md`와 `docs/03_ppt_storyboard.md`를 먼저 정독하시면 전체 프로젝트 맥락을 5분 안에 파악할 수 있습니다.
