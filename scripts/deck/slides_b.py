"""슬라이드 10~17."""
import os

from kit import *          # noqa: F401,F403
from slides_a import FIG, DECK, cap


def _side_cards_right(sl, F, x, y, w, h_total, cards, gutter=0.12):
    stack(sl, x, y, w, cards, gutter=gutter, h_total=h_total)


# ------------------------------------------------------------------ S10 현장① 구성
def s10(doc, F):
    sl = doc.new_slide(12, "Part 02")
    chrome(sl, "[ 12 / Q2-2 · BOTTLENECK 2 · FIELD ]", f"현장 지연 요인: 현장 {F('field_total')}h 중 실사 방문 대기 {F('wait1_pct')}%",
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
        return Card([label(tag, color), heading(name, 13, INK, name="nm"), big(num, unit, color, 28, name="n"),
                     body(note, 11, MUTED, name="nt"), Bar(frac, color)], pad=0.2, gap=0.05, name="strip-" + tag[:2])

    s1 = strip("① WAIT 1", "실사 방문 대기", F("wait1"), "h", F("wait1_pct"), RED, float(F("wait1_pct")) / 100, f"현장 시간의 {F('wait1_pct')}% · 약 {F('wait1_days')}일")
    s2 = strip("② WAIT 2", "수리 착수·공정 대기", F("wait2_res"), "h", F("wait2_res_pct"), RED, float(F("wait2_res_pct")) / 100, f"{F('wait2_res_pct')}% · 재수리 인계 대기 포함")
    s3 = strip("③ WORK", "본수리 실작업", F("rep_work"), "h", F("rep_work_pct"), "64748B", float(F("rep_work_pct")) / 100, f"{F('rep_work_pct')}%")
    s4 = strip("④ WORK", "실사 점검 실작업", F("survey_work"), "h", F("survey_work_pct"), "94A3B8", float(F("survey_work_pct")) / 100, f"{F('survey_work_pct')}% · {F('survey_work_min')}분")
    h1 = row(sl, rx, top, rw, [s1, s2], gutter=0.14)
    h2 = row(sl, rx, top + h1 + 0.14, rw, [s3, s4], gutter=0.14)
    ty = top + h1 + 0.14 + h2 + 0.14
    take = Card([label("TAKEAWAY", RED),
                 Txt([rich(f"대기 합계 **{F('field_wait')}h = 현장 시간의 {F('field_wait_pct')}%**.", 15, INK, accent=RED),
                      rich("병목은 기사의 작업 속도가 아니라 방문 전 대기 관리다.", 15, INK, accent=RED)], name="take")],
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
    chrome(sl, "[ 13 / Q2-2 · BOTTLENECK 2 · QUEUE ]", f"Wait 1 원인: 일 유입 {F('inflow_day')}건 vs CAPA {F('capa_day')}건, 최대 적체 물량 {F('wip_peak')}건",
           sub=f"실사 대기의 원인 — {F('n_surveyed')}건 전수가 방문 실사를 거치는 구조 · 소화율 {F('digest_pct')}% (같은 구간 기준 {F('digest_pct_samewin')}%)",
           source="출처: analysis.sql L1556~1670·L1978~1981 · 유입 1/2~1/7 평균, CAPA 1/1~1/8 평균(기사 11인) · hypothesis 노트북 Cell 15")
    top = BODY_TOP + 0.08
    cw_ = 8.55
    chart = Card([cap("FIG.11", "일별 유입 vs 실사 CAPA 및 적체 대기열(WIP)"),
                  Img(os.path.join(FIG, "slide10_field_bottleneck_wip.png"), max_h=3.9, name="wip")], pad=0.14, gap=0.06, name="wip-card")
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, top, cw_, ch)
    rx, rw = MX + cw_ + 0.2, CW - cw_ - 0.2
    ms = [Card([label("일일 유입", ACC), big(F("inflow_day"), "건/일", ACC, 24, name="a"), body("접수 → 현장 이관 (1/2~1/7 평균)", 11, INK2)], pad=0.2, gap=0.06, name="m1"),
          Card([label(f"실사 CAPA · 기사 {F('n_field_workers')}인", MUTED), big(F("capa_day"), "건/일", INK, 24, name="b"), body(f"실사 착수 (1/1~1/8 평균) · 소화율 {F('digest_pct')}%", 11, INK2)], pad=0.2, gap=0.06, name="m2"),
          Card([label("적체 피크 (DAY 7)", RED), big(F("wip_peak"), "건", RED, 24, name="c"), body(f"Day 1의 {F('wip_day1')}건에서 {F('wip_multiple')}배", 11, INK2)], pad=0.2, gap=0.06, name="m3", line=RED)]
    stack(sl, rx, top, rw, ms, gutter=0.12, h_total=ch)
    ty = top + ch + 0.15
    take = Card([Txt([rich(f"**유입이 실사 처리 용량(CAPA)을 넘는 구조**가 적체와 {F('wait1')}h 대기의 원인 — 초과분이 하루 약 {F('wip_accum_day')}건씩 누적", 13, INK, accent=RED)], name="take")],
                pad=0.2, name="take-card")
    th_ = take.natural_h(CW)
    take.draw(sl, MX, ty, CW, th_)
    assert_body(sl, ty + th_)
    sl.notes(f"그렇다면 실사 대기는 왜 길어질까요? 원인은 처리 용량(CAPA)입니다. 파란 막대가 일일 접수 유입으로 평균 {F('inflow_day')}건, 회색 막대가 기사 {F('n_field_workers')}명의 실사 착수로 평균 {F('capa_day')}건입니다. 유입이 처리 능력을 약 2배 넘으면서 "
             f"미처리 대기열이 Day 1의 {F('wip_day1')}건에서 Day 7에 {F('wip_peak')}건까지 {F('wip_multiple')}배 늘었습니다. 하루 약 {F('wip_accum_day')}건씩 쌓인 셈입니다. "
             f"[예상 질문] 유입과 CAPA 산출 구간이 다른데? → 유입은 집중 유입기(1/2~1/7), CAPA는 1/1~1/8 평균입니다. 같은 구간(1/2~1/7)으로 맞춰도 소화율은 {F('digest_pct_samewin')}%로 결론이 같습니다.")
    return sl


# ------------------------------------------------------------------ S12 OLS
def s12(doc, F):
    sl = doc.new_slide(15, "Part 02")
    chrome(sl, "[ 15 / Q2-3 · DRIVERS · OLS ]", "E2E 리드타임 영향 요인: 실사 방문 대기 ≫ 사내수리 배정",
           sub=f"E2E 리드타임 OLS · R² {F('ols2_r2_pct')}% · F {F('ols2_f')} · N {F('n_valid')} · VIF 최대 {F('ols2_vif_max')}",
           source="출처: hypothesis 노트북 Cell 19 (statsmodels OLS, 재계산 일치) · 종속변수 total_hours")
    top = BODY_TOP + 0.08
    cw_ = 8.55
    chart = Card([cap("FIG.12", "E2E 리드타임 결정 요인 회귀계수"),
                  Img(os.path.join(FIG, "slide11_regression_leadtime_drivers.png"), max_h=3.5, name="ols")], pad=0.14, gap=0.06, name="ols-card")
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, top, cw_, ch)
    rx, rw = MX + cw_ + 0.2, CW - cw_ - 0.2
    cs = [Card([label("실사 방문 대기 · 1시간당", ACC), big("+" + F("ols2_visit_b"), "h/h", ACC, 24, name="a"), body(f"1시간 단축 시 전체 {F('ols2_visit_b')}h 감소 (p < 0.001)", 11, INK2)], pad=0.17, gap=0.06, name="k1"),
          Card([label("사내수리 배정 · vs 즉시·외주", RED), big("+" + F("ols2_intern_b"), "h", RED, 24, name="b"), body("자재 조달·일정 조율 대기 (p < 0.001)", 11, INK2)], pad=0.17, gap=0.06, name="k2"),
          Card([label("비실시간 채널 · 웹·우편", ORG), big("+" + F("ols2_async_b"), "h", RED, 24, name="c"), body(f"웹·우편 접수, p = {F('ols2_async_p')}", 11, INK2)], pad=0.17, gap=0.06, name="k3")]
    stack(sl, rx, top, rw, cs, gutter=0.12, h_total=ch)
    ty = top + ch + 0.15
    take = Card([Txt([rich(f"평균 기여(계수 × 평균값)로 환산하면 **실사 지연 {F('ols2_visit_contrib')}h**({F('ols2_visit_b')} × {F('ols2_visit_mean')}h)가 사내수리 {F('ols2_intern_contrib')}h({F('ols2_intern_b')} × {F('n_intern1_pct')}%)보다 훨씬 크다.", 12.5, INK, accent=ACC),
                      rich(f"2차 에스컬레이션(+{F('ols2_esc_b')}h)은 p = {F('ols2_esc_p')}로 비유의.", 12.5, INK, accent=ACC)], name="take")],
                pad=0.17, name="take-card")
    th_ = take.natural_h(CW)
    take.draw(sl, MX, ty, CW, th_)
    assert_body(sl, ty + th_)
    sl.notes(f"접수·실사·수리 착수 세 병목을 모두 확인했으니, 이 중 무엇이 전체 리드타임에 가장 크게 영향을 주는지 E2E 회귀로 종합합니다(비실시간 채널은 접수 요인이지만 같은 전체 모형의 변수입니다). E2E 리드타임을 설명하는 회귀모형의 설명력은 {F('ols2_r2_pct')}%입니다. 실사 방문 대기는 1시간당 {F('ols2_visit_b')}시간, 사내수리 배정은 +{F('ols2_intern_b')}시간, 비실시간 채널은 +{F('ols2_async_b')}시간 영향을 줍니다. "
             f"실사 지연의 계수가 1.12이므로 실사 대기를 1시간 줄이면 전체 리드타임이 1.12시간 줄어드는 지렛대 효과가 있고, 평균 기여로는 실사 지연 {F('ols2_visit_contrib')}시간이 사내수리 {F('ols2_intern_contrib')}시간보다 큽니다. 2차 에스컬레이션은 비유의합니다. "
             f"[예상 질문] 실사 지연은 리드타임의 구성요소라 계수가 기계적으로 커지는 것 아닌가? → 맞습니다. 그래서 계수 1.12는 순수 인과가 아니라 '실사 대기가 길어질 때 이후 대기도 함께 길어지는 파급'을 포함한 지렛대 추정이며, 사내수리·비실시간 채널은 구성요소가 아닌 외생 요인이라 별도로 해석합니다. [예상 질문] 다중공선성은? → VIF 최대 {F('ols2_vif_max')}로 문제 없습니다. [정정] F-통계량은 노트북 출력 {F('ols2_f')}입니다.")
    return sl


