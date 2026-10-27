"""슬라이드 1~9. 숫자는 모두 F(key) 로만 주입한다."""
import os

from kit import *          # noqa: F401,F403

FIG = os.path.join(ROOT, "outputs", "figures")
DECK = os.path.join(FIG, "deck")


def cap(kicker, text):
    return label(f"{kicker} · {text}")


# ------------------------------------------------------------------ S01 표지
def s01(doc, F):
    sl = doc.new_slide(1, "Part 00")
    sl.text(MX, 0.55, 7.4, [T("[ 00 / 퍼즐데이터 채용 과제 ]", 12, True, ACC, "m", balance=False)],
            structural=True, name="tag", role="tag", max_lines=1)
    sl.text(SLIDE_W - MX - 4.6, 0.57, 4.6, [T("PUZZLEDATA · REPAIR PROCESS ANALYSIS", 9, False, MUTED, "m", align="r", balance=False)],
            structural=True, name="brand", role="brand", max_lines=1)
    # 좌: 제목 블록
    lx, lw_ = MX, 7.3
    y = 2.5
    sl.text(lx, y, lw_, [T("PROCESS MINING × OPERATIONS OPTIMIZATION", 10.5, True, MUTED, "m", balance=False)],
            structural=True, name="kicker", role="label", max_lines=1)
    y += 0.42
    _, th, _ = sl.text(lx, y, lw_, [T("공공임대주택 수리 프로세스", 36, True, INK, balance=False),
                                    T("진단 및 운영 최적화 방안", 36, True, ACC, balance=False)], name="title", role="title", max_lines=2)
    # 우하단: 지원 정보 (가로 배열)
    cw, ch, cx, cy = 6.6, 0.95, SLIDE_W - MX - 6.6, 5.8
    _, card_id = sl.rect(cx, cy, cw, ch, fill=CARD, line=BORDER, name="applicant")
    x0 = cx + 0.2
    for k, v, w_, mono in [("POSITION", "데이터 분석가", 1.6, False), ("LEVEL", "신입", 0.9, False), ("NAME", "조승훈", 1.1, False), ("E.MAIL", "nextbus1245@gmail.com", 2.6, True)]:
        sl.text(x0, cy + 0.15, w_ - 0.1, [T(k, 9.5, True, ACC, "m", balance=False)], structural=True, parent=card_id, name="k-" + k, role="label", max_lines=1)
        sl.text(x0, cy + 0.45, w_ - 0.05, [T(v, 13 if mono else 15, True, INK, "m" if mono else "k", balance=False)], structural=True, parent=card_id, name="v-" + k, role="body", max_lines=1)
        x0 += w_
    sl.hline(MX, 6.98, CW, name="foot-rule")
    sl.text(MX, 7.06, 10.6, [T("퍼즐데이터 수리 프로세스 데이터 분석 과제 · 공공임대주택 수리 이벤트 로그", 9, False, "94A3B8", "m", balance=False)],
            structural=True, name="source", role="foot", max_lines=1)
    sl.notes(
        "안녕하십니까, 퍼즐데이터 데이터 분석가 신입 직무에 지원한 조승훈입니다. 이 보고서는 공공임대주택 수리 이벤트 로그 "
        f"{F('n_events')}행(1,000개 케이스)을 프로세스 마이닝 관점에서 분석해, 리드타임의 {F('wait_B_pct')}가 공정 간 대기라는 사실과 그 구조적 원인, "
        "그리고 실행 가능한 개선안을 제시합니다.")
    return sl


# ------------------------------------------------------------------ S02 목차
def s02(doc, F):
    sl = doc.new_slide(2, "Part 00")
    chrome(sl, "[ 02 / PREVIEW ]", "목차 소개",
           source="PART 01 p.04–06 · PART 02 p.07–15 · PART 03 p.16–18 · PART 04 p.19")
    tiles = [
        ("01", ACC, "질문 1", ACC, ACC_BG, "데이터 진단 및 전처리", 4,
         ["이벤트 로그 프로파일링과 결측 2원화", "순서 기반 결측 복원, 삭제 0건", f"시간 역전 0건, 정상 접수 {F('n_valid')}건, 오접수 {F('n_wrongplace')}건"],
         f"{F('n_events')}", "행 전수 보존"),
        ("02", ORG, "질문 2", ORG, ORG_BG, "AS-IS 심층 분석", 7,
         ["AS-IS 표준 프로세스 모델", "2개 병목 구간: 접수 · 실사", "1개 반복 작업: 반복 수리", "상관·OLS로 소요시간 영향 요인 실증"],
         f"{F('wait_B_pct')}%", "리드타임 중 대기"),
        ("03", GRN, "질문 3", GRN, GRN_BG, "TO-BE 개선 방안", 16,
         [f"사전 분류 적중률 {F('match_upper_pct')}%와 정보 해상도 한계", "Direct Booking 전략: 하나의 병목 줄을 두 갈래로", "단축률 가정 시 감축 효과"],
         f"▼{F('eff_total_pct')}%", "전체 평균 감축(가정)"),
        ("04", MUTED, "마무리", MUTED, SLATE_BG, "핵심 요약", 19,
         ["파트별 핵심 결과 정리"],
         "Q&A", None),
    ]
    cards = []
    for idx, col, pill, pc, pbg, title, target, bl, kn, kl in tiles:
        els = [Txt([T(idx, 40, True, ACC, "m", balance=False)], structural=True, role="body", name="idx"),
               Pill(pill.upper() if pill.isascii() else pill, pc, pbg),
               heading(title, 16, INK, name="ttl"), Gap(0.04), bullets(bl, 11.5)]
        foot = Txt([P([R(kn, 28, True, {"01": INK, "02": RED, "03": GRN, "04": MUTED}[idx], "m")], lh=LH_BIG, balance=False)]
                   + ([T(kl, 11, False, MUTED, balance=False)] if kl else []), name="key")
        cards.append(Card(els, pad=0.24, gap=0.12, min_h=4.7, name=f"tile-{idx}", link=target, foot=foot))
    hh = row(sl, MX, 1.75, CW, cards, gutter=0.2)
    assert_body(sl, 1.75 + hh)
    sl.notes("오늘 발표는 4개 파트입니다. 질문 1에서 데이터 진단과 전처리를, 질문 2에서 프로세스 병목과 원인을, 질문 3에서 개선안과 기대 효과를 보고드리고 핵심 요약으로 마치겠습니다. "
             "각 타일을 클릭하면 해당 파트로 이동합니다.")
    return sl


