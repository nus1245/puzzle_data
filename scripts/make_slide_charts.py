# -*- coding: utf-8 -*-
"""슬라이드 실측 크기(in)에 맞춰 폰트를 설계한 차트를 원천 데이터에서 재생성한다.

기존 outputs/figures/*.png 는 노트북 기준(큰 캔버스)이라 슬라이드에 넣으면 글자가 5~6pt 로 줄어든다.
여기서는 figsize 를 슬라이드 배치 박스와 동일하게 두어 '폰트 pt = 슬라이드에서 보이는 pt' 가 되게 한다.
출력: outputs/figures/v2/*.png  (원본 자산은 수정하지 않는다)
수치는 모두 case_pivot_table.csv 에서 계산하며, 정정 내역은 docs/07_fact_verification.md 참고.
"""
import os
import sys

import matplotlib
import numpy as np
import pandas as pd
import statsmodels.api as sm

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "outputs", "figures", "v2")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "Malgun Gothic", "axes.unicode_minus": False,
    "axes.edgecolor": "#CBD5E1", "axes.linewidth": 0.8, "text.color": "#0F172A",
    "axes.labelcolor": "#475569", "xtick.color": "#64748B", "ytick.color": "#64748B",
})
INK, MUTED, GRID = "#0F172A", "#64748B", "#E2E8F0"
RED, ORG, EMR, BLU, SLATE = "#DC2626", "#EA580C", "#059669", "#2563EB", "#94A3B8"
DPI = 300

piv = pd.read_csv(os.path.join(BASE, "case_pivot_table.csv"))
for c in piv.columns:
    if c.endswith(("_time", "_start", "_complete")):
        piv[c] = pd.to_datetime(piv[c])
m = piv[piv.objectKey.notna()].copy()
hrs = lambda a, b: (m[b] - m[a]).dt.total_seconds() / 3600.0


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    print("saved", path)


def clean_axes(ax, left=False, bottom=False):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_visible(left)
    ax.spines["bottom"].set_visible(bottom)


# =========================================================== A. S08 거시 리드타임 분해 (7.5 x 2.62)
total = hrs("contact_time", "ticket_ready_time")
field = hrs("inform_survey_time", "repair_ready_time")
survey = hrs("survey_start", "survey_complete")
rep = sum(hrs(f"rep{i}_start", f"rep{i}_complete").fillna(0) for i in (1, 2, 3))
f_work = (survey + rep).mean()
f_wait = field.mean() - f_work
settle = hrs("repair_ready_time", "ticket_ready_time").mean()
recept = hrs("contact_time", "inform_survey_time").mean()
T = total.mean()
e2e_wait = T - f_work - settle       # 정산(시스템 처리)·현장 실작업을 뺀 모든 시간 = 대기·조율
print(f"S08  접수 {recept:.2f} 현장 {field.mean():.2f}(작업 {f_work:.2f}/대기 {f_wait:.2f}) 정산 {settle:.2f} E2E {T:.2f} 대기 {e2e_wait:.2f} ({e2e_wait / T * 100:.1f}%)")

fig, ax = plt.subplots(figsize=(7.5, 2.62))
rows = [  # (라벨, 총시간, [(값, 색, 이름)])
    ("01 접수", recept, [(recept, RED, "wait")]),
    ("02 현장", field.mean(), [(f_work, BLU, "work"), (f_wait, RED, "wait")]),
    ("03 정산", settle, [(settle, EMR, "sys")]),
    ("E2E 전체", T, [(f_work, BLU, "work"), (settle, EMR, "sys"), (e2e_wait, RED, "wait")]),
]
for i, (lab, tot, segs) in enumerate(rows):
    y = len(rows) - 1 - i
    left = 0.0
    for val, col, kind in segs:
        w = val / tot * 100
        ax.barh(y, w, left=left, height=0.56, color=col, edgecolor="white", linewidth=1.0)
        if w >= 9:
            ax.text(left + w / 2, y, f"{w:.1f}%", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        elif w >= 3:
            ax.text(left + w / 2, y + 0.43, f"{w:.1f}%", ha="center", va="bottom", color=col, fontsize=8, fontweight="bold")
        left += w
    ax.text(101.5, y, f"{tot:.1f}h", ha="left", va="center", fontsize=10, fontweight="bold", color=INK)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=9.5, fontweight="bold", color=INK)
