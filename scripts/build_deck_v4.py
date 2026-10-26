# -*- coding: utf-8 -*-
"""퍼즐데이터 과제 분석 보고서 — v4 (제출용 완성본: 본문 14장 + 부록 4장).

v3 를 읽고 찾은 약점에 대한 개선:
  1) S07: 글자가 작고 병목이 맵에 보이지 않던 프로세스 맵을 '구간별 대기시간 히트 + 케이스 수 굵기 + 인계·리워크 루프' 맵으로 재설계
  2) 접수 수치 정정: 일정 조율(ArrangeSurvey) 평균 2.01h(접수의 96%), 중앙값 4분 — 웹 4.5h·우편 3.6h 에 집중
  3) 부록 4장(원본 맵 · 지표 정의 · 전처리 규칙 · 가정·한계·후속 검증)으로 심사 질의 방어 근거 확보
  4) 제출용 메타데이터(버전 표기 제거), 본문 Q&A 종결 구조 유지
"""
import os

import deck_common as dc
from pptx.enum.dml import MSO_LINE

dc.EA_WORD_WRAP = True
dc.AUTO_BREAK = True
from deck_common import *  # noqa: E402,F401,F403

OUT = os.path.join(OUT_DIR, "puzzledata_repair_report_v4_final.pptx")
fig = lambda name: os.path.join(FIG_DIR, name)
fig2 = lambda name: os.path.join(FIG_DIR, "v2", name)

Y0, Y1 = 1.78, 6.88
prs = new_presentation()
cw3 = (CW - 2 * 0.25) / 3

PILL_BLUE = (BLU100, BLU800, BLU200)
PILL_ORG = (ORG100, ORG800, ORG200)
PILL_EMR = (EMR100, EMR800, EMR200)
PILL_RED = (RED50, RED700, RED200)
PILL_GRAY = (S100, S700, S300)


def bullets(items, size=11.5, color=S600, after=4.0):
    return [para(t, size, False, color, bullet=True, after=after) for t in items]


def section_card(s, x, y, w, h, pill, pill_style, title, title_color, items, *, line=S200, line_w=0.75,
                 fill=WHITE, bullet_size=11.5, tag=None, tag_color=BLU600, title_size=13.5, big=None,
                 big_color=S900, big_size=22, title_h=0.32, after=4.0):
    """pill + 제목 + (BigNum) + 불릿 + (하단 근거 태그) 로 구성된 표준 정보 카드."""
    add_card(s, x, y, w, h, fill, line, line_w)
    pf, pc, pl = pill_style
    add_pill(s, x + 0.2, y + 0.16, pill, pf, pc, pl, size=9.5)
    cy = y + 0.52
    add_text(s, x + 0.2, cy, w - 0.4, title_h, para(title, title_size, True, title_color))
    cy += title_h + 0.06
    if big:
        bh = big_size * 1.4 / 72 + 0.04
        add_text(s, x + 0.2, cy, w - 0.4, bh, para(big, big_size, True, big_color, mono=True))
        cy += bh + 0.08
    bottom = y + h - (0.42 if tag else 0.15)
    add_text(s, x + 0.2, cy, w - 0.4, bottom - cy, bullets(items, bullet_size, after=after))
    if tag:
        add_text(s, x + 0.2, y + h - 0.37, w - 0.4, 0.24, para(tag, 9.5, True, tag_color, mono=False))


# =================================================================== S01 표지
s = blank_slide(prs, 1, S50)
add_pill(s, 0.8, 0.95, "채용 과제 전형 최종 보고서", BLU50, BLU700, BLU200, size=11, h=0.32, padx=0.18)
add_text(s, 0.8, 1.45, 7.7, 2.3,
         para("프로세스 마이닝 기반\n공공임대주택 수리 프로세스\n진단 및 운영 최적화 방안", 38, True, S900, spacing=0.95),
         name="CoverTitle")
add_text(s, 0.8, 3.85, 7.4, 0.85,
         para("5대 무손실 전처리, 실사 대기 병목(76.8h) 원인 규명 및 3대 데이터 기반 TO-BE 전략", 17, False, S600),
         name="CoverSub")
# 리드타임 105.9h 구성 막대 (시각 앵커)
BX, BW_ = 0.8, 7.4
add_text(s, BX, 4.95, BW_, 0.28, para("E2E 리드타임 105.9h의 구성", 11, True, S600))
segs = [(4.57, BLU600), (5.51, EMR600), (95.79, RED600)]
tot = sum(v for v, _ in segs)
cx = BX
for i, (v, c) in enumerate(segs):
    wv = BW_ * v / tot
    add_box(s, cx, 5.28, wv - (0.03 if i < 2 else 0), 0.36, c, None, name=f"LeadBar-{i + 1}")
    cx += wv
add_text(s, BX, 5.74, BW_, 0.3,
         para([R("■ ", 11, True, BLU600), R("현장 실작업 4.6h   ", 10.5, False, S600),
               R("■ ", 11, True, EMR600), R("정산 시스템 처리 5.5h   ", 10.5, False, S600),
               R("■ ", 11, True, RED600), R("대기·조율 95.8h (90.5%)", 10.5, True, S800)]))
add_text(s, 0.8, 6.55, 7.6, 0.3,
         para("퍼즐데이터 수리 프로세스 데이터 분석 과제  |  제출일 2026. 10. 27", 11, False, S500), name="CoverMeta")
kpis = [
    ([R("13,262행", 34, True, BLU600, True)], S200, "전체 이벤트 로그 · 1,000 케이스 무손실 복원", "#ProcessMining", PILL_BLUE),
    ([R("90.5%", 34, True, ORG600, True)], ORG200, "리드타임(105.9h) 중 공정 간 대기·조율 시간", "#LeadTime_Wait", PILL_ORG),
    ([R("▼ ", 20, True, EMR600), R("64%", 34, True, EMR600, True)], EMR200,
     "TO-BE 1회 방문 패스트트랙 리드타임 감축 목표 (105.9h ➔ 38.0h)", "#TO-BE_ROI", PILL_EMR),
]
for i, (runs, bl, label, tag, ps) in enumerate(kpis):
    y = 0.95 + i * 1.98
    add_card(s, 8.85, y, 3.95, 1.78, WHITE, bl, 1.0, 0.14, f"KPI-{i + 1}")
    add_text(s, 9.15, y + 0.16, 3.4, 0.62, para(runs))
    add_text(s, 9.15, y + 0.84, 3.4, 0.5, para(label, 11.5, False, S600))
    add_pill(s, 9.15, y + 1.38, tag, ps[0], ps[1], ps[2], size=9.5, mono=True)
set_notes(s, "안녕하십니까, 퍼즐데이터 수리 프로세스 데이터 분석 결과 발표를 맡은 지원자입니다. 본 보고서는 네덜란드 공공임대주택 1,000건의 수리 로그를 바탕으로, 단순 통계를 넘어 프로세스 마이닝 관점에서 대기시간 약 90%의 구조적 원인을 밝히고 실질적 개선안을 제시합니다.\n\n[수치 메모] 90.5% = (105.9h − 현장 실작업 4.6h − 정산 시스템 처리 5.5h) ÷ 105.9h. 접수 구간(2.1h)은 대부분 일정 조율(1.9h)이므로 대기·조율에 포함했고, 정산 5.5h는 시스템 자동 처리로 보아 제외한 산정입니다. start→complete 구간만 작업으로 보는 엄격 정의에서는 94.6%이므로 어느 정의로도 '대기가 압도적'이라는 결론은 같습니다. ▼64%는 목표치(가정 기반)이며 검증된 하한은 −17.2h(−16%)입니다.")

# =================================================================== S02 목차
s = blank_slide(prs, 2)
add_chrome(s, 2, "AGENDA · 전체 개요", "원천 데이터 전처리부터 TO-BE 전략까지, 4개 파트로 보고합니다",
           "슬라이드 구성: 질문 1 (04–06) · 질문 2 (07–11) · 질문 3 (12–13) · 질의응답 (14) · 부록 (A-1~A-4)")
tiles = [
    ("01", S300, "질문 1", PILL_BLUE, "데이터 진단 및 전처리", "04–06",
     ["13,262행 이벤트 로그 수사 프로파일링", "도메인 인과 기반 5대 결측치 100% 무손실 복원", "시간 역전 0건 입증 및 927건 코호트 확립"],
     "927건", S900, "분석 코호트 · 시간 역전 0건"),
    ("02", ORG300, "질문 2", PILL_ORG, "프로세스 마이닝 심층 분석", "07–11",
     ["AS-IS E2E 프로세스 표준 모델 (맵)", "3대 대기 병목 분해 (접수 6.6배 vs 현장 76.8h)", "OLS 영향인자 실증 & 수리·리워크"],
     "90.5%", ORG600, "리드타임 중 대기·조율"),
    ("03", EMR400, "질문 3", PILL_EMR, "프로세스 최적화 방안", "12–13",
     ["사전 분류 정합 83~87%와 정보 해상도 한계 규명", "E형 직행 ➔ 실사 대기 20%(-15.4h) 단축", "체크리스트 고도화 & E형 정밀검사로 리워크 차단"],
     "-17.2h", EMR600, "검증된 TO-BE 하한"),
    ("04", S300, "Q & A", PILL_GRAY, "질의응답 (Q&A)", "14",
     ["프로젝트 핵심 진단 및 3대 전략 총괄", "데이터 기반 프로세스 혁신 총평", "질의응답"],
     "Q & A", S700, "자유 질의"),
]
tw, tg = 2.88, (CW - 4 * 2.88) / 3
TILE_LINKS = []                       # (slide, x, y, w, h, 목적 슬라이드 번호) — 모든 슬라이드를 만든 뒤 점프 링크를 건다
for i, (idx, ic, pl, ps, title, rng, bl, big, bigc, cap) in enumerate(tiles):
    x = MX + i * (tw + tg)
    TILE_LINKS.append((s, x, 1.85, tw, 4.9, [4, 7, 12, 14][i]))
    add_card(s, x, 1.85, tw, 4.9, WHITE, S200, 0.75, 0.14, f"Tile-{idx}")
    add_text(s, x + 0.25, 2.0, 1.4, 0.7, para(idx, 40, True, ic, mono=True))
    add_text(s, x + tw - 1.25, 2.12, 1.0, 0.25, para("Slide " + rng, 9.5, True, S500, mono=True, align="r"))
    add_pill(s, x + 0.25, 2.85, pl, ps[0], ps[1], ps[2], size=10)
    add_text(s, x + 0.25, 3.25, tw - 0.5, 0.75, para(title, 17, True, S900, spacing=0.95))
    add_text(s, x + 0.25, 4.0, tw - 0.5, 1.65, bullets(bl, 11.5, after=5))
    add_text(s, x + 0.25, 5.72, tw - 0.5, 0.5, para(big, 24, True, bigc, mono=True))
    add_text(s, x + 0.25, 6.22, tw - 0.5, 0.3, para(cap, 10, False, S500))
set_notes(s, "오늘 발표는 4개 파트로 진행됩니다. 질문 1의 데이터 무손실 전처리를 거쳐, 질문 2의 프로세스 병목과 원인을 규명하고, 질문 3에서 실질적 개선안과 정량적 효과를 제시하며 마무리하겠습니다.")

