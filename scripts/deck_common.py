# -*- coding: utf-8 -*-
"""퍼즐데이터 과제 PPTX 빌더 공용 라이브러리.

- 디자인 토큰: docs/03_ppt_storyboard.md '60-30-10 White Theme' (Tailwind slate/emerald/orange/red/blue)
- 폰트: PPTX 는 폰트를 임베딩할 수 없으므로 어떤 Windows PC 에도 있는 '맑은 고딕'(본문) + 'Consolas'(BigNum)
- 텍스트 박스는 PIL 로 글자 폭을 측정해, 박스 높이를 넘으면 빌드 시점에 경고(WARNINGS)한다.
- 차트 이미지는 항상 종횡비를 보존해 박스 안에 contain 배치한다 (object-contain).
"""
import os
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Union

from lxml import etree
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, "outputs", "figures")
OUT_DIR = os.path.join(BASE_DIR, "outputs", "pptx")

# ------------------------------------------------------------------ 캔버스
SLIDE_W, SLIDE_H = 13.333, 7.5
MX = 0.55                      # 좌우 여백(in)
CW = SLIDE_W - 2 * MX          # 콘텐츠 폭
TOTAL_SLIDES = 14

# ------------------------------------------------------------------ 색상 토큰
WHITE = "FFFFFF"
S50, S100, S200, S300, S400 = "F8FAFC", "F1F5F9", "E2E8F0", "CBD5E1", "94A3B8"
S500, S600, S700, S800, S900 = "64748B", "475569", "334155", "1E293B", "0F172A"
RED50, RED200, RED600, RED700 = "FEF2F2", "FECACA", "DC2626", "B91C1C"
ORG50, ORG100, ORG200, ORG300, ORG600, ORG700, ORG800 = (
    "FFF7ED", "FFEDD5", "FED7AA", "FDBA74", "EA580C", "C2410C", "9A3412")
EMR50, EMR100, EMR200, EMR400, EMR500, EMR600, EMR700, EMR800 = (
    "ECFDF5", "D1FAE5", "A7F3D0", "34D399", "10B981", "059669", "047857", "065F46")
BLU50, BLU100, BLU200, BLU600, BLU700, BLU800 = (
    "EFF6FF", "DBEAFE", "BFDBFE", "2563EB", "1D4ED8", "1E40AF")

FONT = "맑은 고딕"
FONT_NUM = "Consolas"

WARNINGS: List[str] = []
_CTX = {"slide": 0}

# True 이면 모든 문단에 eaLnBrk="0" 을 써서 한글을 어절(공백) 단위로 줄바꿈한다.
# 기본(PowerPoint)은 글자 단위로 끊어 "독/점" 같은 고아 글자가 생긴다. v1 재현을 위해 기본값은 False.
EA_WORD_WRAP = False


def set_context(slide_no: int):
    _CTX["slide"] = slide_no


def warn(msg: str):
    WARNINGS.append(f"[S{_CTX['slide']:02d}] {msg}")


def rgb(hex6: str) -> RGBColor:
    return RGBColor.from_string(hex6)


# ------------------------------------------------------------------ 텍스트 모델
@dataclass
class R:
    """Run: 한 서식의 글자 덩어리."""
    text: str
    size: float = 11.5
    bold: bool = False
    color: str = S600
    mono: bool = False
    italic: bool = False


@dataclass
class P:
    """Paragraph."""
    runs: List[R]
    align: str = "l"            # l / c / r
    bullet: bool = False
    after: float = 0.0          # pt
    before: float = 0.0         # pt
    spacing: float = 1.0        # 줄 간격 배수


def para(text: Union[str, List[R]], size=11.5, bold=False, color=S600, mono=False,
         align="l", bullet=False, after=0.0, before=0.0, spacing=1.0, italic=False) -> P:
    runs = [R(text, size, bold, color, mono, italic)] if isinstance(text, str) else text
    return P(runs, align, bullet, after, before, spacing)