ax.set_xlim(0, 118)
ax.set_ylim(-0.55, 3.75)
ax.set_xticks([])
clean_axes(ax)
ax.tick_params(axis="y", length=0)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (BLU, EMR, RED)]
ax.legend(handles, ["현장 실작업", "정산 시스템 처리", "대기·조율"], loc="upper left", ncol=3, frameon=False,
          fontsize=8.5, bbox_to_anchor=(-0.02, 1.08), handlelength=1.0, columnspacing=1.4)
fig.subplots_adjust(left=0.13, right=0.99, top=0.9, bottom=0.03)
save(fig, "s08_leadtime_breakdown.png")

# =========================================================== B. S10 현장 소요시간 도넛 (2.9 x 2.6)
w1 = hrs("inform_survey_time", "survey_start").mean()
other_wait = field.mean() - w1 - f_work
rep_work, sur_work = rep.mean(), survey.mean()
parts = [w1, other_wait, rep_work, sur_work]
print(f"S10 donut: {[round(p, 2) for p in parts]} sum {sum(parts):.2f}")
fig, ax = plt.subplots(figsize=(2.9, 2.6))
cols = [RED, ORG, BLU, "#38BDF8"]
wedges, _ = ax.pie(parts, colors=cols, startangle=90, counterclock=False,
                   wedgeprops=dict(width=0.34, edgecolor="white", linewidth=2))
for wdg, val in zip(wedges[:2], parts[:2]):
    ang = np.deg2rad((wdg.theta1 + wdg.theta2) / 2)
    ax.text(0.83 * np.cos(ang), 0.83 * np.sin(ang), f"{val / field.mean() * 100:.1f}%", ha="center", va="center",
            color="white", fontsize=9, fontweight="bold")
ax.text(0, 0.1, f"{field.mean():.1f}h", ha="center", va="center", fontsize=17, fontweight="bold", color=INK)
ax.text(0, -0.2, "현장 국면", ha="center", va="center", fontsize=9, color=MUTED)
ax.set_aspect("equal")
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
save(fig, "s10_field_donut.png")

# =========================================================== C. S10 유입 vs CAPA & WIP (6.9 x 2.85)
day = lambda s: s.dt.normalize()
handoff = day(m.inform_survey_time).value_counts().sort_index()
surv = day(m.survey_start).value_counts().sort_index()
days = pd.date_range("1970-01-01", "1970-01-14")
h = handoff.reindex(days, fill_value=0)
s_ = surv.reindex(days, fill_value=0)
wip = h.cumsum() - s_.cumsum()
inflow_avg = handoff["1970-01-02":"1970-01-07"].mean()
capa_avg = surv["1970-01-01":"1970-01-08"].mean()
print(f"S10 flow: inflow {inflow_avg:.1f}, capa {capa_avg:.1f}, wip peak {wip.max()} on {wip.idxmax().date()}")
fig, ax = plt.subplots(figsize=(6.9, 2.85))
x = np.arange(len(days))
ax.bar(x - 0.2, h.values, 0.4, color=BLU, label="현장 이관 유입 (건/일)")
ax.bar(x + 0.2, s_.values, 0.4, color=SLATE, label="실사 착수 (건/일)")
ax.axhline(inflow_avg, color=BLU, ls="--", lw=0.9, alpha=0.7)
ax.axhline(capa_avg, color="#475569", ls=":", lw=1.1)
ax.text(len(days) - 0.35, inflow_avg + 3, f"유입 평균 {inflow_avg:.1f}", ha="right", va="bottom", fontsize=8, color=BLU, fontweight="bold")
ax.text(len(days) - 0.35, capa_avg + 3, f"CAPA {capa_avg:.1f}", ha="right", va="bottom", fontsize=8, color="#475569", fontweight="bold")
ax.set_ylim(0, 175)
ax.set_xticks(x)
ax.set_xticklabels([f"{d.day}" for d in days], fontsize=8)
ax.set_xlabel("1월 (일)", fontsize=8, labelpad=1)
ax.tick_params(axis="y", labelsize=8)
ax.grid(axis="y", color=GRID, lw=0.6)
ax.set_axisbelow(True)
clean_axes(ax, left=False, bottom=True)
ax2 = ax.twinx()
ax2.plot(x, wip.values, color=RED, lw=2.2, marker="o", ms=4, label="미처리 적체 WIP (건, 우축)")
ax2.set_ylim(0, 470)
ax2.tick_params(axis="y", labelsize=8, colors=RED)
for sp in ("top", "left"):
    ax2.spines[sp].set_visible(False)