# =================================================================== S03 Executive Summary
s = blank_slide(prs, 3)
add_chrome(s, 3, "EXECUTIVE SUMMARY · 통괄 핵심 어젠다",
           "현장의 '대기시간'을 줄이고 이해관계자 간 '소통'을 통제하면 프로세스 리드타임을 획기적으로 개선할 수 있다",
           "※ 90.5% = (E2E − 현장 실작업 − 정산 시스템 처리) ÷ E2E, 엄격 정의(start→complete만 작업) 시 94.6% · 근거: analysis.sql 2~5절")
add_box(s, MX, 1.85, CW, 1.0, S900, None, radius=0.12, name="InsightBanner")
add_text(s, MX + 0.35, 1.85, 7.7, 1.0,
         para("공정 리드타임 지연의 본질은 작업자 태만이 아닌 '공정 간 대기·조율(90.5%)'과 '비실시간 접수 소통 공백'에 있다",
              14.5, True, WHITE, spacing=0.95), anchor="m")
add_text(s, MX + 8.5, 1.85, 3.5, 1.0,
         [para("E2E 리드타임 105.9시간 중", 11.5, False, S300),
          para("대기·조율 95.8시간", 20, True, ORG300, mono=True)], anchor="m")
cards3 = [
    ("Step 01", (S900, WHITE, None), "데이터 무결성", "13,262행", S900, "100% 무손실 복원 완결", S200,
     ["임의 행 삭제 0건 (13,262행 전수 보존)", "비정상 시스템 에러 20행(0.15%) 인과 복원", "접수 구간 정상 표본 751건(75.1%)으로 모수 확장"]),
    ("Step 02", (ORG600, WHITE, None), "병목 실증", "대기 90.5%", ORG600, "현장 국면에 대기의 약 98% 편중", ORG200,
     ["실사 방문 대기(76.8h)가 현장 시간의 78.2% 독점", "일 유입 134건 vs 기사 CAPA 68건 ➔ 403건 적체", "비실시간 채널 인계(123건) 발생 시 6.6배 지연"]),
    ("Step 03", (EMR600, WHITE, None), "TO-BE 솔루션", "소통 통제", EMR600, "+ 대기시간 원천 소멸", EMR200,
     ["사전 분류 정합(83~87%)을 활용해 헛걸음 실사 우회", "E형만 직행해도 실사 대기 20%(-15.4h) ➔ 리드타임 -17.2h", "E-1/E-2(리워크 84.6%) 정밀검사로 10일 루프 차단"]),
]
for i, (step, sp, tag, big, bc, sub, bl, items) in enumerate(cards3):
    x = MX + i * (cw3 + 0.25)
    add_card(s, x, 3.1, cw3, 3.75, WHITE, bl, 1.0, 0.14, f"Summary-{i + 1}")
    w1 = add_pill(s, x + 0.25, 3.3, step, sp[0], sp[1], sp[2], size=9.5)
    add_pill(s, x + 0.25 + w1 + 0.1, 3.3, tag, S100, S700, S200, size=9.5)
    add_text(s, x + 0.25, 3.7, cw3 - 0.5, 0.6, para(big, 30, True, bc, mono=True))
    add_text(s, x + 0.25, 4.35, cw3 - 0.5, 0.3, para(sub, 13, True, S700))
    add_text(s, x + 0.25, 4.82, cw3 - 0.5, 1.95, bullets(items, 13, after=7))
set_notes(s, "본 분석을 관통하는 핵심 가설은 명확합니다. 수리가 늦어지는 것은 현장 기사가 느려서가 아니라, 공정 사이의 대기·조율 시간과 접수 단계의 비동기 소통 지연 때문입니다. 이 두 가지를 통제하여 전체 프로세스를 획기적으로 개선하는 여정을 보여드리겠습니다.\n\n[예상 질문] '대기·조율 90.5%'를 어떻게 정의했나? → E2E 105.9h에서 현장 실작업 4.6h와 정산 시스템 처리 5.5h를 뺀 시간입니다. 정산을 작업으로 보지 않고 start→complete 구간만 작업으로 보면 94.6%이므로, 90.5%는 보수적인 값입니다.")

# =================================================================== S04 원천 프로파일링
s = blank_slide(prs, 4)
add_chrome(s, 4, "Part 01 · 질문 1 | Before Profiling",
           "정상 결측은 그대로 보존하고, 시스템 에러 20행(0.15%)만 수사 타겟으로 특정했다",
           "출처: repair2.csv 원천 프로파일링 (EDA-01) · 20행 = 5개 속성 결측이 포함된 18개 케이스의 실제 행")
add_card(s, MX, 1.85, 3.7, 4.95, WHITE, S200, 0.75, 0.14, "ProfileCard")
add_text(s, MX + 0.25, 2.05, 3.2, 0.25, para("원천 데이터셋 프로파일", 10.5, True, S500))
for i, (big, lab) in enumerate([("13,262", "원천 이벤트 행"), ("1,000", "총 관리 케이스"), ("13개", "전체 속성 수")]):
    y = 2.4 + i * 1.08
    add_text(s, MX + 0.25, y, 3.2, 0.66, para(big, 36, True, S900, mono=True))
    add_text(s, MX + 0.25, y + 0.64, 3.2, 0.3, para(lab, 12, False, S500))
add_box(s, MX + 0.2, 5.7, 3.3, 0.98, S50, S200, 0.75, 0.1, "ProfileCallout")
add_text(s, MX + 0.35, 5.7, 3.0, 0.98,
         para("1건 1행의 정형 데이터가 아닌 세부 공정 단위로 기록되는 이벤트 로그(Event Log)의 특성 반영 필수", 10.5, False, S600),
         anchor="m")
RX, RW = 4.5, SLIDE_W - MX - 4.5
add_card(s, RX, 1.85, RW, 3.25, WHITE, S200, 0.75, 0.12, "EDA01Frame")
add_picture_contain(s, fig2("s04_missing_profile.png"), RX + 0.05, 1.88, RW - 0.1, 3.2, pad=0.0,
                    alt="속성별 결측률: 정상 결측 7개 속성 86~93%, 비정상 결측 5개 속성 0.015~0.098%, 중간 구간 컬럼 0개")
rows4 = [
    (EMR50, EMR200, "정상 결측 (무죄)", PILL_EMR, "구조적 Null 86.0~93.0% · 7개 속성 (12,335행)",
     "후속 공정이 없어 비어 있는 값 ➔ 임의 대체 없이 100% 보존", S600),
    (RED50, RED200, "비정상 결측 (유죄)", PILL_RED, "시스템 에러 0.015~0.098% · 5개 속성 (20행)",
     "필수 값 누락 ➔ 18개 케이스, 단 20행만 정밀 복원 타겟", RED600),
    (S50, S200, "진공 구간", PILL_GRAY, "0.1% ~ 86.0% 구간 컬럼 0개",
     "완벽한 양극단 이봉분포 ➔ 정상/비정상 판별의 객관성 입증", S600),
]
for i, (bg, bl, pill, ps, main, side, sc) in enumerate(rows4):
    y = 5.2 + i * 0.56
    add_box(s, RX, y, RW, 0.5, bg, bl, 0.75, 0.1, f"Verdict-{i + 1}")
    add_pill(s, RX + 0.12, y + 0.115, pill, ps[0], ps[1], ps[2], size=9.5, min_w=1.62)
    add_text(s, RX + 1.9, y, 3.35, 0.5, para(main, 10.5, True, S800), anchor="m")
    add_text(s, RX + 5.4, y, RW - 5.5, 0.5, para(side, 10, sc == RED600, sc), anchor="m")
set_notes(s, "데이터를 열어보았을 때 가장 먼저 확인한 것은 구조였습니다. 본 데이터는 공정마다 행이 쌓이는 이벤트 로그로, 90% 안팎의 결측치는 후속 수리가 발생하지 않아 생긴 자연스러운 정상 결측입니다. 반면 필수 속성임에도 비어 있는 값은 13,262행 중 단 20행에 불과했습니다. 이 20행만을 정밀 복원 타겟으로 특정했습니다.\n\n[예상 질문] 왜 결측을 일괄 대체하지 않았나? → 86~93% 결측은 '후속 공정이 없어서' 생기는 구조적 값이라 채우면 오히려 왜곡입니다. 0.1%~86% 사이에 컬럼이 하나도 없는 양극단 분포라 정상/비정상 구분 기준이 자의적이지 않다는 점이 근거입니다.")

# =================================================================== S05 CASE 1~5
s = blank_slide(prs, 5)
add_chrome(s, 5, "Part 01 · 질문 1 | CASE 1 ~ 5 도메인 인과 복원",
           "행 삭제나 단순 대체 없이, 업무 인과 근거로 결측 20행과 오기입·더미 일시까지 100% 무손실 복원했다",
           "출처: analysis.ipynb Cell 18·20·51·53·77·81, analysis.sql · CASE 4·5의 건수에는 결측 행(각 13건)이 포함됨")
cases = [
    ("CASE 1", "taskID", "2", "결측", False, "contact 속성은 FirstContact에만 기록되는 고유 도메인 속성 (Cell 18)",
     "FirstContact / InformClientSurvey 확정 복원"),
    ("CASE 2", "originator", "2", "결측", False, "동일 작업의 시작(start)-완료(complete) 담당자 100.0% 일치 규칙 (Cell 18)",
     "짝 이벤트 담당자(Anne, Paul) 상호 승계"),
    ("CASE 3", "eventtype", "5", "결측", False, "기간 작업 1:1 페어(start→complete 추적) 및 마일스톤 단독 발생 (Cell 20)",
     "1:1 페어 3건 + 마일스톤 2건 100% 복원"),
    ("CASE 4", "date", "879", "결측 13 + 오기입 866", True, "시각 정상 859건 선별, 선·후행 업무 순서 구간 제약(Interval Bounds) 적용 (Cell 51·53)",
     "단일 후보 640건 + 앵커 최근접 219건 매핑 (1970년 통일)"),
    ("CASE 5", "time", "28", "결측 13 + 더미 15", True, "표본 34% 한계 극복 ➔ 접수 정상 표본 751건(75.1%) 확보, 중앙값 4.0분 (Cell 77·81)",
     "정상 자정 7건 보존 + 기준 앵커 역산 21건 (역전 0건)"),
]
for i, (tag, attr, n, amt, hot, clue, fix) in enumerate(cases):
    y = 1.85 + i * 0.83
    add_card(s, MX, y, CW, 0.76, WHITE, S200, 0.75, 0.1, f"Case-{i + 1}")
    nc = ORG600 if hot else S900
    add_text(s, MX + 0.15, y, 1.0, 0.76,
             para([R(n, 22, True, nc, True), R("건", 10.5, True, nc)], align="c"), anchor="m")
    ps = PILL_ORG if hot else PILL_GRAY
    add_pill(s, MX + 1.3, y + 0.1, tag, ps[0], ps[1], ps[2], size=9.5)
    add_text(s, MX + 2.3, y + 0.08, 1.5, 0.3, para(attr, 12.5, True, S900), anchor="m")
    add_text(s, MX + 1.3, y + 0.43, 2.5, 0.28, para(amt, 10, True, ORG700 if hot else S600))
    add_text(s, MX + 3.95, y, 4.2, 0.76, para(clue, 10.5, False, S600), anchor="m")
    add_text(s, MX + 8.35, y, 3.75, 0.76,
             para([R("➔ ", 10.5, True, EMR600), R(fix, 10.5, True, EMR700)]), anchor="m")