# ------------------------------------------------------------------ S13 수리·리워크
def s13(doc, F):
    sl = doc.new_slide(14, "Part 02")
    chrome(sl, "[ 14 / Q2-2 · BOTTLENECK 3 · REPAIR ]", f"Wait 2 요인: 사내수리는 자재 조달 {F('wait2_intern')}h, 재수리 시 +{F('rework_gap_mean')}h 지연",
           sub=f"사내 재수리 {F('n_rework')}건은 평균 총 리드타임 {F('rework_lead_mean')}h — 전체 평균의 {F('rework_lead_x')}배",
           source="출처: analysis.sql L1403~1546 · hypothesis 노트북 Cell 16~17 (정정 차트: 최대 지연과 평균 리드타임 라벨 분리)")
    top = BODY_TOP + 0.08
    cw_ = 8.55
    chart = Card([cap("FIG.13", "수리 방식별 착수 대기와 사내 재수리 루프"),
                  Img(os.path.join(DECK, "slide11_repair_delay_rework.png"), max_h=3.7, name="rw")], pad=0.14, gap=0.06, name="rw-card")
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, top, cw_, ch)
    rx, rw = MX + cw_ + 0.2, CW - cw_ - 0.2
    cs = [Card([label("사내수리 자재 대기", ORG), big(F("wait2_intern"), "h", RED, 24, name="a"), body(f"사내수리 {F('n_intern1')}건만 대기. 즉시·외주는 {F('wait2_imm')}h", 11, INK2)], pad=0.17, gap=0.06, name="k1"),
          Card([label("사내 재수리", RED), big(F("n_rework"), "건", RED, 24, name="b"), body(f"추가 대기 평균 +{F('rework_gap_mean')}h, 최대 {F('rework_gap_max_h')}h({F('rework_gap_max_d')}일)", 11, INK2)], pad=0.17, gap=0.06, name="k2"),
          Card([label("E-1 · E-2 코드 집중", RED), big(F("n_rework_e12"), f"건 · {F('rework_e12_pct')}%", RED, 24, name="c"), body(f"E-1 {F('n_rework_e1')}건 + E-2 {F('n_rework_e2')}건 — 정밀검사 대상", 11, INK2)], pad=0.17, gap=0.06, name="k3")]
    stack(sl, rx, top, rw, cs, gutter=0.12, h_total=ch)
    ty = top + ch + 0.15
    take = Card([Txt([rich(f"1차 수리 완료 뒤 재수리 착수까지 **평균 +{F('rework_gap_mean')}h**, 가장 길게는 **{F('rework_gap_max_d')}일**을 더 기다린다.", 12.5, INK, accent=RED)], name="take")],
                pad=0.17, name="take-card")
    th_ = take.natural_h(CW)
    take.draw(sl, MX, ty, CW, th_)
    assert_body(sl, ty + th_)
    sl.notes(f"다음 병목은 수리 착수 단계입니다. 즉시수리와 외주수리는 착수 대기가 {F('wait2_imm')}시간인데, 사내수리 {F('n_intern1')}건만 부품 조달과 일정 조율로 평균 {F('wait2_intern')}시간을 기다립니다. "
             f"또 사내수리 후 재수리가 이어진 {F('n_rework')}건은 1차 수리 완료 뒤 재수리 착수까지 평균 {F('rework_gap_mean')}시간, 최대 {F('rework_gap_max_h')}시간({F('rework_gap_max_d')}일)을 더 기다렸고, 이 케이스들의 평균 총 리드타임은 {F('rework_lead_mean')}시간입니다. "
             f"재수리 {F('n_rework')}건 중 {F('n_rework_e12')}건({F('rework_e12_pct')}%)이 E-1·E-2 코드에 집중되어 있습니다.")
    return sl


