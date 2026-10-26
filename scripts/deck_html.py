# -*- coding: utf-8 -*-
"""deck_common 과 같은 API 를 제공하는 HTML 백엔드.

build_deck_v3.py 를 수정 없이 실행하면서 deck_common 대신 이 모듈을 주입하면
같은 슬라이드 정의(좌표·텍스트·차트)가 단일 HTML 프레젠테이션 웹앱으로 렌더링된다.
  - 좌표 단위: PPTX 의 inch → 144px/in (13.333in = 1920px), 글자 pt → 2px/pt
  - 한글은 CSS word-break:keep-all 로 어절 단위 줄바꿈
  - 이미지는 base64 로 내장(단일 파일), object-fit:contain 으로 종횡비 보호
  - 내비게이션: ←/→/PageUp/PageDown/Space/Home/End, 하단 점·버튼 클릭, 터치 스와이프, 해시(#8)
  - 발표자 노트: 'S' 키 또는 마이크 버튼으로 하단 시트 토글, 'F' 전체화면, 인쇄(Ctrl+P) 시 슬라이드당 1페이지
"""
import base64
import html
import json
import os
import re
from typing import List

from deck_common import *  # noqa: F401,F403  (색상 토큰, R/P/para, text_w, 경로 상수 등을 그대로 노출)
from deck_common import BULLET_INDENT, LINE_FACTOR, MX, CW, SLIDE_W, TOTAL_SLIDES, text_w, warn  # noqa: F401

PX = 144.0                       # px per inch
HTML_OUT_DIR = os.path.join(BASE_DIR, "outputs", "html")
EA_WORD_WRAP = True              # v3 스크립트가 설정하는 값(무시)
AUTO_BREAK = True


def _px(v: float) -> str:
    return f"{v * PX:.1f}px"


_HY = re.compile(r"(?<=[A-Za-z0-9])-(?=[A-Za-z0-9])")


def _esc(t: str) -> str:
    """HTML 이스케이프 + 영문/숫자 사이 하이픈을 비분리 하이픈(U+2011)으로 바꿔 'TO-/BE' 같은 줄바꿈을 막는다."""
    return _HY.sub("‑", html.escape(t, quote=True)).replace("\n", "<br>")


# ------------------------------------------------------------------ 요소 모델
class _Line:
    dash_style = None


class _Shape:
    """add_box 가 돌려주는 핸들. 이후 속성 변경(점선 등)을 렌더 시점에 반영한다."""

    def __init__(self, cls, style, inner="", tag="div", attrs=""):
        self.cls, self.style, self.inner, self.tag, self.attrs = cls, style, inner, tag, attrs
        self.line = _Line()

    def render(self):
        style = self.style
        if self.line.dash_style is not None:
            style += "border-style:dashed;"
        return f'<{self.tag} class="e {self.cls}" style="{style}" {self.attrs}>{self.inner}</{self.tag}>'


class _Slide:
    def __init__(self, no, bg):
        self.no, self.bg, self.items, self.notes = no, bg, [], ""

    def add(self, el):
        self.items.append(el)
        return el


class _Deck:
    def __init__(self):
        self.slides: List[_Slide] = []
        self.sections = []


# ------------------------------------------------------------------ deck_common 호환 API
def new_presentation():
    return _Deck()


def blank_slide(prs, no, bg=WHITE):
    s = _Slide(no, bg)
    prs.slides.append(s)
    set_context(no)
    return s


def set_notes(slide, text):
    slide.notes = text


def _run_html(r: R) -> str:
    fam = "var(--mono)" if r.mono else "inherit"
    st = f"font-size:{r.size * 2:.1f}px;font-weight:{700 if r.bold else 400};color:#{r.color};font-family:{fam};"
    if r.italic:
        st += "font-style:italic;"
    return f'<span style="{st}">{_esc(r.text)}</span>'


