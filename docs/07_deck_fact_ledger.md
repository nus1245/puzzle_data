# 07. 슬라이드 수치 대조 원장 (Deck Fact Ledger)

> 자동 생성: `scripts/deck/ledger.py` (facts.py 재계산 → build_deck.py 사용 이력). 소스 파일(`analysis.sql`, 노트북, CSV)은 수정하지 않았다.

**기준 우선순위**: ① `repair_cleaned.csv`·`case_pivot_table.csv`·`repair2.csv` 재계산 → ② `analysis.sql` → ③ `analysis.ipynb`·`hypothesis_testing_and_visualization.ipynb`. 원천끼리 다르면 재계산값을 채택하고 차이를 아래에 기록했다.

- 재계산 vs 원천 표기 대조: **62건 중 62건 일치**, 불일치 0건
- 슬라이드에 실린 모든 숫자는 `facts.json`(총 199개)에서 주입되며, 빌드 시 숫자 리터럴이 facts 에 없으면 실패한다.

## 1. 재계산 vs 원천 표기 대조

| 항목 | 재계산 | 원천 표기 | 원천 위치 | 판정 |
|:--|--:|--:|:--|:-:|
| `null_rows` | 20 | 20 | NB-A C81 / EDA-01 (5개 속성 합 22건=2+2+5+13, 중복 제외 20행) | 일치 |
| `null_cases` | 18 | 18 | SQL L1895 맥락 아님 — 스토리보드 S04 | 일치 |
| `date_miswritten` | 866 | 866 | NB-A C81 (결측 13건 + 이상 866건) | 일치 |
| `time_dummy` | 15 | 15 | NB-A C81 (결측 13건 + 더미 15건) | 일치 |
| `baseline_n` | 754 | 754 | NB-A C63 출력 '정상 표본: 754건' (AGENTS.md·docs/02의 751은 구값) | 일치 |
| `date_selected` | 859 | 859 | NB-A C53 '대상 859행 → 확정 859행' | 일치 |
| `time_28` | 28 | 28 | NB-A C77 '대상 28행 → 확정 28행' | 일치 |
| `lead_total` | 105.9 | 105.9 | SQL L1242 | 일치 |
| `field_total` | 98.3 | 98.3 | SQL L1243 | 일치 |
| `rec_total_min` | 125 | 125 | SQL L875 | 일치 |
| `wait_B_pct` | 90.5 | 90.5 | 스토리보드 90.5% — 정의 B 재현 | 일치 |
| `wait_B_h` | 95.8 | 95.8 | 스토리보드 95.8h | 일치 |
| `field_wait_h` | 93.7 | 93.7 | SQL L1331 | 일치 |
| `field_work_pct` | 4.7 | 4.7 | SQL L1272·L1330 (rep3 포함 산식) | 일치 |
| `field_wait_pct` | 95.3 | 95.3 | SQL L1306·L1331 | 일치 |
| `field_work_h` | 4.6 | 4.6 | SQL L1330 | 일치 |
| `wait1` | 76.8 | 76.8 | SQL L1396 | 일치 |
| `wait1_pct` | 78.2 | 78.2 | SQL L1396 | 일치 |
| `wait2_res` | 16.9 | 16.9 | NB-H C13 기술통계 wait2_hours 16.90 / 도넛 | 일치 |
| `wait2_strict` | 15.95 | 15.9 | SQL L1398 (정의 다름: 실사완료→1차 착수) | 일치 |
| `handover_n` | 123 | 123 | SQL L1012 / NB-H C1 | 일치 |
| `single_h` | 1.2 | 1.2 | SQL L995 | 일치 |
| `handover_h` | 7.87 | 7.87 | SQL L996 | 일치 |
| `handover_ratio` | 6.6 | 6.6 | SQL L997 주석은 '약 6.5배'(절삭) / 차트 6.6배 | 일치 |
| `fast_web_min` | 6.8 | 6.8 | 차트 slide09 Panel 3 | 일치 |
| `ols1_r2` | 0.3 | 0.3 | NB-H C9 출력 | 일치 |
| `ols1_f` | 131.9 | 131.9 | NB-H C9 출력 | 일치 |
| `ols1_p_daily` | 0.752 | 0.752 | NB-H C9 출력 | 일치 |
| `ols1_async_b` | 2.62 | 2.62 | NB-H C9 출력 | 일치 |
| `ols1_ho_ci_lo` | 4.295 | 4.295 | NB-H C9 출력 [0.025] | 일치 |
| `ols1_ho_ci_hi` | 5.924 | 5.924 | NB-H C9 출력 [0.975] | 일치 |
| `ols1_daily_b` | 0.0016 | 0.0016 | NB-H C9 출력 | 일치 |
| `ols1b_web` | 2.987 | 2.987 | NB-H C9 Model 2 출력 | 일치 |
| `ols1b_letter` | 2.208 | 2.208 | NB-H C9 Model 2 출력 | 일치 |
| `corr_rec_ho` | 0.48 | 0.48 | 히트맵 reception_detailed_correlation_heatmap.png | 일치 |
| `corr_rec_rt` | -0.43 | -0.43 | 히트맵 (실시간 채널여부) | 일치 |
| `corr_daily_visit` | 0.17 | 0.17 | 히트맵 (일별 접수량 × 현장 실사 대기) | 일치 |
| `inflow_day` | 134.3 | 134.3 | SQL L1978 / NB-H C14 | 일치 |
| `capa_day` | 68 | 68 | SQL L1980 / NB-H C14 | 일치 |
| `wip_peak` | 403 | 403 | SQL L1636 / 차트 | 일치 |
| `digest` | 50.6 | 50.6 | NB-H C14 md | 일치 |
| `ols2_r2` | 0.8776 | 0.8776 | NB-H C19 출력 | 일치 |
| `ols2_f` | 1653 | 1653 | NB-H C19 출력 (스토리보드 1,659.4는 오류) | 일치 |
| `ols2_visit` | 1.123 | 1.123 | NB-H C19 출력 | 일치 |
| `ols2_intern` | 31.75 | 31.75 | NB-H C19 출력 | 일치 |
| `ols2_async` | 4.889 | 4.889 | NB-H C19 출력 | 일치 |
| `wait2_intern` | 30.5 | 30.5 | NB-H C16 md | 일치 |
| `n_rework` | 26 | 26 | SQL L1493 | 일치 |
| `rework_gap_mean` | 32.9 | 32.9 | SQL L1493 | 일치 |
| `rework_max_d` | 10.1 | 10.1 | SQL L1493 | 일치 |
| `rework_e1` | 16 | 16 | SQL L1536 | 일치 |
| `match_upper_pct` | 87.3 | 87.3 | SQL L1899 | 일치 |
| `match_cons_pct` | 83.2 | 83.2 | SQL L1899 | 일치 |
| `n_P4` | 38 | 38 | SQL L1894 | 일치 |
| `settle_client_first` | 469 | 469 | 스토리보드 S07 (원천 미기재 → 재계산) | 일치 |
| `houses` | 890 | 890 | SQL L419 | 일치 |
| `houses_once` | 855 | 855 | SQL L509 | 일치 |
| `dian_share` | 46.9 | 46.9 | SQL L824 | 일치 |
| `recontact_diff` | 22 | 22 | SQL L773 (35채 중 22채 타 상담원) | 일치 |
| `ols1_handover_b` | 5.11 | 5.11 | NB-H C9 출력 (맵의 +5.11h) | 일치 |
| `eff_total` | 34.8 | 34.8 | 사용자 제공 정정안 ① | 일치 |
| `eff_parts_sum` | 34.8 | 34.8 | 표기 구성요소 합 = 표기 총합 (최대잔여법: 자재 15.95→16.0) | 일치 |