for i, (t, d) in enumerate([("데이터 무손실", "임의 삭제 0건 · 13,262행 100% 완전 보존"),
                            ("통계적 강건성", "표본 34% 축소 극복 ➔ 751건(75.1%) 모수 확보"),
                            ("인과 무결성", "시간 역전 0건 달성 · 927건 정상 코호트 확립")]):
    x = MX + i * (cw3 + 0.25)
    add_box(s, x, 6.08, cw3, 0.76, EMR50, EMR200, 0.75, 0.1, f"Badge-{i + 1}")
    add_text(s, x + 0.2, 6.08, cw3 - 0.4, 0.76,
             [para("✓ " + t, 12, True, EMR700), para(d, 10.5, False, S600)], anchor="m")
set_notes(s, "복원 시 단 한 행도 버리지 않았습니다. 시작-완료 담당자의 100% 일치성, 태스크 고유 속성을 활용했고, 일시는 표본 34% 축소 한계를 극복하여 확보한 751건 정상 모수의 대표값을 앵커로부터 역산 적용했습니다. 덕분에 시간 역전 0건의 완벽한 데이터셋을 완성했습니다.\n\n[수치 메모] '결측 20행'은 5개 속성에서 값이 비어 있던 실제 행 수이고, CASE 4의 오기입 866건(미래·1905년 연도)과 CASE 5의 더미 시각 15건은 값은 있으나 이상치인 별도 유형입니다.")

# =================================================================== S06 After profiling
s = blank_slide(prs, 6)
add_chrome(s, 6, "Part 01 · 질문 1 | After Profiling",
           "시간 역전 0건을 입증했고, 오접수 73건을 격리해 927건 클린 코호트를 확립했다",
           "출처: repair_cleaned.csv (13,262행) 직접 집계 · 정상 코호트 = RepairReady 927건 전수")
LW = 6.0
add_card(s, MX, 1.85, LW, 5.0, WHITE, S200, 0.75, 0.14, "VerifyCard")
add_text(s, MX + 0.25, 2.02, LW - 0.5, 0.3, para("Before vs After 데이터 무결성 검증표", 14, True, S900))
H = lambda t, c=S700: dict(text=t, size=11, bold=True, color=c, fill=S100, border=S200)
B = lambda t, c=S600, b=False: dict(text=t, size=11.5, bold=b, color=c)
tbl = [
    [H("검증 항목"), H("Before (원천)"), H("After (정제 무결성)", EMR700)],
    [B("총 이벤트 행 수", S900, True), B("13,262행"), B("13,262행 (100% 완전 보존)", EMR700, True)],
    [B("필수 속성 결측", S900, True), B("20건 (0.15%)", RED600), B("0건 (100% 인과 복원 완료)", EMR700, True)],
    [B("일자 연도 오기입", S900, True), B("866건 (미래연도)", RED600), B("0건 (1970년 통일)", EMR700, True)],
    [B("공정 간 시간 역전", S900, True), B("음수 시간 존재", RED600), B("0건 (3,711 페어 검증)", EMR700, True)],
]
add_table(s, MX + 0.25, 2.5, [1.6, 1.55, 2.35], [0.44, 0.68, 0.68, 0.68, 0.68], tbl, "IntegrityTable")
add_box(s, MX + 0.25, 5.9, 5.5, 0.7, EMR50, EMR200, 0.75, 0.1, "IntegrityBanner")
add_text(s, MX + 0.25, 5.9, 5.5, 0.7, para("전처리 전 구간 무결성 100% 입증 ➔ 임의 행 삭제 0건", 12.5, True, EMR800, align="c"),
         anchor="m")
RX, RW = 6.8, SLIDE_W - MX - 6.8
cw4 = (RW - 3 * 0.13) / 4
for i, (v, l) in enumerate([("1,000", "케이스"), ("890", "고유 주택"), ("13개", "전체 속성"), ("14행", "케이스 중앙값")]):
    x = RX + i * (cw4 + 0.13)
    add_card(s, x, 1.85, cw4, 0.8, S50, S200, 0.75, 0.1, f"Chip-{i + 1}")
    add_text(s, x, 1.93, cw4, 0.4, para(v, 15, True, S900, mono=True, align="c"))
    add_text(s, x, 2.3, cw4, 0.25, para(l, 10, False, S500, align="c"))
hw = (RW - 0.14) / 2
add_card(s, RX, 2.82, hw, 1.95, EMR50, EMR500, 2.0, 0.12, "CleanCohort")
add_pill(s, RX + 0.18, 2.98, "정상 수리 완결 코호트", EMR100, EMR800, EMR200, size=9.5)
add_text(s, RX + 0.18, 3.32, hw - 0.36, 0.55,
         para([R("927건", 28, True, EMR700, mono=True), R(" (92.7%)", 13, True, EMR700, mono=True)]))
add_text(s, RX + 0.18, 3.95, hw - 0.36, 0.75, para("순수 현장수리 분석 대상 ➔ 질문 2 마이닝 모수 확립", 11, False, S600))
add_card(s, RX + hw + 0.14, 2.82, hw, 1.95, S50, S300, 0.75, 0.12, "NoiseCohort")
add_pill(s, RX + hw + 0.32, 2.98, "오접수 조기 종결", S100, S700, S300, size=9.5)
add_text(s, RX + hw + 0.32, 3.32, hw - 0.36, 0.55,
         para([R("73건", 28, True, S500, mono=True), R(" (7.3%)", 13, True, S500, mono=True)]))
add_text(s, RX + hw + 0.32, 3.95, hw - 0.36, 0.75,
         para("타 기관 관할 주택(InformClientWrongPlace) ➔ 분석 노이즈 격리", 11, False, S600))
add_text(s, RX, 4.95, RW, 0.28, para("927건 코호트의 접수 채널 분포 (실측)", 12, True, S800))
for i, (n, v) in enumerate([("Phone", "251건 (27.1%)"), ("Web", "241건 (26.0%)"), ("Personal", "228건 (24.6%)"),
                            ("Letter", "207건 (22.3%)")]):
    x = RX + i * (cw4 + 0.13)
    add_card(s, x, 5.28, cw4, 0.85, S50, S200, 0.75, 0.1, f"Channel-{n}")
    add_text(s, x, 5.34, cw4, 0.3, para(n, 12, True, S900, align="c"))
    add_text(s, x, 5.68, cw4, 0.3, para(v, 10, False, S600, align="c"))
add_text(s, RX, 6.25, RW, 0.3, para("특정 채널 편향 없이 고르게 유입됨을 확인 (단일 채널 쏠림 가설 기각)", 10.5, False, S500))
set_notes(s, "5대 전처리를 완료한 결과, 단 한 건의 결측과 시간 역전도 없는 완전무결한 13,262행 정제 데이터셋이 완성되었습니다. 정제된 데이터를 프로파일링하여 타 기관 관할 오접수 73건을 격리하고, 실제 현장 수리가 이루어진 '927건의 클린 분석 코호트'를 확립했습니다. 이제 질문 2, 대기가 집중된 현장의 진짜 병목을 파헤치겠습니다.\n\n[예상 질문] 오접수 73건을 왜 제외했나? → 타 기관 관할 주택(InformClientWrongPlace)이라 접수 직후 종결되어 현장·정산 공정이 존재하지 않습니다. 포함하면 리드타임 분포가 왜곡되므로 927건을 분석 코호트로 확정했습니다. 927건의 채널 분포(27/26/25/22%)가 고르다는 점도 확인했습니다.")

# =================================================================== S07 AS-IS 프로세스 모델
s = blank_slide(prs, 7)
add_chrome(s, 7, "Part 02 · 질문 2-1 | AS-IS 기준 프로세스 모델",
           "E2E 기준 프로세스는 단방향·병렬 구조이며, 접수→실사 구간의 대기(평균 76.8h)가 가장 굵은 병목이다",
           "출처: repair_cleaned.csv · case_pivot_table.csv (927건 코호트) · 화살표 굵기 = 1차 수리 케이스 수, 색 = 평균 대기시간")
add_card(s, MX, Y0, CW, 3.58, S50, S200, 0.75, 0.14, "ProcessMapFrame")
add_picture_contain(s, fig2("s07_process_map_wait.png"), MX, Y0, CW, 3.58, pad=0.05,
                    alt="E2E 프로세스 맵: 접수→실사 평균 76.8h(중앙값 48.8h) 대기가 가장 굵은 병목, 사내수리 착수 30.5h, 교차 인계 123건, 리워크 26건")
cards7 = [
    ("01 접수", PILL_BLUE, "오접수 격리 & 시스템 앵커",
     ["FirstContact 1,000건 중 73건(7.3%)을 타 기관 관할로 조기 격리", "InformClientSurvey 0초 자동 발송 ➔ 접수 종료 앵커, 기준선 RepairReady 927건"]),
    ("02 현장", PILL_ORG, "단방향 · 역류 0건 앵커",
     ["즉시 ➔ 사내 ➔ 외주로만 전이, 외주 이관 후 사내 역류 0건(0.0%)", "수리 완료 커밋 시 RepairReady(927건) 자동 발행 ➔ 즉시 정산 이관"]),
    ("03 정산", PILL_EMR, "대칭 병렬 AND-Join",
     ["고객 통보 선행 50.6%(469건) vs 재무 전송 선행 49.2%(456건) = 대칭 병렬", "TicketReady는 후행 완료 시각과 99.8%(925건) 일치, 대기 0.0h"]),
]
for i, (pill, ps, title, items) in enumerate(cards7):
    x = MX + i * (cw3 + 0.25)
    y7, h7 = 5.46, 1.42
    add_card(s, x, y7, cw3, h7, WHITE, S200, 0.75, 0.12, f"PhaseCard-{i + 1}")
    wp = add_pill(s, x + 0.2, y7 + 0.14, pill, ps[0], ps[1], ps[2], size=9.5)
    add_text(s, x + 0.2 + wp + 0.12, y7 + 0.1, cw3 - 0.4 - wp - 0.12, 0.34, para(title, 12.5, True, S900), anchor="m")
    add_text(s, x + 0.2, y7 + 0.54, cw3 - 0.4, h7 - 0.6, bullets(items, 10.5, after=3))
set_notes(s, "상세 병목 분석에 앞서, 모든 분석의 기준선이 될 'E2E 기준 프로세스 모델'입니다. 이 모델은 데이터의 3가지 명확한 실측 근거를 바탕으로 도출되었습니다.\n첫째, 접수 단계는 1,000건 중 관할 외 73건의 조기 이탈과 시스템 자동 알림 앵커로 경계가 확립되었습니다.\n둘째, 현장 수리 흐름은 철저한 단방향 에스컬레이션입니다. 사내 기사는 물론 외주 기사 역시 수리를 마친 뒤 완료 커밋을 하면 시스템이 RepairReady를 발송합니다. 외주로 넘어간 후 사내로 되돌아온 역류 케이스는 단 0건입니다.\n셋째, 정산 공정은 고객 통보와 재무 처리가 50.6% 대 49.2%로 대칭 선행하는 병렬 구조이며, 최종 티켓 마감은 늦게 끝난 시각과 99.8% 일치하여 0초에 자동 종결됩니다.\n이처럼 검증된 기준 지도를 토대로, 다음 장부터 90.5%의 대기·조율 시간이 어디서 발생하는지 거시적 분해로 들어가겠습니다. [읽는 법] 화살표 굵기는 1차 수리 케이스 수, 색은 평균 대기시간입니다. 가장 굵은 빨간 화살표가 접수에서 실사까지의 76.8시간(중앙값 48.8시간)이고, 사내수리 착수 30.5시간이 그다음입니다.\n\n[예상 질문] 이 지도에서 재작업(루프)은 어디인가? → 현장 국면의 InternRepair 노드(547 EV / 508 케이스)가 케이스당 복수 발생하는 곳입니다. 사내수리 반복 39회, 하자 재방문(사내→사내) 26건은 슬라이드 11에서 다룹니다. 교차 인계 123건(건당 +5.11h)은 접수 국면 MakeTicket 노드에서 발생합니다.")