# ------------------------------------------------------------------ 글자 폭 측정
_WIN_FONTS = r"C:\Windows\Fonts"
_FONT_FILES = {
    (False, False): "malgun.ttf", (True, False): "malgunbd.ttf",
    (False, True): "consola.ttf", (True, True): "consolab.ttf",
}
_font_cache = {}
_PX_PER_PT = 20
LINE_FACTOR = 1.32              # 맑은 고딕의 줄 높이 ≈ 글자 크기 × 1.32
BULLET_INDENT = 0.17            # in


def _font(bold: bool, mono: bool) -> Optional[ImageFont.FreeTypeFont]:
    key = (bold, mono)
    if key not in _font_cache:
        path = os.path.join(_WIN_FONTS, _FONT_FILES[key])
        try:
            _font_cache[key] = ImageFont.truetype(path, 10 * _PX_PER_PT)
        except OSError:
            _font_cache[key] = None
    return _font_cache[key]


def text_w(text: str, size: float, bold=False, mono=False) -> float:
    """글자 폭(in). 폰트 파일이 없으면 보수적 추정."""
    f = _font(bold, mono)
    if f is None:
        return sum(size * (1.0 if ord(c) > 255 else 0.55) for c in text) / 72.0
    return f.getlength(text) / (10 * _PX_PER_PT) * size / 72.0


def _tokens(p: P):
    """(단어, 크기, bold, mono) 토큰열. 공백은 단어 뒤에 붙인다. '\\n' 은 강제 줄바꿈 토큰."""
    out = []
    for r in p.runs:
        parts = r.text.split("\n")
        for pi, part in enumerate(parts):
            if pi > 0:
                out.append(("\n", r.size, r.bold, r.mono))
            buf = ""
            for ch in part:
                buf += ch
                if ch == " ":
                    out.append((buf, r.size, r.bold, r.mono))
                    buf = ""
            if buf:
                out.append((buf, r.size, r.bold, r.mono))
    return out


def para_lines(p: P, width_in: float):
    """문단이 차지하는 (줄 수, 총 높이 in)."""
    avail = width_in - (BULLET_INDENT if p.bullet else 0)
    lines, cur_w, cur_max = 1, 0.0, max((r.size for r in p.runs), default=11.0)
    height = 0.0
    max_in_line = cur_max
    for tok, size, bold, mono in _tokens(p):
        if tok == "\n":
            height += max_in_line * LINE_FACTOR * p.spacing / 72.0
            lines += 1
            cur_w, max_in_line = 0.0, size
            continue
        w = text_w(tok.rstrip(" "), size, bold, mono)
        wfull = text_w(tok, size, bold, mono)
        if cur_w > 0 and cur_w + w > avail:      # 단어 단위 줄바꿈
            height += max_in_line * LINE_FACTOR * p.spacing / 72.0
            lines += 1
            cur_w, max_in_line = 0.0, size
        if w > avail:                             # 한 단어가 한 줄보다 길면 글자 단위
            per = text_w(tok[0], size, bold, mono)
            n = max(1, int(avail / max(per, 0.01)))
            extra = int(len(tok) / n)
            lines += extra
            height += extra * size * LINE_FACTOR * p.spacing / 72.0
            cur_w = text_w(tok[(extra) * n:], size, bold, mono)
        else:
            cur_w += wfull
        max_in_line = max(max_in_line, size)
    height += max_in_line * LINE_FACTOR * p.spacing / 72.0
    height += (p.after + p.before) / 72.0
    return lines, height


def est_height(paras: Sequence[P], width_in: float) -> float:
    return sum(para_lines(p, width_in)[1] for p in paras)


# ------------------------------------------------------------------ 저수준 서식
def _set_fonts(run, mono: bool):
    run.font.name = FONT_NUM if mono else FONT
    rPr = run._r.get_or_add_rPr()
    latin = rPr.find(qn("a:latin"))
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.Element(qn(tag))
            latin.addnext(el)
            latin = el
        el.set("typeface", FONT)


