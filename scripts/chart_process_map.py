# -*- coding: utf-8 -*-
"""S07 프로세스 맵: 케이스 수(화살표 굵기)와 구간별 평균 대기시간(색)을 한 장에 담은 슬라이드용 맵.

make_slide_charts.py 의 끝에서 import 되어 실행된다. 수치는 모두 case_pivot_table.csv / repair_cleaned.csv 에서 계산한다.
출력: outputs/figures/v2/s07_process_map_wait.png  (12.13 x 3.5 in, 폰트 pt = 슬라이드에서 보이는 pt)
"""
import os
import sys

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "outputs", "figures", "v2")
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})
INK, MUTED = "#0F172A", "#64748B"
RED, ORG, EMR, GRAY = "#DC2626", "#EA580C", "#059669", "#94A3B8"

piv = pd.read_csv(os.path.join(BASE, "case_pivot_table.csv"))
for c in piv.columns:
    if c.endswith(("_time", "_start", "_complete")):
        piv[c] = pd.to_datetime(piv[c])
m = piv[piv.objectKey.notna()].copy()
ev = pd.read_csv(os.path.join(BASE, "repair_cleaned.csv"))
ev = ev[ev.caseID.isin(m.caseID)]
hrs = lambda a, b: (m[b] - m[a]).dt.total_seconds() / 3600.0

# ---- 수치 (모두 원천 계산)
rec_tasks = ["FirstContact", "MakeTicket", "ArrangeSurvey", "InformClientSurvey"]
agents = ["Anne", "Dian", "Monica", "Paul"]
rr = ev[ev.taskID.isin(rec_tasks) & ev.originator.isin(agents)]
ho = set(rr.groupby("caseID").originator.nunique()[lambda x: x > 1].index)
m["handover"] = m.caseID.isin(ho)
m["rec_h"] = hrs("contact_time", "inform_survey_time")
solo_h, hand_h = m[~m.handover].rec_h.mean(), m[m.handover].rec_h.mean()
n_ho = int(m.handover.sum())
w1 = hrs("inform_survey_time", "survey_start")
arr = hrs("survey_arrange_start", "survey_arrange_complete")
mk = hrs("ticket_start", "ticket_complete")
sur = hrs("survey_start", "survey_complete")
w2_by = hrs("survey_complete", "rep1_start").groupby(m.rep1_task).mean()
first = m.rep1_task.value_counts()
cases_any = ev.groupby("taskID").caseID.nunique()
rw = m[(m.rep1_task == "InternRepair") & (m.rep2_task == "InternRepair")]
n_rw = len(rw)
rw_gap = ((rw.rep2_start - rw.rep1_complete).dt.total_seconds() / 3600).mean()
settle = hrs("repair_ready_time", "ticket_ready_time").mean()
recept = hrs("contact_time", "inform_survey_time").mean()
field = hrs("inform_survey_time", "repair_ready_time").mean()
print(f"S07 map: wait1 {w1.mean():.1f}/{w1.median():.1f} arrange {arr.mean():.2f}/{arr.median():.2f} wait2 {w2_by.round(1).to_dict()} "
      f"handover {n_ho} {solo_h:.2f}->{hand_h:.2f} rework {n_rw} +{rw_gap:.1f}h settle {settle:.2f}")


def wait_color(hh):
    return RED if hh >= 24 else (ORG if hh >= 1 else GRAY)


fig = plt.figure(figsize=(12.13, 3.5))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12.13)
ax.set_ylim(0, 3.5)
ax.axis("off")


def zone(x0, x1, title, sub, tot):
    ax.add_patch(FancyBboxPatch((x0, 0.36), x1 - x0, 3.08, boxstyle="round,pad=0,rounding_size=0.12", fc="#F8FAFC", ec="#E2E8F0", lw=1))
    ax.text(x0 + 0.14, 3.27, title, fontsize=10.5, fontweight="bold", color=INK, va="center")
    ax.text(x0 + 0.14, 3.04, sub, fontsize=8, color=MUTED, va="center")
    ax.text(x1 - 0.14, 3.27, tot, fontsize=10.5, fontweight="bold", color=INK, va="center", ha="right", family="Consolas")


def node(cx, cy, w, h, t1, t2, fc="white", ec="#475569", lw=1.1, ls="-"):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.07", fc=fc, ec=ec, lw=lw, ls=ls, zorder=3))
    ax.text(cx, cy + 0.09, t1, fontsize=9, fontweight="bold", color=INK, ha="center", va="center", zorder=4)
    ax.text(cx, cy - 0.12, t2, fontsize=7.8, color=MUTED, ha="center", va="center", zorder=4)


def edge(p0, p1, w=1.2, col=GRAY, ls="-", head=None, rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=head or (8 + w * 1.2), lw=w, color=col, ls=ls, zorder=2,
                                 shrinkA=0, shrinkB=0, connectionstyle=f"arc3,rad={rad}"))


def lab(x, y, t, col=INK, fs=8.8, bold=True):
    ax.text(x, y, t, fontsize=fs, color=col, ha="center", va="center", fontweight="bold" if bold else "normal", zorder=6,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.92))


zone(0.04, 4.3, "01 접수", "1,000 케이스 → 927 통과 · 73 조기 종결", f"{recept:.1f}h")
zone(4.44, 9.1, "02 현장", "927 케이스 · 즉시 → 사내 → 외주 단방향", f"{field:.1f}h")
zone(9.24, 12.09, "03 정산", "927 케이스 전원 종결 · 병렬 AND", f"{settle:.1f}h")

