"""슬라이드 10~17."""
import os

from kit import *          # noqa: F401,F403
from slides_a import FIG, DECK, cap


def _side_cards_right(sl, F, x, y, w, h_total, cards, gutter=0.12):
    stack(sl, x, y, w, cards, gutter=gutter, h_total=h_total)


# ------------------------------------------------------------------ S10 현장① 구성
def s10(doc, F):
    sl = doc.new_slide(12, "Part 02")
    chrome(sl, "[ 12 / Q2-2 · BOTTLENECK 2 · FIELD ]", f"현장 {F('field_total')}h 중 실사 방문 대기가 {F('wait1_pct')}%",
           sub=f"현장 대기 {F('field_wait')}h = 현장 시간의 {F('field_wait_pct')}% · 기사의 실작업은 {F('field_work_pct')}%({F('field_work')}h)에 불과",
           source="출처: analysis.sql L1246~1395 · hypothesis 노트북 Cell 11·13 (Wait 2는 재수리 인계 대기 포함 정의)")
    top, H = BODY_TOP + 0.08, 5.15
    donut = Card([cap("FIG.10", "현장 4대 소요시간 구조 분해"),
                  Img(os.path.join(DECK, "slide10_field_donut_breakdown.png"), max_h=H - 0.62, name="donut")], pad=0.14, gap=0.06, name="donut-card")
    dw = 5.05
    donut.draw(sl, MX, top, dw, H)
    rx, rw = MX + dw + 0.2, CW - dw - 0.2
    gw = (rw - 0.14) / 2

    def strip(tag, name, num, unit, pct, color, frac, note):
        return Card([label(tag, color), heading(name, 13, INK, name="nm"), big(num, unit, color, 32, name="n"),
                     body(note, 11, MUTED, name="nt"), Bar(frac, color)], pad=0.16, gap=0.05, name="strip-" + tag[:2])

    s1 = strip("① WAIT 1", "실사 방문 대기", F("wait1"), "h", F("wait1_pct"), RED, float(F("wait1_pct")) / 100, f"현장 시간의 {F('wait1_pct')}% · 약 {F('wait1_days')}일")
    s2 = strip("② WAIT 2", "수리 착수·공정 대기", F("wait2_res"), "h", F("wait2_res_pct"), ORG, float(F("wait2_res_pct")) / 100, f"{F('wait2_res_pct')}% · 재수리 인계 대기 포함")
    s3 = strip("③ WORK", "본수리 실작업", F("rep_work"), "h", F("rep_work_pct"), ACC, float(F("rep_work_pct")) / 100, f"{F('rep_work_pct')}%")
    s4 = strip("④ WORK", "실사 점검 실작업", F("survey_work"), "h", F("survey_work_pct"), "0EA5E9", float(F("survey_work_pct")) / 100, f"{F('survey_work_pct')}% · {F('survey_work_min')}분")
    h1 = row(sl, rx, top, rw, [s1, s2], gutter=0.14)
    h2 = row(sl, rx, top + h1 + 0.14, rw, [s3, s4], gutter=0.14)
    ty = top + h1 + 0.14 + h2 + 0.14
    take = Card([label("TAKEAWAY", RED),
                 Txt([rich(f"대기 합계 **{F('field_wait')}h = 현장 시간의 {F('field_wait_pct')}%**. 병목은 기사의 작업 속도가 아니라 방문 전 대기 관리다.", 15, INK, accent=RED)], name="take")],
                pad=0.18, gap=0.05, name="take-card", line=RED)
    take.draw(sl, rx, ty, rw, top + H - ty)
    assert_body(sl, top + H)
    sl.notes(f"현장 국면 {F('field_total')}시간 중 기사가 실제로 일한 시간은 {F('field_work_pct')}%({F('field_work')}h)뿐이고 나머지 {F('field_wait_pct')}%({F('field_wait')}h)가 대기입니다. "
             f"그중 접수 후 방문까지 기다리는 실사 방문 대기가 {F('wait1')}시간(약 {F('wait1_days')}일)으로 현장 시간의 {F('wait1_pct')}%를 차지하는 1위 병목입니다. "
             f"[예상 질문] Wait 2가 SQL 주석의 15.9h와 다르다? → SQL은 실사 완료~1차 착수(엄격 정의 {F('wait2_strict')}h), 도넛은 재수리 인계 대기를 포함한 잔여 정의({F('wait2_res')}h)이며 둘 다 데이터로 재현됩니다.")
    return sl