## 2. 원천 간 불일치와 처리 (정정 판정)

| # | 항목 | 충돌 | 채택 | 근거 |
|:-:|:--|:--|:--|:--|
| 1 | 정상 접수 표본 | AGENTS.md·docs/02: 751건(75.1%) ↔ 노트북 Cell 63 출력 754건 | **754건(75.4%)**, 기준 케이스 755 | analysis.ipynb Cell 2~63 재실행으로 754 재현 |
| 2 | E2E F-통계량 | 스토리보드 1,659.4 ↔ NB-H Cell 19 출력 1652.8 | **1,652.8** | statsmodels 재계산 일치 |
| 3 | 대기의 현장 집중도 | 스토리보드 98.0%(93.9/95.8) ↔ 재계산 93.7/95.8 | **97.8%** | S08 차트 현장 행도 93.9→93.7로 정정(§5) |
| 4 | Wait 2 | SQL L1398 15.9h(16.2%, 실사완료→1차 착수) ↔ 도넛 16.9h(17.2%, 잔여 정의) | 도넛 기준 **16.9h(17.2%)**, 정의 병기 | 둘 다 재현: 엄격 15.9h / 잔여 16.9h |
| 5 | 유입/CAPA | SQL 주석(L1552·1634·1668) 135/69/51.1% ↔ 최종 134.3/68.0/50.6% | **134.3 / 68.0 / 50.6%** | 구간이 달라(유입 1/2~1/7, CAPA 1/1~1/8) 같은 구간 소화율 52.5% 병기 |
| 6 | 인계 배수 | SQL 주석 '약 6.5배', docs/02 '7.2배·1.1h' ↔ 재계산 | **6.6배** (7.87/1.20) | SQL 주석은 절삭, docs/02는 구값 |
| 7 | 접수 '대기 1.9h' | SQL에 1.9h 분해 없음, 재계산 미재현 | **접수 총 2.1h(125.0분)**, 접수 전체를 대기로 산정 | 하드코딩 값 → 슬라이드·차트에서 제거 |
| 8 | S08 차트 접수·현장 행 | 정정본도 접수 1.9+현장 93.7=95.6 ≠ E2E 95.8 | 접수 행 0.0%/100.0%(2.1h), 현장 4.7%/95.3%(93.7h) | 형태 유지 재렌더(§5) |
| 9 | S09 채널별 '15분 이내' | CSV가 15.0분 정각 2건을 '15~60분'으로 분류해 막대 합 ≠ 100% | ≤15분으로 통일(대면·전화 100.0%, 우편 52.2%, 웹 47.3%) | 형태 유지 재렌더(§5) |
| 10 | 496.1h(구 S13) | 735건(E 370 + P-1·3 365)×40.5분의 산술 파생, 원천 미기재 | 슬라이드에서 삭제 | 근거 문서 없음 |
| 11 | 자재 대기 38.7h | SQL L1922(E형 맥락) ↔ 30.5h(사내수리 전체) | 30.5h 사용 | NB-H Cell 16 · 재계산 일치 |
| 12 | TO-BE 감축률 | 스토리보드 65%·38.0h, 노트북 Appendix 6 36.0h·65.1% | **전체 평균 ▼32.9%(105.9→71.1h), 사내수리군 ▼39.8%** | §3 참조 — 36.0h는 산식 오류(66.0%≠65.1%, 가중 오류, −22.2h 재현 불가) |