def _para_html(p: P) -> str:
    al = {"l": "left", "c": "center", "r": "right"}[p.align]
    st = (f"text-align:{al};margin-top:{p.before * 2:.1f}px;margin-bottom:{p.after * 2:.1f}px;"
          f"line-height:{LINE_FACTOR * p.spacing:.3f};")
    if p.bullet:
        st += f"padding-left:{BULLET_INDENT * PX:.1f}px;"
    return f'<div class="p{" b" if p.bullet else ""}" style="{st}">{"".join(_run_html(r) for r in p.runs)}</div>'


def add_text(slide, x, y, w, h, paras, anchor="t", margins=(0, 0, 0, 0), name=None, check=True):
    if isinstance(paras, P):
        paras = [paras]
    jc = {"t": "flex-start", "m": "center", "b": "flex-end"}[anchor]
    st = (f"left:{_px(x)};top:{_px(y)};width:{_px(w)};height:{_px(h)};justify-content:{jc};"
          f"padding:{_px(margins[1])} {_px(margins[2])} {_px(margins[3])} {_px(margins[0])};")
    label = f' data-name="{html.escape(name)}"' if name else ""
    return slide.add(_Shape("t", st, "".join(_para_html(p) for p in paras), attrs=label))


def add_box(slide, x, y, w, h, fill=WHITE, line=None, line_w=0.75, radius=0.0, name=None, shape=None):
    st = f"left:{_px(x)};top:{_px(y)};width:{_px(w)};height:{_px(h)};"
    st += f"background:#{fill};" if fill else "background:transparent;"
    if line:
        st += f"border:{max(1.0, line_w * 2):.1f}px solid #{line};"
    if shape is not None:
        st += "border-radius:50%;"
    elif radius > 0:
        st += f"border-radius:{_px(radius)};"
    return slide.add(_Shape("box", st))


def add_card(slide, x, y, w, h, fill=WHITE, line=S200, line_w=0.75, radius=0.12, name=None):
    return add_box(slide, x, y, w, h, fill, line, line_w, radius, name)


def add_circle(slide, x, y, d, fill, line=None, name=None):
    return add_box(slide, x, y, d, d, fill, line, 0.75, 0, name, shape="oval")


def add_pill(slide, x, y, text, fill, color, line=None, size=10, bold=True, h=0.27, padx=0.13,
             mono=False, name=None, min_w=0.0):
    w = max(min_w, text_w(text, size, bold, mono) + 2 * padx + 0.04)
    fam = "var(--mono)" if mono else "inherit"
    st = (f"left:{_px(x)};top:{_px(y)};width:{_px(w)};height:{_px(h)};background:#{fill};color:#{color};"
          f"border-radius:{_px(h / 2)};font-size:{size * 2:.1f}px;font-weight:{700 if bold else 400};font-family:{fam};")
    if line:
        st += f"border:1.5px solid #{line};"
    slide.add(_Shape("pill", st, _esc(text)))
    return w


_img_cache = {}


class _ImgShape(_Shape):
    def __init__(self, style, src, alt):
        super().__init__("im", style)
        self.src, self.alt = src, alt

    def render(self):
        return f'<img class="e im" style="{self.style}" alt="{html.escape(self.alt)}" src="{self.src}">'


def add_picture_contain(slide, path, x, y, w, h, pad=0.0, alt="", name=None):
    """박스(x,y,w,h)에 이미지를 object-fit:contain 으로 배치해 종횡비를 보호한다."""
    if not os.path.exists(path):
        warn(f"이미지 없음: {path}")
        return None
    if path not in _img_cache:
        with open(path, "rb") as f:
            _img_cache[path] = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")
    st = (f"left:{_px(x + pad)};top:{_px(y + pad)};width:{_px(w - 2 * pad)};height:{_px(h - 2 * pad)};"
          "object-fit:contain;")
    return slide.add(_ImgShape(st, _img_cache[path], alt))