# ------------------------------------------------------------------ S03 요약
def s03(doc, F):
    sl = doc.new_slide(3, "Part 00")
    chrome(sl, "[ 03 / EXECUTIVE SUMMARY ]", f"총 리드타임의 {F('wait_B_pct')}%는 작업이 아닌 대기 시간이다",
           source=f"대기 = 총 {F('lead_total')}h − 작업(현장 실작업 {F('field_work')}h + 정산 시스템 처리 {F('stl_total')}h) · 접수 구간은 전부 대기로 산정")
    banner = Card([label("THESIS · 통괄 가설"),
                   Txt([rich(f"수리 지연의 본질은 작업자 태만이 아니라 **공정 간 대기**와 **비실시간 접수의 소통 공백**이다. "
                             f"E2E 리드타임 {F('lead_total')}h 중 순수 대기가 {F('wait_B')}h.", 14, INK, accent=ACC)], name="thesis")],
                  pad=0.22, gap=0.08, name="banner")
    bh = banner.natural_h(CW)
    banner.draw(sl, MX, BODY_TOP + 0.05, CW, bh)
    y = BODY_TOP + 0.05 + bh + 0.2
    c1 = Card([label("STEP 01 · 데이터 진단", ACC), big(F("n_events"), "행", ACC, 44, name="n1"), body("전수 보존 · 임의 삭제 0건", 12, INK, name="s1"),
               Gap(0.04), bullets([f"결측 {F('n_null_rows')}행({F('null_rows_pct')}%)을 업무 순서로 복원",
                                   f"정상 접수 표본 {F('baseline_n')}케이스({F('baseline_pct')}%)로 대체 기준 확보",
                                   f"시간 역전 0건, 정상 접수 {F('n_valid')}건, 오접수 {F('n_wrongplace')}건"], 12)], pad=0.22, name="step1",
              foot=Txt([T("DETAIL → p.04–06", 9.5, True, MUTED, "m", balance=False)], structural=True, role="label"))
    c2 = Card([label("STEP 02 · 병목 규명", ORG), big(F("wait1"), "h", RED, 44, name="n2"), body(f"실사 방문 대기, 현장 시간의 {F('wait1_pct')}%", 12, INK, name="s2"),
               Gap(0.04), bullets([f"일 유입 {F('inflow_day')}건 vs 기사 CAPA {F('capa_day')}건 → 적체 피크 {F('wip_peak')}건",
                                   f"교차 인계 {F('n_handover')}건에서 접수 {F('handover_ratio')}배 지연",
                                   f"사내수리만 자재 대기 {F('wait2_intern')}h, 하자 재방문 +{F('rework_gap_mean')}h"], 12)], pad=0.22, name="step2",
              foot=Txt([T("DETAIL → p.07–15", 9.5, True, MUTED, "m", balance=False)], structural=True, role="label"))
    c3 = Card([label("STEP 03 · 개선 시나리오", GRN), big("▼" + F("eff_total_pct"), "%", GRN, 44, name="n3"), body(f"{F('lead_total')}h → {F('tobe_total')}h (실사 대기 20% 단축 가정)", 12, INK, name="s3"),
               Gap(0.04), bullets([f"Direct Booking 전략: 하나의 병목 줄을 두 갈래로",
                                   f"실사 줄 유입 {F('fast_pct')}% 감소",
                                   f"가정 단축률(실사 대기 20% 감소) 적용 시 −{F('eff_total')}h"], 12)], pad=0.22, name="step3",
              foot=Txt([T("DETAIL → p.16–18", 9.5, True, MUTED, "m", balance=False)], structural=True, role="label"))
    hh = row(sl, MX, y, CW, [c1, c2, c3], gutter=0.2, h=BODY_BOTTOM - 0.12 - y)
    assert_body(sl, y + hh)
    sl.notes(f"핵심 가설은 명확합니다. 수리가 늦어지는 것은 기사가 느려서가 아니라 공정 사이의 대기와 접수 단계의 비동기 소통 지연 때문입니다. "
             f"전체 {F('lead_total')}시간 중 {F('wait_B')}시간({F('wait_B_pct')}%)이 대기입니다. "
             f"[예상 질문] 90.5%의 정의는? → 작업을 현장 실작업({F('field_work')}h)과 정산 시스템 처리({F('stl_total')}h)로 보고 나머지를 대기로 산정했습니다. 현장 실작업만 작업으로 보면 대기 비중은 {F('wait_fieldwork_only_pct')}%입니다.")
    return sl