# ------------------------------------------------------------------ S11 현장② 적체
def s11(doc, F):
    sl = doc.new_slide(13, "Part 02")
    chrome(sl, "[ 13 / Q2-2 · BOTTLENECK 2 · QUEUE ]", f"일 유입 {F('inflow_day')}건 vs CAPA {F('capa_day')}건, 적체 {F('wip_peak')}건",
           sub=f"{F('n_surveyed')}건 전수가 방문 실사를 거치는 구조 · 소화율 {F('digest_pct')}% (같은 구간 기준 {F('digest_pct_samewin')}%)",
           source="출처: analysis.sql L1556~1670·L1978~1981 · 유입 1/2~1/7 평균, CAPA 1/1~1/8 평균(기사 11인) · hypothesis 노트북 Cell 15")
    top = BODY_TOP + 0.08
    cw_ = 8.55
    chart = Card([cap("FIG.11", "일별 유입 vs 실사 CAPA 및 적체 대기열(WIP)"),
                  Img(os.path.join(FIG, "slide10_field_bottleneck_wip.png"), max_h=3.9, name="wip")], pad=0.14, gap=0.06, name="wip-card")
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, top, cw_, ch)
    rx, rw = MX + cw_ + 0.2, CW - cw_ - 0.2
    ms = [Card([label("일일 유입", ACC), big(F("inflow_day"), "건/일", ACC, 30, name="a"), body("접수 → 현장 이관 (1/2~1/7 평균)", 11, INK2)], pad=0.16, gap=0.03, name="m1"),
          Card([label(f"실사 CAPA · 기사 {F('n_field_workers')}인", MUTED), big(F("capa_day"), "건/일", INK, 30, name="b"), body(f"실사 착수 (1/1~1/8 평균) · 소화율 {F('digest_pct')}%", 11, INK2)], pad=0.16, gap=0.03, name="m2"),
          Card([label("적체 피크 (DAY 7)", RED), big(F("wip_peak"), "건", RED, 30, name="c"), body(f"Day 1의 {F('wip_day1')}건에서 {F('wip_multiple')}배", 11, INK2)], pad=0.16, gap=0.03, name="m3", line=RED)]
    stack(sl, rx, top, rw, ms, gutter=0.12, h_total=ch)
    ty = top + ch + 0.15
    take = Card([Txt([rich(f"기사가 느린 것이 아니라 **실사 처리 용량(CAPA)을 넘는 유입**이 적체와 {F('wait1')}h 대기를 만든다 — 하루 약 {F('wip_accum_day')}건씩 누적.", 13, INK, accent=RED)], name="take")],
                pad=0.16, name="take-card")
    th_ = take.natural_h(CW)
    take.draw(sl, MX, ty, CW, th_)
    assert_body(sl, ty + th_)
    sl.notes(f"파란 막대가 일일 접수 유입으로 평균 {F('inflow_day')}건, 회색 막대가 기사 {F('n_field_workers')}명의 실사 착수로 평균 {F('capa_day')}건입니다. 유입이 처리 능력을 약 2배 넘으면서 "
             f"미처리 대기열이 Day 1의 {F('wip_day1')}건에서 Day 7에 {F('wip_peak')}건까지 {F('wip_multiple')}배 늘었습니다. 하루 약 {F('wip_accum_day')}건씩 쌓인 셈입니다. "
             f"[예상 질문] 유입과 CAPA 산출 구간이 다른데? → 유입은 집중 유입기(1/2~1/7), CAPA는 1/1~1/8 평균입니다. 같은 구간(1/2~1/7)으로 맞춰도 소화율은 {F('digest_pct_samewin')}%로 결론이 같습니다.")
    return sl


