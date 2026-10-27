# 📦 [퍼즐데이터 채용 과제 전형] 분석 결과 및 제출 패키지 가이드

> **지원 직무**: 프로세스 마이닝 데이터 분석 / 컨설팅  
> **과제 주제**: 네덜란드 임대 주택 수리 프로세스 데이터(`repair2.csv`) E2E 분석 및 개선 전략  
> **제출 기한**: 2026년 10월 27일 (화) 23:59  
> **제출 구성**: 필수 프레젠테이션 파일(PPTX, PDF) 및 선택 제출 전처리·분석 코드(IPYNB, SQL)

---

## 📂 제출 파일 목록 및 구조 (Deliverables)

```text
├── 📄 puzzledata_repair_report.pptx          [필수 1] 메인 분석 결과 발표 보고서 (15 슬라이드, 16:9 와이드)
├── 📄 puzzledata_repair_report.pdf           [필수 2] 프레젠테이션 열람 및 검토용 PDF
├── 📓 01_data_preprocessing_pipeline.ipynb  [선택 1] 데이터 전처리 및 무결성 복원 파이프라인 (repair2 ➔ cleaned)
│   └── (alias: analysis.ipynb)               ※ 과제 명세서 표기 파일명(`analysis.ipynb`) 100% 동기화
├── 📓 02_process_mining_and_hypothesis_testing.ipynb [선택 2] 프로세스 마이닝 EDA, 슬라이드 시각화 및 OLS 가설검증 통합
├── 📜 03_process_mining_analysis.sql        [선택 3] 프로세스 마이닝 마스터 SQL 스크립트 (2,047 라인)
│   └── (alias: analysis.sql)                 ※ 원천 SQL 스크립트(`analysis.sql`) 100% 동기화
└── 📄 README.md                              본 제출 패키지 안내 문서
```

---

## 🧭 세부 파일별 역할 및 검증 가이드

### 1. [필수] 프레젠테이션 결과 보고서
* **`puzzledata_repair_report.pptx` / `.pdf`**:
  * **디자인 시스템**: Modern Tech Light 테마 (전문 테크 기업 보고서 룩앤필, 고대비 타이포그래피, 고화질 300DPI 렌더링).
  * **슬라이드 구성 (총 15장)**:
    * **P.01~03**: 표지, 목차, Executive Summary (거시 병목 해체 및 핵심 해결 전략).
    * **P.04~06**: [질문 1] 결측치 2원화 진단, CASE 1~5 도메인 인과 복원 성과표, 운영 구조 특성.
    * **P.07~12**: [질문 2] AS-IS E2E 프로세스 맵, 거시 3대 국면 리드타임 분해, 접수 국면 미시 병목(비실시간 채널 및 인계 패널티), 현장 공정 4대 소요시간 및 실사 큐 적체(WIP) 동역학, 수리 착수 대기 및 사내 하자 재방문 루프, E2E 다중 OLS 회귀분석 모형.
    * **P.13~15**: [질문 3] TO-BE 3대 혁신 전략, 패스트트랙 시나리오별 ROI 시뮬레이션(-65.1h 단축), 결언 및 프로세스 마이닝 로드맵.

---

### 2. [선택 1] `01_data_preprocessing_pipeline.ipynb` (`analysis.ipynb`)
* **역할**: 원천 이벤트 로그(`repair2.csv`, 13,262행)의 결측치·이상치를 5대 도메인 인과 메커니즘으로 전수 복원하는 엔드투엔드 정제 파이프라인.
* **핵심 복원 메커니즘**:
  * **CASE 1 (`taskID`, 2건)**: `contact` 고유 속성 기반 `FirstContact` 및 짝 결손 `InformClientSurvey` 복원.
  * **CASE 2 (`originator`, 2건)**: 현장 수리 시작-완료 100% 동일 담당자 규칙(짝 이벤트 `Anne`, `Paul` 승계).
  * **CASE 3 (`eventtype`, 5건)**: 작업 특성별 1:1 페어(3건) 및 단일 마일스톤(2건) 추적 복원.
  * **CASE 4 (`date`, 879건)**: 시각 정상 859건 선별 ➔ 선후행 순서 제약 내 타당 날짜 매핑 (단일 후보 640건 + 최근접 219건).
  * **CASE 5 (`time`, 28건)**: 정상 자정 7건 보존 + 정상 표본(751건) 중앙값 4.0분 기준 앵커 역산 추정 21건.