# =================================================================== S08 거시 리드타임 분해
s = blank_slide(prs, 8)
add_chrome(s, 8, "Part 02 · 질문 2-2 | 거시 리드타임 분해",
           "리드타임 105.9시간의 90.5%는 공정 간 대기·조율이며, 그중 97.8%가 현장 국면에 집중된다",
           "출처: analysis.sql 2절 · 대기·조율 = E2E − 현장 실작업 4.6h − 정산 시스템 처리 5.5h (엄격 정의: start→complete만 작업 시 94.6%)")
add_card(s, MX, Y0, 7.5, 2.62, WHITE, S200, 0.75, 0.14, "LeadtimeChartFrame")
add_picture_contain(s, fig2("s08_leadtime_breakdown.png"), MX, Y0, 7.5, 2.62, pad=0.0,
                    alt="국면별 리드타임 구성: 접수 2.1h 전부 대기·조율, 현장 98.3h 중 대기 95.3%, 정산 5.5h 시스템 처리, E2E 105.9h 중 대기·조율 90.5%")
KX, KW = MX + 7.5 + 0.25, CW - 7.5 - 0.25
kp = [
    (ORG50, ORG200, "E2E 전체 대기", PILL_ORG, "공정 간 대기·조율 시간", "90.5%", ORG600, "95.8h / 105.9h"),
    (RED50, RED200, "현장 국면 편중", PILL_RED, "대기·조율의 현장 독점도", "97.8%", RED600, "현장 93.7h / 전체 95.8h"),
    (EMR50, EMR200, "정산 자동화", PILL_EMR, "정산 구간 대기 0.0시간", "0.0h", EMR600, "시스템 자동 처리 5.5h"),
]
for i, (bg, bl, pill, ps, lab, big, bc, sub) in enumerate(kp):
    y = Y0 + i * 0.91
    add_box(s, KX, y, KW, 0.8, bg, bl, 0.75, 0.1, f"KPI-{i + 1}")
    add_pill(s, KX + 0.15, y + 0.12, pill, ps[0], ps[1], ps[2], size=9.5)
    add_text(s, KX + 0.15, y + 0.46, 2.0, 0.26, para(lab, 10, False, S500))
    add_text(s, KX + 2.0, y + 0.04, KW - 2.15, 0.48, para(big, 25, True, bc, mono=True, align="r"))
    add_text(s, KX + 2.0, y + 0.52, KW - 2.15, 0.24, para(sub, 9.5, False, S600, mono=True, align="r"))
b8 = [
    ("01 접수 병목", PILL_BLUE, "일정 조율 2.0h (접수 2.1h의 96%)", S900, S200, 0.75,
     ["전화·대면(479건): 평균 0.06h, 15분 내 완결", "웹·우편(448건): 평균 4.5h·3.6h — 중앙값은 4분, 일부 케이스에 집중",
      "교차 인계 123건 발생 시 6.6배 폭증 (1.2h ➔ 7.9h)"]),
    ("02 현장 1위 병목", PILL_RED, "실사 방문 대기 76.8h", RED600, RED600, 1.5,
     ["현장 소요시간 98.3h 중 78.2% 독점 (압도적 1위)", "일 유입 134건 vs 기사 CAPA 68건 (소화율 51%)",
      "매일 66건 누적 ➔ 피크 시 403건 미처리 적체(WIP)"]),
    ("03 현장 수리 병목", PILL_ORG, "자재 대기 30.5h & 하자 루프", S900, S200, 0.75,
     ["즉시·외주 대기 0.0h, 사내수리만 부품 대기 30.5h", "하자 재방문 26건 ➔ 평균 +32.9시간 추가 대기",
      "재수리 시 최대 10.1일(241.6h) 장기 억류"]),
]
for i, (pill, ps, title, tc, lc, lw, items) in enumerate(b8):
    x = MX + i * (cw3 + 0.25)
    section_card(s, x, 4.62, cw3, 2.26, pill, ps, title, tc, items, line=lc, line_w=lw, title_size=13.5, bullet_size=11, after=3)
set_notes(s, "수리 프로세스가 지연되는 진짜 원인은 무엇일까요? 기사가 작업을 느리게 해서일까요? 데이터를 쪼개보니 완전히 달랐습니다.\n전체 105.9시간(약 4.4일) 중 현장 실작업과 정산 시스템 처리 시간은 10.1시간(9.5%)에 불과하며, 나머지 95.8시간(90.5%)은 공정 사이에서 멈춰 서 있거나 일정 조율에 쓰인 대기·조율 시간이었습니다. 특히 정산 국면은 인간 개입 없이 시스템이 100% 자동 처리하므로 대기가 0시간이며, 대기·조율의 97.8%가 '현장 국면'에 집중되어 있었습니다.\n이 대기시간의 발원지를 3대 병목으로 정리했습니다. 첫째, 웹·우편의 비동기 소통 부재로 일정이 늘어지는 '일정 조율 병목(평균 2.0시간, 중앙값 4분)'. 둘째, 현장 국면의 78%가 쏠려 있는 압도적 1위의 '실사 방문 대기 병목(76.8h)'. 셋째, 사내 수리 시 자재 조달과 재작업으로 인한 '수리 준비 대기(30.5h) 및 하자 루프(최대 10일)'입니다.\n그렇다면 프로세스의 첫 관문인 접수 국면에서 왜 6.6배의 시간 폭증이 일어났는지, 다음 장에서 살펴보겠습니다.\n\n[예상 질문] 90.5%의 정의는? → 정산 5.5h를 시스템 처리(비대기)로 본 보수적 값입니다. start→complete 구간만 작업으로 보면 94.6%이며, 어느 쪽이든 '대기가 압도적'이라는 결론은 동일합니다.")

# =================================================================== S09 제1병목: 접수
s = blank_slide(prs, 9)
add_chrome(s, 9, "Part 02 · 질문 2-2 | 제1대 병목 (접수 국면)",
           "접수 지연은 물량 과부하가 아닌 '교차 인계(123건)'에서 비롯되며, 비실시간 채널 공백이 6.6배 폭증을 유발했다",
           "출처: analysis.sql 접수 단독 OLS (R² = 0.300, F = 131.9, p < 0.001) · 접수 모델 VIF ≤ 1.20 · 15분 이내 = 접수 소요 ≤ 15분")
add_card(s, MX, Y0, CW, 2.38, WHITE, S200, 0.75, 0.14, "ReceptionChartFrame")
add_picture_contain(s, fig2("s09_reception_3panel.png"), MX, Y0, CW, 2.38, pad=0.03,
                    alt="접수 3패널: 인계 여부별 소요시간 1.2h 대 7.9h, 채널별 완료 속도 분포, 15분 이내 완료 건 평균 소요시간")
c9 = [
    ("가설 기각", PILL_GRAY, "물량 과부하 가설 완전 기각", S900, "r = 0.01", S700, S200, 0.75,
     ["일일 인입량(10~141건)과 소요시간은 무상관", "다중 OLS 계수 p = 0.752 (비유의)", "창구 처리 용량(CAPA) 부족이 원인이 아님"]),
    ("핵심 원인", PILL_ORG, "교차 인계 시 6.6배 시간 폭증", ORG600, "6.6배 (+6.7h)", ORG600, ORG200, 0.75,
     ["단독 처리군(804건): 평균 1.2h (중앙값 8분)", "교차 인계군(123건): 평균 7.9h (중앙값 5.6h)",
      "인계 123건 전수가 웹 69건·우편 54건에서 발생"]),
    ("반전 통찰", PILL_EMR, "Web 채널 6.8분의 본질적 우수성", EMR700, "6.8분 (최속)", EMR600, EMR200, 0.75,
     ["15분 내 완료 건: 웹 6.8분 < 전화 8.2분", "웹 시스템이 아닌 '일정 조율 공백'이 원인", "Direct Booking(자가 일정 확정)으로 제거"]),
]
for i, (pill, ps, title, tc, big, bc, lc, lw, items) in enumerate(c9):
    x = MX + i * (cw3 + 0.25)
    section_card(s, x, 4.3, cw3, 2.58, pill, ps, title, tc, items, line=lc, line_w=lw, big=big, big_color=bc,
                 big_size=19, title_size=13, bullet_size=11, after=3)
set_notes(s, "접수 국면의 지연은 왜 발생했을까요? 특정 날짜에 접수량이 몰려서였을까요? 데이터를 분석해보니 일별 접수량과 소요시간은 전혀 상관이 없었습니다(r=0.01, 회귀계수 p=0.752). 물량 문제가 아니었습니다.\n좌측 Panel 1을 보시면, 진짜 원인은 상담원 간의 '교차 인계(Handover)'였습니다. 단독으로 처리할 때는 1.2시간이면 끝나던 접수가, 상담원 2명 이상 개입되는 순간 7.9시간으로 6.6배 폭증했습니다.\n그렇다면 이 인계는 어디서 발생했을까요? 가운데 Panel 2를 보시면 전화와 대면은 15분 이내 완료율이 사실상 100%였고 인계가 0건이었습니다. 반면 웹과 우편은 약 50%가 60분을 초과하는 장기 지체에 빠졌으며, 발생한 인계 123건 전수가 오직 웹과 우편에서만 나왔습니다.\n그렇다면 웹 채널이 비효율적인 시스템일까요? 우측 Panel 3을 주목해 주십시오. 15분 이내 완료 건만 비교하면, 웹은 평균 6.8분으로 전화(8.2분)나 대면(8.5분)보다 오히려 가장 빨랐습니다.\n즉, 웹 시스템 자체가 느린 게 아닙니다. 신청 접수 후 실시간으로 방문 일정을 확정하지 못해 고객 회신을 기다리다 담당자가 교체되는 '비동기 일정 조율 공백'이 6.6배 지연의 본질이었습니다.\n이제 전체 대기의 대부분이 집중된 최대 핵심 병목, '현장 국면'으로 넘어가겠습니다.")

# =================================================================== S10 제2병목: 현장
s = blank_slide(prs, 10)
add_chrome(s, 10, "Part 02 · 질문 2-2 | 제2대 병목 (현장 국면)",
           "현장 소요시간(98.3h)의 95.3%가 대기이며, 기사 CAPA를 2배 넘는 유입이 403건의 미처리 적체(WIP)를 만들었다",
           "출처: analysis.sql 2-3(Wait 1·2), 3-1~3-5(일별 유입 vs CAPA, WIP) · 유입 = 1/2~1/7 일평균 현장 이관, CAPA = 1/1~1/8 일평균 실사 착수")
LW10 = 5.0
add_card(s, MX, Y0, LW10, 5.1, WHITE, S200, 0.75, 0.14, "FieldDonutCard")
add_text(s, MX + 0.2, Y0 + 0.12, LW10 - 0.4, 0.28, para("현장 소요시간 98.3h 구조 분해", 12, True, S900))
add_picture_contain(s, fig2("s10_field_donut.png"), MX, Y0 + 0.4, LW10, 2.3, pad=0.0,
                    alt="현장 98.3시간 4대 소요시간 구조: 실사 방문 대기 78.2%, 수리 착수·공정 대기 17.2%, 본수리 4.0%, 실사 점검 0.7%")