# ------------------------------------------------------------------ S14 규명
def s14(doc, F):
    sl = doc.new_slide(16, "Part 03")
    chrome(sl, "[ 16 / Q2→Q3 · ROOT CAUSE ]", "적중률은 높은데 정보 해상도가 끊겨 있다",
           sub=f"접수 알파벳 분류가 실제 수리 방식과 맞는데도(E→사내 {F('E_intern_pct')}%, P→즉시 {F('fast_p_prec')}%) 모든 건이 실사 큐 한 줄에 선다",
           source=f"출처: analysis.sql L1888~1928 · case_pivot_table.csv 재계산 · 큐 점유시간 = 실사 착수 후 기사가 그 건에 묶이는 시간(즉시 수리는 실사+수리)")
    top = BODY_TOP + 0.08
    c1 = Card([label("01 · 데이터 팩트", ACC), heading("사전 적중률은 높다", 15, INK, name="h"),
               Img(os.path.join(DECK, "slide12_intake_matching_donut.png"), max_h=2.5, name="donut"),
               Txt([rich(f"E → 사내수리 **{F('E_intern_pct')}%** ({F('n_E')}/{F('n_E')}건)", 15, INK, accent=ACC),
                    rich(f"P → 즉시수리 **{F('fast_p_prec')}%** ({F('n_fast')}/{F('n_P')}건)", 15, INK, accent=ACC)], name="n")], pad=0.2, gap=0.07, name="c1")
    spacer = Gap(0.0)      # 마무리 한 줄을 카드 남는 공간의 세로 가운데에 두는 스페이서
    c2 = Card([label("02 · 원인 규명", ACC), heading("정보 해상도 단절 → 한 줄", 15, INK, name="h"),
               Card([label("접수 (현행)", MUTED), body("알파벳 3분류(B·P·E)만 수집 — 즉시 수리 여부를 가릴 수 없음", 11.5, INK2)], pad=0.14, gap=0.06, fill=SLATE_BG, name="boxA"),
               Card([label("현장 (현행)", MUTED), body(f"{F('survey_work_min')}분 방문 실사 후 세부 코드(1~4) 판정", 11.5, INK2)], pad=0.14, gap=0.06, fill=SLATE_BG, name="boxB"),
               spacer, Txt([rich("채널이 달라도 **실사 대기 큐는 한 줄**", 15, INK, accent=ACC, align="c")], name="res")],
              pad=0.2, gap=0.1, name="c2")
    c3 = Card([label("03 · 분리 근거", GRN), heading("즉시 수리 건을 따로 뺀다", 15, INK, name="h"),
               big(F("n_fast"), "건 · " + F("fast_pct") + "%", INK, 36, name="n"),
               body(f"접수 코드 P-1·3 — 건수는 {F('fast_pct')}%인데 실사 큐 점유시간은 {F('occ_fast_share')}%", 11.5, INK2),
               bullets([f"실사→수리 간격 {F('fast_gap_h')}h, 같은 기사 {F('fast_same_worker_pct')}%",
                        f"건당 점유 {F('occ_fast_h')}h, 나머지({F('occ_rest_h')}h)의 {F('occ_ratio')}배"], 11.5)],
              pad=0.2, gap=0.08, name="c3")
    w3 = (CW - 0.4) / 3
    spacer._h = max(0.0, (max(c1.natural_h(w3), c3.natural_h(w3)) - c2.natural_h(w3)) / 2)
    hh = row(sl, MX, top, CW, [c1, c2, c3], gutter=0.2)
    y = top + hh + 0.15
    ban = Card([label("SO WHAT", ACC), Txt([rich("접수 단계에서 **해상도를 높여** **실사 대기 적체(WIP) 부담**을 줄여야 한다", 15, INK, accent=ACC)], name="sw")],
               pad=0.18, gap=0.05, name="sowhat", line=ACC)
    bh = max(ban.natural_h(CW), BODY_BOTTOM - y)
    ban.draw(sl, MX, y, CW, bh)
    assert_body(sl, y + bh)
    sl.notes(f"접수원의 사전 분류는 이미 현장 결과와 {F('match_cons_pct')}~{F('match_upper_pct')}% 일치합니다. 그런데도 모든 건이 방문 실사를 거치는 이유는 정보 해상도 단절입니다. "
             f"접수는 B·P·E 알파벳만 수집하고, 현장은 약 {F('survey_work_min')}분 실사 후 1~4 세부 코드를 판정합니다. "
             f"그 결과 채널이 달라도 실사로 가는 줄은 하나입니다. 채널별 실사 대기는 {F('ch_wait_min')}~{F('ch_wait_max')}시간으로 통계적으로 차이가 없습니다(Kruskal p={F('ch_kw_p')}). "
             f"이 한 줄에서 즉시 수리 건(접수 코드 P-1·3, {F('n_fast')}건)을 따로 빼자는 것이 제안입니다. 즉시 수리는 건수로는 {F('fast_pct')}%이지만, 실사를 시작하면 기사가 수리까지 연속으로 맡아 큐 점유시간은 {F('occ_fast_share')}%입니다(건당 {F('occ_fast_h')}시간, 나머지 {F('occ_rest_h')}시간). "
             f"실사에서 수리 착수까지 간격은 {F('fast_gap_h')}시간이고 같은 기사가 {F('fast_same_worker_pct')}% 맡았습니다. 고속도로로 비유하면 큐를 오래 점유하는 화물차만 따로 빼자는 것입니다. "
             f"[적중 기준] 비교 대상은 세부코드가 아니라 접수 알파벳(B·P·E)과 실제 1차 수리 방식입니다. 세부코드 1~4는 현장 실사 후 판정되는 값이라 접수 시점에는 없습니다. "
             f"E형 {F('n_E')}건은 전부 사내수리({F('E_intern_pct')}%), P형 {F('n_P')}건 중 즉시수리는 {F('n_fast')}건({F('fast_p_prec')}%)이며 즉시수리 기저율 {F('imm_base_pct')}%의 약 {F('p_imm_lift')}배입니다. 즉시수리 {F('n_imm1')}건 중 P가 잡아낸 비율은 {F('p_imm_recall_pct')}%입니다(놓친 건은 B-1). "
             f"[정정] 도넛의 {F('match_upper_pct')}%는 E·P로 분류된 비율({F('match_upper_n')}/{F('n_valid')}건)이지 예측 정확도가 아닙니다. 사내 완결(즉시·사내) 기준으로 외주 P-4({F('n_P4_extern')}건)를 빼면 {F('match_cons_pct')}%({F('match_cons_n')}건)지만, 아무 건이나 사내 완결로 찍어도 {F('self_base_pct')}%라 변별력이 약해 근거로 쓰지 않습니다. "
             f"엄격 기준(E→사내, P→즉시)의 일치는 E·P 기준 {F('strict_pct_ep')}%, 전체 기준 {F('strict_pct_all')}%({F('strict_n')}건)입니다. 주의: 사내 완결 {F('match_cons_pct')}%(전체 기준)와 P 즉시 {F('fast_p_prec')}%(P 기준)는 서로 다른 값입니다. "
             f"[예상 질문] 알파벳 P·E·B의 의미는? → 원천에 정의서가 없어 실측 수리 방식 분포로 해석했습니다(E 전량 사내, P 대부분 즉시, B 혼합). 세부코드는 (알파벳, 코드) 조합마다 수리 방식이 하나로 정해져 사후 라벨일 수 있어 접수 시점 취득 가능성은 가정입니다. "
             f"[예상 질문] B형은? → B형 {F('n_B')}건은 이미 실사 대기가 평균 {F('b_wait1')}시간으로 큐를 사실상 우회하고 있어 분리 대상에서 뺐습니다.")
    return sl