def _fill_paragraph(p_xml, p: P):
    """python-pptx _Paragraph 에 P 서식을 채운다."""
    p_xml.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p.align]
    p_xml.line_spacing = p.spacing
    p_xml.space_after = Pt(p.after)
    p_xml.space_before = Pt(p.before)
    for r in p.runs:
        parts = r.text.split("\n")
        for i, part in enumerate(parts):
            if i > 0:
                p_xml.add_line_break()
            if part == "" and len(parts) > 1:
                continue
            run = p_xml.add_run()
            run.text = part
            f = run.font
            f.size = Pt(r.size)
            f.bold = r.bold
            f.italic = r.italic
            f.color.rgb = rgb(r.color)
            _set_fonts(run, r.mono)
    pPr = p_xml._p.get_or_add_pPr()
    if EA_WORD_WRAP:
        pPr.set("eaLnBrk", "0")
    if p.bullet:
        pPr.set("marL", str(int(Inches(BULLET_INDENT))))
        pPr.set("indent", str(-int(Inches(BULLET_INDENT))))
        clr = etree.SubElement(pPr, qn("a:buClr"))
        etree.SubElement(clr, qn("a:srgbClr")).set("val", S400)
        etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Arial")
        etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
    else:
        etree.SubElement(pPr, qn("a:buNone"))


def _tf_setup(tf, margins, anchor, wrap=True):
    tf.word_wrap = wrap
    tf.auto_size = None
    l, t, r, b = margins
    tf.margin_left, tf.margin_top = Inches(l), Inches(t)
    tf.margin_right, tf.margin_bottom = Inches(r), Inches(b)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]


# ------------------------------------------------------------------ 어절 단위 줄바꿈 (명시적 줄바꿈 삽입)
# PowerPoint 는 eaLnBrk=0 을 줘도 한글을 글자 단위로 끊어 "지/체", "1/위" 같은 고아 글자를 만든다.
# AUTO_BREAK=True 이면 PIL 로 측정해 어절 단위로 줄을 나누고 줄바꿈(<a:br/>)을 직접 삽입한다.
AUTO_BREAK = False
BREAK_SAFETY = 0.965            # 측정 오차(폴백 글리프 등)를 흡수하기 위해 줄 폭을 약간 줄인다


def auto_break(p: P, width_in: float) -> P:
    avail = (width_in - (BULLET_INDENT if p.bullet else 0)) * BREAK_SAFETY
    toks = []                                    # (token, run_idx)
    for ri, r in enumerate(p.runs):
        for pi, part in enumerate(r.text.split("\n")):
            if pi > 0:
                toks.append(("\n", ri))
            buf = ""
            for ch in part:
                buf += ch
                if ch == " ":
                    toks.append((buf, ri))
                    buf = ""
            if buf:
                toks.append((buf, ri))
    lines: List[list] = [[]]
    cur = 0.0
    for tok, ri in toks:
        if tok == "\n":
            lines.append([])
            cur = 0.0
            continue
        r = p.runs[ri]
        w = text_w(tok.rstrip(" "), r.size, r.bold, r.mono)
        wf = text_w(tok, r.size, r.bold, r.mono)
        if cur > 0 and cur + w > avail:
            lines.append([])
            cur = 0.0
        if w > avail:                            # 한 어절이 한 줄보다 길면 글자 단위로 분할
            piece = ""
            for ch in tok:
                if text_w(piece + ch, r.size, r.bold, r.mono) > avail and piece:
                    lines[-1].append((piece, ri))
                    lines.append([])
                    piece = ""
                piece += ch
            if piece:
                lines[-1].append((piece, ri))
                cur = text_w(piece, r.size, r.bold, r.mono)
            continue
        lines[-1].append((tok, ri))
        cur += wf
    new_runs: List[R] = []
    for li, line in enumerate(lines):
        for ti, (tok, ri) in enumerate(line):
            last_in_line = ti == len(line) - 1
            text = tok.rstrip(" ") if last_in_line else tok
            if new_runs and new_runs[-1]._ri == ri and not new_runs[-1]._closed:
                new_runs[-1].text += text
            else:
                base = p.runs[ri]
                nr = R(text, base.size, base.bold, base.color, base.mono, base.italic)
                nr._ri, nr._closed = ri, False
                new_runs.append(nr)
        if li < len(lines) - 1 and new_runs:
            new_runs[-1].text += "\n"
            new_runs[-1]._closed = True          # 줄바꿈 뒤의 글자는 새 run 으로 시작
    return P(new_runs, p.align, p.bullet, p.after, p.before, p.spacing)