ax2.spines["right"].set_color("#FECACA")
pk = int(wip.values.argmax())
ax2.annotate(f"피크 {int(wip.max())}건", (pk, wip.max()), xytext=(pk - 3.2, wip.max() + 8), fontsize=9, fontweight="bold",
             color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(-0.01, 1.14),
          handlelength=1.2, columnspacing=1.2)
fig.subplots_adjust(left=0.065, right=0.935, top=0.88, bottom=0.17)
save(fig, "s10_wip_flow.png")

# =========================================================== D. S11 평균 기여도 분해 (5.7 x 2.3)
m["visit_lag_hours"] = hrs("inform_survey_time", "survey_start")
m["is_intern_repair"] = (m.rep1_task == "InternRepair").astype(int)
m["is_async_channel"] = m.contact_channel.isin(["Web", "Letter"]).astype(int)
m["is_escalation"] = m.rep2_task.notna().astype(int)
m["total_hours"] = total
cols_x = ["visit_lag_hours", "is_intern_repair", "is_escalation", "is_async_channel"]
fit = sm.OLS(m.total_hours, sm.add_constant(m[cols_x])).fit()
contrib = {c: fit.params[c] * m[c].mean() for c in cols_x}
print("S11 OLS R2 %.4f F %.1f" % (fit.rsquared, fit.fvalue), {k: round(v, 2) for k, v in contrib.items()},
      "sum+const", round(sum(contrib.values()) + fit.params["const"], 2))
order = [("visit_lag_hours", "실사 방문 대기", f"+{fit.params['visit_lag_hours']:.2f}h/h × {m.visit_lag_hours.mean():.1f}h", RED),
         ("is_intern_repair", "사내 수리 배정", f"+{fit.params['is_intern_repair']:.2f}h × {m.is_intern_repair.mean() * 100:.0f}%", ORG),
         ("is_async_channel", "비실시간 접수 채널", f"+{fit.params['is_async_channel']:.2f}h × {m.is_async_channel.mean() * 100:.0f}%", SLATE),
         ("is_escalation", "2차 에스컬레이션 (비유의)", f"+{fit.params['is_escalation']:.2f}h × {m.is_escalation.mean() * 100:.1f}%", "#CBD5E1")]
fig, ax = plt.subplots(figsize=(5.7, 2.3))
for i, (k, lab, formula, col) in enumerate(order):
    y = len(order) - 1 - i
    ax.barh(y, contrib[k], height=0.58, color=col)
    ax.text(contrib[k] + 1.5, y + 0.12, f"{contrib[k]:.1f}h", va="center", ha="left", fontsize=10, fontweight="bold", color=INK)
    ax.text(contrib[k] + 1.5, y - 0.2, formula, va="center", ha="left", fontsize=7.5, color=MUTED)
ax.set_yticks(range(len(order)))
ax.set_yticklabels([o[1] for o in order][::-1], fontsize=9, fontweight="bold", color=INK)
ax.set_xlim(0, 125)
ax.set_xticks([])
clean_axes(ax)
ax.tick_params(axis="y", length=0)
fig.subplots_adjust(left=0.33, right=0.99, top=0.97, bottom=0.03)
save(fig, "s11_ols_contribution.png")

