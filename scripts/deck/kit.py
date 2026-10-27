"""엔진 위의 컴포넌트: 카드·행·칩·막대·표·크롬(태그/제목/출처/페이지)."""
from engine import *            # noqa: F401,F403
from engine import _hex

BODY_TOP, BODY_BOTTOM = 1.62, 6.90


# ------------------------------------------------------------------ 흐름 요소
class Txt:
    def __init__(self, paras, role="body", name="t", anchor="t", structural=False, max_lines=None):
        self.paras = paras if isinstance(paras, (list, tuple)) else [paras]
        self.role, self.name, self.anchor, self.structural, self.max_lines = role, name, anchor, structural, max_lines

    def h(self, w):
        tot = 0.0
        for i, p in enumerate(self.paras):
            hh, _ = para_height_in(p, w)
            tot += hh - (p.before / 72.0 if i == 0 else 0.0)
        return tot

    def draw(self, sl, x, y, w, parent):
        return sl.text(x, y, w, self.paras, parent=parent, name=self.name, anchor=self.anchor, structural=self.structural,
                       role=self.role, max_lines=self.max_lines)[0]


class Gap:
    def __init__(self, hh):
        self._h = hh

    def h(self, w):
        return self._h

    def draw(self, sl, x, y, w, parent):
        return None


class Img:
    """차트 이미지(contain). 폭에 맞춰 높이를 정하되 max_h 를 넘으면 높이에 맞춘다."""

    def __init__(self, path, max_h=None, fixed_h=None, name="chart", pad=0.0):
        self.path, self.max_h, self.fixed_h, self.name, self.pad = path, max_h, fixed_h, name, pad
        iw, ih = Image.open(path).size
        self.asp = iw / ih

    def h(self, w):
        if self.fixed_h:
            return self.fixed_h
        hh = (w - 2 * self.pad) / self.asp + 2 * self.pad
        return min(hh, self.max_h) if self.max_h else hh

    def draw(self, sl, x, y, w, parent):
        return sl.picture(self.path, x, y, w, self.h(w), parent=parent, name=self.name, pad=self.pad)[0]


class Pill:
    def __init__(self, text, color=ACC, bg=ACC_BG, size=9, name="pill"):
        color, bg = ACC, ACC_BG
        self.text, self.color, self.bg, self.size, self.name = text, color, bg, size, name
        self.tw = text_w(text, "m", True, size) * 1.12

    def h(self, w):
        return 0.26

    def draw(self, sl, x, y, w, parent):
        pw = self.tw + 0.2
        sh, rid = sl.rect(x, y, pw, 0.26, fill=self.bg, line=None, parent=parent, name=self.name)
        sl.text(x + 0.1, y, self.tw + 0.02, [T(self.text, self.size, True, self.color, "m")], parent=rid, name=self.name + "-t",
                anchor="m", h=0.26, structural=True, role="pill")
        return sh


class Bar:
    """비율 막대(트랙 + 채움). frac 0~1."""

    def __init__(self, frac, color=ACC, hh=0.09, name="bar"):
        self.frac, self.color, self._h, self.name = frac, color, hh, name

    def h(self, w):
        return self._h

    def draw(self, sl, x, y, w, parent):
        _, rid = sl.rect(x, y, w, self._h, fill=SLATE_BG, line=None, parent=parent, name=self.name + "-track")
        sl.rect(x, y, max(w * self.frac, 0.02), self._h, fill=self.color, line=None, parent=rid, name=self.name + "-fill")
        return None


class Rule:
    def h(self, w):
        return 0.02

    def draw(self, sl, x, y, w, parent):
        sl.hline(x, y + 0.01, w, parent=parent)
        return None


def big(num, unit="", color=INK, size=40, unit_size=None, keep=False, **kw):
    if color == ACC and not keep:                      # 일반 지표는 슬레이트-900, 의미색은 RED/GRN만
        color = INK
    runs = tri_runs(num, size, True, color, "m")
    if unit:
        runs.append(R(unit, unit_size or max(size * 0.4, 12), True, color, "k"))
    return Txt([P(runs, lh=LH_BIG, balance=False)], **kw)