strips = [
    (RED50, RED200, "① 실사 방문 대기 (Wait 1)", "76.81h (78.2%)", RED600, True, RED600),
    (ORG50, ORG200, "② 수리 착수·공정 대기 (Wait 2)", "16.90h (17.2%)", ORG600, True, ORG600),
    (S50, S200, "③ 본수리 순수 작업", "3.90h (4.0%)", S700, False, BLU600),
    (S50, S200, "④ 실사 점검 순수 작업", "0.68h (0.7%, 40.5분)", S700, False, "38BDF8"),
]
for i, (bg, bl, lab, val, vc, b, dot) in enumerate(strips):
    y = Y0 + 2.8 + i * 0.57
    add_box(s, MX + 0.18, y, LW10 - 0.36, 0.48, bg, bl, 0.75, 0.08, f"Strip-{i + 1}")
    add_circle(s, MX + 0.3, y + 0.16, 0.16, dot)
    add_text(s, MX + 0.55, y, 2.6, 0.48, para(lab, 10.5, b, S800), anchor="m")
    add_text(s, MX + 2.95, y, LW10 - 0.36 - 2.87, 0.48, para(val, 10.5, True, vc, mono=True, align="r"), anchor="m")
RX10 = MX + LW10 + 0.25
RW10 = SLIDE_W - MX - RX10
add_card(s, RX10, Y0, RW10, 5.1, WHITE, S200, 0.75, 0.14, "WipCard")
add_text(s, RX10 + 0.2, Y0 + 0.12, RW10 - 0.4, 0.28, para("일별 현장 이관 유입 vs 실사 CAPA 및 적체 대기열(WIP)", 12, True, S900))
add_picture_contain(s, fig2("s10_wip_flow.png"), RX10, Y0 + 0.4, RW10, 2.55, pad=0.0,
                    alt="일별 현장 이관 유입 대 실사 착수 막대와 미처리 적체 대기열(WIP) 꺾은선, 1/7 피크 403건")
mw = (RW10 - 0.36 - 2 * 0.1) / 3
metrics = [
    (BLU50, BLU200, "일일 현장 이관 유입", "134.3건/일", BLU700, "1/2~1/7 평균 · 피크 141건"),
    (S50, S200, "실사 CAPA (기사 11인)", "68.0건/일", S700, "소화율 50.6% 한계"),
    (RED50, RED200, "미처리 적체 피크 (WIP)", "403건 (20배)", RED600, "1/1 20건 ➔ 1/7 403건"),
]
for i, (bg, bl, t, big, bc, sub) in enumerate(metrics):
    x = RX10 + 0.18 + i * (mw + 0.1)
    add_box(s, x, Y0 + 3.08, mw, 1.0, bg, bl, 0.75, 0.1, f"Metric-{i + 1}")
    add_text(s, x + 0.1, Y0 + 3.13, mw - 0.2, 0.26, para(t, 9.5, True, S600))
    add_text(s, x + 0.1, Y0 + 3.4, mw - 0.2, 0.4, para(big, 17, True, bc, mono=True))
    add_text(s, x + 0.1, Y0 + 3.78, mw - 0.2, 0.25, para(sub, 9.5, False, S500))
add_box(s, RX10 + 0.18, Y0 + 4.2, RW10 - 0.36, 0.76, S900, None, radius=0.1, name="TakeawayBanner")
add_text(s, RX10 + 0.35, Y0 + 4.2, RW10 - 0.7, 0.76,
         para("기사가 게으른 것이 아니라, CAPA(68건)의 2배에 이르는 전수 방문 실사 관행(유입 134건)이 403건 적체와 76.8h 대기를 만든 본질이다",
              11.5, True, WHITE, align="c"), anchor="m")
set_notes(s, "현장 국면의 문제점을 살펴보겠습니다. 좌측 도넛 차트를 보시면, 현장에서 보낸 98.3시간 중 기사가 땀 흘려 일한 순수 작업 시간은 4.7%(수리 3.9h, 점검 0.7h)에 불과합니다. 나머지 95.3%(93.7시간)가 전부 대기시간이었습니다.\n특히 전체 리드타임의 72.5%를 단독 차지한 '실사 방문 대기(76.8시간, 3.2일)'는 왜 발생했을까요?\n우측 통합 차트를 보시면 물리적 원인이 드러납니다. 파란색 막대인 일일 현장 이관 유입량은 매일 134건씩 쏟아졌지만, 회색 막대인 현장 기사 11명이 하루에 소화한 실사는 68건에 불과했습니다.\n유입이 처리 능력을 2배 가까이 초과하자, 빨간색 꺾은선인 '미처리 적체 대기열(WIP)'은 첫날 20건에서 7일 만에 403건으로 20배 폭증합니다. 저수조에 물이 넘치듯 403건이 쌓이니, 뒤늦게 방문받는 세입자는 평균 3일 넘게 기다릴 수밖에 없었습니다. 즉, 기사가 게으른 것이 아니라 'CAPA를 초과하는 전수 방문 실사 관행'이 현장 병목의 진짜 원인이었습니다.\n\n[예상 질문] 유입 134.3건과 CAPA 68.0건의 산출 창? → 유입은 인입이 안정된 1/2~1/7(6일) 평균 현장 이관량, CAPA는 1/1~1/8 평균 실사 착수량입니다. 14일 지속 평균으로 보면 CAPA는 63.7건/일(소화율 47%)로 더 낮아져 결론은 동일합니다.")

# =================================================================== S11 OLS & 리워크
s = blank_slide(prs, 11)
add_chrome(s, 11, "Part 02 · 질문 2-3 & 2-2 | 소요시간 영향 요인 & 리워크",
           "OLS 평균 기여: 실사 대기가 105.9h 중 86h(81%), 사내수리가 17h(16%)를 차지하고 하자 루프(26건)가 적체를 키웠다",
           "출처: hypothesis_testing_and_visualization.ipynb Part 5 (E2E OLS, n = 927) · analysis.sql 2-4 · 평균 기여 = 회귀계수 × 변수 평균값")
HW = (CW - 0.25) / 2
add_card(s, MX, Y0, HW, 4.42, WHITE, S200, 0.75, 0.14, "OlsCard")
add_text(s, MX + 0.2, Y0 + 0.1, HW - 0.4, 0.28, para("리드타임 105.9h에 대한 평균 기여 (회귀계수 × 평균)", 11.5, True, S900))
add_picture_contain(s, fig2("s11_ols_contribution.png"), MX + 0.15, Y0 + 0.38, HW - 0.3, 2.3, pad=0.0,
                    alt="E2E 리드타임 평균 기여: 실사 방문 대기 86.3h, 사내 수리 배정 16.6h, 비실시간 채널 2.4h, 2차 에스컬레이션 0.8h")
ols = [
    (ORG50, ORG200, "사내 수리 방식 (is_intern_repair)", "+31.75h (p < 0.001)", ORG700),
    (RED50, RED200, "실사 방문 지연 (visit_lag_hours)", "+1.12h/h (p < 0.001)", RED700),
    (S50, S200, "비실시간 접수 채널 (is_async_channel)", "+4.89h (p = 0.030)", S700),
]
for i, (bg, bl, t, v, vc) in enumerate(ols):
    y = Y0 + 2.76 + i * 0.44
    add_box(s, MX + 0.18, y, HW - 0.36, 0.38, bg, bl, 0.75, 0.08, f"Ols-{i + 1}")
    add_text(s, MX + 0.3, y, 3.4, 0.38, para(t, 10, False, S800), anchor="m")
    add_text(s, MX + 3.5, y, HW - 0.36 - 3.4, 0.38, para(v, 10.5, True, vc, mono=True, align="r"), anchor="m")
add_text(s, MX + 0.2, Y0 + 4.1, HW - 0.4, 0.3,
         para("R² = 0.878 · F = 1,652.8 · p < 0.001 · VIF 최대 1.02 · 2차 에스컬레이션 비유의(p = 0.079)", 9, False, S500))
RX11 = MX + HW + 0.25
add_card(s, RX11, Y0, HW, 4.42, WHITE, S200, 0.75, 0.14, "ReworkCard")
add_text(s, RX11 + 0.2, Y0 + 0.1, HW - 0.4, 0.28, para("수리 방식별 착수 대기와 하자 재방문 루프", 11.5, True, S900))
add_picture_contain(s, fig2("s11_rework_wait.png"), RX11 + 0.15, Y0 + 0.38, HW - 0.3, 2.3, pad=0.0,
                    alt="수리 방식별 착수 대기: 즉시·외주 0.0h, 사내수리 1차 30.5h, 사내 하자 재방문 평균 +32.9h 최대 241.6h")
add_box(s, RX11 + 0.18, Y0 + 2.76, HW - 0.36, 0.78, S50, S200, 0.75, 0.1, "Rework-Block1")
add_text(s, RX11 + 0.3, Y0 + 2.78, HW - 0.6, 0.74,
         [para("사내수리 자재 대기 30.5h", 11, True, S900, after=2),
          para("즉시·외주수리는 대기 0.0h로 즉시 착수. 사내수리만 부품 조달·2차 일정 조율로 대기가 발생.", 10, False, S600)], anchor="m")
add_box(s, RX11 + 0.18, Y0 + 3.6, HW - 0.36, 0.74, RED50, RED200, 0.75, 0.1, "Rework-Block2")
add_text(s, RX11 + 0.3, Y0 + 3.62, HW - 0.6, 0.7,
         [para("사내 하자 리워크 26건: 평균 +32.9시간", 11, True, RED700, after=2),
          para("E-1/E-2가 22건(84.6%)에 집중, 최대 10.1일(241.6h) 억류.", 10, False, RED700)], anchor="m")
add_box(s, MX, 6.3, CW, 0.56, S900, None, radius=0.1, name="OlsBanner")
add_text(s, MX + 0.3, 6.3, 8.6, 0.56,
         para("OLS 계수: 실사 대기가 1시간 길어질수록 전체 리드타임은 평균 1.12시간 길어진다 (관측 기반 연관)", 11.5, True, WHITE), anchor="m")
add_text(s, MX + 8.9, 6.3, CW - 9.2, 0.56, para("β = +1.12h/h (p < 0.001)", 11.5, True, EMR400, mono=True, align="r"), anchor="m")
set_notes(s, "슬라이드 11은 리드타임을 결정하는 핵심 요인과 품질 결함으로 인한 리워크 문제를 함께 보여줍니다.\n좌측의 다중 회귀 모델(설명력 87.8%)에서 각 요인의 회귀계수에 평균값을 곱해 평균 기여를 계산했습니다. 실사 방문 대기는 시간당 1.12시간씩 리드타임을 늘리는데, 평균 대기가 76.8시간이라 평균 약 86시간, 즉 전체 105.9시간의 81%를 차지합니다. 사내수리 배정은 건당 +31.8시간이지만 전체의 52%에만 해당해 평균 17시간(16%), 비실시간 접수는 평균 2.4시간입니다. 계수만 보면 사내수리가 가장 커 보이지만, 평균 기여로 보면 실사 대기가 압도적입니다.\n우측을 보시면, 즉시수리와 외주는 대기가 0시간이지만 사내수리는 부품 준비로 기본 30.5시간이 걸립니다. 특히 1차 수리 실패로 다시 사내수리에 들어간 26건은 부품을 다시 조달하느라 평균 32.9시간, 최대 10일(241.6시간)이나 더 갇히게 됩니다.\n이제 사전 분류의 높은 정합도를 활용하여 이 병목들을 해소하는 전략으로 넘어가겠습니다.\n\n[예상 질문] 회귀가 인과를 증명하나? → 관측 데이터 기반 연관이며, 시뮬레이션 효과는 이 계수를 가정하고 보수적으로(20%) 적용했습니다. 평균 기여는 회귀 분해이지 분산 설명력이 아닙니다. 2차 에스컬레이션 계수는 p=0.079로 비유의입니다.")