# ------------------------------------------------------------------ S15 전략 (하나의 구체적 전략)
def s15(doc, F):
    sl = doc.new_slide(17, "Part 03")
    chrome(sl, "[ 17 / Q3 · TO-BE STRATEGY ]", "Direct Booking 전략: 하나의 병목 줄을 두 갈래로",
           sub="접수 코드를 세분화해 즉시 수리 건을 실사 줄에서 빼고, 기사 캘린더로 바로 예약해 작업 줄로 보낸다",
           source="출처: analysis.sql L1888~1928(사전 분류) · case_pivot_table.csv 재계산 · UI는 제안이며 효과는 다음 장에서 가정과 파일럿으로 다룸")
    top = BODY_TOP + 0.08

    def c(t, col=INK2, bold=False, size=11.5):
        return [T(t, size, bold, col, balance=True)]

    rows_ = [
        [c("정보 입력", INK, True), c("B·P·E 알파벳 3분류만 수집, 텍스트 입력"),
         [rich("**세부 코드(1~4)** 구조화 입력", 11.5, INK, accent=ACC),
         rich("웹 양식 포맷을 **전 채널에 동일 적용**", 11.5, INK, accent=ACC),
         rich(f"(빠른 건 평균 {F('fast_web_min')}분, 전 채널 최속)", 11.5, INK2, accent=ACC)]],
        [c("줄 분리", INK, True), c(f"채널이 달라도 {F('n_valid')}건 전부 실사 큐 한 줄"),
         [rich("**즉시 수리 코드(P-1·3)** 건은 실사 줄에서 빼 **작업 줄**로 직행", 11.5, INK, accent=ACC)]],
        [c("일정 확정", INK, True), c(f"상담원 일정 회신(비동기), 교차 인계 {F('n_handover')}건 ({F('single_h')}h → {F('handover_h')}h)"),
         [rich("**기사 캘린더**에서 고객이 슬롯을 직접 선택 — 상담원 개입 0", 11.5, INK, accent=ACC)]],
        [c("방문", INK, True), c("실사 대기 후 방문, 사내수리는 부품 주문 → 재방문"),
         [rich("즉시 건은 **기본 키트로 1회 방문 수리**, 그 외는 **정밀검사(실사) 유지**", 11.5, INK, accent=ACC)]],
    ]
    tbl = Table([(1.0, "구분", "l"), (3.1, "AS-IS (현행)", "l"), (3.9, "TO-BE (Direct Booking)", "l")], rows_, pad_y=0.06, name="db")
    lw_ = 8.3
    left = Card([label("PROCESS · 접수 → 줄 분리 → 일정 확정 → 방문"), tbl], pad=0.2, gap=0.08, name="db-card")
    rw = CW - lw_ - 0.2
    c1 = Card([label("DIRECT 대상 · 즉시 수리 코드"), big(F("n_fast"), "건", INK, 36, name="n"),
               body(f"P-1·3, 전체의 {F('fast_pct')}%. 수리 {F('fast_rep_h')}h로 사내수리({F('intern_rep_h')}h)의 {F('fast_vs_intern_pct')}%", 11.5, INK2)],
              pad=0.2, gap=0.06, name="elig")
    c2 = Card([label("전제 · 신뢰도"),
               bullets([f"알파벳 P만으로 적중 {F('fast_p_prec')}% — 오분류 {F('n_p_miss')}건({F('p_miss_pct')}%)을 세부 코드로 거름",
                        "전제: 접수 시점에 세부 코드를 얻을 수 있어야 함 (파일럿에서 측정)",
                        f"한계: 우편 {F('n_letter')}건은 웹 전환 필요"], 11.5)],
              pad=0.2, gap=0.06, name="guard")
    h1 = c1.natural_h(rw)
    hh = max(left.natural_h(lw_), h1 + 0.14 + c2.natural_h(rw))
    left.draw(sl, MX, top, lw_, hh)
    c1.draw(sl, MX + lw_ + 0.2, top, rw, h1)
    c2.draw(sl, MX + lw_ + 0.2, top + h1 + 0.14, rw, hh - h1 - 0.14)
    y = top + hh + 0.15

    def ln(t, size=11.5, color=INK2):
        return [rich(t, size, color, accent=ACC, balance=True)]

    def hd(t):
        return T(t, 11, True, ACC, "m", balance=False)

    lanes = Table([(1, "", "l"), (1, "", "l"), (1, "", "l")], [[
        [hd("AS-IS · 줄 1개")] + ln(f"**{F('n_valid')}건 전부 실사 큐 한 줄**") + ln(f"일 유입 {F('inflow_day')}건 vs CAPA {F('capa_day')}건"),
        [hd("TO-BE · 실사 줄 (정밀검사)")] + ln(f"**{F('n_rest')}건** — 일 유입 {F('inflow_day')}→{F('inflow_rest')}건({F('fast_pct')}% 감소)") + ln(f"B형 {F('n_B')}건 · 외주 전환 {F('n_extern_all')}건 · 재작업 집중 E형"),
        [hd("TO-BE · 작업 줄 (즉시)")] + ln(f"**{F('n_fast')}건** — 기본 키트로 1회 방문") + ln(f"실사 {F('fast_svy_h')}h 생략, 수리 {F('fast_rep_h')}h")]],
        pad_y=0.02, head=False, name="lanes")
    ban = Card([label("TWO LANES · 줄을 하나에서 둘로", ACC), lanes], pad=0.18, gap=0.04, name="common")
    bh = max(ban.natural_h(CW), BODY_BOTTOM - y)
    ban.draw(sl, MX, y, CW, bh)
    assert_body(sl, y + bh)
    sl.notes(f"개선 전략은 하나입니다. 접수 단계의 사전 필터 신뢰도를 높여 뒤 공정의 시간을 줄이는 것이고, 구체적으로는 Direct Booking입니다. 지금은 채널이 달라도 {F('n_valid')}건이 전부 실사 큐 한 줄에 서는데, 즉시 수리 건만 따로 뺍니다. "
             f"즉시 수리는 실사 도중 기본 키트로 끝낼 수 있는 작업이라 실사 대기줄을 거칠 이유가 없고, 작업 줄로 바로 이관할 수 있습니다. 수리 시간은 평균 {F('fast_rep_h')}시간으로 사내수리 {F('intern_rep_h')}시간의 {F('fast_vs_intern_pct')}% 수준입니다. "
             f"분류는 접수 정보의 해상도로 합니다. 현재는 B·P·E 알파벳만 받고 상담원이 기사 일정을 확인해 회신하는 비동기 핑퐁이라 교차 인계가 {F('n_handover')}건 발생했습니다. "
             f"웹 양식은 빠른 건 평균 {F('fast_web_min')}분으로 정보 추출이 가장 빨라, 이 포맷을 전 채널에 적용하고 세부 코드(1~4) 수준으로 받습니다. 즉시 코드로 확정된 건은 기사 캘린더에서 고객이 슬롯을 직접 고릅니다. "
             f"보조 전략은 정밀검사입니다. 복합진단 B형 {F('n_B')}건과 외주 전환 {F('n_extern_all')}건(P-4 {F('n_P4_extern')}건 + B-4 {F('n_B4_extern')}건)은 실사를 유지하고, 재작업 {F('n_rework')}건 중 {F('n_rework_e12')}건이 E-1·E-2에 몰려 있어 E형도 정밀검사로 재방문을 막습니다. "
             f"[정정] 외주는 E형이 아니라 P-4와 B-4에서 나왔고 E형 외주는 {F('n_E_extern')}건입니다. "
             f"[예상 질문] 분류가 틀리면? → 알파벳 P만으로도 {F('fast_p_prec')}%({F('n_fast')}/{F('n_P')}건)가 즉시 수리였고, 오분류 {F('n_p_miss')}건({F('p_miss_pct')}%)을 세부 코드로 거르는 것이 고도화의 목표이자 파일럿 KPI입니다. "
             f"[예상 질문] 세부 코드를 접수 시점에 얻을 수 있나? → 로그의 코드는 수리 방식과 100% 일치해 사후 확정 라벨일 수 있고, 접수 시점 취득 가능성은 데이터로 검증할 수 없어 전제로 두었습니다. "
             f"[예상 질문] 기사 풀이 같은데 줄을 나누면? → 기사 {F('n_field_workers')}명이 두 줄을 공유하므로 용량이 늘어나는 것이 아니라 슬롯 배분 정책입니다. 효과는 다음 장에서 가정과 파일럿으로 다룹니다. "
             f"[예상 질문] 우편은? → 우편 {F('n_letter')}건은 웹 전환이 전제입니다.")
    return sl