# ------------------------------------------------------------------ S12 OLS
def s12(doc, F):
    sl = doc.new_slide(14, "Part 02")
    chrome(sl, "[ 14 / Q2-3 · DRIVERS · OLS ]", "소요시간은 실사 지연과 사내수리가 좌우한다",
           sub=f"E2E 리드타임 OLS · R² {F('ols2_r2_pct')}% · F {F('ols2_f')} · N {F('n_valid')} · VIF 최대 {F('ols2_vif_max')}",
           source="출처: hypothesis 노트북 Cell 19 (statsmodels OLS, 재계산 일치) · 종속변수 total_hours")
    top = BODY_TOP + 0.08
    cw_ = 8.55
    chart = Card([cap("FIG.12", "E2E 리드타임 결정 요인 회귀계수"),
                  Img(os.path.join(FIG, "slide11_regression_leadtime_drivers.png"), max_h=3.7, name="ols")], pad=0.14, gap=0.06, name="ols-card")
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, top, cw_, ch)
    rx, rw = MX + cw_ + 0.2, CW - cw_ - 0.2
    cs = [Card([label("실사 방문 대기 · 1시간당", ACC), big("+" + F("ols2_visit_b"), "h/h", ACC, 30, name="a"), body(f"1시간 단축 시 전체 {F('ols2_visit_b')}h 감소 (p < 0.001)", 11, INK2)], pad=0.16, gap=0.03, name="k1"),
          Card([label("사내수리 배정 · vs 즉시·외주", RED), big("+" + F("ols2_intern_b"), "h", RED, 30, name="b"), body("자재 조달·일정 조율 대기 (p < 0.001)", 11, INK2)], pad=0.16, gap=0.03, name="k2"),
          Card([label("비실시간 채널 · 웹·우편", ORG), big("+" + F("ols2_async_b"), "h", ORG, 30, name="c"), body(f"웹·우편 접수, p = {F('ols2_async_p')}", 11, INK2)], pad=0.16, gap=0.03, name="k3")]
    stack(sl, rx, top, rw, cs, gutter=0.12, h_total=ch)
    ty = top + ch + 0.15
    take = Card([Txt([rich(f"평균 기여(계수 × 평균값)로 환산하면 **실사 지연 {F('ols2_visit_contrib')}h**({F('ols2_visit_b')} × {F('ols2_visit_mean')}h)가 사내수리 {F('ols2_intern_contrib')}h({F('ols2_intern_b')} × {F('n_intern1_pct')}%)보다 훨씬 크다. 2차 에스컬레이션(+{F('ols2_esc_b')}h)은 p = {F('ols2_esc_p')}로 비유의.", 12.5, INK, accent=ACC)], name="take")],
                pad=0.16, name="take-card")
    th_ = take.natural_h(CW)
    take.draw(sl, MX, ty, CW, th_)
    assert_body(sl, ty + th_)
    sl.notes(f"E2E 리드타임을 설명하는 회귀모형의 설명력은 {F('ols2_r2_pct')}%입니다. 실사 방문 대기는 1시간당 {F('ols2_visit_b')}시간, 사내수리 배정은 +{F('ols2_intern_b')}시간, 비실시간 채널은 +{F('ols2_async_b')}시간 영향을 줍니다. "
             f"실사 지연의 계수가 1.12이므로 실사 대기를 1시간 줄이면 전체 리드타임이 1.12시간 줄어드는 지렛대 효과가 있고, 평균 기여로는 실사 지연 {F('ols2_visit_contrib')}시간이 사내수리 {F('ols2_intern_contrib')}시간보다 큽니다. 2차 에스컬레이션은 비유의합니다. "
             f"[예상 질문] 다중공선성은? → VIF 최대 {F('ols2_vif_max')}로 문제 없습니다. [정정] F-통계량은 노트북 출력 {F('ols2_f')}입니다.")
    return sl