# =================================================================== S12 핵심 문제 규명
s = blank_slide(prs, 12)
add_chrome(s, 12, "Part 02 & Part 03 발단 | 핵심 문제 규명 & 해결 아젠다",
           "사전 분류가 이미 83~87%의 현장 결과와 맞는데도, '정보 해상도 단절'로 403건 적체와 이중 출장이 고착되었다",
           "출처: analysis.sql 4절(사전 분류 정합성)·5절 시나리오 1 · 87.3% = E+P 전체(낙관 상한), 83.2% = 내부 완결 771건(보수 기준)")
H12 = 5.1
x = MX
add_card(s, x, Y0, cw3, H12, WHITE, S200, 0.75, 0.14, "Fact87")
add_pill(s, x + 0.2, Y0 + 0.16, "데이터 팩트", *PILL_BLUE, size=9.5)
add_text(s, x + 0.2, Y0 + 0.5, cw3 - 0.4, 0.3, para("사전 분류와 현장 결과의 정합도", 13, True, S900))
add_text(s, x + 0.2, Y0 + 0.84, cw3 - 0.4, 0.5,
         para([R("83~87", 26, True, BLU700, True), R("%", 16, True, BLU700, True),
               R("   보수 83.2% ~ 상한 87.3%", 9.5, False, S500)]))
add_picture_contain(s, fig2("s12_planned_vs_actual.png"), x + 0.2, Y0 + 1.42, cw3 - 0.4, 1.85, pad=0.0,
                    alt="사전 분류별 1차 수리 결과: E형 370건 전원 사내수리, P형 439건 중 즉시 365·사내 36·외주 38, B형 118건 분산")
add_text(s, x + 0.2, Y0 + 3.33, cw3 - 0.4, 0.9,
         bullets(["E형 370건: 100% 사내수리 완결", "P형 439건: 91.3%(401건) 내부 완결", "E+P 809건 = 87.3% (P-4 외주 38건 제외 시 83.2%)"],
                 10.5, after=2))
add_box(s, x + 0.2, Y0 + 4.27, cw3 - 0.4, 0.72, BLU50, BLU200, 0.75, 0.08, "Question")
add_text(s, x + 0.32, Y0 + 4.27, cw3 - 0.64, 0.72,
         para("이미 83~87%를 맞히는데 왜 40분짜리 헛걸음 실사로 403건 적체를 자초했는가?", 10.5, True, BLU800), anchor="m")
x = MX + cw3 + 0.25
add_card(s, x, Y0, cw3, H12, WHITE, ORG200, 1.0, 0.14, "ResolutionGap")
add_pill(s, x + 0.2, Y0 + 0.16, "원인 규명", *PILL_ORG, size=9.5)
add_text(s, x + 0.2, Y0 + 0.5, cw3 - 0.4, 0.3, para("정보 해상도 단절", 13, True, ORG600))
add_text(s, x + 0.2, Y0 + 0.84, cw3 - 0.4, 0.5, para("Resolution Gap", 26, True, ORG600, mono=True))
for j, (hd, a, b) in enumerate([("현행 접수 상담원", "알파벳 대분류(B·P·E)만 수집", "한계: 알파벳만으로는 차에 실을 자재 규격을 특정할 수 없음"),
                                ("현장 방문 기사", "40분 방문 실사 후 세부 코드(1~4) 판정", "결과: 실사(40분) ➔ 부품 주문(30.5h) ➔ 재방문 수리 = 이중 출장 고착")]):
    y = Y0 + 1.5 + j * 1.38
    add_box(s, x + 0.2, y, cw3 - 0.4, 1.28, S50, S200, 0.75, 0.08, f"Contrast-{j + 1}")
    add_text(s, x + 0.34, y + 0.08, cw3 - 0.68, 1.14,
             [para(hd, 12, True, S900, after=2), para("➔ " + a, 11, True, S700, after=4), para(b, 11, False, S600)])
add_box(s, x + 0.2, Y0 + 4.27, cw3 - 0.4, 0.72, ORG50, ORG200, 0.75, 0.08, "GapSummary")
add_text(s, x + 0.32, Y0 + 4.27, cw3 - 0.64, 0.72,
         para("접수와 현장의 정보 해상도 단절이 이중 출장 비효율의 핵심 원인", 10.5, True, ORG800), anchor="m")
x = MX + 2 * (cw3 + 0.25)
add_card(s, x, Y0, cw3, H12, WHITE, EMR500, 2.0, 0.14, "ConservativeFix")
add_pill(s, x + 0.2, Y0 + 0.16, "보수적 해결책", *PILL_EMR, size=9.5)
add_text(s, x + 0.2, Y0 + 0.5, cw3 - 0.4, 0.3, para("E형 우선 신뢰 시 즉각적 대기 단축", 13, True, EMR700))
add_text(s, x + 0.2, Y0 + 0.88, cw3 - 0.4, 0.26, para("① CAPA 부하 경감 (일 실사 유입)", 11, True, S900))
mini = [("현재 유입", 134.3, BLU600, S800), ("E형 직행 후", 80.7, EMR600, EMR700), ("기사 CAPA", 68.0, S400, S600)]
MAXW = 1.95
for k, (lab, v, col, tc) in enumerate(mini):
    yy = Y0 + 1.2 + k * 0.3
    add_text(s, x + 0.2, yy, 0.95, 0.24, para(lab, 10, k == 1, tc), anchor="m")
    add_box(s, x + 1.2, yy + 0.03, MAXW * v / 134.3, 0.18, col, None, name=f"MiniBar-{k + 1}")
    add_text(s, x + 1.25 + MAXW * v / 134.3, yy, 0.6, 0.24, para(f"{v:.1f}", 10, True, tc, mono=True), anchor="m")
add_text(s, x + 0.2, Y0 + 2.14, cw3 - 0.4, 0.5,
         para("E형 370건 직행 ➔ 유입 40% 감소, 적체 누적 속도 80.8% 격감 (일 66.3건 ➔ 12.7건)", 10.5, False, S600, bullet=True))
add_text(s, x + 0.2, Y0 + 2.72, cw3 - 0.4, 0.26, para("② 보수적 20% 대기 단축", 11, True, S900))
add_text(s, x + 0.2, Y0 + 3.0, cw3 - 0.4, 0.26,
         para("실사 대기(76.8h) 20% 단축 ➔ -15.4시간", 10.5, False, S600, bullet=True))
add_text(s, x + 0.2, Y0 + 3.3, cw3 - 0.4, 0.26, para("③ OLS 계수(+1.12h/h) 연동", 11, True, S900))
add_text(s, x + 0.2, Y0 + 3.58, cw3 - 0.4, 0.4,
         para("15.4h × 1.12 = 전체 리드타임 -17.2시간", 10.5, False, S600, bullet=True))
add_box(s, x + 0.2, Y0 + 4.0, cw3 - 0.4, 0.99, EMR50, EMR200, 0.75, 0.1, "FloorBig")
add_text(s, x + 0.2, Y0 + 4.04, cw3 - 0.4, 0.58,
         para([R("▼ ", 16, True, EMR600), R("17.2시간", 26, True, EMR600, True)], align="c"), anchor="m")
add_text(s, x + 0.2, Y0 + 4.64, cw3 - 0.4, 0.3, para("검증된 하한 (리드타임의 16.2%)", 10.5, True, EMR800, align="c"))
set_notes(s, "앞선 분석을 종합하면, 병목을 없애기 위한 핵심은 명확합니다. 실사 CAPA의 적체 부담을 덜어내고, 수리 품목 준비 기간을 줄여야 합니다.\nCard 1에서 보시듯, 접수원의 사전 분류는 이미 실제 수리와 매우 높게 일치하고 있었습니다. E형과 P형을 합치면 809건, 87.3%이고, 외주로 빠지는 P-4 38건을 빼는 보수적 기준으로도 83.2%입니다. 특히 E형은 100% 사내수리였습니다.\n이렇게 잘 맞추면서 왜 굳이 40분짜리 실사를 먼저 보내 400건의 대기열을 만들었을까요?\nCard 2의 '정보 해상도의 한계' 때문이었습니다. 접수부는 단순 알파벳(B, P, E)만 넘겨주고, 현장 기술자는 1~4 세부 코드를 써야 부품을 알 수 있어 차에 실을 수가 없었습니다.\n따라서 Card 3의 해결책을 제시합니다. 가장 보수적으로 100% 사내수리인 E형만 실사 없이 직행시켜도, 실사 유입은 40% 줄고 적체 누적 속도는 81% 격감합니다. 여기서 실사 대기를 단 20%만 줄인다고 보수적으로 잡아도 15.4시간이 줄며, 앞선 OLS 계수 1.12에 따라 전체 리드타임 17.2시간 단축이 기대됩니다.\n다음 장에서 두 번째 과제인 '수리 품목 준비 단축 및 리워크 방지'의 구체적 실행 방안을 설명해 드리겠습니다.\n\n[예상 질문] 87.3%는 '적중률'인가? → E형+P형이 차지하는 비중(809/927)으로 낙관 상한입니다. 사내 완결이 확정된 771건 기준 보수 정합도는 83.2%이며 발표에서는 두 값을 함께 제시합니다.")

# =================================================================== S13 TO-BE 실행 전략
s = blank_slide(prs, 13)
add_chrome(s, 13, "Part 03 · 질문 3 | TO-BE 구체적 실행 전략",
           "사전 체크리스트로 자재 대기(30.5h)를 압축하고, E-1/E-2 정밀검사로 리워크 84.6%(+32.9h)를 표적 차단한다",
           "출처: analysis.sql 2-4(리워크 26건: E-1 16·E-2 6)·5절 시나리오 · 통합 목표치는 시나리오 가정 기반이며 검증된 하한은 -17.2h")
c13 = [
    ("전략 1: 자재 대기 단축", PILL_BLUE, "스마트폰 사진 기반 부품 사전 특정", BLU700, BLU200, "30.5h ➔ 사전 패킹", BLU600,
     ["접수 시 고장 부위·모델 라벨 사진 1장을 필수 등록해 출동 전 부품 규격 특정",
      "방문 후 주문하던 30.5h 자재 대기를 '출동 전 사전 패키징'으로 압축",
      "실사(40.5분) 생략으로 회수되는 공수 496.1h(735건)를 부품 준비·상차에 재배치"],
     "근거: 사내수리 485건 · 착수 대기 30.5h"),
    ("전략 2: 품질 루프 차단", PILL_RED, "E-1/E-2 2차 정밀검사 프로토콜", RED600, RED200, "리워크 84.6% 표적", RED600,
     ["사내 하자 리워크 26건 중 84.6%(22건)가 E-1(16건)·E-2(6건)에 집중",
      "정밀검사 체크리스트: 인접 배관·연계 부속 2차 노후도 점검 의무화로 규격 불일치 차단",
      "재수리 평균 +32.9h(최대 10.1일) 재방문 루프 방지"],
     "근거: 리워크 26건 · E-1 16건 + E-2 6건"),
    ("전략 3: 물류·외주 최적화", PILL_EMR, "모듈형 번들 키트 & 외주 직행", EMR700, EMR200, "외주 대기 0.0h 유지", EMR600,
     ["E-1/E-2 출동 시 빈번 고장 연관 부품을 번들 키트로 사전 적재해 재출하 대기 제거",
      "외주 패스트트랙(P-4 38건): 사진상 대규모 배관·전문 공사 식별 시 실사 생략",
      "전문 외주업체(FixIt/DoIt)로 직접 전산 이관"],
     "근거: P-4 38건 · 외주 착수 대기 0.0h"),
]
for i, (pill, ps, title, tc, lc, big, bc, items, tag) in enumerate(c13):
    x = MX + i * (cw3 + 0.25)
    section_card(s, x, Y0, cw3, 3.4, pill, ps, title, tc, items, line=lc, big=big, big_color=bc, big_size=17,
                 title_size=13, bullet_size=11.5, after=5, tag=tag, tag_color=S500)