def add_table(slide, x, y, col_w, row_h, cells, name=None):
    cols = "".join(f'<col style="width:{_px(w)}">' for w in col_w)
    rows = []
    for r, hv in enumerate(row_h):
        tds = []
        for c, spec in enumerate(cells[r]):
            fam = "var(--mono)" if spec.get("mono") else "inherit"
            st = (f"font-size:{spec.get('size', 11.5) * 2:.1f}px;font-weight:{700 if spec.get('bold') else 400};"
                  f"color:#{spec.get('color', S700)};text-align:{ {'l': 'left', 'c': 'center', 'r': 'right'}[spec.get('align', 'l')] };"
                  f"font-family:{fam};border-bottom:1.5px solid #{spec.get('border', S200)};")
            if spec.get("fill"):
                st += f"background:#{spec['fill']};"
            tds.append(f'<td style="{st}">{_esc(spec["text"])}</td>')
        rows.append(f'<tr style="height:{_px(hv)}">{"".join(tds)}</tr>')
    st = f"left:{_px(x)};top:{_px(y)};width:{_px(sum(col_w))};"
    return slide.add(_Shape("tbl", st, f"<colgroup>{cols}</colgroup>{''.join(rows)}", tag="table"))


def add_hotspot(slide, x, y, w, h, target_slide, name="Hotspot"):
    st = f"left:{_px(x)};top:{_px(y)};width:{_px(w)};height:{_px(h)};"
    return slide.add(_Shape("hot", st, "", tag="a", attrs=f'href="#{target_slide.no}" aria-label="슬라이드 {target_slide.no}로 이동"'))


def link_footer_dots(prs, total=TOTAL_SLIDES):
    """HTML 에서는 add_chrome 이 점을 이미 링크(<a>)로 만들어 둔다."""
    return None


def add_sections(prs, sections):
    prs.sections = sections


def add_chrome(slide, no, kicker, title, source, title_size=24, title_h=0.88, page_label=None, dots=True):
    add_pill(slide, MX, 0.36, kicker, S100, S700, S200, size=10, name="Kicker")
    add_text(slide, MX, 0.72, CW, title_h, para(title, title_size, True, S900, spacing=0.92), name="ActionTitle")
    add_text(slide, MX, 7.0, 9.1, 0.36, para(source, 9.5, False, S500), name="Source")
    if dots:
        dots_x = SLIDE_W - MX - 0.95 - TOTAL_SLIDES * 0.125
        for i in range(TOTAL_SLIDES):
            col = S900 if i + 1 == no else (S400 if i + 1 < no else S200)
            st = f"left:{_px(dots_x + i * 0.125)};top:{_px(7.12)};width:{_px(0.07)};height:{_px(0.07)};background:#{col};"
            slide.add(_Shape("dot", st, "", tag="a", attrs=f'href="#{i + 1}" aria-label="슬라이드 {i + 1}"'))
    add_text(slide, SLIDE_W - MX - 0.85, 7.04, 0.85, 0.22,
             para(page_label or f"{no:02d} / {TOTAL_SLIDES}", 10, True, S700, mono=True, align="r"), name="PageNo")