## 3. 정의·산식

- **대기 비중 90.5% (정의 B)**: 작업 = 현장 실작업 4.6h + 정산 시스템 처리 5.5h = 10.1h, 대기 = 105.9 − 10.1 = **95.8h**. 접수 구간(2.1h)은 일정 조율 구간이 대부분(MakeTicket 작업 0.07h)이라 전부 대기로 산정. 현장 실작업만 작업으로 보면 95.7%.
- **현장 실작업 4.6h**: 실사 + 1·2·3차 수리 작업(SQL L1257~1271 산식, rep3 포함). 비율 4.7% / 대기 95.3%.
- **TO-BE 가중평균(상한 시나리오)**: 실사 대기 20% 단축×OLS 1.12 = **−17.2h** · 사내수리 485건 자재 대기 100% 사전화 → 전체 평균 **−16.0h**(원값 15.95) · 리워크 26건 100% 차단 **−0.9h** · 접수 인계 123건 80% 제거 **−0.7h** → 합계 **−34.8h**, 105.9h → 71.1h(▼32.9%). 표기 반올림은 최대잔여법으로 합계에 맞췄다(자재 15.95→16.0).
- **사내수리군**: 같은 가정을 485건에 적용 → 130.9h → 78.8h (−52.1h, ▼39.8%).
- **노트북 Appendix 6의 36.0h(▼65.1%)를 쓰지 않은 이유**: ① (105.87−36.0)/105.87 = 66.0%이지 65.1%가 아님 ② 자재 −30.5h는 사내수리 485건에만 해당(전체 평균 환산 −16.0h) ③ 리워크 −22.2h는 재현되지 않음(22건×32.9h/927 ≈ −0.8h) ④ 기준 105.9h는 전체 평균이지 타겟군(130.9h) 평균이 아님.
- **인계 효과의 두 정의**: 단순 평균 차이 +6.7h(S09) / 채널 통제 OLS +5.11h(프로세스 맵 라벨).
- **S09 '15분 이내'**: ≤15분(15.0분 정각 포함). 빠른 건 평균은 웹 6.8·전화 8.2·대면 8.5·우편 8.4분.
- **정산 순서(S07)**: 927건 전수 기준 고객 통보 선행 469 / 재무 선행 456 / 동시 2, 마감 일치 925(99.8%). 노트북 Cell 75는 정상 표본 335건에서 168:167(50.15%:49.85%).