# ------------------------------------------------------------------ S16 기대 효과
def s16(doc, F):
    sl = doc.new_slide(18, "Part 03")
    chrome(sl, "[ 18 / Q3 · EXPECTED IMPACT ]", f"실사 대기 20% 단축 시 평균 리드타임 ▼{F('eff_total_pct')}%",
           sub="줄 분리의 순수 효과는 로그로 식별할 수 없어 단축률을 가정하고, 파일럿으로 검증한다",
           source="출처: case_pivot_table.csv 재계산 · 실사 대기는 리드타임의 구성요소라 1:1 반영(OLS 계수 미적용) · 단축률은 가정")
    top = BODY_TOP + 0.08
    lw_ = 6.2

    def bars(sl_, x, y, w, parent):
        mx = float(F("lead_total"))
        track = w - 2.05
        cy = y
        for lab, val, col in [("AS-IS", F("lead_total"), "94A3B8"), ("TO-BE", F("tobe_total"), GRN)]:
            sl_.text(x, cy + 0.04, 0.62, [T(lab, 9.5, True, MUTED, "m", balance=False)], parent=parent, name=f"b-{lab}", structural=True, role="label", max_lines=1)
            bw = track * float(val) / mx
            sl_.rect(x + 0.7, cy, bw, 0.34, fill=col, line=None, parent=parent, name=f"b-{lab}-bar")
            sl_.text(x + 0.7 + bw + 0.08, cy + 0.04, 1.1, [T(f"{val}h", 12.5, True, INK, "m", balance=False)], parent=parent, name=f"b-{lab}-v", role="body", max_lines=1)
            cy += 0.46
        sl_.text(x + 0.7, cy + 0.02, w - 0.7, [T(f"▼ {F('eff_total_pct')}% (−{F('eff_total')}h)", 15, True, GRN, "m", balance=False)], parent=parent, name="b-delta", role="body", max_lines=1)

    def c(t, col=INK2, bold=False, size=11.5, font="k", align="l"):
        return [T(t, size, bold, col, font, align=align, balance=False)]

    sens = Table([(1.3, "실사 대기 단축", "l"), (3.1, "평균 리드타임", "l"), (1.3, "감소율", "l")], [
        [c("10%"), c(f"{F('lead_total')} → {F('sens10_after')}h (−{F('sens10_total')}h)", INK2, False, 11.5, "m"), c(f"▼ {F('sens10_pct')}%", INK2, False, 11.5, "m")],
        [c("20% · 기준", INK, True), c(f"{F('lead_total')} → {F('tobe_total')}h (−{F('eff_total')}h)", GRN, True, 11.5, "m"), c(f"▼ {F('eff_total_pct')}%", GRN, True, 11.5, "m")],
        [c("30%"), c(f"{F('lead_total')} → {F('sens30_after')}h (−{F('sens30_total')}h)", INK2, False, 11.5, "m"), c(f"▼ {F('sens30_pct')}%", INK2, False, 11.5, "m")],
    ], pad_y=0.07, name="sens", row_fills={1: GRN_BG})
    left = Card([label("TO-BE vs AS-IS · 평균 리드타임"), Custom(1.3, bars), Rule(), label("SENSITIVITY · 단축률별 효과"), sens], pad=0.22, gap=0.1, name="bars-card")

    prow = [
        [c("대상", INK, True), c(f"즉시 코드 P-1·3 {F('n_fast')}건만 별도 줄로 분리(예약 슬롯 확보), 나머지는 현행 유지", MUTED, False, 11)],
        [c("비교", INK, True), c(f"나머지 실사 줄의 대기(AS-IS {F('wait1')}h)와 즉시 줄의 예약 대기", MUTED, False, 11)],
        [c("품질", INK, True), c(f"직행 적중률(AS-IS P {F('fast_p_prec')}%)과 재방문 건수(AS-IS {F('n_rework')}건)", MUTED, False, 11)],
        [c("판정", INK, True), c("실사 대기 단축률이 가정(10·20·30%)의 어느 구간인지 보고 확대 여부를 정한다", MUTED, False, 11)],
    ]
    ptbl = Table([(1.0, "", "l"), (4.4, "", "l")], prow, pad_y=0.13, head=False, name="pilot")
    right = Card([label("PILOT · 순수 효과 검증 설계"), ptbl,
                  Txt([T("미반영(상방 요인): 자재 사전 확보, 재방문 방지, 접수 인계 제거 — 근거가 부족해 효과에서 제외했습니다.", 11, False, MUTED, balance=True)], name="excl")],
                 pad=0.2, gap=0.12, name="eff-card")
    rw = CW - lw_ - 0.2
    hh = max(left.natural_h(lw_), right.natural_h(rw))
    left.draw(sl, MX, top, lw_, hh)
    right.draw(sl, MX + lw_ + 0.2, top, rw, hh)
    y = top + hh + 0.15
    ban = Card([label("ASSUMPTIONS · 읽는 법", ACC),
                Txt([rich(f"단축률 20%는 **가정**이다. 즉시 건이 빠지면 실사 줄 유입은 {F('fast_pct')}% 줄지만 기사 {F('n_field_workers')}명을 두 줄이 공유해 줄 분리의 순수 효과는 로그로 식별되지 않는다. 20%는 유입 감소율의 약 절반만 반영한 보수 가정이며 파일럿으로 검증한다.", 12, INK2, accent=ACC)], name="asm")],
               pad=0.18, gap=0.05, name="assump")
    bh = max(ban.natural_h(CW), BODY_BOTTOM - y)
    ban.draw(sl, MX, y, CW, bh)
    assert_body(sl, y + bh)
    sl.notes(f"효과는 하나의 가정으로만 계산했습니다. 즉시 수리 {F('n_fast')}건이 실사 줄에서 빠지면 실사 줄 유입이 일 {F('inflow_day')}건에서 {F('inflow_rest')}건으로 {F('fast_pct')}% 줄어듭니다. 이 유입 감소의 약 절반만 대기 단축으로 반영해 실사 대기를 20%, 즉 {F('wait1')}시간에서 {F('wait1_after')}시간으로 {F('eff_total')}시간 줄인다고 가정합니다. "
             f"실사 대기는 리드타임의 구성요소이므로 1대1로 반영해 {F('lead_total')}시간이 {F('tobe_total')}시간, ▼{F('eff_total_pct')}%입니다. 단축률이 10%면 ▼{F('sens10_pct')}%, 30%면 ▼{F('sens30_pct')}%입니다. "
             f"이 숫자는 예측이 아니라 가정입니다. 기사 {F('n_field_workers')}명을 두 줄이 공유하고 관측 데이터에는 줄을 나눈 사례가 없어 순수 효과는 식별되지 않습니다. 그래서 즉시 건만 별도 줄로 운영하는 파일럿을 제안하고, 나머지 줄의 대기와 직행 적중률, 재방문 건수로 판정합니다. "
             f"자재 사전 확보, 재방문 방지, 접수 인계 제거는 근거가 부족해 효과에서 제외했고 상방 요인으로 남깁니다. "
             f"[예상 질문] 20%의 근거는? → 유입 감소율 {F('fast_pct')}%의 약 절반이라는 보수 가정입니다. 참고로 일별 대기열 모델에서 실사 단계가 사라져 해방되는 기사 시간 {F('qm_freed_pct')}%만 반영해도 평균 대기가 약 {F('qm_cut_pct')}% 줄지만, 기준값이 구성상 항등식이고 부하가 큰 8일 구간이라 상한 참고로만 씁니다. "
             f"[예상 질문] 줄별 평균(즉시 줄, 나머지 줄)으로 계산하지 않은 이유는? → 두 줄은 지금 하나의 대기열을 공유한 상태의 평균이라 줄을 나눈 뒤의 대기를 대표하지 않고, B형 {F('n_B')}건(대기 {F('b_wait1')}시간)이 섞여 있어 실제 큐 대기와도 다릅니다.")
    return sl