# ------------------------------------------------------------------ 요소 생성
def add_text(slide, x, y, w, h, paras: Union[P, Sequence[P]], anchor="t",
             margins=(0, 0, 0, 0), name=None, check=True):
    """텍스트 박스. 측정 높이가 h 를 넘으면 경고."""
    if isinstance(paras, P):
        paras = [paras]
    if AUTO_BREAK:
        paras = [auto_break(p, w - margins[0] - margins[2]) for p in paras]
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    _tf_setup(tf, margins, anchor)
    for i, p in enumerate(paras):
        _fill_paragraph(tf.paragraphs[0] if i == 0 else tf.add_paragraph(), p)
    if check:
        need = est_height(paras, w - margins[0] - margins[2]) + margins[1] + margins[3]
        if need > h * 1.03:
            first = paras[0].runs[0].text.replace("\n", " ")[:26]
            warn(f"텍스트 넘침 '{first}…' 필요 {need:.2f}in > 박스 {h:.2f}in (w={w:.2f})")
    return tb


def add_box(slide, x, y, w, h, fill: Optional[str] = WHITE, line: Optional[str] = None,
            line_w=0.75, radius=0.0, name=None, shape=None):
    """사각형/둥근 사각형. radius 는 in 단위 모서리 반경."""
    kind = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if radius > 0 else MSO_SHAPE.RECTANGLE)
    shp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        shp.name = name
    if radius > 0 and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = min(0.5, radius / min(w, h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = rgb(line)
        shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp


def add_card(slide, x, y, w, h, fill=WHITE, line=S200, line_w=0.75, radius=0.12, name=None):
    return add_box(slide, x, y, w, h, fill, line, line_w, radius, name)


def add_pill(slide, x, y, text, fill, color, line=None, size=10, bold=True, h=0.27,
             padx=0.13, mono=False, name=None, min_w=0.0) -> float:
    """알약 배지. 폭을 자동 계산하고 반환한다."""
    w = max(min_w, text_w(text, size, bold, mono) + 2 * padx + 0.04)
    shp = add_box(slide, x, y, w, h, fill, line, 0.75, h / 2, name or f"Pill-{text[:12]}")
    tf = shp.text_frame
    _tf_setup(tf, (0, 0, 0, 0), "m", wrap=False)
    _fill_paragraph(tf.paragraphs[0], para(text, size, bold, color, mono, align="c"))
    return w


def add_circle(slide, x, y, d, fill, line=None, name=None):
    return add_box(slide, x, y, d, d, fill, line, 0.75, 0, name, shape=MSO_SHAPE.OVAL)


def add_picture_contain(slide, path, x, y, w, h, pad=0.0, alt="", name=None):
    """이미지를 종횡비를 지키며 박스(x,y,w,h) 안에 중앙 contain 배치."""
    if not os.path.exists(path):
        warn(f"이미지 없음: {path}")
        return None
    with Image.open(path) as im:
        iw, ih = im.size
    aw, ah = w - 2 * pad, h - 2 * pad
    scale = min(aw / iw, ah / ih)
    pw, ph = iw * scale, ih * scale
    pic = slide.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2),
                                   Inches(pw), Inches(ph))
    if name:
        pic.name = name
    if alt:
        pic._element.nvPicPr.cNvPr.set("descr", alt)
    return pic


def set_bg(slide, hex6: str):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(hex6)


def set_notes(slide, text: str):
    slide.notes_slide.notes_text_frame.text = text


