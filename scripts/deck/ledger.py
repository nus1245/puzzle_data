"""docs/07_deck_fact_ledger.md 생성.  python -X utf8 scripts/deck/ledger.py
선행: facts.py → build_deck.py (facts.json, facts_usage.json)
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = json.load(open(os.path.join(ROOT, "scripts", "deck", "facts.json"), encoding="utf-8"))
USE = json.load(open(os.path.join(ROOT, "scripts", "deck", "facts_usage.json"), encoding="utf-8"))
F, CHK = D["facts"], D["checks"]

RULES = [
    (r"^n_events|^n_cases_all|^n_attrs|^n_valid|^n_wrong|^wrongplace", "repair2.csv · case_pivot_table.csv 행/케이스 수 (NB-A Cell 4·83)"),
    (r"^null_|^n_null|^date_|^time_|^normal_|^void_", "repair2.csv 결측 재계산 · NB-A Cell 53·77·81 · EDA-01"),
    (r"^baseline_", "NB-A Cell 63 코드 재실행(Cell 2~63) — mt_dur_valid"),
    (r"^pairs_|^lead_ok|^lead_distort", "NB-A Cell 83 출력"),
    (r"^lead_total|^field_|^rec_|^stl_|^work_B|^wait_B|^wait1|^wait2|^rep_work|^survey_work", "case_pivot_table.csv 재계산 · SQL L1206~1395 (정의는 §3)"),
    (r"^n_handover|^n_single|^single_|^handover_|^fast_|^n_phone|^n_web|^corr_|^ols1_", "case_pivot_table.csv · repair_cleaned.csv · NB-H Cell 9 · SQL L863~1135"),
    (r"^inflow|^capa|^digest|^wip_|^n_field|^n_surveyed", "case_pivot_table.csv 일별 집계 · SQL L1556~1670·L1978~1981 · NB-H Cell 14·15"),
    (r"^ols2_", "statsmodels OLS 재계산 · NB-H Cell 19 출력"),
    (r"^n_intern1|^n_imm1|^n_ext1|^n_imm_ext|^wait2_(intern|imm|ext)", "case_pivot_table.csv · NB-H Cell 16"),
    (r"^n_rework|^rework_", "case_pivot_table.csv · SQL L1470~1546"),
    (r"^n_[EPB]$|^[EPB]_pct|^match_|^n_P_self|^P_self|^n_P4|^E_intern", "case_pivot_table.csv · SQL L1888~1910"),
    (r"^settle_|^ticket_|^backflow", "case_pivot_table.csv 재계산 (원천 미기재 — NB-A Cell 75는 정상 표본 335건)"),
    (r"^n_houses|^houses_|^intake_|^dian_|^monica_|^recontact_", "repair_cleaned.csv · SQL L419~828·L1138~1202"),
    (r"^eff_|^tobe_|^intern_|^survey_cut|^ols_coef", "TO-BE 가중평균 산식 (SQL L1978~1985 + 효과율 가정, §3)"),
]


def src(key):
    for pat, txt in RULES:
        if re.search(pat, key):
            return txt
    return "재계산"


out = []
w = out.append
w("# 07. 슬라이드 수치 대조 원장 (Deck Fact Ledger)\n")
w("> 자동 생성: `scripts/deck/ledger.py` (facts.py 재계산 → build_deck.py 사용 이력). 소스 파일(`analysis.sql`, 노트북, CSV)은 수정하지 않았다.\n")
w("**기준 우선순위**: ① `repair_cleaned.csv`·`case_pivot_table.csv`·`repair2.csv` 재계산 → ② `analysis.sql` → ③ `analysis.ipynb`·`hypothesis_testing_and_visualization.ipynb`. 원천끼리 다르면 재계산값을 채택하고 차이를 아래에 기록했다.\n")
bad = [c for c in CHK if c[4] != "일치"]
w(f"- 재계산 vs 원천 표기 대조: **{len(CHK)}건 중 {len(CHK) - len(bad)}건 일치**, 불일치 {len(bad)}건\n- 슬라이드에 실린 모든 숫자는 `facts.json`(총 {len(F)}개)에서 주입되며, 빌드 시 숫자 리터럴이 facts 에 없으면 실패한다.\n")

w("## 1. 재계산 vs 원천 표기 대조\n")
w("| 항목 | 재계산 | 원천 표기 | 원천 위치 | 판정 |\n|:--|--:|--:|:--|:-:|")
for k, c, e, where, v in CHK:
    cs = f"{c:.4g}" if isinstance(c, float) else str(c)
    es = f"{e:.4g}" if isinstance(e, float) else str(e)
    w(f"| `{k}` | {cs} | {es} | {where} | {v} |")

w("\n## 2. 원천 간 불일치와 처리 (정정 판정)\n")
w("| # | 항목 | 충돌 | 채택 | 근거 |\n|:-:|:--|:--|:--|:--|")
rows = [
    ("1", "정상 접수 표본", "AGENTS.md·docs/02: 751건(75.1%) ↔ 노트북 Cell 63 출력 754건", f"**{F['baseline_n']['s']}건({F['baseline_pct']['s']}%)**, 기준 케이스 {F['baseline_cases']['s']}", "analysis.ipynb Cell 2~63 재실행으로 754 재현"),
    ("2", "E2E F-통계량", "스토리보드 1,659.4 ↔ NB-H Cell 19 출력 1652.8", f"**{F['ols2_f']['s']}**", "statsmodels 재계산 일치"),
    ("3", "대기의 현장 집중도", "스토리보드 98.0%(93.9/95.8) ↔ 재계산 93.7/95.8", f"**{F['field_wait_of_all_wait_pct']['s']}%**", "S08 차트 현장 행도 93.9→93.7로 정정(§5)"),
    ("4", "Wait 2", "SQL L1398 15.9h(16.2%, 실사완료→1차 착수) ↔ 도넛 16.9h(17.2%, 잔여 정의)", f"도넛 기준 **{F['wait2_res']['s']}h({F['wait2_res_pct']['s']}%)**, 정의 병기", f"둘 다 재현: 엄격 {F['wait2_strict']['s']}h / 잔여 {F['wait2_res']['s']}h"),
    ("5", "유입/CAPA", "SQL 주석(L1552·1634·1668) 135/69/51.1% ↔ 최종 134.3/68.0/50.6%", f"**{F['inflow_day']['s']} / {F['capa_day']['s']} / {F['digest_pct']['s']}%**", f"구간이 달라(유입 1/2~1/7, CAPA 1/1~1/8) 같은 구간 소화율 {F['digest_pct_samewin']['s']}% 병기"),
    ("6", "인계 배수", "SQL 주석 '약 6.5배', docs/02 '7.2배·1.1h' ↔ 재계산", f"**{F['handover_ratio']['s']}배** ({F['handover_h']['s']}/{F['single_h']['s']})", "SQL 주석은 절삭, docs/02는 구값"),
    ("7", "접수 '대기 1.9h'", "SQL에 1.9h 분해 없음, 재계산 미재현", f"**접수 총 {F['rec_total']['s']}h(125.0분)**, 접수 전체를 대기로 산정", "하드코딩 값 → 슬라이드·차트에서 제거"),
    ("8", "S08 차트 접수·현장 행", "정정본도 접수 1.9+현장 93.7=95.6 ≠ E2E 95.8", "접수 행 0.0%/100.0%(2.1h), 현장 4.7%/95.3%(93.7h)", "형태 유지 재렌더(§5)"),
    ("9", "S09 채널별 '15분 이내'", "CSV가 15.0분 정각 2건을 '15~60분'으로 분류해 막대 합 ≠ 100%", "≤15분으로 통일(대면·전화 100.0%, 우편 52.2%, 웹 47.3%)", "형태 유지 재렌더(§5)"),
    ("10", "496.1h(구 S13)", "735건(E 370 + P-1·3 365)×40.5분의 산술 파생, 원천 미기재", "슬라이드에서 삭제", "근거 문서 없음"),
    ("11", "자재 대기 38.7h", "SQL L1922(E형 맥락) ↔ 30.5h(사내수리 전체)", "30.5h 사용", "NB-H Cell 16 · 재계산 일치"),
    ("12", "TO-BE 감축률", "스토리보드 65%·38.0h, 노트북 Appendix 6 36.0h·65.1%, 사용자 제공 ①(−34.8h: 자재 100%·재방문 100%·인계 80% 가정 포함), 이전 덱 188건·771건 구조(−17.6h)", "**전체 평균 ▼" + F["eff_total_pct"]["s"] + "%(" + F["lead_total"]["s"] + "→" + F["tobe_total"]["s"] + "h)**: 실사 대기 20% **가정** 단축 −" + F["eff_total"]["s"] + "h(1:1 반영)", "줄 분리 후 대기는 로그로 식별 불가(기사 11명 공유, 줄을 나눈 사례 없음) → 단일 가정 + 민감도 10·30% + 파일럿 검증 설계. 줄별 평균(즉시 줄·나머지 줄)은 공유 큐 상태의 평균이라 기준값으로 부적합."),
    ("13", "즉시 줄 정의", "이전 덱·논의: 즉시 383건(P-1·3 365 + B-1 18)", f"**P-1·3 {F['n_fast']['s']}건({F['fast_pct']['s']}%)**", f"B형은 실사 대기 평균 {F['b_wait1']['s']}h로 이미 큐를 우회하고 B-1은 접수 시점 분류 불가 → 제외. 즉시 수리 작업 {F['fast_rep_h']['s']}h(383건 기준 1.95h는 B-1 포함 값)"),
    ("14", "실사 큐 점유시간 비중", "사용 초안 75.2%(383건 기준)", f"**{F['occ_fast_share']['s']}%** (365건: 건당 {F['occ_fast_h']['s']}h vs 나머지 {F['occ_rest_h']['s']}h, {F['occ_ratio']['s']}배)", "점유시간 = 실사 착수 후 기사가 묶이는 시간(즉시 수리는 실사+수리 연속, 그 외는 실사만)"),
    ("15", "'외주 위탁이 많은 E형'", "논의 중 진술", f"E형 외주 **{F['n_E_extern']['s']}건**. 외주 {F['n_extern_all']['s']}건 = P-4 {F['n_P4_extern']['s']} + B-4 {F['n_B4_extern']['s']}", "E형은 외주가 아니라 재작업 집중군(재작업 " + F['n_rework']['s'] + "건 중 " + F['n_rework_e12']['s'] + "건)"),
    ("16", "채널별 실사 대기", "가설: 채널이 달라도 실사 줄은 하나", f"웹 {F['ch_wait_web']['s']} · 우편 {F['ch_wait_letter']['s']} · 전화 {F['ch_wait_phone']['s']} · 대면 {F['ch_wait_personal']['s']}h (Kruskal p={F['ch_kw_p']['s']})", "채널 간 차이 유의하지 않음 → 줄 하나 입증"),
]
for r in rows:
    w("| " + " | ".join(r) + " |")

w("\n## 3. 정의·산식\n")
w(f"- **대기 비중 {F['wait_B_pct']['s']}% (정의 B)**: 작업 = 현장 실작업 {F['field_work']['s']}h + 정산 시스템 처리 {F['stl_total']['s']}h = {F['work_B']['s']}h, 대기 = {F['lead_total']['s']} − {F['work_B']['s']} = **{F['wait_B']['s']}h**. 접수 구간({F['rec_total']['s']}h)은 일정 조율 구간이 대부분(MakeTicket 작업 0.07h)이라 전부 대기로 산정. 현장 실작업만 작업으로 보면 {F['wait_fieldwork_only_pct']['s']}%.")
w(f"- **현장 실작업 {F['field_work']['s']}h**: 실사 + 1·2·3차 수리 작업(SQL L1257~1271 산식, rep3 포함). 비율 {F['field_work_pct']['s']}% / 대기 {F['field_wait_pct']['s']}%.")
w(f"- **TO-BE (가정 시나리오)**: 즉시 수리 코드 P-1·3 **{F['n_fast']['s']}건({F['fast_pct']['s']}%)**을 실사 줄에서 분리해 작업 줄로 직행(Direct Booking). 정밀검사(실사) 유지 = 나머지 {F['n_rest']['s']}건(B형 {F['n_B']['s']}, 외주 전환 {F['n_extern_all']['s']}, 재작업 집중 E형). 효과 = 실사 대기 {F['wait1']['s']}h의 20% **가정** 단축 −{F['eff_total']['s']}h를 리드타임에 1:1 반영(구성요소) → {F['lead_total']['s']}h → {F['tobe_total']['s']}h(▼{F['eff_total_pct']['s']}%). 민감도: 10% ▼{F['sens10_pct']['s']}%, 30% ▼{F['sens30_pct']['s']}%. 20%는 실사 줄 유입 감소율({F['fast_pct']['s']}%)의 약 절반.")
w("- **식별 한계**: 기사 풀 11명이 실사·사내수리·즉시 수리를 모두 공유(즉시 수리 7명, 외주만 외부 2곳)하므로 줄 분리는 용량 증설이 아닌 슬롯 배분 정책이다. 관측 데이터에는 줄을 나눈 사례가 없어 분리 후 대기는 추정할 수 없다 → 파일럿으로 검증. 줄별 평균(즉시 68.0h·나머지 83.0h)은 공유 큐 안의 값이고 B형(0.1h)이 섞여 있어 기준값으로 쓰지 않는다.")
w("- **분류 신뢰도 한계**: 세부 코드(1~4)는 수리 방식과 100% 일치해 사후 확정 라벨일 수 있고, 접수 시점 취득 가능 여부는 로그로 검증할 수 없다. 알파벳 P만으로 즉시 수리 적중 " + F['fast_p_prec']['s'] + "%(오분류 " + F['n_p_miss']['s'] + "건)가 하한 근거이며 파일럿 KPI.")
w("- **제외한 효과**: 자재 사전 확보, 재방문 차단, 접수 인계 제거는 근거 부족으로 효과에서 제외(상방 요인).")
w(f"- **참고(미채택) 일별 대기열 모델**: 즉시 줄 분리로 해방되는 실사 단계 기사 시간 {F['qm_freed_pct']['s']}%만 용량에 반영하면 평균 대기 약 {F['qm_cut_pct']['s']}% 감소. 기준값이 구성상 항등식이고 부하가 큰 8일 구간이라 상한 참고로만 사용.")
w(f"- **인계 효과의 두 정의**: 단순 평균 차이 +{F['handover_penalty_h']['s']}h(S09) / 채널 통제 OLS +{F['ols1_handover_b']['s']}h(프로세스 맵 라벨).")
w("- **S09 '15분 이내'**: ≤15분(15.0분 정각 포함). 빠른 건 평균은 웹 6.8·전화 8.2·대면 8.5·우편 8.4분.")
w("- **정산 순서(S07)**: 927건 전수 기준 고객 통보 선행 469 / 재무 선행 456 / 동시 2, 마감 일치 925(99.8%). 노트북 Cell 75는 정상 표본 335건에서 168:167(50.15%:49.85%).")

w("\n## 4. 슬라이드별 사용 수치\n")
for sn in sorted(USE, key=int):
    w(f"### S{int(sn):02d}\n")
    w("| 키 | 표기값 | 원천·정의 |\n|:--|--:|:--|")
    for k in USE[sn]:
        w(f"| `{k}` | {F[k]['s']} | {src(k)} |")
    w("")

w("## 5. 차트 정정 내역 (형태 유지, 값·라벨만)\n")
w("| 차트 | 이전 | 정정 | 처리 |\n|:--|:--|:--|:--|")
w("| `slide08_macro_leadtime_breakdown.png` | 현장 95.5%(93.9h) → (사용자 정정본) 95.3%(93.7h), 접수 9.6%/90.4%(1.9h) | 접수 0.0%/100.0%(2.1h), 현장 4.7%/95.3%(93.7h), E2E 9.5%/90.5%(95.8h) | `charts_fix.py` → `outputs/figures/deck/` |")
w("| `slide09_reception_bottleneck_3panel.png` | 우편 51.7/47.8, 대면 99.6 (합 ≠ 100) | 우편 52.2/47.8, 대면·전화 100.0, 웹 47.3/52.7 | `charts_fix.py` |")
w("| `slide10_field_donut_breakdown.png` | 쐐기 78.1% ↔ 범례 78.2% | 쐐기·범례 78.2% | `charts_fix.py` |")
w("| `slide11_repair_delay_rework.png` | '최대 10.1일, 총 리드타임 171.6h' | 사용자 정정본 사용 (+32.9h·최대 10.1일 / 재작업군 평균 총 리드타임 171.6h) | 원본 PNG 그대로 |")
w("| 그 외 (EDA-01, repair_process_map, wip, ols, slide12 도넛, **reception_detailed_correlation_heatmap**, **reception_standalone_ols_coefficients**) | — | 수치 재계산 일치(히트맵 9×9 전 칸, OLS 계수·CI·p) | 원본 PNG 그대로, S10·S11에 배치 |")

w("\n## 6. 저장소에 남은 구값 (수정하지 않고 보고만)\n")
w("- `AGENTS.md` §4: 751건(75.1%) → 현재 754건(75.4%). §2: `analysis.sql` 1,305행 → 현재 1,985행.")
w("- `docs/02_analysis_insights.md`: 접수 인계 '7.2배·1.1h' → 6.6배·1.20h, 사내수리 계수 31.53 → 31.75(노트북 출력).")
w("- `docs/03_ppt_storyboard.md`: 98.0%, F=1,659.4, 171.6h(최대로 표기), 135/69건, 65%·38.0h, 1.9h 등.")
w("- `analysis.sql` 주석: Wait 2 15.9h(엄격 정의), 접수 '약 6.5배', 135/69/51.1% 구간 주석.")
w("- `hypothesis_testing_and_visualization.ipynb` Appendix 6(Cell 22·23): 36.0h·65.1% 모델.")

open(os.path.join(ROOT, "docs", "07_deck_fact_ledger.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("ledger written:", len(out), "lines")