def label(text, color=MUTED, size=9.5, **kw):
    if color in (RED, GRN, ACC):          # 카드 라벨/인덱스는 단일 브랜드 블루
        color = ACC
    return Txt([T(text, size, True, color, "m", balance=False)], structural=True, role="label", **kw)


def body(text, size=11.5, color=INK2, accent=ACC, **kw):
    return Txt([rich(text, size, color, accent=accent)], **kw)


def bullets(items, size=11.5, color=INK2, gap=3.0):
    return Txt([P(rich(i, size, color).runs, bullet=True, before=(gap if k else 0)) for k, i in enumerate(items)])


def heading(text, size=14, color=INK, **kw):
    return Txt([T(text, size, True, color)], **kw)


class Custom:
    """직접 그리는 요소. fn(sl, x, y, w, parent)."""

    def __init__(self, hh, fn):
        self._h, self.fn = hh, fn

    def h(self, w):
        return self._h

    def draw(self, sl, x, y, w, parent):
        self.fn(sl, x, y, w, parent)
        return None


class Table:
    """행 높이를 내용으로 계산하는 표. cols: [(비율, 헤더, 정렬)], rows: [[P 목록 또는 Txt, ...], ...]."""

    def __init__(self, cols, rows, pad_y=0.09, pad_x=0.1, head=True, name="tbl", row_fills=None):
        self.cols, self.rows, self.pad_y, self.pad_x, self.head, self.name = cols, rows, pad_y, pad_x, head, name
        self.row_fills = row_fills or {}

    def _widths(self, w):
        tot = sum(c[0] for c in self.cols)
        return [w * c[0] / tot for c in self.cols]

    def _cell_h(self, cell, cw):
        el = cell if isinstance(cell, Txt) else Txt(cell)
        return el.h(cw - 2 * self.pad_x)

    def row_hs(self, w):
        ws = self._widths(w)
        hs = []
        for r in self.rows:
            hs.append(max(self._cell_h(c, cw) for c, cw in zip(r, ws)) + 2 * self.pad_y)
        return hs

    def h(self, w):
        return (0.3 if self.head else 0.0) + sum(self.row_hs(w))

    def draw(self, sl, x, y, w, parent):
        ws = self._widths(w)
        cy = y
        if self.head:
            cx = x
            for (_, hd, al), cw in zip(self.cols, ws):
                sl.text(cx + self.pad_x, cy + 0.04, cw - 2 * self.pad_x, [T(hd, 9.5, True, MUTED, "m", align=al, balance=False)],
                        parent=parent, name=self.name + "-h", structural=True, role="label", max_lines=1)
                cx += cw
            cy += 0.3
            sl.hline(x, cy, w, parent=parent)
        for ri, (r, rh) in enumerate(zip(self.rows, self.row_hs(w))):
            par = parent
            if ri in self.row_fills:
                _, par = sl.rect(x, cy + 0.01, w, rh - 0.01, fill=self.row_fills[ri], line=None, parent=parent, name=self.name + "-fill")
            cx = x
            for c, cw in zip(r, ws):
                el = c if isinstance(c, Txt) else Txt(c)
                el.draw(sl, cx + self.pad_x, cy + self.pad_y, cw - 2 * self.pad_x, par)
                cx += cw
            cy += rh
            if ri < len(self.rows) - 1:
                sl.hline(x, cy, w, parent=parent)
        return None