# =========================================================== E. S11 수리 방식별 착수 대기 & 리워크 (5.7 x 2.3)
w2 = hrs("survey_complete", "rep1_start")
rw = m[(m.rep1_task == "InternRepair") & (m.rep2_task == "InternRepair")]
gap = (rw.rep2_start - rw.rep1_complete).dt.total_seconds() / 3600
n_fast = int((m.rep1_task != "InternRepair").sum())
n_int = int((m.rep1_task == "InternRepair").sum())
vals = [w2[m.rep1_task != "InternRepair"].mean(), w2[m.rep1_task == "InternRepair"].mean(), gap.mean()]
print(f"S11 rework: wait {vals[0]:.1f}/{vals[1]:.1f}, rework mean {vals[2]:.1f}, max {gap.max():.1f}h = {gap.max() / 24:.1f}d, n {n_fast}/{n_int}/{len(rw)}")
fig, ax = plt.subplots(figsize=(5.7, 2.3))
xs = [0, 1, 2]
bars = ax.bar(xs, vals, width=0.5, color=[EMR, ORG, RED])
ax.set_ylim(0, 48)
labs = [f"즉시·외주수리\n{n_fast}건 ({n_fast / len(m) * 100:.1f}%)", f"사내수리 1차 착수\n{n_int}건 ({n_int / len(m) * 100:.1f}%)",
        f"사내 하자 재방문\n{len(rw)}건 ({len(rw) / len(m) * 100:.1f}%)"]
ax.set_xticks(xs)
ax.set_xticklabels(labs, fontsize=8.5, color=INK)
ax.tick_params(axis="x", length=0)
for xv, v, extra in zip(xs, vals, ["대기 없음", "자재 조달·일정 조율", f"최대 {gap.max():.1f}h ({gap.max() / 24:.1f}일)"]):
    ax.text(xv, v + 1.2, ("+" if xv == 2 else "") + f"{v:.1f}h", ha="center", va="bottom", fontsize=12, fontweight="bold", color=INK)
    ax.text(xv, v + 6.6, extra, ha="center", va="bottom", fontsize=8, color=MUTED)
ax.set_yticks([])
clean_axes(ax, bottom=True)
fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.2)
save(fig, "s11_rework_wait.png")

# =========================================================== F. S12 사전 분류 → 1차 수리 결과 (3.5 x 1.85)
ct = pd.crosstab(m.planned_repair_type, m.rep1_task)
seq = [("InternRepair", "사내수리", BLU), ("ImmediateRepair", "즉시수리", EMR), ("ExternRepair", "외주수리", ORG)]
print("S12 crosstab\n", ct)
fig, ax = plt.subplots(figsize=(3.5, 1.85))
for i, t in enumerate(["E", "P", "B"]):
    y = 2 - i
    tot = ct.loc[t].sum()
    left = 0
    for key, _lab, col in seq:
        n = int(ct.loc[t, key]) if key in ct.columns else 0
        if n == 0:
            continue
        w = n / tot * 100
        ax.barh(y, w, left=left, height=0.58, color=col, edgecolor="white", linewidth=1)
        if w >= 7:
            ax.text(left + w / 2, y, f"{n}", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
        left += w
ax.set_yticks([0, 1, 2])
ax.set_yticklabels([f"B형 {ct.loc['B'].sum()}건", f"P형 {ct.loc['P'].sum()}건", f"E형 {ct.loc['E'].sum()}건"],
                   fontsize=9, fontweight="bold", color=INK)
ax.set_xlim(0, 100)
ax.set_xticks([])
clean_axes(ax)
ax.tick_params(axis="y", length=0)
hnd = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in seq]
ax.legend(hnd, [s[1] for s in seq], loc="upper center", ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(0.45, 1.2),
          handlelength=1.0, columnspacing=1.0)
fig.subplots_adjust(left=0.2, right=0.99, top=0.86, bottom=0.02)
save(fig, "s12_planned_vs_actual.png")

