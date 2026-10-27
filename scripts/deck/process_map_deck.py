"""슬라이드 7 프로세스 맵 덱 전용판: docs/repair_process_map.html 의 구성(3구간·노드·간선)을 그대로 두고
덱 톤앤매너(맑은 고딕·Consolas, 덱 색상 토큰, 9.5pt 이상 글자)로 다시 그려 PNG 로 렌더한다.

원본 docs/repair_process_map.html 은 수정하지 않는다. 수치는 facts.json 에서만 읽는다.
실행: python -X utf8 scripts/deck/process_map_deck.py   (프로젝트 루트 기준, Edge/Chrome 필요)
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = json.load(open(os.path.join(ROOT, "scripts", "deck", "facts.json"), encoding="utf-8"))["facts"]
s = lambda k: F[k]["s"]

OUT_DIR = os.path.join(ROOT, "outputs", "figures", "deck")
HTML = os.path.join(ROOT, "scripts", "deck", "process_map_deck.html")
PNG = os.path.join(OUT_DIR, "process_map_deck.png")

# 덱 색상 토큰 (engine.py)
INK, INK2, MUTED = "#0F172A", "#334155", "#64748B"
ACC, RED, GRN = "#2563EB", "#E11D48", "#059669"
BORDER, LINE, ZONE_BG = "#E2E8F0", "#94A3B8", "#F8FAFC"
RED_BG, ACC_BG = "#FFF1F2", "#EFF6FF"

KO = "'Malgun Gothic','맑은 고딕',sans-serif"
MONO = "Consolas,'Courier New',monospace"

# 글자 크기(캔버스 단위). 캔버스 폭 ≈ 슬라이드 폭이라 1단위 ≈ 0.96pt
T_ZONE, T_ZSUB, T_NAME, T_SUB, T_EDGE, T_CALL, T_LEG = 14, 10, 11, 10, 10, 11, 10

# ---------------------------------------------------------------- 좌표
ZY, ZH = 4, 182                       # 구간 박스 y, 높이
MID = 110                              # 중앙 행 중심
NH, RH = 40, 32                       # 중앙 행 노드 높이, 수리 노드 높이

z1x, z1w = 1, 334
fc = (9, 84)
mt = (109, 84)
asv = (209, 118)
arrow_len = 72
sv = (asv[0] + asv[1] + arrow_len, 62)          # Survey
z2x = sv[0] - 8
rp_x, rp_w = sv[0] + sv[1] + 28, 108            # 수리 3노드
rr_x, rr_w = rp_x + rp_w + 51, 80               # RepairReady
z2w = rr_x + rr_w + 8 - z2x
z3x = z2x + z2w + 12
cl = (z3x + 8, 118)                             # 고객통보 ∥ 재무전달
tr = (cl[0] + cl[1] + 16, 76)                   # TicketReady
z3w = tr[0] + tr[1] + 8 - z3x
W = z3x + z3w + 2
H = 236

rep_y = {"imm": 44, "int": 94, "ext": 144}      # 수리 노드 상단 y


def rect(x, y, w, h, fill, stroke, sw=1.2, dash=None, rx=6):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def text(x, y, t, size, fill=INK, weight=400, family=KO, anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" font-family="{family}" text-anchor="{anchor}" {extra}>{t}</text>'


def node(x, y, w, h, name, sub, fill="#FFFFFF", stroke=LINE, sw=1.2, dash=None, name_family=MONO, name_fill=INK, sub_fill=MUTED):
    ny = y + (h / 2) - 2 if sub else y + h / 2 + 4
    sy = y + h / 2 + 12
    out = [rect(x, y, w, h, fill, stroke, sw, dash)]
    out.append(text(x + w / 2, ny, name, T_NAME, name_fill, 700, name_family))
    if sub:
        out.append(text(x + w / 2, sy, sub, T_SUB, sub_fill, 400, KO))
    return "\n".join(out)


def build():
    n_in = 1000
    el = []
    # 구간 박스
    for x, w, title, sub in [
        (z1x, z1w, "01 접수", f"{n_in:,}건 유입 · {s('n_wrongplace')}건 이탈 · {s('n_valid')}건 통과"),
        (z2x, z2w, "02 현장", f"{s('n_valid')}건"),
        (z3x, z3w, "03 정산", f"{s('n_valid')}건 · 전부 종결"),
    ]:
        el.append(rect(x, ZY, w, ZH, ZONE_BG, BORDER, 1, None, 8))
        el.append(text(x + 12, ZY + 20, title, T_ZONE, INK, 700, KO, "start"))
        el.append(text(x + 12, ZY + 34, sub, T_ZSUB, MUTED, 400, KO, "start"))

    # 연결선 (노드보다 먼저)
    def arrow(x1, y1, x2, y2, color=LINE, sw=1.3, dash=None, marker="a"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d} marker-end="url(#{marker})"/>'

    def path(d, color=LINE, sw=1.3, dash=None, marker="a"):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{dd} marker-end="url(#{marker})"/>'

    el.append(arrow(fc[0] + fc[1], MID, mt[0], MID))
    el.append(arrow(mt[0] + mt[1], MID, asv[0], MID))
    el.append(arrow(fc[0] + fc[1] / 2, MID + NH / 2, fc[0] + fc[1] / 2, 144, dash="5,4"))
    # 최대 병목 화살표
    ax1, ax2 = asv[0] + asv[1], sv[0]
    el.append(arrow(ax1, MID, ax2, MID, RED, 2.6, None, "r"))
    cxm = (ax1 + ax2) / 2
    el.append(text(cxm, MID - 9, f"평균 {s('wait1')}h", T_EDGE + 1, RED, 700))
    el.append(text(cxm, MID + 17, f"중앙 {s('wait1_median')}h", T_EDGE, MUTED, 400))

    # Survey 분기
    sx = sv[0] + sv[1]
    mid_ys = {"imm": rep_y["imm"] + RH / 2, "int": rep_y["int"] + RH / 2, "ext": rep_y["ext"] + RH / 2}
    el.append(path(f"M {sx} {MID-8} H {sx+8} Q {sx+14} {MID-8} {sx+14} {MID-14} V {mid_ys['imm']+6} Q {sx+14} {mid_ys['imm']} {sx+20} {mid_ys['imm']} H {rp_x}"))
    el.append(arrow(sx, MID, rp_x, MID))
    el.append(path(f"M {sx} {MID+8} H {sx+8} Q {sx+14} {MID+8} {sx+14} {MID+14} V {mid_ys['ext']-6} Q {sx+14} {mid_ys['ext']} {sx+20} {mid_ys['ext']} H {rp_x}"))
    # 수리 유형 간 인계 (즉시 → 사내 → 외주, 역행 0건)
    hx = rp_x + 30
    el.append(arrow(hx, rep_y["imm"] + RH, hx, rep_y["int"], LINE, 1.3, "5,4"))
    el.append(f'<rect x="{hx+5}" y="{rep_y["imm"]+RH+2}" width="30" height="14" rx="2" fill="#FFFFFF"/>')
    el.append(text(hx + 20, rep_y["imm"] + RH + 13, f"{s('esc_imm_intern')}건", T_EDGE, INK2, 400))
    el.append(arrow(hx, rep_y["int"] + RH, hx, rep_y["ext"], LINE, 1.3, "5,4"))
    el.append(f'<rect x="{hx+5}" y="{rep_y["int"]+RH+2}" width="30" height="14" rx="2" fill="#FFFFFF"/>')
    el.append(text(hx + 20, rep_y["int"] + RH + 13, f"{s('esc_intern_extern')}건", T_EDGE, INK2, 400))
    bx = rp_x + rp_w + 15
    el.append(path(f"M {rp_x+rp_w} {rep_y['imm']+RH-5} H {bx-6} Q {bx} {rep_y['imm']+RH-5} {bx} {rep_y['imm']+RH+1} V {rep_y['ext']+RH-7} Q {bx} {rep_y['ext']+RH-5} {bx-6} {rep_y['ext']+RH-5} H {rp_x+rp_w+2}", LINE, 1.3, "5,4"))
    el.append(f'<rect x="{bx-14}" y="{MID+34}" width="28" height="14" rx="2" fill="#FFFFFF"/>')
    el.append(text(bx, MID + 45, f"{s('esc_imm_extern')}건", T_EDGE, INK2, 400))
    # 수리 → RepairReady 합류
    mx = rr_x - 16
    el.append(path(f"M {rp_x+rp_w} {mid_ys['imm']} H {mx-6} Q {mx} {mid_ys['imm']} {mx} {mid_ys['imm']+6} V {MID-8-6} Q {mx} {MID-8} {mx+6} {MID-8} H {rr_x}"))
    el.append(f'<path d="M {rp_x+rp_w} {MID} H {bx-6} A 6 6 0 0 1 {bx+6} {MID} H {rr_x}" fill="none" stroke="{LINE}" stroke-width="1.3" marker-end="url(#a)"/>')
    el.append(path(f"M {rp_x+rp_w} {mid_ys['ext']} H {mx-6} Q {mx} {mid_ys['ext']} {mx} {mid_ys['ext']-6} V {MID+8+6} Q {mx} {MID+8} {mx+6} {MID+8} H {rr_x}"))
    # 정산
    el.append(arrow(rr_x + rr_w, MID, cl[0], MID))
    el.append(arrow(cl[0] + cl[1], MID, tr[0], MID))

    # 노드
    ny0 = MID - NH / 2
    el.append(node(fc[0], ny0, fc[1], NH, "FirstContact", f"{n_in:,}행", ACC_BG, ACC))
    el.append(node(mt[0], ny0, mt[1], NH, "MakeTicket", f"{s('n_valid')}행", RED_BG, RED, 1.6))
    el.append(node(asv[0], ny0, asv[1], NH, "실사 일정 조율·통보", f"{s('n_valid')}행 × 2", name_family=KO))
    el.append(node(fc[0], 144, 152, 32, "InformClientWrongPlace", f"{s('n_wrongplace')}행 · 조기 이탈 {s('wrongplace_pct')}%", "#FFFFFF", LINE, 1.2, "4,3"))
    el.append(node(sv[0], ny0, sv[1], NH, "Survey", f"{s('n_valid')}행"))
    el.append(node(rp_x, rep_y["imm"], rp_w, RH, "ImmediateRepair", f"{s('n_imm1')}행 · {s('n_imm1')}건"))
    el.append(node(rp_x, rep_y["int"], rp_w, RH, "InternRepair", f"{s('intern_ev')}행 · {s('intern_cases')}건"))
    el.append(node(rp_x, rep_y["ext"], rp_w, RH, "ExternRepair", f"{s('extern_ev')}행 · {s('extern_ev')}건", "#F1F5F9", "#64748B"))
    el.append(node(rr_x, ny0, rr_w, NH, "RepairReady", f"{s('n_valid')}행"))
    el.append(node(cl[0], ny0, cl[1], NH, "고객통보 ∥ 재무전달", f"{s('n_valid')}행 × 2 · 동시", name_family=KO))
    el.append(node(tr[0], ny0, tr[1], NH, "TicketReady", f"{s('n_valid')}행 · 종결", "#ECFDF5", GRN))

    # 설명선 (구간 아래)
    cy = ZY + ZH + 18
    lx = mt[0] + mt[1] - 12
    el.append(f'<path d="M {lx} {MID+NH/2} V {cy-14}" fill="none" stroke="{RED}" stroke-opacity="0.55" stroke-width="1" stroke-dasharray="4,3"/>')
    el.append(f'<circle cx="{lx}" cy="{MID+NH/2}" r="2.2" fill="{RED}"/>')
    el.append(text(z1x + z1w / 2, cy, f"교차 인계 {s('n_handover')}건 · 건당 +{s('ols1_handover_b')}h 지연", T_CALL, RED, 700))
    zc = rp_x + rp_w / 2
    el.append(f'<path d="M {zc} {rep_y["ext"]+RH} V {cy-14}" fill="none" stroke="{MUTED}" stroke-opacity="0.6" stroke-width="1" stroke-dasharray="4,3"/>')
    el.append(f'<circle cx="{zc}" cy="{rep_y["ext"]+RH}" r="2.2" fill="{MUTED}"/>')
    el.append(text((z2x + z3x + z3w) / 2 + 20, cy, f"수리 {int(F['rep_ev_total']['v']):,}행 = {s('n_valid')}건 + 유형 간 인계 {s('esc_total')}회 + 사내수리 반복 {s('intern_repeat')}회", T_CALL, INK2, 400))

    # 범례
    ly = ZY + ZH + 44
    el.append(f'<line x1="2" y1="{ly-14}" x2="{W-2}" y2="{ly-14}" stroke="{BORDER}" stroke-width="1"/>')
    x = 4
    el.append(rect(x, ly - 9, 20, 13, RED_BG, RED, 1.4, None, 3)); x += 26
    el.append(text(x, ly + 1, "교차 인계 병목", T_LEG, MUTED, 400, KO, "start")); x += 100
    el.append(arrow(x, ly - 2, x + 26, ly - 2, RED, 2.2, None, "r")); x += 32
    el.append(text(x, ly + 1, "최장 대기", T_LEG, MUTED, 400, KO, "start")); x += 78
    el.append(rect(x, ly - 9, 20, 13, "#FFFFFF", LINE, 1.2, "4,3", 3)); x += 26
    el.append(text(x, ly + 1, "조기 이탈", T_LEG, MUTED, 400, KO, "start")); x += 78
    el.append(rect(x, ly - 9, 20, 13, "#F1F5F9", "#64748B", 1.2, None, 3)); x += 26
    el.append(text(x, ly + 1, "외주", T_LEG, MUTED, 400, KO, "start")); x += 50
    el.append(arrow(x, ly - 2, x + 26, ly - 2, LINE, 1.3, "5,4")); x += 32
    el.append(text(x, ly + 1, "수리 유형 간 인계 (건)", T_LEG, MUTED, 400, KO, "start")); x += 160
    el.append(text(x, ly + 1, "행 = 이벤트 로그 1행 · 건 = 수리 요청 1건", T_LEG, MUTED, 400, KO, "start"))

    defs = (f'<defs><marker id="a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{LINE}"/></marker>'
            f'<marker id="r" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{RED}"/></marker></defs>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs}<rect width="100%" height="100%" fill="#FFFFFF"/>' + "\n".join(el) + "</svg>"
    html = f'<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>html,body{{margin:0;padding:0;background:#fff}}svg{{display:block}}</style></head><body>{svg}</body></html>'
    return html


def find_browser():
    for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe"]:
        if os.path.exists(p):
            return p
    raise SystemExit("Edge/Chrome 을 찾지 못했습니다")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    open(HTML, "w", encoding="utf-8").write(build())
    scale = 3
    cmd = [find_browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={scale}",
           f"--window-size={int(W)},{int(H)}", f"--screenshot={PNG}", "file:///" + HTML.replace("\\", "/")]
    subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    print("캔버스", W, H, "->", PNG)


if __name__ == "__main__":
    main()