# ------------------------------------------------------------------ 카드
class Card:
    def __init__(self, els, pad=0.2, gap=0.09, fill=CARD, line=BORDER, lw=0.75, foot=None, name="card", min_h=0.0, link=None):
        if line in (ACC, GRN):             # 보더는 #E2E8F0 통일, 병목 강조(RED)만 예외
            line = BORDER
        self.els, self.pad, self.gap, self.fill, self.line, self.lw = els, pad, gap, fill, line, lw
        self.foot, self.name, self.min_h, self.link = foot, name, min_h, link

    def inner_h(self, w):
        iw = w - 2 * self.pad
        hs = [e.h(iw) for e in self.els]
        return sum(hs) + self.gap * max(len(hs) - 1, 0)

    def natural_h(self, w):
        iw = w - 2 * self.pad
        fh = (self.foot.h(iw) + self.gap) if self.foot else 0.0
        return max(self.inner_h(w) + fh + 2 * self.pad, self.min_h)

    def h(self, w):                      # 중첩 카드용
        return self.natural_h(w)

    def draw(self, sl, x, y, w, h=None, parent=0):
        h = h if h is not None else self.natural_h(w)
        nat = self.natural_h(w)
        if h + 1e-6 < nat:
            raise LayoutError(f"[S{sl.no}:{self.name}] 카드 높이 {h:.2f}in < 내용 {nat:.2f}in")
        sh, rid = sl.rect(x, y, w, h, fill=self.fill, line=self.line, lw=self.lw, name=self.name, parent=parent)
        iw, cy = w - 2 * self.pad, y + self.pad
        for e in self.els:
            if isinstance(e, Card):
                e.draw(sl, x + self.pad, cy, iw, e.natural_h(iw), parent=rid)
            else:
                e.draw(sl, x + self.pad, cy, iw, rid)
            cy += e.h(iw) + self.gap
        if self.foot:
            fy = y + h - self.pad - self.foot.h(iw)
            self.foot.draw(sl, x + self.pad, fy, iw, rid)
        if self.link:
            sl.doc.links.append((sh, self.link))
        return sh, h


def row(sl, x, y, w, cards, weights=None, gutter=0.2, h=None):
    n = len(cards)
    weights = weights or [1] * n
    avail = w - gutter * (n - 1)
    widths = [avail * wt / sum(weights) for wt in weights]
    hh = h if h is not None else max(c.natural_h(wi) for c, wi in zip(cards, widths))
    cx = x
    for c, wi in zip(cards, widths):
        c.draw(sl, cx, y, wi, hh)
        cx += wi + gutter
    return hh


def stack(sl, x, y, w, cards, gutter=0.12, h_total=None):
    """세로 스택. h_total 이 주어지면 남는 높이를 카드에 균등 분배한다."""
    nat = [c.natural_h(w) for c in cards]
    extra = 0.0
    if h_total is not None:
        extra = (h_total - sum(nat) - gutter * (len(cards) - 1)) / len(cards)
        if extra < -1e-6:
            raise LayoutError(f"[S{sl.no}] 스택 높이 초과: 필요 {sum(nat) + gutter * (len(cards) - 1):.2f} > {h_total:.2f}in")
    cy = y
    for c, hn in zip(cards, nat):
        c.draw(sl, x, cy, w, hn + max(extra, 0.0))
        cy += hn + max(extra, 0.0) + gutter
    return cy - gutter


# ------------------------------------------------------------------ 크롬
def chrome(sl: Slide, tag, title, sub=None, source=None, total=19):
    sl.text(MX, 0.38, 7.5, [T(tag, 11, True, ACC, "m", balance=False)], structural=True, name="tag", role="tag", max_lines=1)
    sl.text(SLIDE_W - MX - 4.6, 0.40, 4.6, [T("PUZZLEDATA · REPAIR PROCESS ANALYSIS", 9, False, MUTED, "m", align="r", balance=False)],
            structural=True, name="brand", role="brand", max_lines=1)
    sl.text(MX, 0.68, CW, [P(tri_runs(title, 26, True, INK), balance=False)], name="title", role="title", max_lines=1)
    if sub:
        sl.text(MX, 1.20, CW, [rich(sub, 12, MUTED, accent=INK2, balance=False)], name="sub", role="sub", max_lines=1)
    sl.hline(MX, 6.98, CW, name="foot-rule")
    if source:
        sl.text(MX, 7.06, 10.6, [T(source, 9, False, "94A3B8", "m", balance=False)], structural=True, name="source", role="foot", max_lines=1)
    sl.text(SLIDE_W - MX - 1.4, 7.06, 1.4, [T(f"{sl.no:02d} / {total}", 9, True, "94A3B8", "m", align="r", balance=False)],
            structural=True, name="page", role="page", max_lines=1)


def assert_body(sl, y_end, name=""):
    if y_end > BODY_BOTTOM + 1e-6:
        raise LayoutError(f"[S{sl.no}] 본문이 하단 {BODY_BOTTOM}in 초과: {y_end:.2f}in {name}")