# =========================================================== G. S09 접수 3패널 (12.0 x 2.35)
rl = pd.read_csv(os.path.join(BASE, "repair_cleaned.csv"))
rec_tasks = ["FirstContact", "MakeTicket", "ArrangeSurvey", "InformClientSurvey"]
agents = ["Anne", "Dian", "Monica", "Paul"]
rr = rl[rl.taskID.isin(rec_tasks) & rl.originator.isin(agents)]
ho = set(rr.groupby("caseID").originator.nunique()[lambda x: x > 1].index) & set(m.caseID)
m["handover"] = m.caseID.isin(ho)
m["rec_min"] = hrs("contact_time", "inform_survey_time") * 60
solo, hand = m[~m.handover].rec_min.mean() / 60, m[m.handover].rec_min.mean() / 60
print(f"S09 solo {solo:.2f}h n={int((~m.handover).sum())}, hand {hand:.2f}h n={int(m.handover.sum())}, x{hand / solo:.1f}")
chan = [("Personal", "대면"), ("Phone", "전화"), ("Web", "웹"), ("Letter", "우편")]
fast = {k: (m[m.contact_channel == k].rec_min <= 15).mean() * 100 for k, _ in chan}
slow = {k: (m[m.contact_channel == k].rec_min > 60).mean() * 100 for k, _ in chan}
fmean = {k: m[(m.contact_channel == k) & (m.rec_min <= 15)].rec_min.mean() for k, _ in chan}
print("S09 fast%", {k: round(v, 1) for k, v in fast.items()}, "slow%", {k: round(v, 1) for k, v in slow.items()},
      "fast mean", {k: round(v, 1) for k, v in fmean.items()})
fig, axs = plt.subplots(1, 3, figsize=(12.0, 2.35), gridspec_kw=dict(width_ratios=[1, 1.35, 1]))
a = axs[0]
a.bar([0, 1], [solo, hand], width=0.5, color=[BLU, RED])
a.set_xticks([0, 1])
a.set_xticklabels([f"단독 처리 ({int((~m.handover).sum())}건)", f"교차 인계 ({int(m.handover.sum())}건)"], fontsize=9.5, fontweight="bold", color=INK)
a.text(0, solo + 0.25, f"{solo:.1f}h", ha="center", fontsize=12, fontweight="bold", color=BLU)
a.text(1, hand + 0.25, f"{hand:.1f}h ({hand / solo:.1f}배)", ha="center", fontsize=12, fontweight="bold", color=RED)
a.set_ylim(0, 10.2)
a.set_yticks([])
clean_axes(a, bottom=True)
a.set_title("인계 여부별 평균 접수 소요시간", fontsize=10, fontweight="bold", loc="left", color=INK)
b = axs[1]
for i, (k, lab) in enumerate(chan):
    y = 3 - i
    mid = 100 - fast[k] - slow[k]
    b.barh(y, fast[k], height=0.58, color=EMR)
    b.barh(y, mid, left=fast[k], height=0.58, color="#CBD5E1")
    b.barh(y, slow[k], left=fast[k] + mid, height=0.58, color=RED)
    if fast[k] > 12:
        b.text(fast[k] / 2, y, f"{fast[k]:.1f}%", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
    if slow[k] > 12:
        b.text(fast[k] + mid + slow[k] / 2, y, f"{slow[k]:.1f}%", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
b.set_yticks([3, 2, 1, 0])
b.set_yticklabels([c[1] for c in chan], fontsize=9.5, fontweight="bold", color=INK)
b.set_xlim(0, 100)
b.set_xticks([])
clean_axes(b)
b.tick_params(axis="y", length=0)
b.set_title("채널별 완료 속도 분포", fontsize=10, fontweight="bold", loc="left", color=INK)
hn = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (EMR, "#CBD5E1", RED)]
b.legend(hn, ["15분 이내", "15~60분", "60분 초과"], loc="lower center", ncol=3, frameon=False, fontsize=8,
         bbox_to_anchor=(0.5, -0.2), handlelength=1.0, columnspacing=1.2)
c_ = axs[2]
vals3 = [fmean[k] for k, _ in chan]
cc = [SLATE, SLATE, EMR, SLATE]
c_.bar(range(4), vals3, width=0.5, color=cc)
for i, v in enumerate(vals3):
    c_.text(i, v + 0.25, f"{v:.1f}분", ha="center", fontsize=10.5, fontweight="bold", color=EMR if cc[i] == EMR else INK)
c_.set_xticks(range(4))
c_.set_xticklabels([c[1] for c in chan], fontsize=9.5, fontweight="bold", color=INK)
c_.set_ylim(0, 11.5)
c_.set_yticks([])
clean_axes(c_, bottom=True)
c_.set_title("15분 이내 완료 건의 평균 소요시간", fontsize=10, fontweight="bold", loc="left", color=INK)
fig.subplots_adjust(left=0.02, right=0.99, top=0.88, bottom=0.2, wspace=0.12)
save(fig, "s09_reception_3panel.png")

# =========================================================== H. S04 결측률 양극단 프로파일 (8.28 x 3.2) — 원천 repair2.csv
raw = pd.read_csv(os.path.join(BASE, "repair2.csv"))
nrow = len(raw)
nulls = raw.isna().sum().sort_values(ascending=False)
print("S04 rows", nrow, {k: int(v) for k, v in nulls.items()})
rate = nulls / nrow * 100
normal = rate[rate >= 50]
abn = rate[rate < 50].sort_values(ascending=False)
print(f"S04 normal {len(normal)} attrs {normal.min():.1f}~{normal.max():.1f}% | abnormal(<50%, incl. caseID 0) {len(abn)} attrs")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.28, 3.2), gridspec_kw=dict(width_ratios=[1.55, 1]))
order = list(rate.sort_values(ascending=False).index)
for i, k in enumerate(order):
    y = len(order) - 1 - i
    col = SLATE if rate[k] >= 50 else RED
    a1.barh(y, rate[k], height=0.62, color=col)
    lab = f"{rate[k]:.1f}%  ({int(nulls[k]):,}행)" if rate[k] >= 50 else (f"{rate[k]:.3f}%  ({int(nulls[k])}행)" if nulls[k] else "0.000%  (0행)")
    a1.text(rate[k] + 1.5, y, lab, va="center", ha="left",
            fontsize=7.5, color=INK if rate[k] >= 50 else RED, fontweight="bold")