# ------------------------------------------------------------------ S04 진단
def s04(doc, F):
    sl = doc.new_slide(4, "Part 01")
    chrome(sl, "[ 04 / Q1 · BEFORE PROFILING ]", f"정상 결측은 보존, 비정상 결측 {F('n_null_rows')}행만 복원 대상",
           sub="결측치를 '정상 결측'과 '비정상 결측'으로 2원화하고, 복원 대상을 최소로 특정했다",
           source="출처: repair2.csv 프로파일링 (EDA-01) · 비정상 결측 20행 = 5개 속성 결측이 포함된 18개 케이스의 실제 행")
    top = 1.75
    img_w = 8.9
    chart = Card([cap("FIG.04", "원천 13개 속성 결측률 분포 (EDA-01)"),
                  Img(os.path.join(FIG, "EDA-01.png"), max_h=3.3, name="eda")], pad=0.14, gap=0.06, name="chart-card")
    ch = chart.natural_h(img_w)
    chart.draw(sl, MX, top, img_w, ch)
    rx, rw = MX + img_w + 0.2, CW - img_w - 0.2
    stats = [Card([label("RAW EVENTS"), big(F("n_events"), "행", INK, 28, name="a")], pad=0.2, gap=0.06, name="st1"),
             Card([label("CASES"), big(F("n_cases_all"), "건", INK, 28, name="b")], pad=0.2, gap=0.06, name="st2"),
             Card([label("ATTRIBUTES"), big(F("n_attrs"), "개", INK, 28, name="c")], pad=0.2, gap=0.06, name="st3")]
    stack(sl, rx, top, rw, stats, gutter=0.12, h_total=ch)
    y2 = top + ch + 0.15
    chips = [
        Card([label("정상 결측 · 보존", GRN), body(f"**{F('normal_missing_attrs')}개 속성 · {F('normal_missing_min')}~{F('normal_missing_max')}%**", 12.5, INK, accent=GRN),
              body("특정 이벤트에서만 기록되는 값", 11, INK2)], pad=0.2, gap=0.06, name="chip-n"),
        Card([label("비정상 결측 · 복원 대상", RED), body(f"**5개 속성 · {F('n_null_rows')}행({F('null_rows_pct')}%) · {F('n_null_cases')}케이스**", 12.5, INK, accent=RED),
              body("필수 속성이 빈 행만 정밀 복원", 11, INK2)], pad=0.2, gap=0.06, name="chip-e"),
        Card([label("결측률 분포 · 판별 기준", MUTED), body(f"**0.1~86.0% 사이 속성 {F('void_cols')}개**", 12.5, INK, accent=INK),
              body("결측률이 양극단이라 판별이 명확", 11, INK2)], pad=0.2, gap=0.06, name="chip-v"),
    ]
    hh = row(sl, MX, y2, CW, chips, gutter=0.2)
    assert_body(sl, y2 + hh)
    sl.notes(f"데이터를 열어 가장 먼저 확인한 것은 구조였습니다. 이 데이터는 공정마다 행이 쌓이는 이벤트 로그이고, 약 {F('normal_missing_min')}~{F('normal_missing_max')}%의 결측은 접수·실사·수리 완료 등 특정 이벤트에서만 기록되는 속성이라 구조적으로 비는 정상 결측입니다. "
             f"반면 필수 속성이 비어 있는 비정상 결측 행은 {F('n_events')}행 중 {F('n_null_rows')}행({F('n_null_cases')}개 케이스)뿐이어서 이 행만 복원 대상으로 특정했습니다. 0.1~86.0% 구간에는 속성이 하나도 없어 판별 기준이 명확합니다.")
    return sl


