# puzzle_data: 공공임대주택 수리 프로세스 이벤트 로그 분석 및 운영 최적화

> **퍼즐데이터(PuzzleData) 채용 과제 전형 제출 저장소**  
> **지원 직무**: 데이터 분석가 (신입)  
> **지원자**: 조승훈 · nextbus1245@gmail.com  
> **과제 주제**: 공공임대주택 수리 이벤트 로그(`repair2.csv`, 13,262행 · 1,000케이스) E2E 프로세스 마이닝 및 병목 개선 전략  
> **제출일**: 2026-10-27

---

## 🔄 분석 파이프라인 흐름 (Core Pipeline)

본 프로젝트는 데이터 정제부터 최종 전략 수립 및 보고서 작성까지 체계적인 4단계 파이프라인으로 구성되어 있습니다:

```
[1단계: 전처리 파이프라인]       [2단계: SQL 마스터 분석]        [3단계: 시각화 & 가설검증]         [4단계: 최종 결과 보고서]
01_data_preprocessing_pipeline   03_process_mining_analysis   02_process_mining_and_hypothesis   puzzledata_repair_report
   (analysis.ipynb)      ───>      (analysis.sql)     ───>         testing.ipynb        ───>       (.pptx / .pdf)
(결측·오기입 5대 인과 복원)      (MySQL 마스터뷰 & 병목)     (EDA·슬라이드차트·OLS 통계검정)     (19장 와이드 발표 보고서)
```

1. **[1단계] 전처리 파이프라인 (`01_data_preprocessing_pipeline.ipynb` / `analysis.ipynb`)**:
   - 원천 로그(`repair2.csv`, 13,262행) 정제, 5대 컬럼 결측치 0건 복원, 1905년 이상치 치환, 시간 순서(seq/sub_seq) 무결성 및 역전 0건 확보 ➔ 정제 산출물 `repair_cleaned.csv` 및 `case_pivot_table.csv` 생성
2. **[2단계] SQL 마스터 분석 (`03_process_mining_analysis.sql` / `analysis.sql`)**:
   - MySQL(`repair_db`) 적재, 케이스별 1행 마스터 뷰(`case_master_view`, 927건 유효 코호트) 생성, 거시 리드타임 3대 국면 분해, 재수리 루프 추적, TO-BE 시뮬레이션, 접수 지연 226건 사전코드 vs 실사코드 교차 진단 (총 2,060 라인)
3. **[3단계] EDA, 시각화 및 가설검증 통합 노트북 (`02_process_mining_and_hypothesis_testing.ipynb` / `hypothesis_testing_and_visualization.ipynb`)**:
   - [과제 질문 1] 결측치 2원화 진단 차트(`EDA-01.png`), [질문 2] 거시/미시 병목 차트, 일별 실사 큐 적체(WIP) 동역학, 수리 착수 대기 및 사내 재수리 루프, [질문 2-3] E2E 다중 OLS 회귀분석, [질문 3] TO-BE 패스트트랙 시뮬레이션
4. **[4단계] 최종 프레젠테이션 보고서 (`puzzledata_repair_report.pptx` / `puzzledata_repair_report.pdf`)**:
   - Modern Tech Light 테마 19장 16:9 와이드 발표 보고서 (고해상도 300DPI 차트 탑재, 고대비 타이포그래피, 인쇄/열람용 PDF 동봉)

---

## 📂 제출 파일 및 결과물 목록 (Deliverables)

```text
├── 📄 puzzledata_repair_report.pptx          [필수 1] 메인 분석 결과 발표 보고서 (19 슬라이드, 16:9 와이드)
├── 📄 puzzledata_repair_report.pdf           [필수 2] 프레젠테이션 열람 및 검토용 PDF (레이아웃 기준본)
├── 📓 01_data_preprocessing_pipeline.ipynb  [선택 1] 데이터 전처리 및 무결성 복원 파이프라인 (repair2 ➔ cleaned)
│   └── (alias: analysis.ipynb)               ※ 과제 명세서 표기 파일명(`analysis.ipynb`) 100% 동기화
├── 📓 02_process_mining_and_hypothesis_testing.ipynb [선택 2] 프로세스 마이닝 EDA, 슬라이드 시각화 및 OLS 가설검증 통합
│   └── (alias: hypothesis_testing_and_visualization.ipynb)
├── 📜 03_process_mining_analysis.sql        [선택 3] 프로세스 마이닝 마스터 SQL 스크립트 (2,060 라인)
│   └── (alias: analysis.sql)                 ※ 원천 SQL 스크립트(`analysis.sql`) 100% 동기화
├── 📦 puzzledata_repair_analysis_submission.zip [제출 패키지] 필수 및 선택 결과물 원클릭 압축본 (3.75 MB)
└── 📄 README.md                              본 안내 문서
```