## 4. 슬라이드별 사용 수치

### S01

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `n_cases_all` | 1,000 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_events` | 13,262 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `wait_B_pct` | 90.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |

### S02

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `eff_total_pct` | 32.9 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `match_upper_pct` | 87.3 | case_pivot_table.csv · SQL L1888~1910 |
| `n_events` | 13,262 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `wait_B_pct` | 90.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |

### S03

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `baseline_n` | 754 | NB-A Cell 63 코드 재실행(Cell 2~63) — mt_dur_valid |
| `baseline_pct` | 75.4 | NB-A Cell 63 코드 재실행(Cell 2~63) — mt_dur_valid |
| `capa_day` | 68.0 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `eff_handover` | 0.7 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_material` | 16.0 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_rework` | 0.9 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_survey` | 17.2 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_total_pct` | 32.9 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `field_work` | 4.6 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `handover_ratio` | 6.6 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `inflow_day` | 134.3 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `intern_asis` | 130.9 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `intern_eff_pct` | 39.8 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `intern_tobe` | 78.8 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `lead_total` | 105.9 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `n_events` | 13,262 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_handover` | 123 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_null_rows` | 20 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `null_rows_pct` | 0.15 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `rework_gap_mean` | 32.9 | case_pivot_table.csv · SQL L1470~1546 |
| `stl_total` | 5.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `tobe_total` | 71.1 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `wait1` | 76.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait1_pct` | 78.2 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_intern` | 30.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait_B` | 95.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait_B_pct` | 90.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait_fieldwork_only_pct` | 95.7 | 재계산 |
| `wip_peak` | 403 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |

### S04

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `n_attrs` | 13 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_cases_all` | 1,000 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_events` | 13,262 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_null_cases` | 18 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `n_null_rows` | 20 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `normal_missing_attrs` | 7 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `normal_missing_max` | 93.0 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `normal_missing_min` | 86.0 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `null_rows_pct` | 0.15 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `void_cols` | 0 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |

### S05

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `baseline_cases` | 755 | NB-A Cell 63 코드 재실행(Cell 2~63) — mt_dur_valid |
| `baseline_median_min` | 4.0 | NB-A Cell 63 코드 재실행(Cell 2~63) — mt_dur_valid |
| `baseline_n` | 754 | NB-A Cell 63 코드 재실행(Cell 2~63) — mt_dur_valid |
| `baseline_pct` | 75.4 | NB-A Cell 63 코드 재실행(Cell 2~63) — mt_dur_valid |
| `date_missing` | 13 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `date_miswritten` | 866 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `date_nearest` | 219 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `date_selected` | 859 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `date_single` | 640 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `date_total` | 879 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `n_events` | 13,262 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_null_rows` | 20 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `null_eventtype` | 5 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `null_originator` | 2 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `null_taskID` | 2 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `pairs_checked` | 3,711 | NB-A Cell 83 출력 |
| `time_dummy` | 15 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `time_estimated` | 21 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `time_midnight_kept` | 7 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `time_missing` | 13 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `time_total` | 28 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |

### S06

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `date_miswritten` | 866 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `dian_share` | 46.9 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `houses_once_pct` | 96.1 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `intake_hours` | 24 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `lead_distort_before` | 595 | NB-A Cell 83 출력 |
| `lead_ok_before_n` | 405 | NB-A Cell 83 출력 |
| `lead_ok_before_pct` | 40.5 | NB-A Cell 83 출력 |
| `monica_share` | 53.1 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `n_cases_all` | 1,000 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_events` | 13,262 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_houses` | 890 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `n_houses_once` | 855 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `n_null_rows` | 20 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_wrongplace` | 73 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `null_rows_pct` | 0.15 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `pairs_checked` | 3,711 | NB-A Cell 83 출력 |
| `recontact_diff` | 22 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `recontact_diff_pct` | 62.9 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `recontact_houses` | 35 | repair_cleaned.csv · SQL L419~828·L1138~1202 |
| `wrongplace_pct` | 7.3 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |

### S07

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `backflow` | 0 | case_pivot_table.csv 재계산 (원천 미기재 — NB-A Cell 75는 정상 표본 335건) |
| `handover_penalty_h` | 6.7 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_wrongplace` | 73 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `settle_client_first` | 469 | case_pivot_table.csv 재계산 (원천 미기재 — NB-A Cell 75는 정상 표본 335건) |
| `settle_client_first_pct` | 50.6 | case_pivot_table.csv 재계산 (원천 미기재 — NB-A Cell 75는 정상 표본 335건) |
| `settle_fin_first` | 456 | case_pivot_table.csv 재계산 (원천 미기재 — NB-A Cell 75는 정상 표본 335건) |
| `settle_fin_first_pct` | 49.2 | case_pivot_table.csv 재계산 (원천 미기재 — NB-A Cell 75는 정상 표본 335건) |
| `ticket_match_n` | 925 | case_pivot_table.csv 재계산 (원천 미기재 — NB-A Cell 75는 정상 표본 335건) |
| `ticket_match_pct` | 99.8 | case_pivot_table.csv 재계산 (원천 미기재 — NB-A Cell 75는 정상 표본 335건) |
| `wrongplace_pct` | 7.3 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |

### S08

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `field_wait_of_all_wait_pct` | 97.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `field_work` | 4.6 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `handover_ratio` | 6.6 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `lead_total` | 105.9 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `n_intern1` | 485 | case_pivot_table.csv · NB-H Cell 16 |
| `rec_total` | 2.1 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `stl_total` | 5.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait1` | 76.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait1_pct` | 78.2 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_imm` | 0.0 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_intern` | 30.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait_B` | 95.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait_B_pct` | 90.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait_fieldwork_only_pct` | 95.7 | 재계산 |
| `work_B` | 10.1 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |

### S09

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `corr_daily_rec` | 0.01 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `fast_phone_min` | 8.2 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `fast_web_min` | 6.8 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `handover_h` | 7.87 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `handover_letter` | 54 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `handover_penalty_h` | 6.7 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `handover_ratio` | 6.6 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `handover_web` | 69 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_handover` | 123 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_single` | 804 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_f` | 131.9 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_handover_b` | 5.11 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_p_daily` | 0.752 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_r2` | 0.3000 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_vif_max` | 1.20 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `single_h` | 1.20 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |

### S10

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `corr_daily_rec` | 0.01 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `corr_daily_visit` | 0.17 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `corr_rec_ho` | 0.48 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `corr_rec_letter` | 0.18 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `corr_rec_rt` | -0.43 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `corr_rec_web` | 0.32 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_handover` | 123 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |

### S11

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `handover_penalty_h` | 6.7 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `ols1_async_b` | 2.62 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_daily_b` | 0.0016 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_f` | 131.9 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_handover_b` | 5.11 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_ho_ci_hi` | 5.92 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_ho_ci_lo` | 4.30 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_p_daily` | 0.752 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_r2_pct` | 30.0 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1_vif_max` | 1.20 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `ols1b_letter` | 2.21 | 재계산 |
| `ols1b_web` | 2.99 | 재계산 |

### S12

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `field_total` | 98.3 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `field_wait` | 93.7 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `field_wait_pct` | 95.3 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `field_work` | 4.6 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `field_work_pct` | 4.7 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `rep_work` | 3.9 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `rep_work_pct` | 4.0 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `survey_work` | 0.7 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `survey_work_min` | 40.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `survey_work_pct` | 0.7 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait1` | 76.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait1_days` | 3.2 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait1_pct` | 78.2 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_res` | 16.9 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_res_pct` | 17.2 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_strict` | 15.9 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |

### S13

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `capa_day` | 68.0 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `digest_pct` | 50.6 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `digest_pct_samewin` | 52.5 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `inflow_day` | 134.3 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `n_field_workers` | 11 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `n_surveyed` | 927 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `wait1` | 76.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wip_accum_day` | 66.3 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `wip_day1` | 20 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `wip_multiple` | 20 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `wip_peak` | 403 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |

### S14

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `n_intern1_pct` | 52.3 | case_pivot_table.csv · NB-H Cell 16 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `ols2_async_b` | 4.89 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_async_p` | 0.030 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_esc_b` | 5.96 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_esc_p` | 0.079 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_f` | 1,652.8 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_intern_b` | 31.75 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_intern_contrib` | 16.6 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_r2_pct` | 87.8 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_vif_max` | 1.02 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_visit_b` | 1.12 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_visit_contrib` | 86.3 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_visit_mean` | 76.8 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |

### S15

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `n_intern1` | 485 | case_pivot_table.csv · NB-H Cell 16 |
| `n_rework` | 26 | case_pivot_table.csv · SQL L1470~1546 |
| `n_rework_e1` | 16 | case_pivot_table.csv · SQL L1470~1546 |
| `n_rework_e12` | 22 | case_pivot_table.csv · SQL L1470~1546 |
| `n_rework_e2` | 6 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_e12_pct` | 84.6 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_gap_max_d` | 10.1 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_gap_max_h` | 241.6 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_gap_mean` | 32.9 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_lead_mean` | 171.6 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_lead_x` | 1.6 | case_pivot_table.csv · SQL L1470~1546 |
| `wait2_imm` | 0.0 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_intern` | 30.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |

### S16

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `E_intern_pct` | 100.0 | case_pivot_table.csv · SQL L1888~1910 |
| `P_self_pct` | 91.3 | case_pivot_table.csv · SQL L1888~1910 |
| `match_cons_n` | 771 | case_pivot_table.csv · SQL L1888~1910 |
| `match_cons_pct` | 83.2 | case_pivot_table.csv · SQL L1888~1910 |
| `match_upper_n` | 809 | case_pivot_table.csv · SQL L1888~1910 |
| `match_upper_pct` | 87.3 | case_pivot_table.csv · SQL L1888~1910 |
| `n_E` | 370 | case_pivot_table.csv · SQL L1888~1910 |
| `n_P` | 439 | case_pivot_table.csv · SQL L1888~1910 |
| `n_P4_extern` | 38 | case_pivot_table.csv · SQL L1888~1910 |
| `n_P_self` | 401 | case_pivot_table.csv · SQL L1888~1910 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `survey_work_min` | 40.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_intern` | 30.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |

### S17

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `eff_survey` | 17.2 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `n_E` | 370 | case_pivot_table.csv · SQL L1888~1910 |
| `n_P4_extern` | 38 | case_pivot_table.csv · SQL L1888~1910 |
| `n_handover` | 123 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_rework` | 26 | case_pivot_table.csv · SQL L1470~1546 |
| `n_rework_e1` | 16 | case_pivot_table.csv · SQL L1470~1546 |
| `n_rework_e12` | 22 | case_pivot_table.csv · SQL L1470~1546 |
| `n_rework_e2` | 6 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_e12_pct` | 84.6 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_gap_max_d` | 10.1 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_gap_max_h` | 241.6 | case_pivot_table.csv · SQL L1470~1546 |
| `rework_gap_mean` | 32.9 | case_pivot_table.csv · SQL L1470~1546 |
| `wait2_intern` | 30.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |

### S18

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `eff_handover` | 0.7 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_material` | 16.0 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_rework` | 0.9 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_survey` | 17.2 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_total` | 34.8 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `eff_total_pct` | 32.9 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `intern_asis` | 130.9 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `intern_eff` | 52.1 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `intern_eff_pct` | 39.8 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `intern_tobe` | 78.8 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `lead_total` | 105.9 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `n_handover` | 123 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `n_intern1` | 485 | case_pivot_table.csv · NB-H Cell 16 |
| `n_rework` | 26 | case_pivot_table.csv · SQL L1470~1546 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `tobe_total` | 71.1 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `wait2_intern` | 30.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |

### S19

| 키 | 표기값 | 원천·정의 |
|:--|--:|:--|
| `capa_day` | 68.0 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `eff_total_pct` | 32.9 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `handover_ratio` | 6.6 | case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135 |
| `inflow_day` | 134.3 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |
| `lead_total` | 105.9 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `match_cons_pct` | 83.2 | case_pivot_table.csv · SQL L1888~1910 |
| `match_upper_pct` | 87.3 | case_pivot_table.csv · SQL L1888~1910 |
| `n_events` | 13,262 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `n_null_rows` | 20 | repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01 |
| `n_rework` | 26 | case_pivot_table.csv · SQL L1470~1546 |
| `n_valid` | 927 | repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83) |
| `ols2_intern_b` | 31.75 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `ols2_visit_b` | 1.12 | statsmodels OLS 재계산 · NB-H Cell 19 출력 |
| `rework_gap_mean` | 32.9 | case_pivot_table.csv · SQL L1470~1546 |
| `tobe_total` | 71.1 | TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3) |
| `wait1` | 76.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait2_intern` | 30.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait_B` | 95.8 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wait_B_pct` | 90.5 | case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3) |
| `wip_peak` | 403 | case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15 |