YM = 1.68
# ---- 01 접수
node(0.72, YM, 1.1, 0.6, "FirstContact", f"{int(cases_any['FirstContact']):,}건", fc="#EEF2F7")
node(2.1, YM, 1.1, 0.6, "MakeTicket", f"{int(cases_any['MakeTicket'])}건 · 소요 {mk.mean() * 60:.0f}분", fc="#FEF2F2", ec=RED)
node(3.52, YM, 1.3, 0.6, "일정 조율·통보", f"{int(cases_any['ArrangeSurvey'])}건 · 평균 {arr.mean():.1f}h")
node(0.72, 0.82, 1.1, 0.5, "조기 종결", "73건 (7.3%) · 타 기관", fc="#F8FAFC", ec=GRAY, ls="--")
edge((0.72, YM - 0.3), (0.72, 1.07), 1.0, GRAY, ls="--")
edge((1.27, YM), (1.55, YM), 1.4)
edge((2.65, YM), (2.87, YM), 1.4)
edge((1.82, YM + 0.3), (2.38, YM + 0.3), 1.8, ORG, head=10, rad=-1.5)
lab(2.1, 2.62, f"교차 인계 {n_ho}건 · {solo_h:.1f}h → {hand_h:.1f}h ({hand_h / solo_h:.1f}배)", ORG, 8.4)
web, let = arr[m.contact_channel == "Web"].mean(), arr[m.contact_channel == "Letter"].mean()
rt = arr[m.contact_channel.isin(["Phone", "Personal"])].mean()
lab(3.52, 1.0, f"웹 {web:.1f}h · 우편 {let:.1f}h · 전화·대면 {rt:.2f}h\n(전체 중앙값 {arr.median() * 60:.0f}분 — 일부 케이스에 집중)", MUTED, 7.8, bold=False)
# ---- 최대 병목: 접수 → 실사 (존 경계 위)
edge((4.17, YM), (4.84, YM), 7.5, RED, head=16)
lab(4.37, 2.3, f"실사 방문 대기\n평균 {w1.mean():.1f}h · 중앙값 {w1.median():.1f}h", RED, 9.2)
# ---- 02 현장
SX = 5.3
node(SX, YM, 0.92, 0.6, "Survey", f"{int(cases_any['Survey'])}건 · {sur.mean() * 60:.0f}분")
BX, BW = 7.3, 1.56
for name, y in [("ExternRepair", 2.4), ("InternRepair", YM), ("ImmediateRepair", 0.76)]:
    ncase, nfirst = int(cases_any[name]), int(first.get(name, 0))
    wv = float(w2_by[name])
    col = wait_color(wv)
    node(BX, y, BW, 0.56, name, f"{ncase}건 (1차 {nfirst})", fc="#F1F5F9" if name == "ExternRepair" else "white")
    edge((SX + 0.46, YM), (BX - BW / 2, y), 1.0 + 3.5 * nfirst / 485, col, head=9)
    lab((SX + 0.46 + BX - BW / 2) / 2 + (0.05 if y == YM else 0), (YM + y) / 2 + (0.2 if y == YM else 0), f"{wv:.1f}h", col, 9.2)
    edge((BX + BW / 2, y), (8.2, YM + (y - YM) * 0.28), 1.1, GRAY, head=7)
edge((BX - 0.55, YM - 0.28), (BX - 0.1, YM - 0.28), 1.8, RED, head=10, rad=0.9)
lab(BX + 0.62, YM - 0.5, f"리워크 {n_rw}건 · +{rw_gap:.1f}h", RED, 8.4)
node(8.65, YM, 0.84, 0.6, "RepairReady", f"{int(cases_any['RepairReady'])}건", fc="#ECFDF5", ec=EMR)
# ---- 03 정산
edge((9.08, YM), (9.5, YM), 1.4)
node(10.2, YM, 1.4, 0.6, "고객통보 ∥ 재무전달", f"{int(cases_any['ReadyInformClient'])}건 × 2 · AND")
edge((10.9, YM), (11.12, YM), 1.4)
node(11.58, YM, 0.92, 0.6, "TicketReady", f"{int(cases_any['TicketReady'])}건", fc="#EEF2F7")
lab(10.67, 2.55, f"정산 평균 {settle:.1f}h · 시스템 자동 처리", EMR, 8.4)
# ---- 범례
ax.text(0.1, 0.16, "화살표 굵기 = 1차 수리 케이스 수 · 색 = 평균 대기시간", fontsize=8, color=MUTED, va="center")
for k, (txt, col) in enumerate([("≥ 24h", RED), ("1~24h", ORG), ("< 1h", GRAY)]):
    ax.plot([4.55 + k * 0.95, 4.85 + k * 0.95], [0.16, 0.16], color=col, lw=3.2)
    ax.text(4.92 + k * 0.95, 0.16, txt, fontsize=8, color=MUTED, va="center")
ax.text(12.05, 0.16, "927건 코호트 · 평균 기준", fontsize=8, color=MUTED, va="center", ha="right")
path = os.path.join(OUT, "s07_process_map_wait.png")
fig.savefig(path, dpi=300, facecolor="white")
plt.close(fig)
print("saved", path)