a1.set_yticks(range(len(order)))
a1.set_yticklabels(order[::-1], fontsize=7.5, color=INK)
a1.set_xlim(0, 150)
a1.set_xticks([0, 50, 100])
a1.tick_params(axis="x", labelsize=7.5)
a1.set_title("전체 13개 속성 결측률 (%)", fontsize=9.5, fontweight="bold", loc="left", color=INK)
a1.text(56, 2.2, "← 0.1%~86.0% 구간 컬럼 0개 (진공 구간)", fontsize=8, color=MUTED, va="center")
clean_axes(a1, left=True, bottom=True)
a1.tick_params(axis="y", length=0)
abn_keys = list(abn.index)
for i, k in enumerate(abn_keys):
    y = len(abn_keys) - 1 - i
    a2.barh(y, rate[k], height=0.62, color=RED if nulls[k] > 0 else GRID)
    a2.text(rate[k] + 0.003, y, f"{rate[k]:.3f}% ({int(nulls[k])}행)", va="center", ha="left", fontsize=7.5, color=RED if nulls[k] > 0 else MUTED,
            fontweight="bold")
a2.set_yticks(range(len(abn_keys)))
a2.set_yticklabels(abn_keys[::-1], fontsize=8, color=INK)
a2.set_xlim(0, 0.2)
a2.set_xticks([0, 0.05, 0.1])
a2.tick_params(axis="x", labelsize=7.5)
a2.set_title("비정상 결측 5개 속성 (확대, %)", fontsize=9.5, fontweight="bold", loc="left", color=RED)
clean_axes(a2, left=True, bottom=True)
a2.tick_params(axis="y", length=0)
fig.subplots_adjust(left=0.2, right=0.99, top=0.9, bottom=0.1, wspace=0.62)
save(fig, "s04_missing_profile.png")

# I. S07 프로세스 맵(구간별 대기시간 히트)은 별도 모듈에서 그린다
import chart_process_map  # noqa: E402,F401