# TO-BE 효과 범위: 검증된 하한과 가정 기반 목표를 분리해서 보여준다
PY, PH = 5.3, 1.58
add_card(s, MX, PY, CW, PH, WHITE, S200, 0.75, 0.12, "RoiPanel")
add_pill(s, MX + 0.25, PY + 0.16, "TO-BE 효과 범위 (E2E 리드타임)", *PILL_EMR, size=9.5)
add_text(s, MX + 0.25, PY + 0.52, 3.35, 1.0,
         [para("하한은 시뮬레이션으로 검증, 통합 목표는 가정 기반", 11, True, S800, after=3),
          para("하한 = 실사 대기 20% 단축 × OLS 1.12 · 목표 = 자재 대기·리워크 차단까지 합산한 가정", 9.5, False, S500)])
bars13 = [("AS-IS 현재", 105.9, S700, None, "105.9h", S800),
          ("검증 하한", 88.7, EMR600, None, "88.7h  (-17.2h · -16%)", EMR700),
          ("통합 목표", 38.0, EMR100, EMR600, "약 38h  (-67.9h · -64% · 가정)", EMR700)]
BX0, BMAX = MX + 5.0, 4.9
for k, (lab, v, col, ln, txt, tcol) in enumerate(bars13):
    yy = PY + 0.17 + k * 0.46
    add_text(s, MX + 3.85, yy, 1.1, 0.34, para(lab, 10.5, True, S800), anchor="m")
    bar = add_box(s, BX0, yy + 0.03, BMAX * v / 105.9, 0.28, col, ln, 1.25, name=f"RoiBar-{k + 1}")
    if ln:
        bar.line.dash_style = MSO_LINE.DASH
    add_text(s, BX0 + BMAX * v / 105.9 + 0.12, yy, 2.7, 0.34, para(txt, 10.5, True, tcol, mono=True), anchor="m")
set_notes(s, "슬라이드 12에서 제시한 두 번째 과제, '수리 품목 준비 기간 단축과 리워크 방지'의 구체적 실행 방안입니다.\nCard 1을 보시면, 접수 단계에서 스마트폰 사진 1장을 의무 등록받아 부품 모델 라벨을 사전에 특정합니다. 기사가 부품을 미리 알고 챙겨 나가기 때문에, 30.5시간이나 걸리던 자재 대기를 사전에 크게 압축할 수 있습니다.\nCard 2는 품질 리워크의 해결책입니다. 10일씩 걸리기도 하는 사내 리워크 26건의 85%(22건)가 E-1과 E-2 코드에 쏠려 있었습니다. 따라서 E코드 건에 대해서는 '인접 배관 2차 정밀검사 체크리스트' 작성을 의무화하여, 추가 하자를 현장에서 즉시 잡아냅니다.\n마지막 Card 3처럼 연관 부품을 묶은 '모듈형 번들 키트'를 들고 나가고, 사진상 외주 공사(P-4)는 즉시 외주업체로 패스트트랙 이관하면, 자재 대기(30.5h)와 리워크 루프(+32.9h)를 함께 줄일 수 있습니다.\n\n[예상 질문] 38시간 목표의 근거는? → 시뮬레이션으로 검증된 값은 '실사 대기 20% 단축 → −17.2h(−16%)'입니다. 자재 대기 사전화와 리워크 차단까지 더한 통합 목표(약 60% 이상)는 가정에 기반한 목표치이며, 파일럿 후 실측으로 확정해야 합니다. 496.1h는 E형 370건 + P형 즉시 365건(735건) × 40.5분입니다.")

# =================================================================== S14 Q&A
s = blank_slide(prs, 14)
add_chrome(s, 14, "Part 04 · 마무리 | 질의응답 (Q&A)",
           "경청해 주셔서 감사합니다. 수리 프로세스 최적화 방안에 대한 질의응답을 진행하겠습니다",
           "출처: 퍼즐데이터 과제 분석 보고서 (Slide 01 ~ 14 완결 · 부록 A-1~A-4 별첨)")
journey = [
    ("Part 01", PILL_BLUE, S50, S200, S900, "전수 보존 & 인과 복원", "13,262행 임의 삭제 0건 · 결측 20행 복원 · 시간 역전 0건", "927건", S900, "정상 코호트"),
    ("Part 02", PILL_ORG, ORG50, ORG200, ORG800, "병목 원인 규명", "76.8h 실사 대기 · 일 134건 유입 vs CAPA 68건 · 접수 인계 6.6배", "403건", RED600, "WIP 피크"),
    ("Part 03", PILL_EMR, EMR50, EMR200, EMR800, "TO-BE 실행 전략", "E형 직행 · 사진 사전 패킹 · E-1/E-2 정밀검사 ➔ 통합 목표 60% 이상", "-17.2h", EMR600, "검증된 하한"),
]
for i, (pl, ps, bg, bl, tc, t, d, big, bc, cap) in enumerate(journey):
    y = 1.85 + i * 1.7
    add_card(s, MX, y, 6.0, 1.5, bg, bl, 0.75, 0.12, f"Journey-{i + 1}")
    add_pill(s, MX + 0.22, y + 0.2, pl, ps[0], ps[1], ps[2], size=9.5)
    add_text(s, MX + 1.3, y + 0.14, 2.85, 1.25, [para(t, 13.5, True, tc, after=5), para(d, 11, False, S600)])
    add_text(s, MX + 4.2, y + 0.3, 1.65, 0.55, para(big, 24, True, bc, mono=True, align="r"))
    add_text(s, MX + 4.2, y + 0.88, 1.65, 0.3, para(cap, 10, False, S500, align="r"))
HX = 6.85
add_card(s, HX, 1.85, SLIDE_W - MX - HX, 4.9, WHITE, EMR500, 2.0, 0.16, "QaHero")
hw_ = SLIDE_W - MX - HX
pw = text_w("QUESTION & ANSWER", 10.5, True) + 0.4
add_pill(s, HX + (hw_ - pw) / 2, 2.2, "QUESTION & ANSWER", EMR100, EMR800, None, size=10.5, h=0.32)
add_text(s, HX, 2.8, hw_, 1.2, para("Q & A", 66, True, S900, mono=True, align="c"))
add_text(s, HX, 4.2, hw_, 0.5, para("경청해 주셔서 감사합니다", 22, True, S900, align="c"))
add_text(s, HX, 4.85, hw_, 0.8,
         para("데이터 진단부터 병목 규명, 실행 전략까지\n자유롭게 질문해 주시기 바랍니다.", 13.5, False, S600, align="c"))
add_text(s, HX + 0.3, 6.15, hw_ - 0.6, 0.4,
         para("퍼즐데이터 채용 과제 수리 프로세스 데이터 분석 및 운영 최적화 방안  |  2026. 10. 27", 9.5, False, S500, align="c"))
set_notes(s, "이상으로 공공임대주택 수리 프로세스 데이터 분석 및 운영 최적화 방안 발표를 모두 마칩니다. 13,262행의 무손실 전처리부터 76.8시간의 실사 대기 병목 규명, 그리고 현장에 즉시 적용 가능한 3대 최적화 전략까지 전 과정에 대해 궁금하신 점이나 추가 논의하고 싶으신 부분에 대해 편하게 질문해 주시기 바랍니다. 경청해 주셔서 대단히 감사합니다.\n\n[핵심 숫자 치트시트] 13,262행·1,000케이스·927건 코호트(오접수 73건) / E2E 105.9h = 현장 98.3h + 접수 2.1h + 정산 5.5h / 대기·조율 90.5%(엄격 94.6%) / 실사 대기 76.8h(현장의 78.2%) / 유입 134.3건·CAPA 68.0건·WIP 피크 403건 / 교차 인계 123건 6.6배(1.2h→7.9h) / 사내수리 착수 대기 30.5h·리워크 26건 +32.9h·E-1/E-2 22건(84.6%) / 정합도 83.2~87.3% / 검증 하한 -17.2h(-16%), 통합 목표 약 38h(-64%, 가정).")

# =================================================================== Appendix (본문 14장·Q&A 이후 참고 자료)
H2 = lambda t, c=S700: dict(text=t, size=10.5, bold=True, color=c, fill=S100, border=S200)
B2 = lambda t, c=S600, b=False: dict(text=t, size=10.5, bold=b, color=c)

# ---- A-1 원본 프로세스 맵
s = blank_slide(prs, 15)
add_chrome(s, 15, "Appendix A-1 | 원본 프로세스 맵",
           "원본 프로세스 맵(이벤트 수 기준)은 노드 빈도와 반복 구간의 근거 자료이다",
           "출처: repair_cleaned.csv 프로세스 마이닝 (노드 = 이벤트 수 EV, 구간 머리말 = 케이스 수) · docs/repair_process_map.html",
           page_label="A-1", dots=False)
add_card(s, MX, Y0, CW, 3.62, S50, S200, 0.75, 0.14, "OriginalMapFrame")
add_picture_contain(s, fig("process_map_crop.png"), MX, Y0, CW, 3.62, pad=0.05,
                    alt="원본 프로세스 맵: 접수·현장·정산 노드의 이벤트 수와 평균·중앙값 대기(76.8h / 48.8h)")
a1 = [("노드 = 이벤트 수(EV)", "InternRepair 547 EV / 508 케이스처럼 한 케이스에서 같은 업무가 반복되면 EV가 케이스보다 많다. 사내수리 반복은 39회."),
      ("수리 1,062 EV > 927 케이스", "한 케이스 안에서 수리 유형이 바뀌거나 반복된 경우(복수 유형 91건)가 포함된다. 1차 실패 후 2차 수리 전환은 117건(12.6%)."),
      ("MakeTicket의 교차 인계", "접수 4활동에 상담원 2명 이상이 관여한 123건(13.3%). 건당 +5.11h는 접수 단독 OLS의 계수이며 본문의 6.6배는 평균 비교.")]
for i, (t, d) in enumerate(a1):
    x = MX + i * (cw3 + 0.25)
    add_card(s, x, 5.55, cw3, 1.33, WHITE, S200, 0.75, 0.12, f"A1Note-{i + 1}")
    add_text(s, x + 0.2, 5.65, cw3 - 0.4, 1.15, [para(t, 11.5, True, S900, after=3), para(d, 10.5, False, S600)])
set_notes(s, "부록입니다. 본문 7쪽의 맵은 케이스 수와 평균 대기를 중심으로 다시 그린 것이고, 이 장은 원본 맵(이벤트 수 기준)입니다. 질문이 나오면 노드별 이벤트 수와 반복 구간의 근거로 사용합니다.")