# ------------------------------------------------------------------ S05 CASE 1~5
def s05(doc, F):
    sl = doc.new_slide(5, "Part 01")
    chrome(sl, "[ 05 / Q1 · CASE 1–5 ]", "삭제 없이, 업무 순서로 결측과 오기입 교정 복원",
           sub=f"비정상 결측 {F('n_null_rows')}행에 더해 날짜 오기입 {F('date_miswritten')}행·더미 시각 {F('time_dummy')}행까지 5개 유형을 근거 기반으로 복원",
           source="출처: analysis.ipynb Cell 18·20·53·63·77·81")
    sl.text(SLIDE_W - MX - 7.0, BODY_TOP + 0.02, 7.0, [T("단위 · 행 = 이벤트 로그 1행 / 케이스 = 수리 요청 1건", 10, False, MUTED, "m", align="r", balance=False)],
            structural=True, name="unit-legend", role="label", max_lines=1)

    def tg(t, c=INK):
        return Txt([T(t, 10, True, c, "m", balance=False)], structural=True, role="label")

    def two(a, b):
        return [T(a, 12, True, INK, balance=False), T(b, 11, False, MUTED, balance=False)]

    rows_ = [
        [tg("CASE 1"), two("taskID", f"결측 {F('null_taskID')}행"),
         [T("contact 속성은 FirstContact에만 기록되는 고유 속성", 11.5, False, INK2)],
         [T("→ FirstContact · InformClientSurvey 복원", 11.5, True, GRN)]],
        [tg("CASE 2"), two("originator", f"결측 {F('null_originator')}행"),
         [T("같은 작업의 시작·완료 담당자 일치율 100%", 11.5, False, INK2)],
         [T("→ 짝 이벤트 담당자 승계 (Anne, Paul)", 11.5, True, GRN)]],
        [tg("CASE 3"), two("eventtype", f"결측 {F('null_eventtype')}행"),
         [T("기간 작업 1:1 페어 3행 + 마일스톤 단독 2행", 11.5, False, INK2)],
         [T("→ 짝 추적으로 5행 전수 복원", 11.5, True, GRN)]],
        [tg("CASE 4"), two("date", f"{F('date_total')}행 (결측 {F('date_missing')} + 오기입 {F('date_miswritten')})"),
         [T(f"시각이 정상인 {F('date_selected')}행에 선·후행 업무 순서 구간 제약을 적용", 11.5, False, INK2)],
         [T(f"→ 단일 후보 {F('date_single')}행 + 앵커 최근접 {F('date_nearest')}행 (1970년 통일)", 11.5, True, GRN)]],
        [tg("CASE 5"), two("time", f"{F('time_total')}행 (결측 {F('time_missing')} + 더미 {F('time_dummy')})"),
         [T(f"정상 접수 표본 {F('baseline_n')}케이스의 중앙값 {F('baseline_median_min')}분을 앵커로 역산", 11.5, False, INK2)],
         [T(f"→ 정상 자정 {F('time_midnight_kept')}행 보존 + 역산 추정 {F('time_estimated')}행", 11.5, True, GRN)]],
    ]
    tbl = Table([(0.9, "CASE", "l"), (3.0, "속성 · 규모", "l"), (4.3, "근거", "l"), (4.8, "복원", "l")], rows_, pad_y=0.04, name="cases")
    card = Card([tbl], pad=0.18, name="cases-card")
    ch = card.natural_h(CW)
    card.draw(sl, MX, BODY_TOP + 0.34, CW, ch)
    y = BODY_TOP + 0.34 + ch + 0.15
    badges = [
        Card([label("데이터 무손실", GRN), big(F("n_events"), "행", GRN, 36, name="b1"), body("임의 삭제 0건 · 전수 보존", 11, INK2)], pad=0.2, gap=0.06, name="bd1"),
        Card([label("시간 역전", GRN), big("0", "건", GRN, 36, name="b2"), body(f"작업 페어 {F('pairs_checked')}개 · 5개 검증 항목 위반 0", 11, INK2)], pad=0.2, gap=0.06, name="bd2"),
        Card([label("기준 표본", ACC), big(F("baseline_n"), "케이스", ACC, 36, name="b3"), body(f"전체의 {F('baseline_pct')}% · 중앙값 {F('baseline_median_min')}분", 11, INK2)], pad=0.2, gap=0.06, name="bd3"),
    ]
    hh = row(sl, MX, y, CW, badges, gutter=0.2)
    assert_body(sl, y + hh)
    sl.notes(f"복원 과정에서 단 한 행도 버리지 않았습니다. 시작·완료 담당자의 일치율 100%와 태스크 고유 속성을 근거로 CASE 1~3을 복원했고, 날짜는 시각이 정상인 {F('date_selected')}행에 순서 제약을 걸어 복원했습니다. "
             f"시각은 정상 접수 표본 {F('baseline_n')}케이스의 중앙값 {F('baseline_median_min')}분을 앵커로 역산했습니다. 그 결과 시간 역전이 0건인 데이터셋을 확보했습니다. "
             f"[예상 질문] 표본 수가 751건이 아닌가? → 현재 노트북(Cell 63) 재실행 기준 {F('baseline_n')}건(기준 케이스 {F('baseline_cases')}건)입니다.")
    return sl