# ------------------------------------------------------------------ S13 수리·리워크
def s13(doc, F):
    sl = doc.new_slide(15, "Part 02")
    chrome(sl, "[ 15 / Q2-2 · BOTTLENECK 3 · REPAIR ]", f"사내수리는 자재 {F('wait2_intern')}h, 하자는 +{F('rework_gap_mean')}h 지연",
           sub=f"사내 하자 재방문 {F('n_rework')}건은 평균 총 리드타임 {F('rework_lead_mean')}h — 전체 평균의 {F('rework_lead_x')}배",
           source="출처: analysis.sql L1403~1546 · hypothesis 노트북 Cell 16~17 (정정 차트: 최대 지연과 평균 리드타임 라벨 분리)")
    top = BODY_TOP + 0.08
    cw_ = 8.55
    chart = Card([cap("FIG.13", "수리 방식별 착수 대기와 하자 재방문 루프"),
                  Img(os.path.join(FIG, "slide11_repair_delay_rework.png"), max_h=3.9, name="rw")], pad=0.14, gap=0.06, name="rw-card")
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, top, cw_, ch)
    rx, rw = MX + cw_ + 0.2, CW - cw_ - 0.2
    cs = [Card([label("사내수리 자재 대기", ORG), big(F("wait2_intern"), "h", ORG, 30, name="a"), body(f"사내수리 {F('n_intern1')}건만 대기. 즉시·외주는 {F('wait2_imm')}h", 11, INK2)], pad=0.16, gap=0.03, name="k1"),
          Card([label("사내 하자 재방문", RED), big(F("n_rework"), "건", RED, 30, name="b"), body(f"추가 대기 평균 +{F('rework_gap_mean')}h, 최대 {F('rework_gap_max_h')}h({F('rework_gap_max_d')}일)", 11, INK2)], pad=0.16, gap=0.03, name="k2"),
          Card([label("E-1 · E-2 코드 집중", RED), big(F("n_rework_e12"), f"건 · {F('rework_e12_pct')}%", RED, 30, name="c"), body(f"E-1 {F('n_rework_e1')}건 + E-2 {F('n_rework_e2')}건 — 정밀검사 대상", 11, INK2)], pad=0.16, gap=0.03, name="k3")]
    stack(sl, rx, top, rw, cs, gutter=0.12, h_total=ch)
    ty = top + ch + 0.15
    take = Card([Txt([rich(f"1차 수리 실패 뒤 부품을 다시 조달하는 동안 **평균 +{F('rework_gap_mean')}h**, 가장 길게는 **{F('rework_gap_max_d')}일**을 더 기다린다.", 12.5, INK, accent=RED)], name="take")],
                pad=0.16, name="take-card")
    th_ = take.natural_h(CW)
    take.draw(sl, MX, ty, CW, th_)
    assert_body(sl, ty + th_)
    sl.notes(f"즉시수리와 외주수리는 착수 대기가 {F('wait2_imm')}시간인데, 사내수리 {F('n_intern1')}건만 부품 조달과 일정 조율로 평균 {F('wait2_intern')}시간을 기다립니다. "
             f"또 사내수리 후 하자로 재방문한 {F('n_rework')}건은 부품을 다시 조달하느라 평균 {F('rework_gap_mean')}시간, 최대 {F('rework_gap_max_h')}시간({F('rework_gap_max_d')}일)을 더 기다렸고, 이 케이스들의 평균 총 리드타임은 {F('rework_lead_mean')}시간입니다. "
             f"재방문 {F('n_rework')}건 중 {F('n_rework_e12')}건({F('rework_e12_pct')}%)이 E-1·E-2 코드에 집중되어 있습니다.")
    return sl