# ------------------------------------------------------------------ HTML 셸 (CSS + JS)
_CSS = """
:root{--mono:'JetBrains Mono','Cascadia Mono',Consolas,'D2Coding',monospace}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden;background:#F1F5F9;color:#0F172A;
 font-family:'Pretendard','Pretendard Variable','Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',sans-serif;
 -webkit-font-smoothing:antialiased}
#stage{position:absolute;left:50%;top:50%;width:1920px;height:1080px;background:#fff;flex:none;
 transform-origin:center center;box-shadow:0 12px 48px rgba(15,23,42,.14)}
.slide{position:absolute;inset:0;display:none;overflow:hidden}
.slide.active{display:block;animation:fade .28s ease}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.e{position:absolute}
.t{display:flex;flex-direction:column;word-break:keep-all;overflow-wrap:break-word}
.p{position:relative}
.p.b::before{content:"•";position:absolute;left:0;top:0;color:#94A3B8;font-size:inherit;line-height:inherit}
.pill{display:flex;align-items:center;justify-content:center;white-space:nowrap}
.im{display:block}
table.tbl{border-collapse:collapse;table-layout:fixed}
table.tbl td{padding:6px 17px;vertical-align:middle;word-break:keep-all;line-height:1.35}
a.hot{display:block;cursor:pointer;border-radius:20px}
a.hot:hover{background:rgba(37,99,235,.05);outline:3px solid rgba(37,99,235,.35)}
a.dot{display:block;border-radius:50%;cursor:pointer}
a.dot::after{content:"";position:absolute;inset:-9px -3px}
#progress{position:fixed;left:0;top:0;right:0;height:5px;background:rgba(148,163,184,.25);z-index:30}
#progress i{display:block;height:100%;width:0;background:#2563EB;transition:width .3s ease}
#ui{position:fixed;right:18px;top:14px;display:flex;align-items:center;gap:6px;z-index:30;
 padding:6px 8px;border-radius:999px;background:rgba(255,255,255,.92);border:1px solid #E2E8F0;
 box-shadow:0 6px 22px rgba(15,23,42,.12);backdrop-filter:blur(8px);transition:opacity .35s}
#ui.idle{opacity:0}
#ui button{all:unset;display:grid;place-items:center;width:38px;height:38px;border-radius:50%;cursor:pointer;color:#334155}
#ui button:hover,#ui button:focus-visible{background:#F1F5F9;color:#0F172A}
#ui button[aria-pressed=true]{background:#DBEAFE;color:#1D4ED8}
#ui svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
#counter{min-width:84px;text-align:center;font:700 14px var(--mono);color:#334155}
#notes{position:fixed;left:0;right:0;bottom:0;z-index:40;max-height:44vh;overflow:auto;
 background:rgba(255,255,255,.95);backdrop-filter:blur(14px);border-top:1px solid #CBD5E1;
 box-shadow:0 -12px 40px rgba(15,23,42,.16);transform:translateY(102%);transition:transform .28s ease}
#notes.open{transform:none}
#notes .in{max-width:1180px;margin:0 auto;padding:18px 28px 28px}
#notes h2{font-size:13px;font-weight:700;color:#64748B;letter-spacing:.04em;margin-bottom:10px;display:flex;justify-content:space-between}
#notes h2 kbd{font:700 12px var(--mono);background:#F1F5F9;border:1px solid #CBD5E1;border-radius:5px;padding:1px 7px;color:#334155}
#notes p{font-size:18px;line-height:1.75;color:#1E293B;word-break:keep-all;white-space:pre-line}
@media print{
 html,body{overflow:visible;background:#fff}
 #ui,#progress,#notes{display:none!important}
 #stage{position:static;transform:none!important;box-shadow:none;width:auto;height:auto}
 .slide{display:block!important;position:relative;width:1920px;height:1080px;page-break-after:always;break-after:page;animation:none}
 a.hot:hover{background:none;outline:none}
 @page{size:1920px 1080px;margin:0}
}
"""

