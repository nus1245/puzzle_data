# puzzle_data

수리 프로세스 이벤트 로그 데이터 분석 및 프로세스 마이닝 프로젝트.

## 🚀 빠른 시작 및 환경 인수인계 가이드
새로운 환경(노트북, 새 PC 등) 세팅 및 분석 재개 시 아래 인수인계 문서 참조:
- 📖 [docs/00_handover_and_setup_guide.md](docs/00_handover_and_setup_guide.md)

## 🔄 3단계 분석 파이프라인 흐름 (Core Pipeline)
본 프로젝트는 데이터 정제부터 최종 전략 수립까지 명확한 3단계 파이프라인으로 구성되어 있습니다:

```
[1단계: 전처리 노트북]           [2단계: SQL 분석 수행]          [3단계: 가설 검증 및 시각화 노트북]
  analysis.ipynb       ───>      analysis.sql        ───>  hypothesis_testing_and_visualization.ipynb
(원천 로그 결측치/이상치 정제)     (MySQL 적재 & 마스터뷰 EDA)      (6대 가설 통계 검정 & 출판급 차트 도출)
```

1. **[1단계] 전처리 노트북 (`analysis.ipynb`)**: 
   - 원천 로그(`repair2.csv`) 정제, 5대 컬럼 결측치 0건 복원, 1905년 이상치 치환, 시간 순서(seq/sub_seq) 무결성 확보 ➔ 정제 산출물 `repair_cleaned.csv` 생성
2. **[2단계] SQL 분석 수행 (`analysis.sql`)**: 
   - MySQL(`repair_db`) 적재, 케이스별 1행 마스터 뷰(`case_master_view`) 생성, 전수 EDA, 공정별 리드타임 및 병목 구간 집계
3. **[3단계] 가설 검증 및 시각화 노트북 (`hypothesis_testing_and_visualization.ipynb`)**: 
   - 전담제/기사배정/에스컬레이션/병렬정산/채널편향/교차인계 등 **6대 핵심 비즈니스 가설 통계적 검정(Welch's t-test, 상관분석 등) 및 2x2 고해상도 시각화** 완료

## 📁 주요 문서
- [00_handover_and_setup_guide.md](docs/00_handover_and_setup_guide.md): 노트북 환경 세팅 및 작업 인수인계 가이드
- [01_eda_plan.md](docs/01_eda_plan.md): 5단계 EDA 및 분석 실행 계획서
- [02_analysis_insights.md](docs/02_analysis_insights.md): 비즈니스 관점의 분석 인사이트 및 도출 내역
- [05_cleaned_data_dictionary.md](docs/05_cleaned_data_dictionary.md): 24열 정제 데이터셋 딕셔너리 및 SQL 쿼리 가이드

## 💾 데이터 파일
- `repair2.csv`: 원본 수리 데이터 파일 (13,262행 x 13열)
- `repair_cleaned.csv`: 전처리 완료 데이터 파일 (13,262행 x 24열, 결측치 0건, SQL 집계용)