# ------------------------------------------------------------------ S06 무결성·운영 특성
def s06(doc, F):
    sl = doc.new_slide(6, "Part 01")
    chrome(sl, "[ 06 / Q1 · AFTER PROFILING ]", "시간 역전 0건, 접수·현장 모두 단일 풀",
           source="출처: analysis.ipynb Cell 81·83, analysis.sql L760~828(배정비)·L1138~1202(24시간 접수), repair_cleaned.csv")

    def c(t, color=INK2, bold=False, size=11.5):
        return [T(t, size, bold, color, balance=False)]

    rows_ = [
        [c("총 이벤트 행"), c(f"{F('n_events')}행"), c(f"{F('n_events')}행 · 삭제 0건", GRN, True)],
        [c("필수 속성 결측 행"), c(f"{F('n_null_rows')}행 ({F('null_rows_pct')}%)"), c("0건 · 업무 순서 복원", GRN, True)],
        [c("일자 연도 오기입"), c(f"{F('date_miswritten')}행"), c("0건 · 1970년 통일", GRN, True)],
        [c("리드타임 정상 산출"), c(f"{F('lead_ok_before_pct')}% ({F('lead_ok_before_n')}/{F('n_cases_all')})"), c(f"100% ({F('n_cases_all')}/{F('n_cases_all')})", GRN, True)],
        [c("시간 왜곡·역전"), c(f"{F('lead_distort_before')}건 왜곡"), c(f"0건 · {F('pairs_checked')}개 페어 검증", GRN, True)],
    ]
    tbl = Table([(2.2, "검증 항목", "l"), (2.2, "BEFORE (원천)", "l"), (2.9, "AFTER (정제)", "l")], rows_, pad_y=0.1, name="ba")
    callout = Txt([rich(f"정상 접수 **{F('n_valid')}건** · 오접수 {F('n_wrongplace')}건({F('wrongplace_pct')}%)으로 구분", 12, GRN, accent=GRN, bold=True)], name="callout")
    checks = Txt([T(t, 11, False, INK2, balance=False) for t in [
        "① 케이스 내 모든 업무 쌍의 순서 위반 0건", "② 재작업 시작·완료 교대 위반 0건", "③ FirstContact가 케이스 최초가 아닌 행 0건",
        "④ TicketReady가 케이스 최종이 아닌 행 0건", "⑤ 소요시간 음수(complete < start) 0건"]], name="checks")
    left = Card([label("TABLE · 전처리 무결성 검증"), tbl, Gap(0.04), callout, Rule(), label(f"TEMPORAL INTEGRITY · 5개 항목 위반 0건 ({F('pairs_checked')} 페어)", GRN), checks],
                pad=0.2, gap=0.08, name="ba-card", min_h=5.0)
    lw_ = 6.5
    lh = left.natural_h(lw_)
    left.draw(sl, MX, BODY_TOP + 0.08, lw_, max(lh, 5.18))
    rx, rw = MX + lw_ + 0.2, CW - lw_ - 0.2
    c1 = Card([label("01 · 근무 형태", ACC), heading("24시간 상시 접수, 야간 방치 가설 기각", 14, INK, name="h1"),
               big(f"{F('intake_hours')}", "개 시간대", ACC, 36, name="n1"),
               body("접수 이벤트 0~23시 전 시간대에서 발생", 11.5, INK2),
               body("지연 원인은 영업 외 방치가 아닌 일정 조율 마찰", 11.5, INK2)],
              pad=0.2, gap=0.06, name="op1")
    c2 = Card([label("02 · 조직 구조", ORG), heading("지역 전담제 X, 단일 공유 풀", 14, INK, name="h2"),
               big(f"{F('dian_share')} : {F('monica_share')}", "%", RED, 36, name="n2"),
               body("정상 접수 케이스 접수 비중 (Dian : Monica)", 11.5, INK2),
               bullets([f"배정 현장 기사 고르게 분산 (접수원별 기사 출동 비율: 평균 {F('dian_share')}%)",
                        f"2회 이상 접수 주택 {F('recontact_houses')}채 중 {F('recontact_diff_pct')}%({F('recontact_diff')}채)는 초기 접수 담당자에게 비인계"], 11)],
              pad=0.2, gap=0.06, name="op2")
    stack(sl, rx, BODY_TOP + 0.08, rw, [c1, c2], gutter=0.14, h_total=5.18)
    sl.notes(f"전처리를 마친 결과, 행 손실 없이 시간 역전 0건인 {F('n_events')}행 데이터셋을 확보했습니다. 이 과정에서 수리회사의 운영 특성 두 가지가 드러났습니다. "
             f"첫째, 접수 이벤트가 24개 시간대 모두에서 발생해 야간 방치 가설은 기각됩니다. "
             f"둘째, 1회 접수 주택이 {F('houses_once_pct')}%라 지역 분담처럼 보이지만 재접수 {F('recontact_houses')}채 중 {F('recontact_diff')}채는 다른 상담원이 받았고, 현장 출동 케이스의 접수 담당 비중(Dian:Monica)도 {F('dian_share')}:{F('monica_share')}로 고르게 분산돼 접수와 현장 모두 구역 제한 없는 단일 풀입니다. "
             "이 환경을 바탕으로 질문 2의 기준 프로세스 모델로 넘어가겠습니다.")
    return sl


# ------------------------------------------------------------------ S07 AS-IS 프로세스
def s07(doc, F):
    sl = doc.new_slide(7, "Part 02")
    chrome(sl, "[ 07 / Q2-1 · AS-IS PROCESS ]", "수리 프로세스(E2E) 라인",
           source=f"※ 맵의 '+5.11h'는 채널 통제 OLS 계수, S09의 +{F('handover_penalty_h')}h는 단순 평균 차이 · 노드 EV = 이벤트 수")
    cw_ = CW
    chart = Card([cap("FIG.07", "E2E 기준 프로세스 맵 (접수 → 현장 → 정산) · 케이스 기준 927건"),
                  Img(os.path.join(FIG, "repair_process_map.png"), max_h=3.2, name="map")], pad=0.14, gap=0.06, name="map-card")
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, BODY_TOP + 0.05, cw_, ch)
    y = BODY_TOP + 0.05 + ch + 0.15
    chips = [
        Card([label("01 · 접수", ACC), Txt([rich(f"**{F('n_wrongplace')}건({F('wrongplace_pct')}%)** 오접수 격리", 11.5, INK2, accent=ACC),
                                           rich(f"→ 정상 접수 **{F('n_valid')}건**", 11.5, INK2, accent=ACC)], name="c1t")], pad=0.2, gap=0.06, name="c1"),
        Card([label("02 · 현장 · 단방향 에스컬레이션"), Txt([rich("**즉시 → 사내 → 외주**로만 인계되는 단방향", 11.5, INK2, accent=ACC),
                                                           rich(f"즉시→사내 {F('esc_imm_intern')} · 즉시→외주 {F('esc_imm_extern')} · 사내→외주 {F('esc_intern_extern')}", 11.5, INK2, accent=RED),
                                                           rich(f"총 {F('esc_total')}회 · **역행 {F('backflow_all')}건**", 11.5, INK2, accent=RED, align="c")], name="esc")], pad=0.2, gap=0.06, name="c2"),
        Card([label("03 · 정산", GRN), bullets(["수리 완료 후 **고객 통보·재무 전송** 병렬 시행",
                                                f"티켓 발행 = 병렬 종료 시각: **{F('ticket_match_n')}건({F('ticket_match_pct')}%)** 일치, {F('ticket_mismatch_n')}건은 {F('ticket_gap_min')}분 차이"], 11.5)], pad=0.2, gap=0.06, name="c3"),
    ]
    hh = row(sl, MX, y, CW, chips, weights=[0.8, 1.1, 1.1], gutter=0.2)
    assert_body(sl, y + hh)
    sl.notes(f"병목 분석 전에, 모든 분석의 기준선이 될 E2E 프로세스 모델입니다. 접수 단계에서 오접수 {F('n_wrongplace')}건이 조기 이탈하고 {F('n_valid')}건이 정상 접수가 됩니다. "
             f"현장은 단방향 에스컬레이션입니다. 즉시수리에서 사내수리로 {F('esc_imm_intern')}건, 즉시수리에서 외주로 {F('esc_imm_extern')}건, 사내수리에서 외주로 {F('esc_intern_extern')}건, 총 {F('esc_total')}회 인계되기만 하고 외주 이후 되돌아간 전이는 {F('backflow_all')}건입니다. 정산은 고객 통보 {F('settle_client_first')}건 : 재무 전송 {F('settle_fin_first')}건({F('settle_client_first_pct')}% : {F('settle_fin_first_pct')}%)으로 대칭 선행하는 병렬 구조이며, "
             f"고객 통보와 재무 전송은 병렬이고, 티켓 발행 시각은 늦게 끝난 쪽과 {F('n_valid')}건 중 {F('ticket_match_n')}건({F('ticket_match_pct')}%) 일치하며 나머지 {F('ticket_mismatch_n')}건은 {F('ticket_gap_min')}분 차이입니다. [근거 보강] 시각이 원본인 정상 표본 335건에서도 168:167로 대등합니다(노트북 Cell 75).")
    return sl


