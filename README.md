# puzzle_data

수리 프로세스 이벤트 로그 데이터 분석 및 프로세스 마이닝 프로젝트.

## 🚀 빠른 시작 및 환경 인수인계 가이드
새로운 환경(노트북, 새 PC 등) 세팅 및 분석 재개 시 아래 인수인계 문서 참조:
- 📖 [docs/00_handover_and_setup_guide.md](docs/00_handover_and_setup_guide.md)

## 📁 주요 문서
- [00_handover_and_setup_guide.md](docs/00_handover_and_setup_guide.md): 노트북 환경 세팅 및 작업 인수인계 가이드
- [01_eda_plan.md](docs/01_eda_plan.md): 5단계 EDA 및 분석 실행 계획서
- [02_analysis_insights.md](docs/02_analysis_insights.md): 비즈니스 관점의 분석 인사이트 및 도출 내역
- [05_cleaned_data_dictionary.md](docs/05_cleaned_data_dictionary.md): 24열 정제 데이터셋 딕셔너리 및 SQL 쿼리 가이드

## 💾 데이터 파일
- `repair2.csv`: 원본 수리 데이터 파일 (13,262행 x 13열)
- `repair_cleaned.csv`: 전처리 완료 데이터 파일 (13,262행 x 24열, 결측치 0건, SQL 집계용)