# ------------------------------------------------------------------ S17 Q&A
def s17(doc, F):
    sl = doc.new_slide(19, "Part 04")
    chrome(sl, "[ 19 / Q&A ]", "질의응답 (Q&A)", source="퍼즐데이터 수리 프로세스 데이터 분석 과제 · 조승훈 · 2026.10.27")
    top, H = BODY_TOP + 0.08, 4.75
    lw_ = 6.3

    def step(tag, col, head, desc):
        return Card([label(tag, col), heading(head, 15, INK, name="h"), body(desc, 12, INK2)], pad=0.22, gap=0.06, name="st-" + tag[:2])

    steps = [step("PART 01 · 데이터 무결성", ACC, f"{F('n_events')}행 전수 보존, 결측 {F('n_null_rows')}행 복원", f"삭제 0건 · 시간 역전 0건 · 정상 접수 {F('n_valid')}건, 오접수 {F('n_wrongplace')}건"),
             step("PART 02 · 병목 규명", ORG, f"실사 대기 {F('wait1')}h, 적체 {F('wip_peak')}건, 인계 {F('handover_ratio')}배", f"일 유입 {F('inflow_day')}건 vs CAPA {F('capa_day')}건 · 소요시간은 실사 지연이 좌우"),
             step("PART 03 · TO-BE 시나리오", GRN, f"전체 평균 ▼{F('eff_total_pct')}% ({F('lead_total')}h → {F('tobe_total')}h)", "Direct Booking 전략 · 하나의 병목 줄을 두 갈래로 · 단축률 가정")]
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
    sl.notes(f"이상으로 발표를 마칩니다. {F('n_events')}행 전수 보존 전처리, {F('wait1')}시간의 실사 대기 병목과 원인 규명, 그리고 가정을 명시하고 파일럿으로 검증하는 TO-BE 시나리오까지 설명드렸습니다. 질문 주시면 답변드리겠습니다. 감사합니다.\n\n"
             f"[핵심 숫자 치트시트] 리드타임 {F('lead_total')}h · 대기 {F('wait_B')}h({F('wait_B_pct')}%) · 실사 대기 {F('wait1')}h · 유입 {F('inflow_day')} vs CAPA {F('capa_day')} · 적체 {F('wip_peak')}건 · 인계 {F('handover_ratio')}배 · "
             f"OLS 실사 {F('ols2_visit_b')}h/h · 사내수리 +{F('ols2_intern_b')}h · 자재 {F('wait2_intern')}h · 재방문 {F('n_rework')}건 +{F('rework_gap_mean')}h · 적중률 {F('match_upper_pct')}/{F('match_cons_pct')}% · 감축 ▼{F('eff_total_pct')}%")
    return sl