# ------------------------------------------------------------------ S08 거시 분해
def s08(doc, F):
    sl = doc.new_slide(8, "Part 02")
    chrome(sl, "[ 08 / Q2-2 · MACRO DECOMPOSITION ]", f"리드타임 {F('lead_total')}h의 {F('wait_B_pct')}%는 공정 간 대기",
           sub=f"대기 = {F('lead_total')}h − 작업({F('field_work')}h 현장 실작업 + {F('stl_total')}h 정산 처리) = {F('wait_B')}h · 현장 국면이 대기의 {F('field_wait_of_all_wait_pct')}%",
           source=f"출처: analysis.sql L1206~1395 · 접수 {F('rec_total')}h는 일정 조율 구간이 대부분이라 전부 대기로 산정(현장 실작업만 작업이면 {F('wait_fieldwork_only_pct')}%)")
    chart = Card([cap("FIG.08", "3대 국면별 실작업 vs 단순 대기 (정정본)"),
                  Img(os.path.join(DECK, "slide08_macro_leadtime_breakdown.png"), max_h=2.9, name="macro")], pad=0.14, gap=0.06, name="macro-card")
    cw_ = CW
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, BODY_TOP + 0.15, cw_, ch)
    y = BODY_TOP + 0.15 + ch + 0.15
    chips = [
        Card([label("01 · 접수", ACC), big(F("rec_total"), "h", ACC, 36, name="a"), body(f"일정 조율 구간. 교차 인계 시 {F('handover_ratio')}배 지연 (p.9)", 11, INK2)], pad=0.2, gap=0.06, name="c1"),
        Card([label("02 · 현장 국면 · 1위 병목", RED), big(F("wait1"), "h", RED, 36, name="b"), body(f"실사 방문 대기. 현장 시간의 {F('wait1_pct')}%를 독점", 11, INK2)], pad=0.2, gap=0.06, name="c2", line=RED),
        Card([label("03 · 수리 착수 대기", ORG), big(F("wait2_intern"), "h", RED, 36, name="c"), body(f"사내수리 {F('n_intern1')}건만 자재 대기, 즉시·외주는 {F('wait2_imm')}h", 11, INK2)], pad=0.2, gap=0.06, name="c3"),
    ]
    hh = row(sl, MX, y, CW, chips, gutter=0.2)
    assert_body(sl, y + hh)
    sl.notes(f"수리가 늦어지는 진짜 원인은 무엇일까요? 전체 {F('lead_total')}시간 중 작업은 {F('work_B')}시간에 불과하고 {F('wait_B')}시간({F('wait_B_pct')}%)이 공정 사이의 대기였습니다. "
             f"이 대기의 {F('field_wait_of_all_wait_pct')}%가 현장 국면에 있습니다. 3대 병목은 접수 일정 조율, 현장 실사 방문 대기({F('wait1')}h), 사내수리 자재 대기({F('wait2_intern')}h)입니다. "
             f"[예상 질문] 정산 {F('stl_total')}h를 왜 작업으로 보나? → 시스템 자동 처리 구간이라 보수적으로 작업으로 산정했고, 이를 대기로 보면 대기 비중은 더 커집니다.")
    return sl