# ------------------------------------------------------------------ S14 규명
def s14(doc, F):
    sl = doc.new_slide(16, "Part 03")
    chrome(sl, "[ 16 / Q2→Q3 · ROOT CAUSE ]", "적중률은 높은데 정보 해상도가 끊겨 있다",
           sub=f"접수 사전 분류가 이미 현장과 {F('match_cons_pct')}~{F('match_upper_pct')}% 일치하는데도 전수 방문 실사가 유지된 이유",
           source=f"출처: analysis.sql L1888~1928 · 낙관 상한 {F('match_upper_pct')}%(E+P {F('match_upper_n')}건) · 보수 {F('match_cons_pct')}%(외주 P-4 {F('n_P4_extern')}건 제외)")
    top = BODY_TOP + 0.08
    c1 = Card([label("01 · 데이터 팩트", ACC), heading("사전 적중률은 높다", 15, INK, name="h"),
               Img(os.path.join(FIG, "slide12_intake_matching_donut.png"), max_h=2.15, name="donut"),
               big(F("match_upper_pct"), "% (상한)", ACC, 34, name="n"),
               body(f"E+P {F('match_upper_n')}/{F('n_valid')}건 · 보수 기준 {F('match_cons_pct')}%({F('match_cons_n')}건)", 11.5, INK2)], pad=0.2, gap=0.07, name="c1")
    c2 = Card([label("02 · 원인 규명", ORG), heading("정보 해상도 단절", 15, INK, name="h"),
               Card([label("접수 (현행)", MUTED), body("알파벳 3분류(B·P·E)만 수집 — 차에 실을 자재 규격 특정 불가", 11.5, INK2)], pad=0.14, gap=0.04, fill=SLATE_BG, name="boxA"),
               Card([label("현장 (현행)", MUTED), body(f"{F('survey_work_min')}분 방문 실사 후 세부 코드(1~4) 판정", 11.5, INK2)], pad=0.14, gap=0.04, fill=SLATE_BG, name="boxB"),
               Txt([rich(f"→ 실사 → 부품 주문(**{F('wait2_intern')}h**) → 재방문, **이중 출장**이 고착", 12.5, INK, accent=ORG)], name="res")],
              pad=0.2, gap=0.1, name="c2")
    c3 = Card([label("03 · 직행 근거", GRN), heading("E형은 전원 사내수리", 15, INK, name="h"),
               big(F("n_E"), "건 · " + F("E_intern_pct") + "%", GRN, 34, name="n"),
               body(f"E형 {F('n_E')}건은 사내수리로 100% 완결 — 실사 없이 직행해도 안전", 11.5, INK2),
               bullets([f"P형 {F('n_P')}건 중 {F('n_P_self')}건({F('P_self_pct')}%)이 사내 자체 완결",
                        f"외주 전환은 P-4 {F('n_P4_extern')}건뿐"], 11.5)],
              pad=0.2, gap=0.08, name="c3")
    hh = row(sl, MX, top, CW, [c1, c2, c3], gutter=0.2)
    y = top + hh + 0.15
    ban = Card([label("SO WHAT", ACC), Txt([rich("접수 단계에서 **부품 규격까지 특정**하면 실사 없이 **1회 방문**이 가능하다 — TO-BE 전략의 출발점", 14, INK, accent=ACC)], name="sw")],
               pad=0.18, gap=0.05, name="sowhat", line=ACC)
    bh = max(ban.natural_h(CW), BODY_BOTTOM - y)
    ban.draw(sl, MX, y, CW, bh)
    assert_body(sl, y + bh)
    sl.notes(f"접수원의 사전 분류는 이미 현장 결과와 {F('match_cons_pct')}~{F('match_upper_pct')}% 일치합니다. E형 {F('n_E')}건은 전원 사내수리로 끝났습니다. 그런데도 모든 건이 방문 실사를 거친 이유는 정보 해상도 단절입니다. "
             f"접수는 B·P·E 알파벳만 수집하고, 현장은 약 {F('survey_work_min')}분 실사 후 1~4 세부 코드로 부품을 정하기 때문에 실사 → 부품 주문 → 재방문의 이중 출장이 굳어졌습니다. "
             f"[정정] {F('match_upper_pct')}%는 E+P 전체를 포함한 낙관 상한이고, 외주 전환 위험 P-4({F('n_P4_extern')}건)를 뺀 보수 기준은 {F('match_cons_pct')}%입니다.")
    return sl