## 5. 차트 정정 내역 (형태 유지, 값·라벨만)

| 차트 | 이전 | 정정 | 처리 |
|:--|:--|:--|:--|
| `slide08_macro_leadtime_breakdown.png` | 현장 95.5%(93.9h) → (사용자 정정본) 95.3%(93.7h), 접수 9.6%/90.4%(1.9h) | 접수 0.0%/100.0%(2.1h), 현장 4.7%/95.3%(93.7h), E2E 9.5%/90.5%(95.8h) | `charts_fix.py` → `outputs/figures/deck/` |
| `slide09_reception_bottleneck_3panel.png` | 우편 51.7/47.8, 대면 99.6 (합 ≠ 100) | 우편 52.2/47.8, 대면·전화 100.0, 웹 47.3/52.7 | `charts_fix.py` |
| `slide10_field_donut_breakdown.png` | 쐐기 78.1% ↔ 범례 78.2% | 쐐기·범례 78.2% | `charts_fix.py` |
| `slide11_repair_delay_rework.png` | '최대 10.1일, 총 리드타임 171.6h' | 사용자 정정본 사용 (+32.9h·최대 10.1일 / 재작업군 평균 총 리드타임 171.6h) | 원본 PNG 그대로 |
| 그 외 (EDA-01, repair_process_map, wip, ols, slide12 도넛, **reception_detailed_correlation_heatmap**, **reception_standalone_ols_coefficients**) | — | 수치 재계산 일치(히트맵 9×9 전 칸, OLS 계수·CI·p) | 원본 PNG 그대로, S10·S11에 배치 |

## 6. 저장소에 남은 구값 (수정하지 않고 보고만)

- `AGENTS.md` §4: 751건(75.1%) → 현재 754건(75.4%). §2: `analysis.sql` 1,305행 → 현재 1,985행.
- `docs/02_analysis_insights.md`: 접수 인계 '7.2배·1.1h' → 6.6배·1.20h, 사내수리 계수 31.53 → 31.75(노트북 출력).
- `docs/03_ppt_storyboard.md`: 98.0%, F=1,659.4, 171.6h(최대로 표기), 135/69건, 65%·38.0h, 1.9h 등.
- `analysis.sql` 주석: Wait 2 15.9h(엄격 정의), 접수 '약 6.5배', 135/69/51.1% 구간 주석.
- `hypothesis_testing_and_visualization.ipynb` Appendix 6(Cell 22·23): 36.0h·65.1% 모델.