# ---- A-2 지표 정의
s = blank_slide(prs, 16)
add_chrome(s, 16, "Appendix A-2 | 핵심 지표 정의",
           "본문 수치는 모두 아래 정의와 산식으로 927건 코호트에서 재계산했다",
           "출처: analysis.sql 2·3절, hypothesis_testing_and_visualization.ipynb Part 3~5, scripts/verify_deck_facts.py (재계산 76항목)",
           page_label="A-2", dots=False)
defs = [
    ("케이스 리드타임", "FirstContact 시작 → TicketReady 완료 (접수 ~ 정산 종료)", "평균 105.9h", "SQL 2-1"),
    ("현장 국면", "InformClientSurvey → RepairReady", "98.3h (리드타임의 92.8%)", "SQL 2-1"),
    ("현장 실작업", "Survey + 수리 1~3차의 start → complete 합", "4.6h (현장의 4.7%)", "SQL 2-2"),
    ("실사 방문 대기 (Wait 1)", "InformClientSurvey → Survey start", "76.8h (중앙값 48.8h)", "SQL 2-3"),
    ("수리 착수 대기 (Wait 2)", "Survey complete → 1차 수리 start", "15.9h (사내수리 30.5h)", "SQL 2-3"),
    ("대기·조율 시간", "리드타임 − 현장 실작업 − 정산 시스템 처리(5.5h)", "95.8h = 90.5% (엄격 94.6%)", "재계산"),
    ("교차 인계", "접수 4활동(FirstContact·MakeTicket·ArrangeSurvey·InformClientSurvey)에 상담원 2명 이상 관여", "123건 (13.3%)", "노트북 Part 2"),
    ("리워크(하자 재방문)", "1차·2차 수리가 모두 InternRepair", "26건, 평균 +32.9h", "SQL 2-4"),
    ("WIP (현장 적체)", "누적 현장 이관 − 누적 실사 착수", "피크 403건 (1/7)", "SQL 3-1"),
    ("평균 기여", "OLS 계수 × 변수 평균 (E2E, n = 927, R² = 0.878)", "실사 대기 86.3h (81%)", "노트북 Part 5"),
]
rows_a2 = [[H2("지표"), H2("정의 · 산식"), H2("값"), H2("출처")]]
for t, d, v, src in defs:
    rows_a2.append([B2(t, S900, True), B2(d), B2(v, S800, True), B2(src, S500)])
add_table(s, MX, 1.82, [2.35, 5.55, 2.6, 1.73], [0.4] + [0.465] * len(defs), rows_a2, "DefinitionTable")
set_notes(s, "부록입니다. '대기·조율 90.5%'는 정산 5.5h를 시스템 처리로 보고 제외한 값이며, start→complete 구간만 작업으로 보면 94.6%입니다. 모든 수치는 scripts/verify_deck_facts.py로 원천(case_pivot_table.csv, repair_cleaned.csv)에서 재계산했습니다.")

# ---- A-3 전처리 규칙
s = blank_slide(prs, 17)
add_chrome(s, 17, "Appendix A-3 | 전처리 규칙 요약",
           "5대 비정상 항목은 업무 인과 규칙으로 복원했고, 정상 결측은 대체하지 않고 보존했다",
           "출처: analysis.ipynb Cell 18·20·51·53·77·81 · CASE 4·5 건수에는 결측 행(각 13건)이 포함됨",
           page_label="A-3", dots=False)
rules = [
    ("CASE 1 · taskID", "결측 2건", "contact 값은 FirstContact에만 기록되는 속성 → FirstContact / InformClientSurvey로 확정", "2건 복원", "Cell 18"),
    ("CASE 2 · originator", "결측 2건", "동일 작업의 start·complete 담당자가 100.0% 일치 → 짝 이벤트의 담당자(Anne, Paul) 승계", "2건 복원", "Cell 18"),
    ("CASE 3 · eventtype", "결측 5건", "기간 작업은 start → complete 1:1 페어(3건), 마일스톤은 complete 단독(2건)으로 추적", "5건 복원", "Cell 20"),
    ("CASE 4 · date", "결측 13 + 오기입 866 = 879건", "시각이 정상인 859건을 골라 선·후행 업무의 순서 구간 안에서 날짜 매핑 (단일 후보 640 + 앵커 최근접 219), 연도는 1970으로 통일", "879건 정규화", "Cell 51·53"),
    ("CASE 5 · time", "결측 13 + 더미 15 = 28건", "정상 자정 7건은 보존, 접수 구간 정상 표본 751건(75.1%)의 중앙값 4.0분을 앵커로 역산(21건)", "28건 복원 · 역전 0건", "Cell 51·77·81"),
]
rows_a3 = [[H2("대상 속성"), H2("이상 유형 · 건수"), H2("복원 규칙"), H2("결과"), H2("근거")]]
for a, b, c_, d, e_ in rules:
    rows_a3.append([B2(a, S900, True), B2(b, ORG700, True), B2(c_), B2(d, EMR700, True), B2(e_, S500)])
add_table(s, MX, 1.82, [1.95, 2.2, 5.0, 1.75, 1.33], [0.4] + [0.74] * 5, rows_a3, "RuleTable")
add_box(s, MX, 6.08, CW, 0.76, EMR50, EMR200, 0.75, 0.1, "RuleBanner")
add_text(s, MX + 0.3, 6.08, CW - 0.6, 0.76,
         [para("정상 결측(구조적 Null 86.0~93.0%, 7개 속성)은 후속 공정이 없어서 비어 있는 값이므로 임의 대체 없이 100% 보존", 11, True, EMR800, after=2),
          para("결과: 임의 행 삭제 0건 · 필수 속성 결측 0건 · 시간 역전 0건(3,711개 페어 양수 검증) · 분석 코호트 927건", 10.5, False, S600)], anchor="m")
set_notes(s, "부록입니다. 전처리 원칙은 두 가지입니다. 첫째, 행을 지우거나 평균으로 일괄 대체하지 않고 업무 인과(담당자 일치, 태스크 고유 속성, 선후행 순서)로 복원했습니다. 둘째, 후속 공정이 없어서 비어 있는 정상 결측은 보존했습니다. 복원 후 시간 역전은 0건입니다.")

# ---- A-4 가정·한계·후속 검증
s = blank_slide(prs, 18)
add_chrome(s, 18, "Appendix A-4 | 가정 · 한계 · 후속 검증",
           "결론의 적용 범위를 명시하고, TO-BE 효과는 파일럿으로 확정하는 것을 제안한다",
           "출처: analysis.sql 3·5절, 노트북 Part 5·7 · 파일럿 설계는 분석 결과에 근거한 제안이며 실측 전 확정치가 아님",
           page_label="A-4", dots=False)
a4 = [
    ("데이터 한계", PILL_GRAY, "927건이 짧은 기간에 집중됨", S900, S200,
     ["접수가 1/1~1/8 단 8일에 몰려 있어 계절·요일 효과는 관측되지 않음", "날짜를 1970년으로 정규화해 월·요일 분석은 불가",
      "단일 기관·단일 프로세스 로그라 타 기관 일반화에는 추가 검증 필요"]),
    ("분석 한계", PILL_ORG, "연관 분석과 정의 의존성", ORG700, ORG200,
     ["OLS는 관측 기반 연관이며 인과 추정이 아님, 평균 기여는 분산 설명력이 아님",
      "대기 비율은 정의에 따라 90.5% ~ 95.7% (본문은 가장 보수적인 값)",
      "CAPA는 산출 구간에 따라 63.7~69.2건/일, 결론(유입의 약 2배)은 동일"]),
    ("TO-BE 가정", PILL_EMR, "검증된 하한 −17.2h, 목표는 가정", EMR700, EMR500,
     ["검증: 실사 대기 20% 단축 × OLS 1.12 = −17.2h (리드타임의 16.2%)",
      "가정: 자재 대기·리워크 차단을 더한 통합 목표(약 38h)는 파일럿 실측으로 확정",
      "산출 근거가 없는 수치는 본문에서 '목표'로만 표기"]),
]
for i, (pill, ps, title, tc, lc, items) in enumerate(a4):
    x = MX + i * (cw3 + 0.25)
    section_card(s, x, Y0, cw3, 3.1, pill, ps, title, tc, items, line=lc, line_w=2.0 if i == 2 else 0.75,
                 title_size=13, bullet_size=11.5, after=6)
# 파일럿 설계 제안 (후속 검증 계획)
add_card(s, MX, 5.0, CW, 1.88, S50, S200, 0.75, 0.14, "PilotPlan")
add_pill(s, MX + 0.25, 5.14, "후속 검증: 파일럿 설계 제안", *PILL_EMR, size=9.5)
add_text(s, MX + 3.0, 5.14, CW - 3.25, 0.27, para("분석에서 도출한 검증 하한(−17.2h)을 실측으로 확인하고 통합 목표를 확정하기 위한 제안", 10.5, False, S500), anchor="m")
pilot = [("E형 직행", "대상", "사전 분류 E형(370건 규모, 사내수리 100% 완결)을 실사 없이 직행"),
         ("2주", "기간", "인입 피크가 포함되도록 설정해 적체(WIP) 동역학까지 관측"),
         ("4개 KPI", "측정", "실사 대기 · WIP · 리워크율 · 케이스 리드타임"),
         ("−15.4h 이상", "성공 기준", "실사 대기 20% 단축, OLS 환산 리드타임 −17.2h 이상")]
pw_ = (CW - 0.5 - 3 * 0.15) / 4
for i, (big, lab_, d) in enumerate(pilot):
    x = MX + 0.25 + i * (pw_ + 0.15)
    add_box(s, x, 5.55, pw_, 1.2, WHITE, EMR200, 0.75, 0.1, f"Pilot-{i + 1}")
    add_text(s, x + 0.15, 5.6, pw_ - 0.3, 0.4, para([R(big, 15, True, EMR700, True)]), anchor="m")
    add_text(s, x + 0.15, 6.0, pw_ - 0.3, 0.7,
             [para(lab_, 9.5, True, S500, after=1), para(d, 10, False, S600)])
set_notes(s, "부록입니다. 결론의 적용 범위를 정직하게 밝혀 두었습니다. 검증된 효과는 17.2시간 단축이고, 통합 목표인 약 38시간은 가정에 기반한 목표라 파일럿에서 확정해야 한다는 점을 질문받으면 이 장으로 답합니다.")

# ---- 슬라이드 쇼 내비게이션: 목차 타일 점프, 하단 인디케이터 점프, PowerPoint 섹션
for sl, tx, ty, tw_, th, tgt in TILE_LINKS:
    add_hotspot(sl, tx, ty, tw_, th, prs.slides[tgt - 1], f"TileLink-{tgt}")
link_footer_dots(prs)
add_sections(prs, [("Part 00 · 인트로", [1, 2, 3]), ("Part 01 · 데이터 진단·전처리", [4, 5, 6]),
                   ("Part 02 · 프로세스 마이닝 분석", [7, 8, 9, 10, 11]), ("Part 03 · TO-BE 전략", [12, 13]),
                   ("Part 04 · Q&A", [14]), ("Appendix · 참고 자료", [15, 16, 17, 18])])

save_deck(prs, OUT, "프로세스 마이닝 기반 공공임대주택 수리 프로세스 진단 및 운영 최적화 방안",
          "퍼즐데이터 채용 과제 — 수리 프로세스 데이터 분석")