# ------------------------------------------------------------------ S15 전략
def s15(doc, F):
    sl = doc.new_slide(17, "Part 03")
    chrome(sl, "[ 17 / Q3 · TO-BE STRATEGY ]", "대기 3종을 겨냥한 TO-BE 3대 전략",
           sub="실사 대기 · 자재 대기 · 하자 재방문을 각각 겨냥하고, 접수 단계의 정보 해상도를 높이는 것이 공통 열쇠",
           source="출처: analysis.sql L1530~1546(리워크 코드)·L1888~1985(사전 분류·시나리오) · 효과율은 가정값")
    top = BODY_TOP + 0.08
    c1 = Card([label("전략 1 · 사진 기반 사전 특정", ACC), heading("자재 대기를 출동 전으로 당긴다", 16, INK, name="h"),
               label("겨냥: 자재 대기", MUTED), big(F("wait2_intern"), "h", ACC, 44, name="n"),
               bullets(["접수 시 고장 부위·모델 라벨 사진을 필수 첨부",
                        "출동 전 부품 규격을 특정해 사전 상차",
                        f"E형 {F('n_E')}건은 실사 없이 1회 방문 직행 (실사 대기 20% 단축 가정 → −{F('eff_survey')}h)"], 12.5, gap=5)],
              pad=0.24, gap=0.1, name="s1")
    c2 = Card([label("전략 2 · E-1/E-2 정밀검사", RED), heading("재방문 루프를 현장에서 차단", 16, INK, name="h"),
               label("겨냥: 하자 재방문", MUTED), big("+" + F("rework_gap_mean"), "h", RED, 44, name="n"),
               bullets([f"재방문 {F('n_rework')}건 중 {F('n_rework_e12')}건({F('rework_e12_pct')}%)이 E-1({F('n_rework_e1')}건)·E-2({F('n_rework_e2')}건)",
                        "인접 배관·연계 부속 2차 점검 체크리스트 의무화",
                        f"최대 {F('rework_gap_max_h')}h({F('rework_gap_max_d')}일) 재방문 루프 제거"], 12.5, gap=5)],
              pad=0.24, gap=0.1, name="s2")
    c3 = Card([label("전략 3 · 번들 키트 · 외주 직행", GRN), heading("접수 인계와 외주 대기를 없앤다", 16, INK, name="h"),
               label("겨냥: 접수·외주 대기", MUTED), big(F("n_P4_extern"), "건 직행", GRN, 44, name="n"),
               bullets(["E-1/E-2 빈번 부품을 번들 키트로 사전 상차",
                        f"P-4 외주 {F('n_P4_extern')}건은 사진 식별 후 외주로 직행",
                        f"웹·우편 Direct Booking으로 교차 인계 {F('n_handover')}건 제거 (80% 가정)"], 12.5, gap=5)],
              pad=0.24, gap=0.1, name="s3")
    hh = row(sl, MX, top, CW, [c1, c2, c3], gutter=0.2)
    y = top + hh + 0.15
    ban = Card([label("COMMON KEY", ACC), Txt([rich("공통 열쇠는 **접수 단계의 정보 해상도** — 사진·라벨·세부 코드로 부품을 특정하면 실사·재방문·인계가 함께 줄어든다. 효과는 다음 장에서 가정과 함께 정량화한다.", 14, INK, accent=ACC)], name="ck")],
               pad=0.18, gap=0.05, name="common", line=ACC)
    bh = max(ban.natural_h(CW), BODY_BOTTOM - y)
    ban.draw(sl, MX, y, CW, bh)
    assert_body(sl, y + bh)
    sl.notes("세 가지 대기를 각각 겨냥합니다. 첫째 사진 기반 사전 특정으로 사내수리의 자재 대기를 출동 전으로 당기고, E형은 실사 없이 직행시킵니다. "
             f"둘째 재방문 {F('n_rework')}건의 {F('rework_e12_pct')}%가 몰린 E-1·E-2에 정밀검사 체크리스트를 의무화합니다. 셋째 번들 키트와 외주 직행, 웹·우편 Direct Booking으로 접수 인계를 없앱니다. "
             "다음 장에서 이 전략들의 효과를 가정과 함께 정량화합니다.")
    return sl