* **산출물**: 13,262행 전수 보존(임의 삭제 0건), 시간 역전 0건 달성된 `repair_cleaned.csv` 및 `case_pivot_table.csv`.

---

### 3. [선택 2] `02_process_mining_and_hypothesis_testing.ipynb`
* **역할**: 보고서에 수록된 모든 고화질 차트 생성 코드와 슬라이드 주장 수치의 계량경제학적 통계 검증(OLS 다중 회귀, VIF, p-value)을 통합한 마스터 노트북.
* **포함된 시각화 및 검증 파이프라인**:
  * **Part I**: 결측치 2원화(Bimodal) 프로파일 2-Panel 차트 (`EDA-01.png`, Slide 04).
  * **Part II**: 거시 리드타임 3대 국면(접수 2.1h, 현장 98.3h, 정산 5.5h) 가로 막대 차트 (`slide08_macro_leadtime_breakdown.png`, Slide 08).
  * **Part III**: 접수 국면 3-Panel 통합 병목 진단 (`slide09_reception_bottleneck_3panel.png`, Slide 09) & 상관관계 히트맵 (`reception_detailed_correlation_heatmap.png`) & 접수 OLS 회귀분석 (인계 패널티 `+5.11h`, p < 0.001).
  * **Part IV**: 현장 4대 소요시간 구조 분해 도넛 (`slide10_field_donut_breakdown.png`, Slide 10) & 일별 실사 큐 적체(WIP) 동역학 차트 (`slide10_field_bottleneck_wip.png`, Slide 10) & 현장 OLS 회귀분석 (실사 대기 표준화 Beta `0.807`).
  * **Part V**: 수리 착수 대기 및 사내 하자 재방문 루프 결합 차트 (`slide11_repair_delay_rework_combined.png`, Slide 11).
  * **Part VI**: 엔드투엔드 전체 리드타임 다중 OLS 회귀분석 (Slide 12 모형).
  * **Part VII**: 코호트 분석 및 TO-BE 패스트트랙 시뮬레이션 (Slide 13~14 / Appendix ROI).

---

### 4. [선택 3] `03_process_mining_analysis.sql` (`analysis.sql`)
* **역할**: 927건 정상 분석 코호트의 프로세스 마이닝 지표를 전수 산출하는 2,047개 라인의 마스터 SQL 스크립트.
* **주요 구성 섹션**:
  * **Section 1**: 원천 적재 및 시간 정합성 검증 (`Complete < Start` 역전 0건 전수 입증).
  * **Section 2**: 케이스별 1행 원천 타임라인 뷰(`case_master_view`) 생성 (접수-조사-1~3차 수리-정산 피벗).
  * **Section 3**: 대기시간 vs 실작업시간 거시 분해 및 채널별·인계별 미시 지표 산출.
  * **Section 4**: 현장 실사 대기 및 1~3차 수리 재작업 루프(사내 하자 재방문 36건, 외주 전환 81건 등) 전수 추적.
  * **Section 5**: TO-BE 패스트트랙 시나리오별 실사 CAPA(68건) 부하율 및 OLS 순단축 시뮬레이션.
  * **Section 6**: 비실시간 장기 지연(60분 초과 226건) 사전코드(P/E/B) vs 실사 세부코드(1~4) 교차 진단 (Direct Booking 88.1% 원천 흡수 실증).

---

## 🛠️ 실행 환경 및 재현 (Reproduction)
* **언어 및 환경**: Python 3.10+ / MySQL 8.0+
* **필수 패키지**: `pip install pandas numpy matplotlib seaborn statsmodels python-pptx`
* 모든 노트북과 시각화 스크립트는 로컬 환경에서 재실행 시 슬라이드 및 보고서 수치와 100% 완벽히 일치하도록 재현성이 확보되어 있습니다.
