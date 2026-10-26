# -*- coding: utf-8 -*-
"""
퍼즐데이터 과제 분석 보고서 마스터 프리젠테이션 생성 스크립트 (19 Slides 완결본)
스토리라인: docs/03_ppt_storyboard.md 기반
폰트: 맑은 고딕 (Malgun Gothic)
레이아웃: 16:9 와이드스크린 (13.333" x 7.5")
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# -------------------------------------------------------------
# 색상 정의 (Color Palette)
# -------------------------------------------------------------
NAVY = RGBColor(15, 23, 42)       # #0F172A
SLATE = RGBColor(51, 65, 85)      # #334155
MUTED = RGBColor(100, 116, 139)   # #64748B
LIGHT_BG = RGBColor(248, 250, 252)# #F8FAFC
CARD_BG = RGBColor(241, 245, 249) # #F1F5F9
CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0
WHITE = RGBColor(255, 255, 255)   # #FFFFFF
ORANGE = RGBColor(234, 88, 12)    # #EA580C
RED = RGBColor(220, 38, 38)       # #DC2626
GREEN = RGBColor(5, 150, 105)     # #059669
GREEN_LIGHT = RGBColor(236, 253, 245) # #ECFDF5
RED_LIGHT = RGBColor(254, 242, 242)   # #FEF2F2
BLUE_ACCENT = RGBColor(37, 99, 235)  # #2563EB

FONT_FAMILY = "맑은 고딕"

BASE_DIR = r"C:\Users\nextb\.gemini\antigravity-ide\scratch\puzzle_data"
FIGURES_DIR = os.path.join(BASE_DIR, "outputs", "figures")
OUT_PPTX_1 = os.path.join(BASE_DIR, "outputs", "pptx", "repair_analysis_full_presentation.pptx")
OUT_PPTX_2 = r"c:\Users\nextb\OneDrive\Desktop\퍼즐데이터\수리프로세스_분석보고서_최종_19slides.pptx"

# -------------------------------------------------------------
# 헬퍼 함수
# -------------------------------------------------------------
def set_font(run, name=FONT_FAMILY, size_pt=14, bold=False, color=NAVY):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = color

def create_shape(slide, shape_type, left, top, width, height, fill_color, border_color=None, border_width_pt=1):
    shp = slide.shapes.add_shape(shape_type, left, top, width, height)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill_color
    if border_color:
        shp.line.color.rgb = border_color
        shp.line.width = Pt(border_width_pt)
    else:
        shp.line.fill.background()
    return shp

def add_header(slide, kicker, title, category=None):
    # 상단 카테고리 / 키커 뱃지
    tx_kicker = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(10), Inches(0.35))
    tf_k = tx_kicker.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    run_k = p_k.add_run()
    run_k.text = kicker.upper()
    set_font(run_k, size_pt=11, bold=True, color=ORANGE)

    # 슬라이드 메인 헤드라인 (두괄식)
    tx_title = slide.shapes.add_textbox(Inches(0.6), Inches(0.72), Inches(12.13), Inches(0.75))
    tf_t = tx_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    run_t = p_t.add_run()
    run_t.text = title
    set_font(run_t, size_pt=20, bold=True, color=NAVY)

    # 슬라이드 번호 안내 / 우측 파트 뱃지
    if category:
        badge = create_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), Inches(0.4), Inches(1.9), Inches(0.32), SLATE)
        tf_b = badge.text_frame
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        r_b = p_b.add_run()
        r_b.text = category
        set_font(r_b, size_pt=10, bold=True, color=WHITE)

def add_source(slide, text):
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(7.08), Inches(12.13), Inches(0.25))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    set_font(run, size_pt=9.5, bold=False, color=MUTED)

# -------------------------------------------------------------
# 메인 빌드 시작
# -------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# =============================================================
# SLIDE 01: 표지 (Title Cover)
# =============================================================
s1 = prs.slides.add_slide(blank_layout)
# 다크 네이비 배경
bg1 = create_shape(s1, MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5), NAVY)

# 좌측 상단 뱃지
b1 = create_shape(s1, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(3.2), Inches(0.45), SLATE)
p_b1 = b1.text_frame.paragraphs[0]
p_b1.alignment = PP_ALIGN.CENTER
r_b1 = p_b1.add_run()
r_b1.text = "채용 과제 전형 최종 보고서"
set_font(r_b1, size_pt=12, bold=True, color=WHITE)

# 대형 메인 타이틀
tx_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(7.8), Inches(2.6))
tf_t = tx_title.text_frame
tf_t.word_wrap = True
p1 = tf_t.paragraphs[0]
r1 = p1.add_run()
r1.text = "프로세스 마이닝 기반\n공공임대주택 수리 프로세스\n진단 및 운영 최적화 방안"
set_font(r1, size_pt=34, bold=True, color=WHITE)

# 서브 타이틀
tx_sub = s1.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(7.8), Inches(1.0))
tf_s = tx_sub.text_frame
tf_s.word_wrap = True
p_s = tf_s.paragraphs[0]
r_s = p_s.add_run()
r_s.text = "5대 무손실 전처리, 실사 대기 병목(76.8h) 원인 규명 및\n3대 데이터 기반 TO-BE 전략 수립"
set_font(r_s, size_pt=16, bold=False, color=RGBColor(203, 213, 225))

# 하단 제출 정보
tx_info = s1.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(7.8), Inches(0.4))
tf_i = tx_info.text_frame
p_i = tf_i.paragraphs[0]
r_i = p_i.add_run()
r_i.text = "퍼즐데이터 채용 전형   |   16:9 Widescreen Analysis Report"
set_font(r_i, size_pt=12, bold=False, color=MUTED)

# 우측 3대 KPI 콜아웃 카드
kpi_items = [
    ("13,262행", "이벤트 로그 원천 무손실 보존", "100% 무결성 복원", WHITE),
    ("90.5%", "리드타임 중 공정 간 단순 대기", "현장 국면 집중 98.0%", ORANGE),
    ("▼ 65.1%", "TO-BE 리드타임 획기적 단축", "4.4일 ➔ 1.5일 (36.0h)", RGBColor(52, 211, 153))
]
for idx, (val, title, desc, col) in enumerate(kpi_items):
    top_pos = Inches(1.5 + idx * 1.8)
    card_kpi = create_shape(s1, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.0), top_pos, Inches(3.5), Inches(1.55), RGBColor(30, 41, 59))
    
    # 텍스트
    tx_k = s1.shapes.add_textbox(Inches(9.25), top_pos + Inches(0.12), Inches(3.0), Inches(1.3))
    tf_k = tx_k.text_frame
    tf_k.word_wrap = True
    
    p_val = tf_k.paragraphs[0]
    r_val = p_val.add_run()
    r_val.text = val
    set_font(r_val, size_pt=32, bold=True, color=col)
    
    p_tl = tf_k.add_paragraph()
    r_tl = p_tl.add_run()
    r_tl.text = title
    set_font(r_tl, size_pt=13, bold=True, color=WHITE)
    
    p_ds = tf_k.add_paragraph()
    r_ds = p_ds.add_run()
    r_ds.text = desc
    set_font(r_ds, size_pt=11, bold=False, color=RGBColor(148, 163, 184))

print("Slide 01 generated.")

# =============================================================
# SLIDE 02: 목차 (Table of Contents)
# =============================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Agenda", "원천 데이터 전처리부터 심층 프로세스 분석, 실현 가능한 TO-BE 전략까지", "Part 00. 인트로")

parts = [
    ("PART 01", "데이터 진단\n및 전처리", "질문 1 대응", [
        "이벤트 로그 구조 프로파일링",
        "5대 비정상 결측치 인과 복원",
        "100% 무손실 927건 코호트 확립"
    ], NAVY),
    ("PART 02", "프로세스 마이닝\n심층 분석", "질문 2 대응", [
        "E2E 기준 프로세스 모델 도출",
        "거시 리드타임 대기 90.5% 분해",
        "3대 병목(접수·현장·품질) 규명",
        "다중 OLS 회귀 영향 요인"
    ], ORANGE),
    ("PART 03", "프로세스\n최적화 방안", "질문 3 대응", [
        "소통 통제: Web 자가 예약 체계",
        "대기 단축: 1회 방문 원샷 직행",
        "정량적 ROI: 리드타임 65% 감축"
    ], GREEN),
    ("PART 04", "엔지니어링\n신뢰성 보증", "품질 검증", [
        "MySQL 마스터 뷰 무결성 검증",
        "파이썬 통계 파이프라인 재현성",
        "질의응답 (Q&A Defense)"
    ], SLATE)
]

col_w = Inches(2.85)
col_gap = Inches(0.24)
for i, (p_num, p_title, p_tag, p_bullets, p_col) in enumerate(parts):
    left_pos = Inches(0.6 + i * (2.85 + 0.24))
    c = create_shape(s2, MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.75), col_w, Inches(4.9), CARD_BG, CARD_BORDER)
    
    tx = s2.shapes.add_textbox(left_pos + Inches(0.25), Inches(1.95), col_w - Inches(0.5), Inches(4.5))
    tf = tx.text_frame
    tf.word_wrap = True
    
    # 파트 번호
    p_no = tf.paragraphs[0]
    r_no = p_no.add_run()
    r_no.text = p_num
    set_font(r_no, size_pt=22, bold=True, color=p_col)
    
    # 타이틀
    p_ti = tf.add_paragraph()
    r_ti = p_ti.add_run()
    r_ti.text = p_title
    set_font(r_ti, size_pt=16, bold=True, color=NAVY)
    
    # 뱃지
    p_bg = tf.add_paragraph()
    r_bg = p_bg.add_run()
    r_bg.text = f"[{p_tag}]"
    set_font(r_bg, size_pt=11, bold=True, color=MUTED)
    
    # 구분선 대체 여백 후 불릿
    for b in p_bullets:
        p_bl = tf.add_paragraph()
        r_bl = p_bl.add_run()
        r_bl.text = f"•  {b}"
        set_font(r_bl, size_pt=12.5, bold=False, color=SLATE)

add_source(s2, "보고서 구성 안내: 질문 1 (Slide 04~06) ➔ 질문 2 (Slide 07~13) ➔ 질문 3 (Slide 14~15) ➔ 신뢰성 (Slide 16)")
print("Slide 02 generated.")

# =============================================================
# SLIDE 03: Executive Summary & 통괄 핵심 가설
# =============================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Executive Summary", "현장의 '대기시간'을 줄이고, 이해관계자 간 '소통'을 통제하면 프로세스가 혁신된다", "Part 00. 인트로")

# 상단 통괄 명제 배너
b_top = create_shape(s3, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(12.13), Inches(0.9), NAVY)
tx_top = s3.shapes.add_textbox(Inches(0.8), Inches(1.72), Inches(11.7), Inches(0.75))
tf_top = tx_top.text_frame
tf_top.word_wrap = True
p_tt = tf_top.paragraphs[0]
r_tt = p_tt.add_run()
r_tt.text = "🎯 핵심 발견: 수리가 지연되는 근본 원인은 기사의 작업 속도가 아니라, 공정 간 '단순 대기(90.5%)'와 비실시간 접수의 '소통 공백(6.6배 지연)'이다."
set_font(r_tt, size_pt=14, bold=True, color=WHITE)

cards_s3 = [
    ("01. 원천 진단", "100% 무손실 복원", NAVY, [
        ("이벤트 로그 특성 반영", "90% 결측은 후속 미발생 정상치 (무죄)"),
        ("시스템 에러 특정", "단 20행(0.15%)을 도메인 인과로 복원"),
        ("분석 모수 확립", "시간 역전 0건 & 927건 클린 코호트 확립")
    ]),
    ("02. 병목 규명", "대기 90.5% + 소통 지연", ORANGE, [
        ("접수 국면 소통 병목", "Web/우편의 비동기 조율 지연 ➔ 6.6배 폭증"),
        ("현장 국면 실사 적체", "기사 CAPA(69건/일) 초과 ➔ 76.8h 대기"),
        ("사내 수리 착수 지연", "부품 조달 대기 30.5h + 하자 루프 10.1일")
    ]),
    ("03. 처방 및 효과", "리드타임 ▼ 65% 감축", GREEN, [
        ("Web 자가 일정 예약", "비동기 핑퐁 차단 ➔ 교차 인계 0건화"),
        ("1회 방문 원샷 직행", "87.3% 사전 키팅 직행 ➔ 546시간 회수"),
        ("외주 패스트트랙", "1차 실패 시 즉시 이관 ➔ 1.5일로 단축")
    ])
]

cw3 = Inches(3.85)
cg3 = Inches(0.29)
for i, (c_hd, c_kpi, c_col, c_rows) in enumerate(cards_s3):
    left_pos = Inches(0.6 + i * (3.85 + 0.29))
    create_shape(s3, MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(2.75), cw3, Inches(4.15), CARD_BG, CARD_BORDER)
    
    # 카드 헤더 스트립
    create_shape(s3, MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(2.75), cw3, Inches(0.75), c_col)
    tx_ch = s3.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.8), cw3 - Inches(0.4), Inches(0.65))
    tf_ch = tx_ch.text_frame
    p_ch1 = tf_ch.paragraphs[0]
    r_ch1 = p_ch1.add_run()
    r_ch1.text = c_hd + "  |  " + c_kpi
    set_font(r_ch1, size_pt=13, bold=True, color=WHITE)
    
    # 카드 내용
    tx_cb = s3.shapes.add_textbox(left_pos + Inches(0.25), Inches(3.65), cw3 - Inches(0.5), Inches(3.1))
    tf_cb = tx_cb.text_frame
    tf_cb.word_wrap = True
    for idx_r, (sub_tit, sub_desc) in enumerate(c_rows):
        p_st = tf_cb.paragraphs[0] if idx_r == 0 else tf_cb.add_paragraph()
        r_st = p_st.add_run()
        r_st.text = f"■  {sub_tit}\n"
        set_font(r_st, size_pt=12.5, bold=True, color=NAVY)
        r_sd = p_st.add_run()
        r_sd.text = f"    {sub_desc}\n"
        set_font(r_sd, size_pt=11.5, bold=False, color=SLATE)

add_source(s3, "통괄 요약: 분석 전체를 관통하는 핵심 메커니즘 도식화 (E2E Lead Time 105.9h ➔ 36.0h)")
print("Slide 03 generated.")

# =============================================================
# SLIDE 04: [질문 1] 원천 데이터 수사 프로파일링 및 결측치 2원화 (Before)
# =============================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Part 01 · 질문 1  |  Before Profiling", "정상 결측은 100% 보존하고, 시스템 에러 20행(0.15%)만 복원 타겟으로 특정했다", "Part 01. 질문 1")

# 좌측 원천 메타 프로파일 카드
create_shape(s4, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(3.7), Inches(5.25), CARD_BG, CARD_BORDER)
tx_m = s4.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(3.2), Inches(4.8))
tf_m = tx_m.text_frame
tf_m.word_wrap = True

p_m1 = tf_m.paragraphs[0]
r_m1 = p_m1.add_run()
r_m1.text = "13,262행\n"
set_font(r_m1, size_pt=36, bold=True, color=NAVY)
r_m1_s = p_m1.add_run()
r_m1_s.text = "총 이벤트 로그 레코드\n\n"
set_font(r_m1_s, size_pt=13, bold=False, color=MUTED)

r_m2 = p_m1.add_run()
r_m2.text = "1,000건  ·  13개 속성\n"
set_font(r_m2, size_pt=22, bold=True, color=SLATE)
r_m2_s = p_m1.add_run()
r_m2_s.text = "수리 의뢰 케이스 및 데이터 컬럼\n\n"
set_font(r_m2_s, size_pt=13, bold=False, color=MUTED)

r_m3 = p_m1.add_run()
r_m3.text = "📌 이벤트 로그의 본질\n"
set_font(r_m3, size_pt=13, bold=True, color=ORANGE)
r_m3_s = p_m1.add_run()
r_m3_s.text = "1건 1행의 정형 데이터가 아닌, 수리 진행 단계마다 타임스탬프와 함께 적재되는 동적 트랜잭션 로그 구조임."
set_font(r_m3_s, size_pt=11.5, bold=False, color=SLATE)

# 우측 상단 이미지 (EDA-01.png)
fig_eda01 = os.path.join(FIGURES_DIR, "EDA-01.png")
if os.path.exists(fig_eda01):
    s4.shapes.add_picture(fig_eda01, Inches(4.55), Inches(1.65), width=Inches(8.18))

# 우측 하단 2원화 판정표 카드
create_shape(s4, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.55), Inches(5.0), Inches(8.18), Inches(1.9), WHITE, CARD_BORDER)
tx_judge = s4.shapes.add_textbox(Inches(4.75), Inches(5.1), Inches(7.78), Inches(1.7))
tf_j = tx_judge.text_frame
tf_j.word_wrap = True

p_j1 = tf_j.paragraphs[0]
r_j1 = p_j1.add_run()
r_j1.text = "🟩 정상 결측 (구조적 Null, 86.0% ~ 93.0%): "
set_font(r_j1, size_pt=11.5, bold=True, color=GREEN)
r_j1_d = p_j1.add_run()
r_j1_d.text = "RepairCode, EstimatedRepairTime 등 7개 속성 (12,335건) ➔ [무죄] 후속 수리 미발생 자연 결측으로 100% 보존\n"
set_font(r_j1_d, size_pt=11, bold=False, color=SLATE)

p_j2 = tf_j.add_paragraph()
r_j2 = p_j2.add_run()
r_j2.text = "🟥 비정상 결측 (시스템 에러, 0.015% ~ 0.098%): "
set_font(r_j2, size_pt=11.5, bold=True, color=RED)
r_j2_d = p_j2.add_run()
r_j2_d.text = "taskID(2건), originator(2건), eventtype(5건), date/time(13건) ➔ [유죄] 18개 케이스, 단 20행만 정밀 복원 타겟 특정\n"
set_font(r_j2_d, size_pt=11, bold=False, color=SLATE)

p_j3 = tf_j.add_paragraph()
r_j3 = p_j3.add_run()
r_j3.text = "⬜ 진공 구간 (0.1% ~ 86.0%): "
set_font(r_j3, size_pt=11.5, bold=True, color=MUTED)
r_j3_d = p_j3.add_run()
r_j3_d.text = "결측 비율이 중간 구간에 위치한 컬럼 0개 ➔ 완벽한 양극단 이봉분포로 정상/비정상 기준의 객관성 입증"
set_font(r_j3_d, size_pt=11, bold=False, color=SLATE)

add_source(s4, "출처: repair2.csv 원천 프로파일링 (EDA-01) · 13개 속성 전수 결측률 조사 결과")
print("Slide 04 generated.")

# =============================================================
# SLIDE 05: [질문 1] 5대 비정상 결측치 교정 및 도메인 인과 복원 (CASE 1~5)
# =============================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Part 01 · 질문 1  |  CASE 1 ~ 5", "행 삭제나 단순 대체 없이, 도메인 인과 규칙으로 20행을 100% 무손실 복원했다", "Part 01. 질문 1")

cases = [
    ("CASE 1", "taskID (작업명)", "결측 2건", "contact 속성은 FirstContact에만 기록되는 고유 속성", "FirstContact · InformClientSurvey 확정 복원 ➔ 누락 0건"),
    ("CASE 2", "originator (담당자)", "결측 2건", "동일 작업의 시작(start)-완료(complete) 담당자 100% 일치", "짝 이벤트 담당자(Anne, Paul) 상호 승계 복원 ➔ 누락 0건"),
    ("CASE 3", "eventtype (상태)", "결측 5건", "기간 작업은 start➔complete 1:1 짝, 마일스톤은 complete 단독", "1:1 페어(3건) 및 마일스톤(2건) 100% 복원 ➔ 누락 0건"),
    ("CASE 4", "date (일자 이상치)", "총 879건 (결측13+오기866)", "1905년 리셋 및 2020~2022년 미래 연도 오기입. 선후행 순서 구간 제약 적용", "단일 후보 640건 확정 + 앵커 최근접 219건 매핑 ➔ 1970년 통일"),
    ("CASE 5", "time (시각 결측·더미)", "총 28건 (결측13+더미15)", "표본 34% 축소 한계 극복 ➔ 접수 구간 정상 모수 751건(75.1%) 확보", "자정 7건 보존 + 대표값(중앙값 4.0분) 앵커 역산 ➔ 시간 역전 0건")
]

rh = Inches(0.82)
rg = Inches(0.08)
for i, (c_tag, c_attr, c_amt, c_clue, c_fix) in enumerate(cases):
    top_pos = Inches(1.65 + i * (0.82 + 0.08))
    create_shape(s5, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), top_pos, Inches(12.13), rh, CARD_BG, CARD_BORDER)
    
    # 텍스트 박스 3단
    tx_c = s5.shapes.add_textbox(Inches(0.8), top_pos + Inches(0.08), Inches(3.0), rh - Inches(0.16))
    tf_c = tx_c.text_frame
    p_c1 = tf_c.paragraphs[0]
    r_tag = p_c1.add_run()
    r_tag.text = f"{c_tag}  "
    set_font(r_tag, size_pt=11, bold=True, color=ORANGE)
    r_attr = p_c1.add_run()
    r_attr.text = f"{c_attr}\n"
    set_font(r_attr, size_pt=13, bold=True, color=NAVY)
    r_amt = p_c1.add_run()
    r_amt.text = c_amt
    set_font(r_amt, size_pt=10.5, bold=True, color=RED)
    
    tx_clue = s5.shapes.add_textbox(Inches(3.9), top_pos + Inches(0.08), Inches(4.3), rh - Inches(0.16))
    tf_clue = tx_clue.text_frame
    tf_clue.word_wrap = True
    p_cl = tf_clue.paragraphs[0]
    r_cl_t = p_cl.add_run()
    r_cl_t.text = "🔍 도메인 단서: "
    set_font(r_cl_t, size_pt=11, bold=True, color=SLATE)
    r_cl = p_cl.add_run()
    r_cl.text = c_clue
    set_font(r_cl, size_pt=11, bold=False, color=SLATE)
    
    tx_fix = s5.shapes.add_textbox(Inches(8.3), top_pos + Inches(0.08), Inches(4.3), rh - Inches(0.16))
    tf_fix = tx_fix.text_frame
    tf_fix.word_wrap = True
    p_fx = tf_fix.paragraphs[0]
    r_fx_t = p_fx.add_run()
    r_fx_t.text = "➔ 복원 판정: "
    set_font(r_fx_t, size_pt=11, bold=True, color=GREEN)
    r_fx = p_fx.add_run()
    r_fx.text = c_fix
    set_font(r_fx, size_pt=11, bold=True, color=NAVY)

# 하단 3대 무결성 성과 배지
badges_s5 = [
    ("데이터 100% 무손실", "임의 행 삭제 0건 (13,262행 전수 보존)"),
    ("통계적 강건성 입증", "표본 34% 축소 한계 극복 (751건 정상 모수 활용)"),
    ("인과 무결성 보증", "공정 간 시간 역전 0건 달성 & 927건 코호트 확립")
]
bw5 = Inches(3.85)
bg5 = Inches(0.29)
for i, (b_title, b_desc) in enumerate(badges_s5):
    l_pos = Inches(0.6 + i * (3.85 + 0.29))
    create_shape(s5, MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(6.25), bw5, Inches(0.68), GREEN_LIGHT, GREEN)
    tx_b = s5.shapes.add_textbox(l_pos + Inches(0.15), Inches(6.28), bw5 - Inches(0.3), Inches(0.6))
    tf_b = tx_b.text_frame
    p_b = tf_b.paragraphs[0]
    r_bt = p_b.add_run()
    r_bt.text = f"✓ {b_title}\n"
    set_font(r_bt, size_pt=11.5, bold=True, color=GREEN)
    r_bd = p_b.add_run()
    r_bd.text = b_desc
    set_font(r_bd, size_pt=10.5, bold=False, color=SLATE)

add_source(s5, "출처: analysis.ipynb Cell 18, 20, 51, 53, 77, 81 복원 파이프라인 무결성 검증 결과")
print("Slide 05 generated.")

# =============================================================
# SLIDE 06: [질문 1] 전처리 무결성 검증 및 927건 분석 코호트 확립 (After)
# =============================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Part 01 · 질문 1  |  After Profiling", "시간 역전 0건을 입증했고, 오접수 73건을 격리해 927건 클린 코호트를 확립했다", "Part 01. 질문 1")

# 좌측: Before vs After 무결성 검증 표 카드
create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(6.0), Inches(5.25), WHITE, CARD_BORDER)
tx_tbl_title = s6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(0.4))
tf_tt = tx_tbl_title.text_frame
p_tt = tf_tt.paragraphs[0]
r_tt = p_tt.add_run()
r_tt.text = "📊 Before vs After 데이터 무결성 검증표"
set_font(r_tt, size_pt=14, bold=True, color=NAVY)

# 표 생성
table_shape = s6.shapes.add_table(5, 3, Inches(0.8), Inches(2.25), Inches(5.6), Inches(3.6))
tbl = table_shape.table
tbl.columns[0].width = Inches(1.8)
tbl.columns[1].width = Inches(1.6)
tbl.columns[2].width = Inches(2.2)

tbl_data = [
    [("검증 항목", True, WHITE, NAVY), ("Before (원천)", True, WHITE, MUTED), ("After (정제)", True, WHITE, GREEN)],
    [("총 이벤트 수", True, NAVY, None), ("13,262행", False, SLATE, None), ("13,262행 (100% 보존)", True, GREEN, None)],
    [("필수 속성 결측", True, NAVY, None), ("20건 누락", False, RED, None), ("0건 (100% 복원)", True, GREEN, None)],
    [("일자 연도 이상치", True, NAVY, None), ("866건 오기입", False, RED, None), ("0건 (1970년 통일)", True, GREEN, None)],
    [("프로세스 시간 역전", True, NAVY, None), ("음수 소요시간", False, RED, None), ("0건 (3,711 페어 양수)", True, GREEN, None)]
]

for row_idx, row in enumerate(tbl_data):
    for col_idx, (text, is_bold, text_col, bg_col) in enumerate(row):
        c_cell = tbl.cell(row_idx, col_idx)
        if bg_col:
            c_cell.fill.solid()
            c_cell.fill.fore_color.rgb = bg_col
        else:
            c_cell.fill.solid()
            c_cell.fill.fore_color.rgb = LIGHT_BG if row_idx % 2 == 1 else WHITE
        p = c_cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
        r = p.add_run()
        r.text = text
        set_font(r, size_pt=11.5, bold=is_bold, color=text_col)

# 표 하단 결과 요약 배너
create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.05), Inches(5.6), Inches(0.65), GREEN_LIGHT, GREEN)
tx_res = s6.shapes.add_textbox(Inches(0.9), Inches(6.1), Inches(5.4), Inches(0.55))
tf_res = tx_res.text_frame
p_res = tf_res.paragraphs[0]
r_res = p_res.add_run()
r_res.text = "✓ 전처리 결과: 필수 결측 20건 ➔ 0건, 임의 행 삭제 0건 (완전 무결)"
set_font(r_res, size_pt=11.5, bold=True, color=GREEN)

# 우측: 코호트 분리 및 4대 접수 채널 카드
create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.65), Inches(5.93), Inches(5.25), CARD_BG, CARD_BORDER)

# 상단 메타 칩 4개
chips = [("1,000건", "수리 케이스"), ("890채", "고유 주택"), ("13개", "데이터 속성"), ("14행", "케이스당 중앙값")]
chw = Inches(1.3)
for i, (v, l) in enumerate(chips):
    cp_left = Inches(7.0 + i * 1.36)
    create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, cp_left, Inches(1.85), chw, Inches(0.85), WHITE, CARD_BORDER)
    tx_cp = s6.shapes.add_textbox(cp_left, Inches(1.9), chw, Inches(0.75))
    tf_cp = tx_cp.text_frame
    p_cp1 = tf_cp.paragraphs[0]
    p_cp1.alignment = PP_ALIGN.CENTER
    r_cp1 = p_cp1.add_run()
    r_cp1.text = f"{v}\n"
    set_font(r_cp1, size_pt=14, bold=True, color=NAVY)
    r_cp2 = p_cp1.add_run()
    r_cp2.text = l
    set_font(r_cp2, size_pt=10, bold=False, color=MUTED)

# 코호트 2원화 분리 박스
create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(2.9), Inches(5.53), Inches(1.2), WHITE, GREEN)
tx_coh1 = s6.shapes.add_textbox(Inches(7.2), Inches(2.95), Inches(5.1), Inches(1.1))
tf_c1 = tx_coh1.text_frame
tf_c1.word_wrap = True
p_c1 = tf_c1.paragraphs[0]
r_c1_t = p_c1.add_run()
r_c1_t.text = "🟩 정상 수리 완결 코호트: 927건 (92.7%)\n"
set_font(r_c1_t, size_pt=13, bold=True, color=GREEN)
r_c1_d = p_c1.add_run()
r_c1_d.text = "현장 실사 및 수리가 정상 완결된 순수 분석 모수 ➔ [질문 2 프로세스 분석 대상]"
set_font(r_c1_d, size_pt=11.5, bold=False, color=SLATE)

create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(4.25), Inches(5.53), Inches(1.05), WHITE, CARD_BORDER)
tx_coh2 = s6.shapes.add_textbox(Inches(7.2), Inches(4.3), Inches(5.1), Inches(0.95))
tf_c2 = tx_coh2.text_frame
tf_c2.word_wrap = True
p_c2 = tf_c2.paragraphs[0]
r_c2_t = p_c2.add_run()
r_c2_t.text = "⬜ 오접수 조기 종결: 73건 (7.3%)\n"
set_font(r_c2_t, size_pt=12.5, bold=True, color=MUTED)
r_c2_d = p_c2.add_run()
r_c2_d.text = "타 기관 관할 주택(InformClientWrongPlace) ➔ 분석 왜곡 방지를 위해 격리"
set_font(r_c2_d, size_pt=11, bold=False, color=SLATE)

# 4대 접수 채널 균등 분포 바
tx_ch_t = s6.shapes.add_textbox(Inches(7.0), Inches(5.45), Inches(5.53), Inches(0.3))
tf_cht = tx_ch_t.text_frame
p_cht = tf_cht.paragraphs[0]
r_cht = p_cht.add_run()
r_cht.text = "📌 927건 코호트의 접수 채널 분포 (실측치)"
set_font(r_cht, size_pt=11.5, bold=True, color=SLATE)

ch_items = [("Phone", "251건 (27.1%)"), ("Web", "241건 (26.0%)"), ("Personal", "228건 (24.6%)"), ("Letter", "207건 (22.3%)")]
for i, (cn, cp) in enumerate(ch_items):
    c_left = Inches(7.0 + i * 1.39)
    create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(5.8), Inches(1.33), Inches(0.9), WHITE, CARD_BORDER)
    tx_ci = s6.shapes.add_textbox(c_left, Inches(5.85), Inches(1.33), Inches(0.8))
    tf_ci = tx_ci.text_frame
    p_ci = tf_ci.paragraphs[0]
    p_ci.alignment = PP_ALIGN.CENTER
    r_ci1 = p_ci.add_run()
    r_ci1.text = f"{cn}\n"
    set_font(r_ci1, size_pt=12, bold=True, color=NAVY)
    r_ci2 = p_ci.add_run()
    r_ci2.text = cp
    set_font(r_ci2, size_pt=10, bold=False, color=SLATE)

add_source(s6, "출처: repair_cleaned.csv (13,262행) 직접 프로파일링 결과 · 순수 분석 코호트 927건 확립")
print("Slide 06 generated.")

# =============================================================
# SLIDE 07: [질문 2-1] AS-IS 표준 프로세스 및 엔드투엔드(E2E) 경로
# =============================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Part 02 · 질문 2-1  |  AS-IS 기준 프로세스 모델", "단방향 에스컬레이션과 병렬 정산이 입증된 E2E 기준 프로세스 모델", "Part 02. 질문 2")

# 프로세스 맵 이미지 임베딩
fig_map = os.path.join(FIGURES_DIR, "repair_process_map.png")
if os.path.exists(fig_map):
    s7.shapes.add_picture(fig_map, Inches(0.6), Inches(1.6), width=Inches(12.13), height=Inches(3.3))

# 하단 3대 국면 추출 데이터 근거 카드 3단
c7_items = [
    ("01 접수 국면 추출 근거", [
        ("조기 이탈 분기", "FirstContact 1,000건 중 73건(7.3%)이 InformClientWrongPlace로 즉시 종결"),
        ("접수 종료 앵커", "일정 조율 직후 InformClientSurvey(System)가 0초에 자동 발송되어 국면 확정")
    ], NAVY),
    ("02 현장 국면 추출 근거 (단방향)", [
        ("단방향 에스컬레이션", "수리는 즉시 ➔ 사내 ➔ 외주로만 전이되며, 외주 후 사내 역류는 0건 (0.0%)"),
        ("수리 완료 앵커", "기사의 완료 커밋 즉시 시스템이 RepairReady(927건)를 자동 발행하여 정산 전환")
    ], ORANGE),
    ("03 정산 국면 추출 근거 (AND-Join)", [
        ("대칭 병렬 선행비", "고객통보 선행 50.6%(469건) vs 재무전송 선행 49.2%(456건)로 완벽한 50:50 대칭"),
        ("자동 마감 일치율", "TicketReady는 두 작업 선행 0건, 후행 작업 완료 시각과 99.8%(925건) 일치")
    ], GREEN)
]

c7_w = Inches(3.85)
c7_g = Inches(0.29)
for i, (head, rows, col) in enumerate(c7_items):
    l_pos = Inches(0.6 + i * (3.85 + 0.29))
    create_shape(s7, MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(5.1), c7_w, Inches(1.85), CARD_BG, CARD_BORDER)
    
    tx = s7.shapes.add_textbox(l_pos + Inches(0.2), Inches(5.2), c7_w - Inches(0.4), Inches(1.65))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_h = tf.paragraphs[0]
    r_h = p_h.add_run()
    r_h.text = f"{head}\n"
    set_font(r_h, size_pt=12.5, bold=True, color=col)
    
    for r_tit, r_val in rows:
        p_r = tf.add_paragraph()
        r_rt = p_r.add_run()
        r_rt.text = f"• {r_tit}: "
        set_font(r_rt, size_pt=10.5, bold=True, color=NAVY)
        r_rv = p_r.add_run()
        r_rv.text = r_val
        set_font(r_rv, size_pt=10, bold=False, color=SLATE)

add_source(s7, "출처: repair_cleaned.csv 프로세스 마이닝 모델 (노드 수치: 이벤트 발생 건수, 엣지: 전이 건수)")
print("Slide 07 generated.")

# =============================================================
# SLIDE 08: [질문 2-2 총괄] 거시 리드타임 분해: 실작업(9.5%) vs 대기(90.5%)
# =============================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Part 02 · 질문 2-2  |  거시 리드타임 분해", "리드타임 105.9시간의 90.5%는 공정 간 단순 대기이며, 98.0%가 현장 국면에 집중된다", "Part 02. 질문 2")

# 상단 좌측: slide08_macro_leadtime_breakdown.png 차트
fig_s8 = os.path.join(FIGURES_DIR, "slide08_macro_leadtime_breakdown.png")
if os.path.exists(fig_s8):
    s8.shapes.add_picture(fig_s8, Inches(0.6), Inches(1.65), width=Inches(7.8), height=Inches(3.3))

# 상단 우측: 핵심 KPI 카드 2개
kpi_s8 = [
    ("90.5%", "공정 간 단순 대기", "95.8시간 / 총 105.9시간 (실작업 9.5%)", ORANGE),
    ("98.0%", "대기의 현장 국면 집중도", "현장 대기 93.9h / 전체 대기 95.8h (정산 대기 0h)", RED)
]
for i, (v, t, d, col) in enumerate(kpi_s8):
    t_pos = Inches(1.65 + i * 1.7)
    create_shape(s8, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), t_pos, Inches(4.13), Inches(1.55), CARD_BG, CARD_BORDER)
    tx = s8.shapes.add_textbox(Inches(8.85), t_pos + Inches(0.12), Inches(3.6), Inches(1.3))
    tf = tx.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = f"{v}  "
    set_font(r1, size_pt=34, bold=True, color=col)
    r1_t = p1.add_run()
    r1_t.text = f"{t}\n"
    set_font(r1_t, size_pt=14, bold=True, color=NAVY)
    
    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = d
    set_font(r2, size_pt=11.5, bold=False, color=SLATE)

# 하단 3대 병목 내비게이션 카드
bottlenecks = [
    ("01 접수 국면 일정 조율 병목", "비동기 소통 대기 1.9h (접수의 90.4%)", [
        "전화·대면(479건): 지연율 0%",
        "웹·우편(448건): 비동기 핑퐁 발생",
        "교차 인계 123건 ➔ 6.6배 폭증 (Slide 09)"
    ], NAVY),
    ("02 현장 국면 실사 방문 대기 (1위)", "76.8h = 현장 국면의 78.2% 독점 🚨", [
        "일 135건 인입 vs 기사 실사 69건 (51.1%)",
        "매일 약 66건 적체 누적",
        "피크 시점 403건 대기열(WIP) 폭증 (Slide 10)"
    ], ORANGE),
    ("03 현장 국면 수리 착수·하자 루프", "착수 대기 15.9h (사내수리 30.5h)", [
        "즉시·외주는 대기 0h, 사내수리만 지연",
        "원인: 부품 조달 및 재방문 공백",
        "하자 재방문 루프 26건, 최대 10.1일 (Slide 11)"
    ], RED)
]

c8_w = Inches(3.85)
c8_g = Inches(0.29)
for i, (hd, badge, b_list, col) in enumerate(bottlenecks):
    l_pos = Inches(0.6 + i * (3.85 + 0.29))
    create_shape(s8, MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(5.15), c8_w, Inches(1.85), CARD_BG, CARD_BORDER)
    tx = s8.shapes.add_textbox(l_pos + Inches(0.2), Inches(5.2), c8_w - Inches(0.4), Inches(1.7))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_h = tf.paragraphs[0]
    r_h = p_h.add_run()
    r_h.text = f"{hd}\n"
    set_font(r_h, size_pt=12.5, bold=True, color=NAVY)
    r_b = p_h.add_run()
    r_b.text = f"• {badge}\n"
    set_font(r_b, size_pt=11, bold=True, color=col)
    
    for item in b_list:
        p_i = tf.add_paragraph()
        r_i = p_i.add_run()
        r_i.text = f"- {item}"
        set_font(r_i, size_pt=10.5, bold=False, color=SLATE)

add_source(s8, "출처: analysis.sql 2절 리드타임 분해 집계표 · E2E Total 105.9h (실작업 10.1h, 단순 대기 95.8h)")
print("Slide 08 generated.")

# =============================================================
# SLIDE 09: [질문 2-2] 제1대 병목: 접수 일정 조율 병목(1.9h)과 교차 인계 6.6배
# =============================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Part 02 · 질문 2-2  |  제1대 병목: 접수 국면", "접수 지연은 일감 과부하가 아닌 '교차 인계(123건)'에서 기인하며, 소요시간을 6.6배 폭증시킨다", "Part 02. 질문 2")

fig_s9 = os.path.join(FIGURES_DIR, "slide09_reception_bottleneck_3panel.png")
if os.path.exists(fig_s9):
    s9.shapes.add_picture(fig_s9, Inches(0.6), Inches(1.65), width=Inches(12.13), height=Inches(3.4))

s9_cards = [
    ("가설 기각: 물량 부하 무관", "r ≈ 0.08 상관 없음", [
        "일별 접수 인입량(일 10~40건)과 접수 소요시간의 상관계수는 0.08로 거의 무관",
        "접수 창구의 물리적 처리 용량(CAPA) 부족 가설 완전 기각"
    ], MUTED),
    ("핵심 동인: 교차 인계 패널티", "1.2h ➔ 7.9h (6.6배 지연 🚨)", [
        "단독 처리군 (804건, 86.7%): 평균 1.20시간 (중앙값 8.0분) 즉시 완료",
        "교차 인계군 (123건, 13.3%): 평균 7.87시간 (중앙값 5.6시간)으로 6.6배 폭증",
        "상담원 교체 시 컨텍스트 전환 및 이력 재확인 비용 발생"
    ], RED),
    ("반전 통찰: Web 채널의 잠재력", "Web 즉시완료 시 6.8분 최속 ⭐", [
        "실시간 채널(전화/대면): 15분 이내 완료율 100% (인계 0건)",
        "인계 123건 전수(100%)가 비실시간 채널(Web·Letter)에서만 발생",
        "그러나 서류 완비 시 Web 채널은 6.8분으로 전화(8.2분)보다 오히려 최속!"
    ], GREEN)
]

for i, (hd, badge, b_list, col) in enumerate(s9_cards):
    l_pos = Inches(0.6 + i * (3.85 + 0.29))
    create_shape(s9, MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(5.2), c8_w, Inches(1.8), CARD_BG, CARD_BORDER)
    tx = s9.shapes.add_textbox(l_pos + Inches(0.2), Inches(5.25), c8_w - Inches(0.4), Inches(1.65))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_h = tf.paragraphs[0]
    r_h = p_h.add_run()
    r_h.text = f"{hd}\n"
    set_font(r_h, size_pt=12.5, bold=True, color=NAVY)
    r_b = p_h.add_run()
    r_b.text = f"• {badge}\n"
    set_font(r_b, size_pt=11, bold=True, color=col)
    
    for item in b_list:
        p_i = tf.add_paragraph()
        r_i = p_i.add_run()
        r_i.text = f"- {item}"
        set_font(r_i, size_pt=10, bold=False, color=SLATE)

add_source(s9, "출처: slide09_reception_bottleneck_3panel · 927건 접수 트랜잭션 및 인계 전수 분석")
print("Slide 09 generated.")

# =============================================================
# SLIDE 10: [질문 2-2] 제2대 병목: 현장 국면 압도적 대기 76.8h & 403건 WIP
# =============================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Part 02 · 질문 2-2  |  제2대 병목: 현장 국면", "대기시간의 78.2%가 쏠린 '실사 대기(76.8h)'는 기사 CAPA 한계로 누적된 403건의 대기열(WIP)이 원인이다", "Part 02. 질문 2")

fig_s10 = os.path.join(FIGURES_DIR, "slide10_field_bottleneck_wip.png")
if os.path.exists(fig_s10):
    s10.shapes.add_picture(fig_s10, Inches(0.6), Inches(1.65), width=Inches(12.13), height=Inches(3.4))

s10_cards = [
    ("일일 파이프라인 불균형", "소화율 51.1% (일 66건 적체)", [
        "일일 접수 이관량: 일평균 135건 (120~141건)",
        "현장 기사 11인의 실사 처리량: 일평균 69.2건",
        "공급 능력이 수요의 51%에 불과하여 매일 약 66건씩 미처리 적체 누적"
    ], ORANGE),
    ("대기열(WIP) 20배 폭증", "피크 시점 403건 적체 🚨", [
        "1월 1일: 20건 적체 (실사 대기시간 10.7시간)",
        "1월 7일: 403건 적체 피크 도달 (대기열 20배 폭증)",
        "1월 4~6일 유입 건의 평균 실사 대기시간 93.6시간(약 4일) 기록"
    ], RED),
    ("기사 1인당 물리적 한계", "일평균 6.3건 실사 한계", [
        "기사 1인당 일일 6.0~7.1건(순수 실사 4.1~4.8시간) 소화",
        "가구 간 이동 시간 및 1차 즉시수리 병행으로 물리적 CAPA 한계 도달",
        "해법: 헛걸음 실사 생략 및 1회 방문 직행 필수 (Slide 14)"
    ], NAVY)
]

for i, (hd, badge, b_list, col) in enumerate(s10_cards):
    l_pos = Inches(0.6 + i * (3.85 + 0.29))
    create_shape(s10, MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(5.2), c8_w, Inches(1.8), CARD_BG, CARD_BORDER)
    tx = s10.shapes.add_textbox(l_pos + Inches(0.2), Inches(5.25), c8_w - Inches(0.4), Inches(1.65))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_h = tf.paragraphs[0]
    r_h = p_h.add_run()
    r_h.text = f"{hd}\n"
    set_font(r_h, size_pt=12.5, bold=True, color=NAVY)
    r_b = p_h.add_run()
    r_b.text = f"• {badge}\n"
    set_font(r_b, size_pt=11, bold=True, color=col)
    
    for item in b_list:
        p_i = tf.add_paragraph()
        r_i = p_i.add_run()
        r_i.text = f"- {item}"
        set_font(r_i, size_pt=10, bold=False, color=SLATE)

add_source(s10, "출처: slide10_field_bottleneck_wip · analysis.sql L1345, L1583 실사 대기열 동역학 분석")
print("Slide 10 generated.")

# =============================================================
# SLIDE 11: [질문 2-3 & 2-2] 소요시간 영향 요인 및 수리·리워크 병목 실증
# =============================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Part 02 · 질문 2-3 & 2-2  |  소요시간 영향 요인 및 수리·리워크 병목", "리드타임의 87.8%를 결정하는 3대 병목 요인과 현장 수리 리워크(26건)의 지연 충격을 실증했다", "Part 02. 질문 2")

# 좌측: OLS 회귀계수 차트
fig_s11_l = os.path.join(FIGURES_DIR, "slide11_regression_leadtime_drivers.png")
if os.path.exists(fig_s11_l):
    s11.shapes.add_picture(fig_s11_l, Inches(0.6), Inches(1.65), width=Inches(5.9), height=Inches(3.3))

# 우측: 수리 대기 및 리워크 차트
fig_s11_r = os.path.join(FIGURES_DIR, "slide11_repair_delay_rework.png")
if os.path.exists(fig_s11_r):
    s11.shapes.add_picture(fig_s11_r, Inches(6.8), Inches(1.65), width=Inches(5.9), height=Inches(3.3))

# 하단 2단 요약 카드 (좌: 병목 3대 요인, 우: 리워크 품질 결함)
s11_bottom_cards = [
    ("소요시간 3대 병목 요인 (다중 OLS, R² = 0.878)", "거시 지연 인자", [
        "사내 수리 방식 (is_intern): 계수 +31.75h (p < 0.001) ➔ 자재 대기로 총 소요시간 +31.8h 증가",
        "실사 방문 대기 (visit_lag): 계수 +1.12h/h (p < 0.001) ➔ 실사 1시간 지연당 총 시간 1.12h 선형 증가",
        "비실시간 접수 (is_async): 계수 +4.89h (p = 0.030) ➔ Web·Letter 접수 시 소통 및 인계로 +4.9h 지연"
    ], ORANGE, Inches(0.6), Inches(5.9)),
    ("현장 수리 품질 및 재수리(리워크) 문제", "미시 리워크 충격", [
        "1차 착수 지연 격차: 즉시/외주는 0.0h 종결, 사내수리만 부품 준비로 30.5h 대기 독점",
        "재(再) 사내수리 루프 (26건): 1차 실패 후 재방문 시 부품 재출하로 +32.9h 추가 대기 누적",
        "극단적 장기 지연: 최대 10.1일(241.6h) 대기, 총 리드타임 171.6h에 달하는 최악의 세입자 경험"
    ], RED, Inches(6.8), Inches(5.9))
]

for hd, badge, b_list, col, l_pos, w_card in s11_bottom_cards:
    create_shape(s11, MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(5.1), w_card, Inches(1.9), CARD_BG, CARD_BORDER)
    tx = s11.shapes.add_textbox(l_pos + Inches(0.2), Inches(5.15), w_card - Inches(0.4), Inches(1.75))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_h = tf.paragraphs[0]
    r_h = p_h.add_run()
    r_h.text = f"{hd}  "
    set_font(r_h, size_pt=12, bold=True, color=NAVY)
    r_b = p_h.add_run()
    r_b.text = f"[{badge}]\n"
    set_font(r_b, size_pt=10.5, bold=True, color=col)
    
    for item in b_list:
        p_i = tf.add_paragraph()
        r_i = p_i.add_run()
        r_i.text = f"• {item}"
        set_font(r_i, size_pt=10, bold=False, color=SLATE)

add_source(s11, "출처: slide11_regression & slide11_repair_delay · analysis.sql Step 2-4 OLS 및 수리 착수/재작업 집계")
print("Slide 11 generated.")

# =============================================================
# SLIDE 12: [질문 2-2 & 질문 3 발단] 핵심 문제 규명 및 해결 아젠다
# =============================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "Part 02 · 질문 2-2 & 질문 3 발단  |  핵심 문제 규명 및 해결 아젠다", "현장 실사의 CAPA 적체 부담을 덜어내고, 수리 품목 준비 기간을 줄여야 병목이 근본적으로 사라진다", "Part 02. 질문 2")

c12_w = Inches(3.85)
c12_h = Inches(5.3)

# -----------------
# Card 1: 사전 적중률 87.3%와 이중 출장의 모순
# -----------------
create_shape(s12, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), c12_w, c12_h, CARD_BG, CARD_BORDER)

# Card 1 Header Text
tx_c1_h = s12.shapes.add_textbox(Inches(0.8), Inches(1.75), c12_w - Inches(0.4), Inches(0.7))
tf_c1_h = tx_c1_h.text_frame
tf_c1_h.word_wrap = True
p_c1_h = tf_c1_h.paragraphs[0]
r_c1_h1 = p_c1_h.add_run()
r_c1_h1.text = "사전 적중률 87.3%와 모순\n"
set_font(r_c1_h1, size_pt=13, bold=True, color=NAVY)
r_c1_h2 = p_c1_h.add_run()
r_c1_h2.text = "• 방향은 맞췄으나 이중 출장 고수"
set_font(r_c1_h2, size_pt=10.5, bold=True, color=ORANGE)

# Card 1 Donut Image
fig_donut = os.path.join(FIGURES_DIR, "slide12_intake_matching_donut.png")
if os.path.exists(fig_donut):
    s12.shapes.add_picture(fig_donut, Inches(0.8), Inches(2.45), width=Inches(3.45), height=Inches(2.45))

# Card 1 Bottom Bullets
tx_c1_b = s12.shapes.add_textbox(Inches(0.8), Inches(4.95), c12_w - Inches(0.4), Inches(1.9))
tf_c1_b = tx_c1_b.text_frame
tf_c1_b.word_wrap = True
c1_bullets = [
    "E형 (370건): 100.0% 전원 사내수리 완결",
    "P형 (439건): 91.3%(401건) 사내 자체 완결",
    "모순: 이미 87%나 방향을 맞추면서 왜 927건 전원에게 40분 실사를 보내 403건 적체를 자초했는가?"
]
for i, b in enumerate(c1_bullets):
    p_b = tf_c1_b.paragraphs[0] if i == 0 else tf_c1_b.add_paragraph()
    r_b = p_b.add_run()
    r_b.text = f"• {b}"
    set_font(r_b, size_pt=10, bold=(i == 2), color=RED if i == 2 else SLATE)

# -----------------
# Card 2: 정보 해상도의 한계 (현행 관행의 딜레마)
# -----------------
create_shape(s12, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.74), Inches(1.65), c12_w, c12_h, CARD_BG, CARD_BORDER)
tx_c2 = s12.shapes.add_textbox(Inches(4.94), Inches(1.75), c12_w - Inches(0.4), c12_h - Inches(0.2))
tf_c2 = tx_c2.text_frame
tf_c2.word_wrap = True

p_c2_h = tf_c2.paragraphs[0]
r_c2_h1 = p_c2_h.add_run()
r_c2_h1.text = "정보 해상도의 한계\n"
set_font(r_c2_h1, size_pt=13, bold=True, color=NAVY)
r_c2_h2 = p_c2_h.add_run()
r_c2_h2.text = "• 현행 관행의 정보 단절 딜레마\n\n"
set_font(r_c2_h2, size_pt=10.5, bold=True, color=RED)

c2_sections = [
    ("현행 접수부 관행", [
        "접수 상담원은 단순 알파벳 대분류(B, P, E)만 수집",
        "세입자의 구체적 고장 부품이나 규격 정보 파악 불가"
    ]),
    ("현행 현장조사부 관행", [
        "현장 기술자가 40분간 방문 실사 후 1, 2, 3, 4 세부 코드 판정",
        "현장에 도착해서 눈으로 보고서야 필요 자재를 비로소 확인"
    ]),
    ("정보 단절(Resolution Gap)의 대가", [
        "단순 알파벳(E/P)만으로는 차에 실어갈 부품을 특정할 수 없음",
        "결국 '실사(40분) ➔ 부품 주문(30.5h) ➔ 재방문 수리'라는 비효율적 이중 출장 관행이 고착화됨"
    ])
]

for sec_t, sec_list in c2_sections:
    p_sec = tf_c2.add_paragraph()
    r_st = p_sec.add_run()
    r_st.text = f"[{sec_t}]\n"
    set_font(r_st, size_pt=10.5, bold=True, color=NAVY)
    for s_item in sec_list:
        p_si = tf_c2.add_paragraph()
        r_si = p_si.add_run()
        r_si.text = f"• {s_item}"
        set_font(r_si, size_pt=9.5, bold=False, color=SLATE)
    p_sp = tf_c2.add_paragraph()
    r_sp = p_sp.add_run()
    r_sp.text = ""

# -----------------
# Card 3: 핵심 해결 과제 (2대 병목의 동시 해소)
# -----------------
create_shape(s12, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.88), Inches(1.65), c12_w, c12_h, CARD_BG, CARD_BORDER)
tx_c3 = s12.shapes.add_textbox(Inches(9.08), Inches(1.75), c12_w - Inches(0.4), c12_h - Inches(0.2))
tf_c3 = tx_c3.text_frame
tf_c3.word_wrap = True

p_c3_h = tf_c3.paragraphs[0]
r_c3_h1 = p_c3_h.add_run()
r_c3_h1.text = "2대 핵심 해결 과제 도출\n"
set_font(r_c3_h1, size_pt=13, bold=True, color=NAVY)
r_c3_h2 = p_c3_h.add_run()
r_c3_h2.text = "• Part 03을 관통하는 TO-BE 아젠다\n\n"
set_font(r_c3_h2, size_pt=10.5, bold=True, color=GREEN)

c3_sections = [
    ("1. 실사 CAPA 적체 부담 제거", [
        "목표: 현장 실사 대기시간(76.8h) 원천 소멸",
        "방안: 접수 체크리스트 고도화로 높은 적중률(87.3%)을 살려 실사 대기열 우회(Bypass)",
        "효과: 1회 방문 수리 직행으로 일일 실사 유입 135건 ➔ 15건으로 급감 (기사 CAPA 68건 내 진입)"
    ]),
    ("2. 수리 품목 준비 기간 단축", [
        "목표: 사내수리 자재 대기(30.5h) 단축 & 리워크 차단",
        "방안: 고장 부품 사전 특정화로 출동 전 모듈형 패키징 키트 지참 출고",
        "품질 대책: 리워크 84.6%를 차지하는 E-1 / E-2 계열에 정밀검사 도입 ➔ 추가 대기(+32.9h) 원천 차단"
    ])
]

for sec_t, sec_list in c3_sections:
    p_sec = tf_c3.add_paragraph()
    r_st = p_sec.add_run()
    r_st.text = f"[{sec_t}]\n"
    set_font(r_st, size_pt=11, bold=True, color=BLUE_ACCENT if "1." in sec_t else ORANGE)
    for s_item in sec_list:
        p_si = tf_c3.add_paragraph()
        r_si = p_si.add_run()
        r_si.text = f"• {s_item}"
        set_font(r_si, size_pt=9.5, bold=("목표" in s_item or "84.6%" in s_item), color=NAVY if "목표" in s_item else SLATE)
    p_sp = tf_c3.add_paragraph()
    r_sp = p_sp.add_run()
    r_sp.text = ""

add_source(s12, "출처: slide12_intake_matching_donut · analysis.sql L1840~1878 접수-현장 정합도 및 TO-BE 가설")
print("Slide 12 generated.")

# =============================================================
# SLIDE 13: [질문 2-3] 리소스 생산성: 상담원 2인 균등성 및 기사 11인 매트릭스
# =============================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Part 02 · 질문 2-3  |  리소스 생산성 심층 분석", "상담원 2인은 업무를 완벽히 균등 분담하며, 기사 11인 중 최상위 기사(Anne)가 프로세스를 견인한다", "Part 02. 질문 2")

fig_s13 = os.path.join(FIGURES_DIR, "slide13_resource_productivity.png")
if os.path.exists(fig_s13):
    s13.shapes.add_picture(fig_s13, Inches(0.6), Inches(1.65), width=Inches(12.13), height=Inches(3.4))

s13_cards = [
    ("접수 상담원 2인: 완벽한 균등성", "개인 역량 차이 0건 입증", [
        "Monica: 490건 (52.9%) / 인계율 13.5% (66건) / 평균 접수 2.1h",
        "Dian: 437건 (47.1%) / 인계율 13.1% (57건) / 평균 접수 2.0h",
        "결론: 개인의 태만이나 역량 부족이 아니며 단일 룰에 의해 균등 작동"
    ], NAVY),
    ("핵심 에이스 기사: Anne", "즉시수리 370건 (96.6%) 단독 완결 ⭐", [
        "실사 218건(23.5%) 및 1차 수리 204건(22.0%) 전담 수행",
        "특히 현장 40분 원샷 즉시수리(ImmediateRepair)의 96.6%를 완결",
        "숙련 기사의 현장 즉시 완결 능력이 병목 해소의 핵심 레버"
    ], GREEN),
    ("사내수리 전담 기사 및 외주 배분", "사내수리 200건 전담 & 외주 50:50", [
        "Paul 기사: 사내수리 200건(41.2%), 실사 188건 전담",
        "외주 전문업체: DoIt(30건) vs FixIt(29건)으로 50:50 완벽 균등 배분",
        "인력 간 전문성 편차에 따른 표준 매뉴얼화 및 키팅 도입 필요"
    ], ORANGE)
]

for i, (hd, badge, b_list, col) in enumerate(s13_cards):
    l_pos = Inches(0.6 + i * (3.85 + 0.29))
    create_shape(s13, MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, Inches(5.2), c8_w, Inches(1.8), CARD_BG, CARD_BORDER)
    tx = s13.shapes.add_textbox(l_pos + Inches(0.2), Inches(5.25), c8_w - Inches(0.4), Inches(1.65))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_h = tf.paragraphs[0]
    r_h = p_h.add_run()
    r_h.text = f"{hd}\n"
    set_font(r_h, size_pt=12.5, bold=True, color=NAVY)
    r_b = p_h.add_run()
    r_b.text = f"• {badge}\n"
    set_font(r_b, size_pt=11, bold=True, color=col)
    
    for item in b_list:
        p_i = tf.add_paragraph()
        r_i = p_i.add_run()
        r_i.text = f"- {item}"
        set_font(r_i, size_pt=10, bold=False, color=SLATE)

add_source(s13, "출처: slide13_resource_productivity · analysis.sql L1190, L1590 리소스 생산성 교차 분석")
print("Slide 13 generated.")

# =============================================================
# SLIDE 14: [질문 3] TO-BE 전략 1 & 2: 소통 통제 (Web 자가 예약 & 1회 방문 원샷 직행)
# =============================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "Part 03 · 질문 3  |  TO-BE 프로세스 최적화 전략 1 & 2", "접수 소통 통제와 1회 방문 직행(87.3%)으로 546시간의 기사 공수를 회수한다", "Part 03. 질문 3")

# AS-IS vs TO-BE 대비 레이아웃 (좌우 2분할)
# 좌측: AS-IS 병목 프로세스
create_shape(s14, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(5.9), Inches(5.25), RED_LIGHT, RED)
tx_as = s14.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(5.4), Inches(4.8))
tf_as = tx_as.text_frame
tf_as.word_wrap = True

p_as1 = tf_as.paragraphs[0]
r_as1 = p_as1.add_run()
r_as1.text = "🔴 AS-IS: 비동기 소통 공백 & 전수 실사 의무화\n"
set_font(r_as1, size_pt=14, bold=True, color=RED)

as_steps = [
    ("비실시간 접수 핑퐁", "Web/우편 신청 후 유선 일정 조율 ➔ 123건 교차 인계 발생 (6.6배 지연)"),
    ("전수 100% 방문 실사", "모든 건에 대해 기사가 현장 방문(40분)하여 눈으로만 확인 (일 135건 유입)"),
    ("WIP 대기열 403건 적체", "기사 실사 CAPA(69건/일) 초과 ➔ 실사 전 대기시간 76.8시간 (3.2일) 발생"),
    ("2차 방문 시 부품 조달", "실사 후 돌아와 부품 신청 ➔ 사내수리 착수 대기 30.5시간 추가 누적")
]
for st_t, st_d in as_steps:
    p = tf_as.add_paragraph()
    r_t = p.add_run()
    r_t.text = f"▼ {st_t}\n"
    set_font(r_t, size_pt=11.5, bold=True, color=NAVY)
    r_d = p.add_run()
    r_d.text = f"  {st_d}\n"
    set_font(r_d, size_pt=10.5, bold=False, color=SLATE)

# 우측: TO-BE 혁신 프로세스
create_shape(s14, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.65), Inches(5.93), Inches(5.25), GREEN_LIGHT, GREEN)
tx_to = s14.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.4), Inches(4.8))
tf_to = tx_to.text_frame
tf_to.word_wrap = True

p_to1 = tf_to.paragraphs[0]
r_to1 = p_to1.add_run()
r_to1.text = "🟢 TO-BE: 소통 통제(자가예약) & 87.3% 1회 방문 직행\n"
set_font(r_to1, size_pt=14, bold=True, color=GREEN)

to_steps = [
    ("전략 1. Web 디지털 자가 예약", "사진 2장 필수 첨부 + 세입자 캘린더 직접 확정 ➔ 인계율 0% & 소통공백 소멸"),
    ("전략 2. E·P형 1회 방문 원샷 직행", "유형 정합도 87.3% 기반: 부품 사전 상차 후 실사 없이 즉시 수리 출동"),
    ("E형 규격품 (370건, 100%)", "사전 키팅(Pre-kitting) 후 원샷 출동 ➔ 실사 40분 + 자재대기 38.7h 동시 제거"),
    ("P형 경미하자 (365건, 91.3%)", "범용 소모품 차량 원샷 직행 출동 ➔ 당일 현장 수리 완결"),
    ("정량 효과: 546시간 기사 공수 회수", "실사 유입 927건 ➔ 118건으로 87.3% 급감 ➔ 실사 대기(76.8h) 완전 소멸!")
]
for st_t, st_d in to_steps:
    p = tf_to.add_paragraph()
    r_t = p.add_run()
    r_t.text = f"★ {st_t}\n"
    set_font(r_t, size_pt=11.5, bold=True, color=GREEN)
    r_d = p.add_run()
    r_d.text = f"  {st_d}\n"
    set_font(r_d, size_pt=10.5, bold=False, color=SLATE)

add_source(s14, "출처: 질문 3 프로세스 혁신 방안 · 접수 유형 정합도 87.3% 및 헛걸음 실사(40.5분) 제거 공수 산출")
print("Slide 14 generated.")

# =============================================================
# SLIDE 15: [질문 3] TO-BE 전략 3 & 정량 ROI: 패스트트랙 및 65% 리드타임 감축
# =============================================================
s15 = prs.slides.add_slide(blank_layout)
add_header(s15, "Part 03 · 질문 3  |  TO-BE 전략 3 & 정량적 ROI", "외주 패스트트랙과 3대 전략 결합으로 총 리드타임을 4.4일에서 1.5일로 65.1% 감축한다", "Part 03. 질문 3")

# 좌측: 전략 3 및 정량 성과 요약 카드
create_shape(s15, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(5.1), Inches(5.25), CARD_BG, CARD_BORDER)
tx_s15_l = s15.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(4.6), Inches(4.8))
tf_15l = tx_s15_l.text_frame
tf_15l.word_wrap = True

p_15_1 = tf_15l.paragraphs[0]
r_15_1 = p_15_1.add_run()
r_15_1.text = "⚡ 전략 3: 외주 패스트트랙 가동\n"
set_font(r_15_1, size_pt=14, bold=True, color=NAVY)

r_15_1_d = p_15_1.add_run()
r_15_1_d.text = (
    "• 사내 수리 1차 미완결 시 재방문(26건, 10.1일 지연)을 전면 금지하고 전문 외주업체로 즉시 전산 이관.\n"
    "• 외주 이관 대기는 0.0시간이므로 최대 10일의 하자 지연 루프를 원천 차단.\n\n"
)
set_font(r_15_1_d, size_pt=11, bold=False, color=SLATE)

p_15_2 = tf_15l.add_paragraph()
r_15_2 = p_15_2.add_run()
r_15_2.text = "📊 3대 전략 결합 정량 ROI 성과표\n"
set_font(r_15_2, size_pt=13, bold=True, color=GREEN)

roi_table_items = [
    ("총 리드타임", "105.9h (4.4일)", "36.0h (1.5일)", "▼ 65.1% 감축 ⭐"),
    ("실사 방문 대기", "76.8시간", "4.0시간 이내", "▼ 94.8% 절감"),
    ("수리 착수 대기", "15.9시간", "12.0시간", "사전 상차 단축"),
    ("접수 처리 시간", "2.1시간", "0.5시간", "30분 이내 확정"),
    ("교차 인계율", "13.3% (123건)", "0.0%", "원천 소멸"),
    ("회수된 기사 공수", "0시간", "546.3시간", "본수리 역량 재배치")
]

for item, before, after, eff in roi_table_items:
    p_roi = tf_15l.add_paragraph()
    r_it = p_roi.add_run()
    r_it.text = f"• {item}: "
    set_font(r_it, size_pt=10.5, bold=True, color=NAVY)
    r_ba = p_roi.add_run()
    r_ba.text = f"{before} ➔ {after} "
    set_font(r_ba, size_pt=10, bold=False, color=SLATE)
    r_ef = p_roi.add_run()
    r_ef.text = f"({eff})\n"
    set_font(r_ef, size_pt=10, bold=True, color=GREEN if "감축" in eff or "소멸" in eff or "절감" in eff else ORANGE)

# 우측: slide15_roi_leadtime_reduction.png 차트
fig_s15 = os.path.join(FIGURES_DIR, "slide15_roi_leadtime_reduction.png")
if os.path.exists(fig_s15):
    s15.shapes.add_picture(fig_s15, Inches(5.95), Inches(1.65), width=Inches(6.78), height=Inches(5.25))

add_source(s15, "출처: slide15_roi_leadtime_reduction · analysis.sql Step 3 TO-BE 시뮬레이션 및 정량 ROI 산출 모델")
print("Slide 15 generated.")

# =============================================================
# SLIDE 16: [마무리] 엔지니어링 신뢰성 보증 및 질의응답 (Q&A)
# =============================================================
s16 = prs.slides.add_slide(blank_layout)
add_header(s16, "Part 04 · 마무리  |  엔지니어링 신뢰성 보증", "1,878행의 SQL 마스터 뷰와 무결성 파이프라인으로 100% 재현성을 보증합니다", "Part 04. 마무리")

# 좌측: 4대 엔지니어링 파이프라인 무결성 체크리스트
create_shape(s16, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(6.5), Inches(5.25), CARD_BG, CARD_BORDER)
tx_s16_l = s16.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(6.0), Inches(4.8))
tf_16l = tx_s16_l.text_frame
tf_16l.word_wrap = True

p_16_1 = tf_16l.paragraphs[0]
r_16_1 = p_16_1.add_run()
r_16_1.text = "🛡️ 4대 엔지니어링 파이프라인 무결성 검증\n"
set_font(r_16_1, size_pt=14, bold=True, color=NAVY)

checks = [
    ("1. 무손실 전처리 파이프라인 (repair_cleaned.csv)", [
        "13,262행 전수 100% 보존 (임의 행 삭제 0건)",
        "18개 케이스 비정상 결측 인과 복원 완료 & 시간 역전 0건 입증"
    ]),
    ("2. SQL 프로세스 마이닝 모델 (analysis.sql)", [
        "1,878행의 MySQL 마스터 뷰(case_master_view) 기반 설계",
        "리드타임, 대기시간, WIP 동역학, OLS 회귀 공식 산출 쿼리 완비"
    ]),
    ("3. 가설 검정 및 고해상도 시각화 파이프라인", [
        "hypothesis_testing_and_visualization.ipynb 전수 무오류 실행 통과",
        "모든 분석 수치와 시각화 차트 100% 일치"
    ]),
    ("4. 에셋 및 문서 규격화", [
        "outputs/figures/ 11종 정밀 차트 에셋 및 스토리보드 완벽 동기화",
        "실무 시스템 즉시 이식 가능한 재현성 확보"
    ])
]

for ch_tit, ch_sub in checks:
    p = tf_16l.add_paragraph()
    r_t = p.add_run()
    r_t.text = f"✓ {ch_tit}\n"
    set_font(r_t, size_pt=11.5, bold=True, color=GREEN)
    for s_txt in ch_sub:
        r_s = p.add_run()
        r_s.text = f"   • {s_txt}\n"
        set_font(r_s, size_pt=10.5, bold=False, color=SLATE)

# 우측: 질의응답 (Q&A) 배너 카드
create_shape(s16, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.4), Inches(1.65), Inches(5.33), Inches(5.25), NAVY)
tx_qa = s16.shapes.add_textbox(Inches(7.7), Inches(2.3), Inches(4.7), Inches(4.0))
tf_qa = tx_qa.text_frame
tf_qa.word_wrap = True

p_qa1 = tf_qa.paragraphs[0]
p_qa1.alignment = PP_ALIGN.CENTER
r_qa1 = p_qa1.add_run()
r_qa1.text = "Q & A\n\n"
set_font(r_qa1, size_pt=40, bold=True, color=WHITE)

p_qa2 = tf_qa.add_paragraph()
p_qa2.alignment = PP_ALIGN.CENTER
r_qa2 = p_qa2.add_run()
r_qa2.text = (
    "\"현장의 대기시간을 줄이고,\n"
    "이해관계자 간 소통을 통제하여\n"
    "리드타임 65% 감축을 달성하겠습니다.\"\n\n\n"
    "경청해 주셔서 대단히 감사합니다.\n"
    "질문해 주시면 성심껏 답변드리겠습니다."
)
set_font(r_qa2, size_pt=14, bold=False, color=RGBColor(203, 213, 225))

add_source(s16, "엔지니어링 보증: MySQL analysis.sql (1,878 lines), Python hypothesis_testing_and_visualization.ipynb")
print("Slide 16 generated.")

# =============================================================
# SLIDE 17: [Appendix 1] 5대 전처리 알고리즘 명세 및 751건 모수 확장
# =============================================================
s17 = prs.slides.add_slide(blank_layout)
add_header(s17, "Part 05 · 부록 1  |  Appendix 1: 전처리 심화", "도메인 1:1 짝 추적과 접수 표본 분리(751건 모수 확보)로 100% 무손실 복원을 달성했다", "Part 05. 부록")

c17_cases = [
    ("CASE 1. taskID (2건)", "7124행(contact:Web, MakeTicket 직전) ➔ FirstContact 확정 / 7785행(ArrangeSurvey 직후) ➔ InformClientSurvey"),
    ("CASE 2. originator (2건)", "시작-종료 담당자 100% 일치 실측 ➔ 8217행(Survey) Anne 승계 / 12880행(InternRepair) Paul 승계"),
    ("CASE 3. eventtype (5건)", "1:1 페어(6953 ArrangeSurvey, 8217 Survey, 9843 Immediate) + 마일스톤(8144 Survey, 13159 TicketReady)"),
    ("CASE 4. date 이상치 (879건)", "1905년 리셋(6건)+미래 연도(860건) ➔ 선후행 구간 제약 ➔ 단일 후보 640건 즉시 확정 + 앵커 219건 매핑 (1970년 통일)")
]

for i, (hd, desc) in enumerate(c17_cases):
    t_pos = Inches(1.65 + i * 0.95)
    create_shape(s17, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), t_pos, Inches(12.13), Inches(0.85), CARD_BG, CARD_BORDER)
    tx = s17.shapes.add_textbox(Inches(0.85), t_pos + Inches(0.1), Inches(11.6), Inches(0.65))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r_t = p.add_run()
    r_t.text = f"{hd}  |  "
    set_font(r_t, size_pt=12, bold=True, color=ORANGE)
    r_d = p.add_run()
    r_d.text = desc
    set_font(r_d, size_pt=11, bold=False, color=SLATE)

# 하단 CASE 5 모수 확장 강조 카드
create_shape(s17, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.6), Inches(12.13), Inches(1.3), GREEN_LIGHT, GREEN)
tx_c17_bot = s17.shapes.add_textbox(Inches(0.85), Inches(5.7), Inches(11.6), Inches(1.1))
tf_17b = tx_c17_bot.text_frame
tf_17b.word_wrap = True
p_b1 = tf_17b.paragraphs[0]
r_b1 = p_b1.add_run()
r_b1.text = "★ CASE 5. time 파손 복원 및 표본 모수 확장 전략 (34% 한계 ➔ 75.1% 확보)\n"
set_font(r_b1, size_pt=12.5, bold=True, color=GREEN)
r_b2 = p_b1.add_run()
r_b2.text = (
    "• 전 공정 완전무결 기준 시 표본 34~39%(398건) 축소 한계 ➔ 접수 구간 정상 표본 분리 전략으로 75.1%(751건) 대규모 모수 확보.\n"
    "• 751건 실측 대표값(소요시간 중앙값 4.0분) 도출 ➔ 정상 자정 7건 보존 + 기준 앵커로부터 4.0분 역산 추정 21건 적용 ➔ 시간 역전 0건 달성!"
)
set_font(r_b2, size_pt=11, bold=False, color=SLATE)

add_source(s17, "출처: analysis.ipynb Cell 18, 20, 51, 53, 77, 81 / repair2.csv 전처리 알고리즘 명세서")
print("Slide 17 generated.")

# =============================================================
# SLIDE 18: [Appendix 2] 프로세스 마이닝 다중 회귀분석 모델 상세
# =============================================================
s18 = prs.slides.add_slide(blank_layout)
add_header(s18, "Part 05 · 부록 2  |  Appendix 2: 다중 회귀분석 상세", "교차인계(β=+6.67h)와 비실시간 채널(β=+3.82h)이 접수 지연을 통계적으로 결정한다", "Part 05. 부록")

# 좌측 회귀 모델 상세표 카드
create_shape(s18, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(6.8), Inches(5.25), WHITE, CARD_BORDER)
tx_s18_t = s18.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(6.3), Inches(0.4))
tf_18t = tx_s18_t.text_frame
p_18t = tf_18t.paragraphs[0]
r_18t = p_18t.add_run()
r_18t.text = "📋 접수 소요시간(Receipt Duration) 회귀 결과표"
set_font(r_18t, size_pt=13.5, bold=True, color=NAVY)

# 표 생성
tbl_s18 = s18.shapes.add_table(6, 4, Inches(0.85), Inches(2.35), Inches(6.3), Inches(3.2)).table
tbl_s18.columns[0].width = Inches(2.5)
tbl_s18.columns[1].width = Inches(1.3)
tbl_s18.columns[2].width = Inches(1.2)
tbl_s18.columns[3].width = Inches(1.3)

tbl_s18_data = [
    [("독립 변수 (Variable)", True, WHITE, NAVY), ("회귀계수 (β)", True, WHITE, NAVY), ("t-value", True, WHITE, NAVY), ("p-value", True, WHITE, NAVY)],
    [("교차 인계 발생 (is_handover)", True, RED, None), ("+6.67", True, RED, None), ("18.42", False, SLATE, None), ("< 0.001 ***", True, RED, None)],
    [("우편 접수 (Letter_Channel)", True, NAVY, None), ("+4.15", True, ORANGE, None), ("11.23", False, SLATE, None), ("< 0.001 ***", True, ORANGE, None)],
    [("웹 접수 (Web_Channel)", True, NAVY, None), ("+3.82", True, ORANGE, None), ("10.54", False, SLATE, None), ("< 0.001 ***", True, ORANGE, None)],
    [("야간 접수 여부 (night_contact)", False, SLATE, None), ("+1.24", False, SLATE, None), ("2.04", False, SLATE, None), ("0.042 *", False, SLATE, None)],
    [("상담원 개인 더미 (Monica/Dian)", False, MUTED, None), ("-0.12 ~ +0.15", False, MUTED, None), ("0.42", False, MUTED, None), ("0.672 (무의미)", True, MUTED, None)]
]

for row_idx, row in enumerate(tbl_s18_data):
    for col_idx, (text, is_bold, text_col, bg_col) in enumerate(row):
        cell = tbl_s18.cell(row_idx, col_idx)
        if bg_col:
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if row_idx % 2 == 1 else WHITE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
        r = p.add_run()
        r.text = text
        set_font(r, size_pt=10.5, bold=is_bold, color=text_col)

# 모델 통계량 요약 배너
create_shape(s18, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(5.8), Inches(6.3), Inches(0.85), CARD_BG, CARD_BORDER)
tx_m_stat = s18.shapes.add_textbox(Inches(0.95), Inches(5.85), Inches(6.1), Inches(0.75))
tf_ms = tx_m_stat.text_frame
p_ms = tf_ms.paragraphs[0]
r_ms = p_ms.add_run()
r_ms.text = "• 모델 통계량: F(4, 922) = 184.2 (p < 0.0001), R² = 0.428 (Adj R² = 0.425)\n• 상담원 개인 편차는 p > 0.35로 통계적 유의성이 전혀 없음 (시스템 구조 문제)"
set_font(r_ms, size_pt=10.5, bold=False, color=SLATE)

# 우측: 회귀 분석 핵심 함의 카드
create_shape(s18, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.65), Inches(1.65), Inches(5.08), Inches(5.25), CARD_BG, CARD_BORDER)
tx_s18_r = s18.shapes.add_textbox(Inches(7.9), Inches(1.85), Inches(4.58), Inches(4.8))
tf_18r = tx_s18_r.text_frame
tf_18r.word_wrap = True

p_r1 = tf_18r.paragraphs[0]
r_r1 = p_r1.add_run()
r_r1.text = "💡 다중 회귀분석의 3대 핵심 함의\n\n"
set_font(r_r1, size_pt=13.5, bold=True, color=NAVY)

r_ins = [
    ("인계 패널티의 압도성 (β = +6.67h)", "상담원 간 인계가 발생하는 순간 평균 6.7시간의 순지연이 추가 발생함. 단일 요인 중 가장 강력한 지연 트리거."),
    ("비실시간 채널의 소통 공백 (β = +3.8h ~ 4.2h)", "웹과 우편은 접수 후 고객 회신을 기다리는 비동기 핑퐁 구조로 인해 기본 4시간 안팎의 추가 지연을 야기."),
    ("인력 탓 배제: 프로세스 개선 필요", "상담원 개인 더미는 모두 통계적으로 유의하지 않음. 사람을 바꿀 것이 아니라 '자가 예약 시스템'으로 소통을 통제해야 함.")
]
for t_in, d_in in r_ins:
    p = tf_18r.add_paragraph()
    r_it = p.add_run()
    r_it.text = f"■ {t_in}\n"
    set_font(r_it, size_pt=11.5, bold=True, color=ORANGE)
    r_id = p.add_run()
    r_id.text = f"   {d_in}\n"
    set_font(r_id, size_pt=10.5, bold=False, color=SLATE)

add_source(s18, "출처: analysis.sql 라인 1076~1298 다중 OLS 회귀분석 쿼리 및 case_master_view")
print("Slide 18 generated.")

# =============================================================
# SLIDE 19: [Appendix 3] 리소스 생산성 및 공정별 크로스탭
# =============================================================
s19 = prs.slides.add_slide(blank_layout)
add_header(s19, "Part 05 · 부록 3  |  Appendix 3: 리소스 크로스탭", "상담원 4인과 현장 기사는 단일 가용 풀(Shared Pool)로 건전하게 운영되고 있다", "Part 05. 부록")

# 상단: 상담원 4인 접수 운영 크로스탭
create_shape(s19, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.65), Inches(12.13), Inches(2.45), WHITE, CARD_BORDER)
tx_s19_t = s19.shapes.add_textbox(Inches(0.85), Inches(1.8), Inches(11.6), Inches(0.35))
tf_19t = tx_s19_t.text_frame
p_19t = tf_19t.paragraphs[0]
r_19t = p_19t.add_run()
r_19t.text = "👥 상담원 4인 접수 운영 매트릭스 (처리량 및 인계율)"
set_font(r_19t, size_pt=13, bold=True, color=NAVY)

tbl_s19_top = s19.shapes.add_table(5, 5, Inches(0.85), Inches(2.2), Inches(11.6), Inches(1.7)).table
for c_i in range(5):
    tbl_s19_top.columns[c_i].width = Inches(2.32)

tbl_top_data = [
    [("상담원", True, WHITE, NAVY), ("총 처리 건수 (비중)", True, WHITE, NAVY), ("평균 접수 소요시간", True, WHITE, NAVY), ("교차 인계 발생 건수", True, WHITE, NAVY), ("인계 발생률 (%)", True, WHITE, NAVY)],
    [("Anne", True, NAVY, None), ("248건 (26.8%)", False, SLATE, None), ("1.9시간", False, SLATE, None), ("34건", False, SLATE, None), ("13.7%", True, GREEN, None)],
    [("Dian", True, NAVY, None), ("235건 (25.3%)", False, SLATE, None), ("2.1시간", False, SLATE, None), ("31건", False, SLATE, None), ("13.2%", True, GREEN, None)],
    [("Monica", True, NAVY, None), ("228건 (24.6%)", False, SLATE, None), ("2.0시간", False, SLATE, None), ("29건", False, SLATE, None), ("12.7%", True, GREEN, None)],
    [("Paul", True, NAVY, None), ("216건 (23.3%)", False, SLATE, None), ("2.2시간", False, SLATE, None), ("30건", False, SLATE, None), ("13.9%", True, GREEN, None)]
]
for row_idx, row in enumerate(tbl_top_data):
    for col_idx, (text, is_bold, text_col, bg_col) in enumerate(row):
        cell = tbl_s19_top.cell(row_idx, col_idx)
        if bg_col:
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if row_idx % 2 == 1 else WHITE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        set_font(r, size_pt=10.5, bold=is_bold, color=text_col)

# 하단: 수리 주체별 성과 비교표
create_shape(s19, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.3), Inches(12.13), Inches(2.6), WHITE, CARD_BORDER)
tx_s19_b = s19.shapes.add_textbox(Inches(0.85), Inches(4.45), Inches(11.6), Inches(0.35))
tf_19b = tx_s19_b.text_frame
p_19b = tf_19b.paragraphs[0]
r_19b = p_19b.add_run()
r_19b.text = "🔧 수리 주체별 운영 성과 및 품질 리스크 대조표"
set_font(r_19b, size_pt=13, bold=True, color=NAVY)

tbl_s19_bot = s19.shapes.add_table(4, 5, Inches(0.85), Inches(4.85), Inches(11.6), Inches(1.85)).table
for c_i in range(5):
    tbl_s19_bot.columns[c_i].width = Inches(2.32)

tbl_bot_data = [
    [("수리 방식", True, WHITE, NAVY), ("수행 건수 (비중)", True, WHITE, NAVY), ("착수 대기시간", True, WHITE, NAVY), ("순수 작업시간", True, WHITE, NAVY), ("2차 하자 재작업률", True, WHITE, NAVY)],
    [("즉시 수리 (Immediate)", True, GREEN, None), ("383건 (41.3%)", False, SLATE, None), ("0.0시간 (즉시)", True, GREEN, None), ("2.8시간 (당일 완결)", False, SLATE, None), ("0.0% (루프 없음)", True, GREEN, None)],
    [("외주 수리 (Extern)", True, BLUE_ACCENT, None), ("132건 (14.2%)", False, SLATE, None), ("0.0시간 (전산 이관)", True, BLUE_ACCENT, None), ("외주 전문업체 전담", False, SLATE, None), ("0.0% (전문업체)", True, GREEN, None)],
    [("사내 수리 (Intern)", True, RED, None), ("412건 (44.5%)", False, SLATE, None), ("30.5시간 (자재 대기)", True, RED, None), ("3.5시간", False, SLATE, None), ("11.9% (49건 하자 루프)", True, RED, None)]
]
for row_idx, row in enumerate(tbl_bot_data):
    for col_idx, (text, is_bold, text_col, bg_col) in enumerate(row):
        cell = tbl_s19_bot.cell(row_idx, col_idx)
        if bg_col:
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if row_idx % 2 == 1 else WHITE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        set_font(r, size_pt=10.5, bold=is_bold, color=text_col)

add_source(s19, "출처: analysis.sql 및 case_pivot_table.csv · 상담원 4인 운영 및 수리 방식별 교차 크로스탭")
print("Slide 19 generated.")

# -------------------------------------------------------------
# 파일 저장
# -------------------------------------------------------------
prs.save(OUT_PPTX_1)
print(f"Saved to {OUT_PPTX_1}")

shutil.copyfile(OUT_PPTX_1, OUT_PPTX_2)
print(f"Copied to {OUT_PPTX_2}")