# ------------------------------------------------------------------ S09 접수 병목
def s09(doc, F):
    sl = doc.new_slide(9, "Part 02")
    chrome(sl, "[ 09 / Q2-2 · BOTTLENECK 1 · RECEPTION ]", "접수 지연은 물량이 아닌 교차 인계 탓",
           sub=f"접수 소요시간 = 최초 접수 → 방문 일정 확정 · 15분 이내는 ≤15분 · 인계 효과 +{F('handover_penalty_h')}h(단순 차이), +{F('ols1_handover_b')}h(OLS)",
           source=f"출처: analysis.sql L863~1135 · hypothesis 노트북 Cell 9 (접수 OLS R²={F('ols1_r2')}, F={F('ols1_f')}, VIF 최대 {F('ols1_vif_max')})")
    chart = Card([cap("FIG.09", "접수 구간 3-Panel (인계 · 채널 · 15분 이내 평균)"),
                  Img(os.path.join(DECK, "slide09_reception_bottleneck_3panel.png"), max_h=2.75, name="rec")], pad=0.14, gap=0.06, name="rec-card")
    ch = chart.natural_h(CW)
    chart.draw(sl, MX, BODY_TOP + 0.15, CW, ch)
    y = BODY_TOP + 0.15 + ch + 0.15
    chips = [
        Card([label("핵심 원인 · 교차 인계"), big(F("handover_ratio"), "배", RED, 36, name="a"),
              body(f"단독 {F('n_single')}건 {F('single_h')}h → 인계 {F('n_handover')}건 {F('handover_h')}h. 인계는 전부 웹 {F('handover_web')} · 우편 {F('handover_letter')}", 11.5, INK2)],
             pad=0.2, gap=0.06, name="c1"),
        Card([label("이봉 분포 · 단기 지연이 아니다"),
              Txt([rich(f"웹·우편은 **15분 이내 단기 접수({F('async_fast_pct')}%)** 아니면 **60분 초과 장기 대기({F('async_slow_pct')}%)**로 일정이 확정된다. 15~60분 구간은 {F('async_mid_n')}건", 12, INK, accent=RED)], name="b1"),
              body(f"인계 {F('ho_slow_n')}건은 모두 60분 초과 (최소 {F('ho_min_min')}분)", 11.5, INK2)],
             pad=0.2, gap=0.06, name="c2"),
        Card([label("반전 · 웹은 느리지 않다"), big(F("fast_web_min"), "분", INK, 36, name="c"),
              body(f"빠른 건의 평균: 웹 {F('fast_web_min')}분 < 전화 {F('fast_phone_min')}분. 병목은 일정 조율 공백", 11.5, INK2)],
             pad=0.2, gap=0.06, name="c3"),
    ]
    hh = row(sl, MX, y, CW, chips, gutter=0.2)
    assert_body(sl, y + hh)
    sl.notes(f"접수 구간의 핵심은 이봉 분포입니다. 가운데 패널을 보면 전화·대면은 항상 15분 이내에 끝나지만, 웹·우편은 15분 이내 단기 접수({F('async_fast_pct')}%) 아니면 60분 초과 장기 대기({F('async_slow_pct')}%)로 갈리고(접수 소요시간은 최초 접수에서 방문 일정이 확정되기까지의 시간) 그 사이 15~60분 구간은 {F('async_mid_n')}건입니다. 즉 조금씩 늦어지는 것이 아니라 일정 조율이 막히는 순간 장기 지연으로 넘어갑니다. 교차 인계 {F('n_handover')}건은 전부 이 장기 대기 쪽에서, 웹·우편에서만 발생했습니다(물량과의 무관성은 다음 장에서 확인). "
             f"단독 처리 {F('n_single')}건은 평균 {F('single_h')}시간이지만 인계 {F('n_handover')}건은 {F('handover_h')}시간으로 {F('handover_ratio')}배입니다. 인계 {F('n_handover')}건은 전부 웹·우편에서만 발생했습니다. "
             f"그렇다고 웹이 느린 것은 아닙니다. 빠르게 끝난 건만 보면 웹이 {F('fast_web_min')}분으로 가장 빠르며, 문제는 일정 확정을 위한 비동기 조율 공백입니다. "
             "[예상 질문] 15분 이내 비율이 100%가 아닌 이유? → 15.0분 정각 건을 포함해 ≤15분으로 통일했습니다.")
    return sl


# ------------------------------------------------------------------ S10 접수 영향 요인① 상관 히트맵
def s10r(doc, F):
    sl = doc.new_slide(10, "Part 02")
    chrome(sl, "[ 10 / Q2-3 · RECEPTION DRIVERS ]", "접수 시간은 인계·채널과 연동, 물량과는 무관",
           sub="접수 국면 9개 변수의 피어슨 상관 — 방향을 보여주고, 다음 장의 OLS가 순수 효과를 분리한다",
           source=f"출처: hypothesis 노트북 Cell 7 (피어슨 r, N={F('n_valid')}) · 전 칸 재계산 일치 · 소요시간 = 최초 접수 → 방문 일정 확정(조율 완료)")
    top, H = BODY_TOP + 0.08, 5.15
    lw_ = 5.75
    heat = Card([cap("FIG.10", "접수 국면 9대 변수 상관 매트릭스"),
                 Img(os.path.join(FIG, "reception_detailed_correlation_heatmap.png"), max_h=H - 0.62, name="heat")], pad=0.14, gap=0.06, name="heat-card")
    heat.draw(sl, MX, top, lw_, H)
    rx, rw = MX + lw_ + 0.2, CW - lw_ - 0.2
    stats = [
        Card([label("교차 인계 ↔ 접수 시간", ORG), big(f"r = +{F('corr_rec_ho')}", "", RED, 24, name="a"),
              body(f"양(+)의 상관 — 인계 시 접수가 길어진다 (인계 {F('n_handover')}건)", 11, INK2)], pad=0.17, gap=0.06, name="s1"),
        Card([label("실시간 채널 ↔ 접수 시간", ACC), big("r = −" + F("corr_rec_rt").lstrip("-"), "", ACC, 24, keep=True, name="b"),
              body(f"전화·대면은 빠르고 웹·우편은 느리다", 11, INK2)], pad=0.17, gap=0.06, name="s2"),
        Card([label("일별 접수량 ↔ 접수 시간", MUTED), big(f"r = {F('corr_daily_rec')}", "", "94A3B8", 24, name="c"),
              body(f"물량 무관 — 현장 실사 대기와는 r = {F('corr_daily_visit')}", 11, INK2)], pad=0.17, gap=0.06, name="s3"),
    ]
    take = Card([label("READING", ACC), Txt([rich("상관은 방향만 보여준다. **채널과 인계가 서로 얽혀 있어** 순수 효과는 다음 장의 OLS로 분리한다.", 12.5, INK, accent=ACC)], name="rd")],
                pad=0.17, gap=0.06, name="read-card", line=ACC)
    th = take.natural_h(rw)
    stack(sl, rx, top, rw, stats, gutter=0.12, h_total=H - th - 0.14)
    take.draw(sl, rx, top + H - th, rw, th)
    assert_body(sl, top + H)
    sl.notes(f"접수 구간에 영향을 줄 만한 9개 변수의 상관관계입니다. 접수 소요시간과 가장 강하게 같이 움직이는 것은 교차 인계(r={F('corr_rec_ho')})와 실시간 채널 여부(r=−{F('corr_rec_rt').lstrip('-')})입니다. "
             f"반면 일별 접수량은 r={F('corr_daily_rec')}로 접수 시간과 무관하고, 오히려 현장 실사 대기와 r={F('corr_daily_visit')}의 약한 양의 상관을 보입니다. 접수량은 접수창구가 아니라 뒤의 현장 대기열에 영향을 준다는 뜻입니다. "
             "다만 상관은 변수 간 얽힘을 통제하지 못하므로, 다음 장에서 회귀분석으로 순수 효과를 분리합니다. "
             "[예상 질문] 상관이 인과인가? → 아닙니다. 그래서 OLS로 채널·인계·물량을 동시에 통제해 확인합니다.")
    return sl