# ------------------------------------------------------------------ 표
NO_STYLE_ID = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"   # No Style, No Grid


def _cell_border(cell, bottom: Optional[str] = None, width_pt=0.75):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for old in tcPr.findall(qn(tag)):
            tcPr.remove(old)
    idx = 0
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = etree.Element(qn(tag))
        if tag == "a:lnB" and bottom:
            ln.set("w", str(int(Pt(width_pt))))
            sf = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr")).set("val", bottom)
        else:
            ln.set("w", "0")
            etree.SubElement(ln, qn("a:noFill"))
        tcPr.insert(idx, ln)
        idx += 1


def add_table(slide, x, y, col_w: Sequence[float], row_h: Sequence[float],
              cells: Sequence[Sequence[dict]], name=None):
    """cells[r][c] = dict(text, size, bold, color, fill, align, mono). 선은 하단 헤어라인만."""
    nr, nc = len(row_h), len(col_w)
    gf = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(col_w)), Inches(sum(row_h)))
    if name:
        gf.name = name
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for attr in ("firstRow", "bandRow", "firstCol", "lastRow", "lastCol", "bandCol"):
        tblPr.set(attr, "0")
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is None:
        sid = etree.SubElement(tblPr, qn("a:tableStyleId"))
    sid.text = NO_STYLE_ID
    for c, wv in enumerate(col_w):
        tbl.columns[c].width = Inches(wv)
    for r, hv in enumerate(row_h):
        tbl.rows[r].height = Inches(hv)
    for r in range(nr):
        for c in range(nc):
            spec = cells[r][c]
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            _cell_border(cell, bottom=spec.get("border", S200))
            fill = spec.get("fill")
            if fill:
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb(fill)
            else:
                cell.fill.background()
            tf = cell.text_frame
            tf.word_wrap = True
            p = para(spec["text"], spec.get("size", 11.5), spec.get("bold", False),
                     spec.get("color", S700), spec.get("mono", False), spec.get("align", "l"))
            if AUTO_BREAK:
                p = auto_break(p, col_w[c] - 0.24)
            _fill_paragraph(tf.paragraphs[0], p)
            need = para_lines(p, col_w[c] - 0.24)[1] + 0.08
            if need > row_h[r] * 1.03:
                warn(f"표 셀 넘침 r{r}c{c} '{spec['text'][:16]}' 필요 {need:.2f} > {row_h[r]:.2f}")
    return gf


# ------------------------------------------------------------------ 공통 크롬 (kicker / title / footer)
def add_chrome(slide, no: int, kicker: str, title: str, source: str,
               title_size=24, title_h=0.88, page_label=None, dots=True):
    """콘텐츠 슬라이드 공통 틀: 상단 키커 배지 + 액션 타이틀 + 하단 출처/페이지 인디케이터.
    부록 슬라이드는 page_label="A-1", dots=False 로 본문 인디케이터를 쓰지 않는다."""
    add_pill(slide, MX, 0.36, kicker, S100, S700, S200, size=10, name="Kicker")
    add_text(slide, MX, 0.72, CW, title_h,
             para(title, title_size, True, S900, spacing=0.92), name="ActionTitle")
    # footer
    add_text(slide, MX, 7.0, 9.1, 0.36, para(source, 9.5, False, S500), name="Source")
    if dots:
        dots_x = SLIDE_W - MX - 0.95 - 14 * 0.125
        for i in range(TOTAL_SLIDES):
            add_circle(slide, dots_x + i * 0.125, 7.12, 0.07,
                       S900 if i + 1 == no else (S400 if i + 1 < no else S200), name=f"Dot{i + 1}")
    add_text(slide, SLIDE_W - MX - 0.85, 7.04, 0.85, 0.22,
             para(page_label or f"{no:02d} / {TOTAL_SLIDES}", 10, True, S700, mono=True, align="r"), name="PageNo")