_JS = """
const slides=[...document.querySelectorAll('.slide')], N=slides.length;
const notes=JSON.parse(document.getElementById('notes-data').textContent);
const stage=document.getElementById('stage'), bar=document.querySelector('#progress i'), counter=document.getElementById('counter');
const sheet=document.getElementById('notes'), sheetBody=document.getElementById('notes-body'), sheetHead=document.getElementById('notes-head');
const ui=document.getElementById('ui'), notesBtn=document.getElementById('notesBtn');
let cur=0, idleT;
function fit(){const s=Math.min(innerWidth/1920,(innerHeight-8)/1080);stage.style.transform=`translate(-50%,-50%) scale(${s})`}
function show(n){
  cur=Math.max(0,Math.min(N-1,n));
  slides.forEach((el,i)=>el.classList.toggle('active',i===cur));
  bar.style.width=((cur+1)/N*100)+'%';
  counter.textContent=String(cur+1).padStart(2,'0')+' / '+String(N).padStart(2,'0');
  sheetHead.firstChild.textContent='발표 대본 · Slide '+String(cur+1).padStart(2,'0');
  sheetBody.textContent=notes[cur]||'(이 슬라이드의 발표 대본이 없습니다)';
  sheet.scrollTop=0;
  history.replaceState(null,'','#'+(cur+1));
}
const next=()=>show(cur+1), prev=()=>show(cur-1);
function toggleNotes(force){const o=force===undefined?!sheet.classList.contains('open'):force;sheet.classList.toggle('open',o);notesBtn.setAttribute('aria-pressed',o)}
function toggleFs(){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen?.()}
addEventListener('keydown',e=>{
  if(e.metaKey||e.ctrlKey||e.altKey)return;
  switch(e.code){
    case 'ArrowRight':case 'PageDown':case 'Space':e.preventDefault();next();break;
    case 'ArrowLeft':case 'PageUp':e.preventDefault();prev();break;
    case 'Home':show(0);break; case 'End':show(N-1);break;
    case 'KeyS':toggleNotes();break; case 'KeyF':toggleFs();break;
    case 'Escape':toggleNotes(false);break;
  }
});
addEventListener('hashchange',()=>{const n=parseInt(location.hash.slice(1),10);if(n&&n-1!==cur)show(n-1)});
addEventListener('resize',fit);
document.getElementById('next').onclick=next; document.getElementById('prev').onclick=prev;
notesBtn.onclick=()=>toggleNotes(); document.getElementById('fs').onclick=toggleFs;
let sx=null;
addEventListener('touchstart',e=>{sx=e.touches[0].clientX},{passive:true});
addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>60)(dx<0?next:prev)();sx=null},{passive:true});
function wake(){ui.classList.remove('idle');clearTimeout(idleT);idleT=setTimeout(()=>ui.classList.add('idle'),3000)}
['mousemove','keydown','touchstart'].forEach(ev=>addEventListener(ev,wake)); wake();
const wantNotes=/notes/.test(location.search+location.hash);
fit(); show((parseInt(location.hash.slice(1),10)||1)-1);
if(wantNotes)toggleNotes(true);
"""

_ICON = {
    "prev": '<svg viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></svg>',
    "next": '<svg viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>',
    "mic": '<svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/></svg>',
    "fs": '<svg viewBox="0 0 24 24"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg>',
}


def save_deck(prs, path, title, subject=""):
    os.makedirs(HTML_OUT_DIR, exist_ok=True)
    out = os.path.join(HTML_OUT_DIR, "puzzledata_repair_report.html")
    secs = "".join(
        f'<section class="slide" id="s{s.no}" style="background:#{s.bg}" aria-label="슬라이드 {s.no}">'
        + "".join(el.render() for el in s.items) + "</section>"
        for s in prs.slides)
    notes = json.dumps([s.notes for s in prs.slides], ensure_ascii=False).replace("</", "<\\/")
    page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(subject)}">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
<style>{_CSS}</style>
</head>
<body>
<div id="progress" aria-hidden="true"><i></i></div>
<main id="stage">{secs}</main>
<nav id="ui" aria-label="슬라이드 내비게이션">
 <button id="prev" title="이전 (←)" aria-label="이전 슬라이드">{_ICON['prev']}</button>
 <span id="counter">01 / {len(prs.slides):02d}</span>
 <button id="next" title="다음 (→)" aria-label="다음 슬라이드">{_ICON['next']}</button>
 <button id="notesBtn" title="발표자 노트 (S)" aria-label="발표자 노트 토글" aria-pressed="false">{_ICON['mic']}</button>
 <button id="fs" title="전체화면 (F)" aria-label="전체화면">{_ICON['fs']}</button>
</nav>
<aside id="notes" aria-label="발표자 노트"><div class="in"><h2 id="notes-head"><span>발표 대본</span><kbd>S</kbd></h2><p id="notes-body"></p></div></aside>
<script id="notes-data" type="application/json">{notes}</script>
<script>{_JS}</script>
</body>
</html>"""
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"saved: {out}  ({len(prs.slides)} slides, {len(page) / 1e6:.2f} MB)")