# ------------------------------------------------------------------ S11 접수 영향 요인② 접수 단독 OLS
def s11r(doc, F):
    sl = doc.new_slide(11, "Part 02")
    chrome(sl, "[ 11 / Q2-3 · RECEPTION OLS ]", f"접수 지연은 인계 +{F('ols1_handover_b')}h·채널 +{F('ols1_async_b')}h가 설명한다",
           sub=f"접수 소요시간 OLS · R² {F('ols1_r2_pct')}% · F {F('ols1_f')} · N {F('n_valid')} · VIF 최대 {F('ols1_vif_max')}",
           source="출처: hypothesis 노트북 Cell 9 (statsmodels OLS, 재계산 일치) · 종속변수 receipt_hours · 채널 세분화는 전화 기준")
    top = BODY_TOP + 0.08
    cw_ = 8.55
    chart = Card([cap("FIG.11", "접수 단독 OLS 회귀계수와 95% 신뢰구간"),
                  Img(os.path.join(FIG, "reception_standalone_ols_coefficients.png"), max_h=3.75, name="ols")], pad=0.14, gap=0.06, name="rols-card")
    ch = chart.natural_h(cw_)
    chart.draw(sl, MX, top, cw_, ch)
    rx, rw = MX + cw_ + 0.2, CW - cw_ - 0.2
    cs = [Card([label("교차 인계 · 95% CI", ORG), big("+" + F("ols1_handover_b"), "h", RED, 24, name="a"), body(f"CI {F('ols1_ho_ci_lo')}~{F('ols1_ho_ci_hi')}h (p < 0.001)", 11, INK2)], pad=0.2, gap=0.06, name="k1"),
          Card([label("비실시간 채널 · 웹·우편", ACC), big("+" + F("ols1_async_b"), "h", ACC, 24, name="b"), body(f"웹 +{F('ols1b_web')}h · 우편 +{F('ols1b_letter')}h", 11, INK2)], pad=0.2, gap=0.06, name="k2"),
          Card([label("일별 접수량 · +1건당", MUTED), big("+" + F("ols1_daily_b"), "h", INK, 24, name="c"), body(f"p = {F('ols1_p_daily')} — 기각, 물량 무관", 11, INK2)], pad=0.2, gap=0.06, name="k3")]
    stack(sl, rx, top, rw, cs, gutter=0.12, h_total=ch)
    ty = top + ch + 0.15
    take = Card([Txt([rich(f"인계·채널이 접수 시간 변동의 **{F('ols1_r2_pct')}%**를 설명하고 물량은 기여하지 않는다 — 병목은 용량이 아니라 **소통 구조**다.", 12.5, INK, accent=ACC)], name="take")],
                pad=0.2, name="take-card")
    th_ = take.natural_h(CW)
    take.draw(sl, MX, ty, CW, th_)
    assert_body(sl, ty + th_)
    sl.notes(f"접수 소요시간을 종속변수로 채널, 인계, 일별 접수량을 동시에 넣은 회귀입니다. 교차 인계는 다른 조건이 같을 때 접수 시간을 +{F('ols1_handover_b')}시간(95% 신뢰구간 {F('ols1_ho_ci_lo')}~{F('ols1_ho_ci_hi')}) 늘리고, "
             f"비실시간 채널(웹·우편)은 +{F('ols1_async_b')}시간 늘립니다. 일별 접수량은 +1건당 {F('ols1_daily_b')}시간, p={F('ols1_p_daily')}로 유의하지 않습니다. 모형 설명력은 {F('ols1_r2_pct')}%이며 다중공선성은 VIF 최대 {F('ols1_vif_max')}로 문제 없습니다. "
             f"채널을 세분화하면 전화 대비 웹 +{F('ols1b_web')}시간, 우편 +{F('ols1b_letter')}시간이고 대면은 차이가 없습니다. "
             f"[예상 질문] 단순 평균 차이 +{F('handover_penalty_h')}h와 +{F('ols1_handover_b')}h가 다른 이유? → 후자는 채널과 물량을 통제한 순수 효과입니다.")
    return sl