# ------------------------------------------------------------------ S16 기대 효과
def s16(doc, F):
    sl = doc.new_slide(18, "Part 03")
    chrome(sl, "[ 18 / Q3 · EXPECTED IMPACT ]", f"전체 평균 ▼{F('eff_total_pct')}%, 사내수리군은 ▼{F('intern_eff_pct')}%",
           sub="효과율은 가정값이며 구성요소 간 중복 효과는 보정하지 않은 상한 시나리오",
           source="출처: analysis.sql L1931~1985(시나리오) · hypothesis 노트북 Cell 19(OLS 1.12) · 사내수리군은 같은 가정을 485건에 적용")
    top = BODY_TOP + 0.08
    lw_ = 6.2

    def bars(sl_, x, y, w, parent):
        mx = float(F("intern_asis"))
        track = w - 2.05
        cy = y
        groups = [("전체 927건", F("lead_total"), F("tobe_total"), F("eff_total"), F("eff_total_pct")),
                  (f"사내수리 {F('n_intern1')}건", F("intern_asis"), F("intern_tobe"), F("intern_eff"), F("intern_eff_pct"))]
        for gi, (nm, a, b, eff, pct) in enumerate(groups):
            sl_.text(x, cy, w, [T(nm, 12.5, True, INK, balance=False)], parent=parent, name=f"g{gi}-nm", role="body", max_lines=1)
            cy += 0.28
            for lab, val, col in [("AS-IS", a, "94A3B8"), ("TO-BE", b, GRN)]:
                sl_.text(x, cy + 0.04, 0.62, [T(lab, 9.5, True, MUTED, "m", balance=False)], parent=parent, name=f"g{gi}-{lab}", structural=True, role="label", max_lines=1)
                bw = track * float(val) / mx
                _, rid = sl_.rect(x + 0.7, cy, bw, 0.32, fill=col, line=None, parent=parent, name=f"g{gi}-{lab}-bar")
                sl_.text(x + 0.7 + bw + 0.08, cy + 0.03, 1.1, [T(f"{val}h", 12.5, True, INK, "m", balance=False)], parent=parent, name=f"g{gi}-{lab}-v", role="body", max_lines=1)
                cy += 0.42
            sl_.text(x + 0.7, cy + 0.0, w - 0.7, [T(f"▼ {pct}% (−{eff}h)", 15, True, GRN, "m", balance=False)], parent=parent, name=f"g{gi}-delta", role="body", max_lines=1)
            cy += 0.52

    left = Card([label("TO-BE vs AS-IS · 평균 리드타임"), Custom(3.2, bars)], pad=0.22, gap=0.12, name="bars-card")

    def c(t, col=INK2, bold=False, size=11.5, font="k"):
        return [T(t, size, bold, col, font, balance=False)]

    rows_ = [
        [c("실사 대기 단축"), c("20% 단축 × OLS 1.12", MUTED, False, 11), c(f"−{F('eff_survey')}h", INK, True, 12.5, "m")],
        [c("자재 사전 패킹"), c(f"사내수리 {F('n_intern1')}건 자재 대기 100% 사전화", MUTED, False, 11), c(f"−{F('eff_material')}h", INK, True, 12.5, "m")],
        [c("리워크 차단"), c(f"재방문 {F('n_rework')}건 100% 차단", MUTED, False, 11), c(f"−{F('eff_rework')}h", INK, True, 12.5, "m")],
        [c("접수 인계 제거"), c(f"교차 인계 {F('n_handover')}건 80% 제거", MUTED, False, 11), c(f"−{F('eff_handover')}h", INK, True, 12.5, "m")],
        [c("합계 (가중평균)", INK, True), c(f"{F('lead_total')}h → {F('tobe_total')}h", GRN, True, 11.5), c(f"−{F('eff_total')}h", GRN, True, 13, "m")],
    ]
    tbl = Table([(2.2, "구성요소", "l"), (3.4, "가정", "l"), (1.3, "효과", "l")], rows_, pad_y=0.12, name="eff", row_fills={4: GRN_BG})
    right = Card([label("DECOMPOSITION · 927건 가중평균"), tbl], pad=0.2, gap=0.1, name="eff-card")
    rw = CW - lw_ - 0.2
    hh = max(left.natural_h(lw_), right.natural_h(rw))
    left.draw(sl, MX, top, lw_, hh)
    right.draw(sl, MX + lw_ + 0.2, top, rw, hh)
    y = top + hh + 0.15
    ban = Card([label("ASSUMPTIONS · 읽는 법", ORG),
                Txt([rich(f"항목별 효과는 전체 {F('n_valid')}건 평균으로 환산한 값이다(사내수리 {F('n_intern1')}건 대상 −{F('wait2_intern')}h → 전체 평균 −{F('eff_material')}h). 효과율(위 표 순서대로 20%·100%·100%·80%)이 바뀌면 효과는 비례해 달라지며, 표기 반올림은 합계와 일치하도록 보정했다.", 12, INK2, accent=ORG)], name="asm")],
               pad=0.18, gap=0.05, name="assump", line=ORG)
    bh = max(ban.natural_h(CW), BODY_BOTTOM - y)
    ban.draw(sl, MX, y, CW, bh)
    assert_body(sl, y + bh)
    sl.notes(f"효과를 보수적으로 정량화했습니다. 실사 대기를 20% 줄이면 OLS 계수 1.12가 곱해져 {F('eff_survey')}시간, 사내수리 {F('n_intern1')}건의 자재 대기를 사전화하면 전체 평균으로 {F('eff_material')}시간, "
             f"리워크와 접수 인계 제거가 각각 {F('eff_rework')}·{F('eff_handover')}시간으로 합계 {F('eff_total')}시간입니다. 전체 평균 {F('lead_total')}시간이 {F('tobe_total')}시간(약 3일)으로 ▼{F('eff_total_pct')}%입니다. "
             f"같은 가정을 사내수리군에 적용하면 {F('intern_asis')}시간에서 {F('intern_tobe')}시간(▼{F('intern_eff_pct')}%)입니다. "
             "[예상 질문] 효과율 근거는? → 실사 20%는 보수적 가정, 나머지는 해당 대기의 전량 제거를 가정한 상한이며 구성요소 간 중복은 보정하지 않았습니다. 가정이 바뀌면 효과는 비례해 달라집니다.")
    return sl