# ------------------------------------------------------------------ 네비게이션 (슬라이드 쇼 점프 링크 / 섹션)
def add_hotspot(slide, x, y, w, h, target_slide, name="Hotspot"):
    """완전 투명하지만 클릭 가능한 영역(알파 0 채움)을 올려 슬라이드 쇼에서 target_slide 로 점프시킨다.
    채움이 없는 도형은 PowerPoint 에서 내부 클릭이 통과하므로 알파 0 의 채움을 쓴다."""
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.name = name
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(WHITE)
    srgb = shp._element.spPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
    etree.SubElement(srgb, qn("a:alpha")).set("val", "0")
    shp.line.fill.background()
    shp.shadow.inherit = False
    shp.click_action.target_slide = target_slide
    return shp


def link_footer_dots(prs, total=TOTAL_SLIDES):
    """모든 슬라이드의 하단 인디케이터 점(●)을 해당 슬라이드로 가는 링크로 만든다."""
    dots_x = SLIDE_W - MX - 0.95 - total * 0.125
    for s in list(prs.slides)[1:total]:                  # 표지와 부록에는 인디케이터가 없다
        for i in range(total):
            add_hotspot(s, dots_x + i * 0.125 - 0.02, 7.06, 0.125, 0.2, prs.slides[i], f"Nav-{i + 1}")


def add_sections(prs, sections):
    """PowerPoint 섹션(리본 > 구역)을 만든다. sections = [(이름, [1-based 슬라이드 번호...]), ...]."""
    import uuid
    P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
    pres = prs._element
    ids = [sid.get("id") for sid in pres.sldIdLst]
    ext_lst = pres.find(qn("p:extLst"))
    if ext_lst is None:
        ext_lst = etree.SubElement(pres, qn("p:extLst"))
    ext = etree.SubElement(ext_lst, qn("p:ext"))
    ext.set("uri", "{521415D9-36F7-43E2-AB2F-B90AF26B5E84}")
    sec_lst = etree.SubElement(ext, "{%s}sectionLst" % P14, nsmap={"p14": P14})
    for name, nums in sections:
        sec = etree.SubElement(sec_lst, "{%s}section" % P14)
        sec.set("name", name)
        sec.set("id", "{" + str(uuid.uuid4()).upper() + "}")
        lst = etree.SubElement(sec, "{%s}sldIdLst" % P14)
        for n in nums:
            etree.SubElement(lst, "{%s}sldId" % P14).set("id", ids[n - 1])


# ------------------------------------------------------------------ 저장
def _patch_theme_fonts(prs):
    """테마 글꼴을 맑은 고딕으로 바꿔, PowerPoint 에서 새로 입력한 글자도 일관된 서체를 쓰게 한다."""
    master = prs.slide_master
    theme = master.part.part_related_by(RT.THEME)
    xml = etree.fromstring(theme.blob)
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    for tag in ("a:majorFont", "a:minorFont"):
        el = xml.find(f".//{tag}", ns)
        if el is None:
            continue
        el.find("a:latin", ns).set("typeface", FONT)
        ea = el.find("a:ea", ns)
        if ea is not None:
            ea.set("typeface", FONT)
    theme._blob = etree.tostring(xml, xml_declaration=True, encoding="UTF-8", standalone=True)


def new_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    return prs


def blank_slide(prs, no: int, bg=WHITE):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, bg)
    set_context(no)
    return s


def save_deck(prs, path: str, title: str, subject: str = ""):
    _patch_theme_fonts(prs)
    cp = prs.core_properties
    cp.title = title
    cp.subject = subject
    cp.author = "퍼즐데이터 채용 과제"
    cp.keywords = "process mining, repair process, lead time, bottleneck"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    prs.save(path)
    print(f"saved: {path}  ({len(prs.slides)} slides)")
    if WARNINGS:
        print(f"\n[빌드 경고 {len(WARNINGS)}건]")
        for w_ in WARNINGS:
            print("  -", w_)
    else:
        print("[빌드 경고 0건] 모든 텍스트가 박스 안에 들어갑니다 (측정 기준).")