---

## 📊 핵심 분석 결과 요약 (Ground Truth)

* **데이터 전처리 (13,262행 전수 보존, 임의 삭제 0건)**:
  * 비정상 결측 20행 전수 복원, 선후행 시간 역전 0건 달성.
  * 정상 분석 코호트 927건(92.7%) 및 오접수 조기 종료 73건(7.3%) 분리.
* **거시 리드타임 구조 (총 105.9시간)**:
  * 접수 국면 2.1h, 현장 국면 98.3h, 정산 국면 5.5h.
  * 순수 작업 시간 7.5h vs 대기시간 95.8h(총 리드타임의 **90.5%가 대기시간**).
* **압도적 1위 병목**:
  * **현장 실사 방문 대기(Wait 1) 76.8시간** (현장 소요시간의 78.2% 차지).
  * 8일간 피크 일평균 실사 유입 134.3건 vs 현장 기사 11인 일일 CAPA 68.0건으로, 유입량이 처리능력의 1.98배에 달해 최대 403건의 대기열(WIP) 적체 발생.
* **접수 국면 미시 병목**:
  * 비실시간 채널(Web 8.8h, Letter 7.6h) 평균 8.1시간 vs 실시간 채널(Phone, Personal) 14분.
  * 담당자 간 교차 인계(Handover) 123건 발생 시 소요시간 1.20h ➔ 7.87h로 6.6배 급증 (인계 패널티 OLS 계수 `+5.11h`, p < 0.001).
* **수리 국면 지연 요인**:
  * 사내수리 자재 준비 및 착수 대기 30.5시간, 사내 재수리(Loop) 26건 발생 시 추가 대기 평균 `+32.9시간` 누적.
* **E2E 리드타임 영향 요인 (다중 OLS 회귀, R² 87.8%)**:
  * 전체 완결 납기에 가장 결정적인 영향 변수는 **실사 방문 대기시간(표준화 Beta 0.807, p < 0.001)**.
* **TO-BE 최적화 전략 (Direct Booking & 사전 부품 특정화)**:
  * 접수원 사전 분류(E, P)의 현장 수리 일치율 입증 (E형 사내수리 100%, P형 83.1% 즉시수리).
  * 웹/앱 양식 사진·증상 추출 및 기사 캘린더 연동 Direct Booking 도입 시 즉시수리 365건(39.4%)을 실사 대기열에서 분리.
  * 실사 대기 20% 단축 가정 시 평균 리드타임 105.9h ➔ 90.5h (**▼14.5% / -15.4h 순단축**).

---

## 🛠️ 실행 환경 및 재현 (Reproduction)

* **언어 및 환경**: Python 3.10+ / MySQL 8.0+
* **필수 패키지**: `pip install pandas numpy matplotlib seaborn statsmodels python-pptx`
* **수치 일관성 보장**:
  * 보고서의 모든 정량 지표는 `case_pivot_table.csv` 및 `repair_cleaned.csv` 기반의 `scripts/deck/facts.py` ➔ `facts.json` 자동 검증 파이프라인을 통해 전수 일치(Zero-Violation)하도록 통제되어 있습니다.

---

## 💾 원본 및 정제 데이터 파일

* `repair2.csv`: 원본 수리 프로세스 이벤트 로그 (13,262행 × 13열, 1,000 케이스)
* `repair_cleaned.csv`: 전처리 완료 데이터셋 (13,262행 × 24열, 결측치 0건, 시간 역전 0건)
* `case_pivot_table.csv`: 1,000개 케이스별 공정 타임라인 및 비즈니스 속성 피벗 테이블