# ------------------------------------------------------------------ S17 Q&A
def s17(doc, F):
    sl = doc.new_slide(19, "Part 04")
    chrome(sl, "[ 19 / Q&A ]", "질의응답 (Q&A)", source="퍼즐데이터 수리 프로세스 데이터 분석 과제 · 조승훈 · 2026.10.27")
    top, H = BODY_TOP + 0.08, 4.75
    lw_ = 6.3

    def step(tag, col, head, desc):
        return Card([label(tag, col), heading(head, 15, INK, name="h"), body(desc, 12, INK2)], pad=0.22, gap=0.06, name="st-" + tag[:2])

    steps = [step("PART 01 · 데이터 무결성", ACC, f"{F('n_events')}행 전수 보존, 결측 {F('n_null_rows')}행 복원", f"삭제 0건 · 시간 역전 0건 · 분석 코호트 {F('n_valid')}건"),
             step("PART 02 · 병목 규명", ORG, f"실사 대기 {F('wait1')}h, 적체 {F('wip_peak')}건, 인계 {F('handover_ratio')}배", f"일 유입 {F('inflow_day')}건 vs CAPA {F('capa_day')}건 · 소요시간은 실사 지연이 좌우"),
             step("PART 03 · TO-BE 시나리오", GRN, f"전체 평균 ▼{F('eff_total_pct')}% ({F('lead_total')}h → {F('tobe_total')}h)", "사진 사전 특정 · E-1/E-2 정밀검사 · Direct Booking (가정 기반 상한)")]
    stack(sl, MX, top, lw_, steps, gutter=0.14, h_total=H)
    rx, rw = MX + lw_ + 0.2, CW - lw_ - 0.2
    hero = Card([label("QUESTION & ANSWER", ACC), Gap(0.3),
                 Txt([T("Q & A", 64, True, INK, "m", align="c", balance=False)], structural=True, name="qa", role="body"),
                 Txt([T("경청해 주셔서 감사합니다", 22, True, INK, align="c", balance=False)], name="thx"),
                 Txt([T("데이터 진단부터 병목 규명, 실행 전략까지 자유롭게 질문해 주십시오.", 12.5, False, INK2, align="c")], name="msg"),
                 Rule(),
                 Txt([T("조승훈 · 데이터 분석가 (신입) · 2026.10.27", 11, False, MUTED, "m", align="c", balance=False)], structural=True, name="who", role="body")],
                pad=0.3, gap=0.16, name="hero", line=ACC)
    hero.draw(sl, rx, top, rw, H)
    assert_body(sl, top + H)
    sl.notes(f"이상으로 발표를 마칩니다. {F('n_events')}행 전수 보존 전처리, {F('wait1')}시간의 실사 대기 병목과 원인 규명, 그리고 가정을 명시한 TO-BE 시나리오까지 설명드렸습니다. 질문 주시면 답변드리겠습니다. 감사합니다.\n\n"
             f"[핵심 숫자 치트시트] 리드타임 {F('lead_total')}h · 대기 {F('wait_B')}h({F('wait_B_pct')}%) · 실사 대기 {F('wait1')}h · 유입 {F('inflow_day')} vs CAPA {F('capa_day')} · 적체 {F('wip_peak')}건 · 인계 {F('handover_ratio')}배 · "
             f"OLS 실사 {F('ols2_visit_b')}h/h · 사내수리 +{F('ols2_intern_b')}h · 자재 {F('wait2_intern')}h · 재방문 {F('n_rework')}건 +{F('rework_gap_mean')}h · 적중률 {F('match_upper_pct')}/{F('match_cons_pct')}% · 감축 ▼{F('eff_total_pct')}%")
    return sl
