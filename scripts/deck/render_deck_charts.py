"""Modern Tech Light 테마 통합 시각화 스크립트.

카드 컨테이너 명시적 배경색(#FFFFFF) 및 고대비(Contrast) 스타일 적용:
  1. 배경색 및 투명도:
     - transparent=False 설정
     - fig.patch.set_facecolor('#FFFFFF') 및 ax.set_facecolor('#FFFFFF') 명시 채움
  2. 텍스트 및 축 색상 대비 (밝은 배경 가이드라인):
     - Y축 라벨(변수명): 진한 네이비/차콜 (#1E293B)
     - X축 눈금 및 라벨: 중간 그레이 (#64748B)
     - 밝은 막대 내부 수치 텍스트: 어두운 색상 (#0F172A)
  3. 저장 파라미터:
     - plt.savefig('경로.png', facecolor=fig.get_facecolor(), edgecolor='none', transparent=False, dpi=300, bbox_inches='tight')

주요 차트 5종:
  - p.04: 원천 13개 속성 결측률 분포 (EDA-01.png)
  - p.08: 3대 국면 실작업 vs 단순대기 리드타임 분해 (slide08_macro_leadtime_breakdown.png)
  - p.10: 접수 국면 9대 핵심 변수 상관관계 히트맵 (reception_detailed_correlation_heatmap.png)
  - p.12: 현장 공정 4대 소요시간 구조 분해 도넛 (slide10_field_donut_breakdown.png)
  - p.13: 일별 접수 유입 vs 실사 CAPA 불균형 & 403건 WIP 적체 (slide10_field_bottleneck_wip.png)
  + p.09: 접수 국면 3-Panel 통합 병목 진단 (slide09_reception_bottleneck_3panel.png)
"""
import json
import os
import sys

os.environ["MPLBACKEND"] = "Agg"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea

# -----------------------------------------------------------------------------
# 0. 글로벌 설정
# -----------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)

FIG_DIR = os.path.join(ROOT, "outputs", "figures")
DECK_DIR = os.path.join(ROOT, "outputs", "figures", "deck")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(DECK_DIR, exist_ok=True)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Pretendard", "Malgun Gothic", "AppleGothic", "NanumGothic", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# facts.json 원천 기준 로드
FACTS_PATH = os.path.join(ROOT, "scripts", "deck", "facts.json")
F = json.load(open(FACTS_PATH, encoding="utf-8"))["facts"]
fs = lambda k: float(F[k]["s"])

BG_COLOR = "#FFFFFF"   # PPT 카드 컨테이너 배경색(Pure White)과 100% 일치


def save_fig(fig, rel_path, also_deck=False):
    """카드 컨테이너 명시적 배경색 채움 및 transparent=False 300 DPI 저장"""
    out1 = os.path.join(FIG_DIR, rel_path)
    os.makedirs(os.path.dirname(out1), exist_ok=True)
    fig.savefig(
        out1,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        transparent=False,
        dpi=300,
        bbox_inches="tight",
    )
    print(f"✅ [저장 완료] {out1} (solid #FFFFFF, transparent=False, 300 DPI)")
    if also_deck:
        out2 = os.path.join(DECK_DIR, os.path.basename(rel_path))
        fig.savefig(
            out2,
            facecolor=fig.get_facecolor(),
            edgecolor="none",
            transparent=False,
            dpi=300,
            bbox_inches="tight",
        )
        print(f"✅ [저장 완료] {out2} (solid #FFFFFF, transparent=False, 300 DPI)")
    plt.close(fig)


# -----------------------------------------------------------------------------
# 1. p.04: 결측률 바 차트 (EDA-01.png)
#    - 카드 컨테이너 배경색 #FFFFFF 명시적 채움
#    - 비정상 결측 막대 색상: #E11D48
#    - 정상 결측 막대 색상: #CBD5E1 (슬레이트 연회색), 결측 0건: #64748B
#    - 수치 라벨 중앙 정렬: 정상 결측 막대 내부 수치 #0F172A (어두운 색상 대비 확보)
#    - Y축 라벨: 진한 네이비/차콜 (#1E293B), X축 눈금/라벨: 중간 그레이 (#64748B)
# -----------------------------------------------------------------------------
def render_p04_eda_missing():
    df = pd.read_csv("repair2.csv")
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df)) * 100.0
    summary_df = pd.DataFrame({
        "col": df.columns,
        "count": null_counts.values,
        "pct": null_pct.values
    }).sort_values(by="pct", ascending=True).reset_index(drop=True)

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(16, 7.2), dpi=300, gridspec_kw={"width_ratios": [1.15, 1.0]})
    fig.patch.set_facecolor(BG_COLOR)
    ax_left.set_facecolor(BG_COLOR)
    ax_right.set_facecolor(BG_COLOR)

    # [Left Plot] 전체 13개 속성 거시 프로파일 (0% ~ 100%)
    # 정상 결측: #CBD5E1, 비정상 결측: #E11D48, 결측 없음: #64748B
    colors_left = ["#CBD5E1" if p >= 80 else ("#E11D48" if p > 0 else "#64748B") for p in summary_df["pct"]]
    y_pos = np.arange(len(summary_df))
    bars_left = ax_left.barh(y_pos, summary_df["pct"], color=colors_left, height=0.62, edgecolor="none", zorder=3)

    ax_left.set_yticks(y_pos)
    ax_left.set_yticklabels(summary_df["col"], fontsize=10.5, fontweight="bold", color="#1E293B")
    ax_left.set_xlim(0, 115)
    ax_left.set_xlabel("결측률 (%)", fontsize=10, fontweight="bold", color="#64748B", labelpad=8)
    ax_left.grid(axis="x", linestyle=":", alpha=0.6, color="#CBD5E1", zorder=1)
    ax_left.spines["top"].set_visible(False)
    ax_left.spines["right"].set_visible(False)
    ax_left.spines["left"].set_color("#CBD5E1")
    ax_left.spines["bottom"].set_color("#CBD5E1")
    ax_left.tick_params(colors="#64748B", labelsize=10)

    # 막대 내부 수치 텍스트: 어두운 색상 #0F172A 중앙 정렬 (대비 극대화)
    for bar, count, pct in zip(bars_left, summary_df["count"], summary_df["pct"]):
        w = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2.0
        if pct >= 80:
            ax_left.text(w / 2.0, y, f"{pct:.1f}% ({count:,}행)", va="center", ha="center", fontsize=10, fontweight="bold", color="#0F172A", zorder=4)
        elif pct > 0:
            ax_left.text(w + 1.5, y, f"{pct:.3f}% ({count}행)", va="center", ha="left", fontsize=9.5, fontweight="bold", color="#E11D48", zorder=4)
        else:
            ax_left.text(w + 1.5, y, "0.0% (0행)", va="center", ha="left", fontsize=9.5, fontweight="bold", color="#0F172A", zorder=4)

    # [Right Plot] 비정상 결측 5대 속성 미시 정밀 감식 (0% ~ 0.12%)
    abnormal_df = summary_df[summary_df["pct"] < 1.0].copy().reset_index(drop=True)
    y_zoom = np.arange(len(abnormal_df))
    zoom_colors = ["#64748B" if p == 0 else "#E11D48" for p in abnormal_df["pct"]]

    bars_right = ax_right.barh(y_zoom, abnormal_df["pct"], color=zoom_colors, height=0.55, edgecolor="none", zorder=3)
    ax_right.set_yticks(y_zoom)
    ax_right.set_yticklabels(abnormal_df["col"], fontsize=11, fontweight="bold", color="#1E293B")
    ax_right.set_xlim(0, 0.14)
    ax_right.set_xlabel("결측률 정밀 스케일 (%)", fontsize=10, fontweight="bold", color="#64748B", labelpad=8)
    ax_right.grid(axis="x", linestyle=":", alpha=0.6, color="#CBD5E1", zorder=1)
    ax_right.spines["top"].set_visible(False)
    ax_right.spines["right"].set_visible(False)
    ax_right.spines["left"].set_color("#CBD5E1")
    ax_right.spines["bottom"].set_color("#CBD5E1")
    ax_right.tick_params(colors="#64748B", labelsize=10)

    for bar, count, pct in zip(bars_right, abnormal_df["count"], abnormal_df["pct"]):
        w = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2.0
        if pct > 0:
            ax_right.text(w + 0.003, y, f"{pct:.3f}% ({count}행)", va="center", ha="left", fontsize=10.5, fontweight="bold", color="#E11D48", zorder=4)
        else:
            ax_right.text(w + 0.003, y, "0.000% (0행)", va="center", ha="left", fontsize=10.5, fontweight="bold", color="#0F172A", zorder=4)

    plt.tight_layout()
    save_fig(fig, "EDA-01.png")


# -----------------------------------------------------------------------------
# 2. p.08: 실작업 vs 대기 바 (slide08_macro_leadtime_breakdown.png)
#    - 카드 컨테이너 배경색 #FFFFFF 명시적 채움
#    - 실작업: #0284C7 (Sky Blue), 단순 대기: #F43F5E (Soft Rose)
#    - Y축 라벨: #1E293B, X축 라벨: #64748B, 총시간 수치: #0F172A
# -----------------------------------------------------------------------------
def render_p08_leadtime_breakdown():
    phases = ["E2E 전체 총괄", "03 정산 국면", "02 현장 국면", "01 접수 국면"]
    work_pct = [fs("work_B_pct"), 100.0, fs("field_work_pct"), 0.0]
    wait_pct = [fs("wait_B_pct"), 0.0, fs("field_wait_pct"), 100.0]
    wait_hours = [fs("wait_B"), 0.0, fs("field_wait"), fs("rec_total")]
    hours_total = [fs("lead_total"), fs("stl_total"), fs("field_total"), fs("rec_total")]

    y = np.arange(len(phases))
    height = 0.44

    fig, ax = plt.subplots(figsize=(14, 4.6), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    bars_work = ax.barh(y, work_pct, height, label="순수 실작업 시간 (Value-added Work)", color="#0284C7", alpha=0.92, edgecolor="none", zorder=3)
    bars_wait = ax.barh(y, wait_pct, height, left=work_pct, label="공정 간 단순 대기시간 (Waiting Lag)", color="#F43F5E", alpha=0.90, edgecolor="none", zorder=3)

    for idx, (w_p, wt_p, wt_h, h_t) in enumerate(zip(work_pct, wait_pct, wait_hours, hours_total)):
        if w_p > 8.0:
            ax.text(w_p / 2.0, idx, f"{w_p:.1f}%", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10.5, zorder=4)
        if wt_p > 15.0:
            ax.text(w_p + wt_p / 2.0, idx, f"{wt_p:.1f}% ({wt_h:.1f}h 대기)", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10.5, zorder=4)
        ax.text(102.5, idx, f"{h_t:.1f} 시간", ha="left", va="center", color="#0F172A", fontweight="bold", fontsize=11.5, zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels(phases, fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_xlim(0, 118)
    ax.set_ylim(-0.6, 3.7)
    ax.set_xlabel("국면별 소요시간 구성 비중 (%)", fontsize=10, fontweight="bold", color="#64748B", labelpad=6)
    ax.grid(axis="x", linestyle=":", alpha=0.6, color="#CBD5E1", zorder=1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.tick_params(colors="#64748B", labelsize=10)

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2, fontsize=10, frameon=False)

    plt.tight_layout()
    save_fig(fig, "slide08_macro_leadtime_breakdown.png", also_deck=True)


# -----------------------------------------------------------------------------
# 3. p.09: 접수 국면 3-Panel 통합 병목 진단 (slide09_reception_bottleneck_3panel.png)
#    - 카드 컨테이너 배경색 #FFFFFF 명시적 채움
#    - Y축 라벨: #1E293B, X축 라벨: #64748B, 수치 라벨 고대비 확보
# -----------------------------------------------------------------------------
def render_p09_reception_3panel():
    piv = pd.read_csv("case_pivot_table.csv")
    for col in ["contact_time", "inform_survey_time"]:
        piv[col] = pd.to_datetime(piv[col], errors="coerce")
    v = piv[piv.objectKey.notna()].copy()
    v["m"] = (v.inform_survey_time - v.contact_time).dt.total_seconds() / 60.0

    ev = pd.read_csv("repair_cleaned.csv")
    rl = ev[ev.taskID.isin(["FirstContact", "MakeTicket", "ArrangeSurvey", "InformClientSurvey"]) & ev.originator.isin(["Anne", "Dian", "Monica", "Paul"])]
    ho = set(rl.groupby("caseID").originator.nunique()[lambda x: x > 1].index)

    df_leadtime = pd.DataFrame({
        "receipt_group": np.where(v.caseID.isin(ho), "인계 발생군 (13.3%)", "단독 처리군 (86.7%)"),
        "duration_hours": v.m / 60.0
    })
    df_cohort = pd.DataFrame({
        "contact_channel": v.contact_channel,
        "arrange_duration_minutes": v.m,
        "cohort_group": np.where(v.m <= 15.0, "15분 이내 (Fast Cohort)", np.where(v.m > 60.0, "60분 초과 (Slow Cohort)", "15~60분 (Mid Cohort)"))
    })

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.0), dpi=300, gridspec_kw={"width_ratios": [1, 1.25, 1]})
    fig.patch.set_facecolor(BG_COLOR)
    for ax in axes:
        ax.set_facecolor(BG_COLOR)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#CBD5E1")
        ax.spines["bottom"].set_color("#CBD5E1")
        ax.tick_params(colors="#64748B", labelsize=10)

    # [Panel 1] 단독 vs 인계
    single_data = df_leadtime[df_leadtime["receipt_group"].str.contains("단독")]
    handover_data = df_leadtime[df_leadtime["receipt_group"].str.contains("인계")]
    means = [single_data["duration_hours"].mean(), handover_data["duration_hours"].mean()]
    colors_p1 = ["#2563EB", "#E11D48"]

    bars1 = axes[0].bar([0, 1], means, color=colors_p1, width=0.45, zorder=3)
    axes[0].text(0, means[0] + 0.25, f"{means[0]:.1f} 시간", ha="center", va="bottom", fontsize=11.5, fontweight="bold", color="#2563EB", zorder=4)
    axes[0].text(1, means[1] + 0.25, f"{means[1]:.1f} 시간 (6.6배)", ha="center", va="bottom", fontsize=11.5, fontweight="bold", color="#E11D48", zorder=4)
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(["단독 처리 (804건)", "교차 인계 (123건)"], fontsize=10.5, fontweight="bold", color="#1E293B")
    axes[0].set_ylabel("평균 접수 소요시간 (시간, h)", fontsize=10, fontweight="bold", color="#64748B")
    axes[0].set_ylim(0, 10)
    axes[0].grid(axis="y", linestyle=":", alpha=0.5, color="#CBD5E1", zorder=0)

    # [Panel 2] 채널별 코호트 양극화
    cohort_summary = pd.crosstab(df_cohort["contact_channel"], df_cohort["cohort_group"], normalize="index") * 100.0
    channel_order = ["Personal", "Phone", "Web", "Letter"]
    cohort_summary = cohort_summary.reindex(channel_order)
    colors_cohort = {"15분 이내 (Fast Cohort)": "#059669", "60분 초과 (Slow Cohort)": "#E11D48"}

    bottom = np.zeros(len(channel_order))
    for col in ["15분 이내 (Fast Cohort)", "60분 초과 (Slow Cohort)"]:
        if col in cohort_summary.columns:
            vals = cohort_summary[col].values
            axes[1].barh(channel_order, vals, left=bottom, label=col.split(" (")[0], color=colors_cohort[col], height=0.48, zorder=3)
            for i, val in enumerate(vals):
                if val > 10.0:
                    axes[1].text(bottom[i] + val / 2.0, i, f"{val:.1f}%", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10.5, zorder=4)
            bottom += vals

    axes[1].set_xlabel("비율 (%)", fontsize=10, fontweight="bold", color="#64748B")
    axes[1].set_xlim(0, 100)
    axes[1].grid(axis="x", linestyle=":", alpha=0.5, color="#CBD5E1", zorder=0)
    axes[1].legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False, fontsize=10)
    axes[1].set_yticks(range(len(channel_order)))
    axes[1].set_yticklabels(["대면", "전화", "웹 (Web)", "우편"], fontsize=10.5, fontweight="bold", color="#1E293B")

    # [Panel 3] Fast 집단 분석
    fast_data = df_cohort[df_cohort["cohort_group"].str.contains("Fast")]
    fast_avg = fast_data.groupby("contact_channel")["arrange_duration_minutes"].mean().reindex(channel_order)
    colors_fast = ["#CBD5E1", "#CBD5E1", "#059669", "#CBD5E1"]
    bars3 = axes[2].bar(channel_order, fast_avg, color=colors_fast, width=0.45, zorder=3)

    for i, bar in enumerate(bars3):
        yval = bar.get_height()
        is_web = (channel_order[i] == "Web")
        txt_color = "#059669" if is_web else "#0F172A"
        axes[2].text(bar.get_x() + bar.get_width() / 2.0, yval + 0.25, f"{yval:.1f}분",
                     ha="center", va="bottom", fontweight="bold", fontsize=10.5, color=txt_color, zorder=4)

    axes[2].set_ylabel("평균 소요시간 (분, min)", fontsize=10, fontweight="bold", color="#64748B")
    axes[2].set_ylim(0, 10.5)
    axes[2].set_xticks(range(len(channel_order)))
    axes[2].set_xticklabels(["대면", "전화", "웹 (Web)", "우편"], fontsize=10.5, fontweight="bold", color="#1E293B")
    axes[2].grid(axis="y", linestyle=":", alpha=0.5, color="#CBD5E1", zorder=0)

    plt.tight_layout()
    save_fig(fig, "slide09_reception_bottleneck_3panel.png", also_deck=True)


# -----------------------------------------------------------------------------
# 4. p.10: 상관관계 히트맵 (reception_detailed_correlation_heatmap.png)
#    - 카드 컨테이너 배경색 #FFFFFF 명시적 채움
#    - Coolwarm 발산 팔레트, 12.5pt 상관계수 확대
#    - 축 눈금/라벨: #1E293B, 컬러바 라벨: #64748B
# -----------------------------------------------------------------------------
def render_p10_correlation_heatmap():
    piv = pd.read_csv("case_pivot_table.csv")
    for col in ["contact_time", "inform_survey_time", "survey_start"]:
        piv[col] = pd.to_datetime(piv[col], errors="coerce")
    vdf = piv[piv.objectKey.notna()].copy()
    vdf["receipt_hours"] = (vdf.inform_survey_time - vdf.contact_time).dt.total_seconds() / 3600.0
    vdf["visit_lag_hours"] = (vdf.survey_start - vdf.inform_survey_time).dt.total_seconds() / 3600.0

    ev = pd.read_csv("repair_cleaned.csv")
    rl = ev[ev.taskID.isin(["FirstContact", "MakeTicket", "ArrangeSurvey", "InformClientSurvey"]) & ev.originator.isin(["Anne", "Dian", "Monica", "Paul"])]
    ho = set(rl.groupby("caseID").originator.nunique()[lambda x: x > 1].index)
    vdf["is_handover"] = vdf.caseID.isin(ho).astype(int)

    vdf["is_realtime_channel"] = vdf["contact_channel"].isin(["Personal", "Phone"]).astype(int)
    vdf["is_web"] = (vdf["contact_channel"] == "Web").astype(int)
    vdf["is_letter"] = (vdf["contact_channel"] == "Letter").astype(int)
    vdf["is_phone"] = (vdf["contact_channel"] == "Phone").astype(int)
    vdf["is_personal"] = (vdf["contact_channel"] == "Personal").astype(int)

    vdf["contact_date"] = vdf["contact_time"].dt.date
    daily_vol = vdf.groupby("contact_date")["caseID"].transform("count")
    vdf["daily_intake_volume"] = daily_vol

    rec_corr_df = pd.DataFrame({
        "접수 소요시간(h)": vdf["receipt_hours"],
        "일별 접수량(건)": vdf["daily_intake_volume"],
        "실시간 채널여부": vdf["is_realtime_channel"],
        "교차 인계(Handover)": vdf["is_handover"],
        "현장 실사 대기(h)": vdf["visit_lag_hours"],
        "웹 접수(Web)": vdf["is_web"],
        "우편 접수(Letter)": vdf["is_letter"],
        "전화 접수(Phone)": vdf["is_phone"],
        "대면 접수(Personal)": vdf["is_personal"]
    })
    corr_matrix = rec_corr_df.corr()

    fig, ax = plt.subplots(figsize=(9.2, 8.0), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-0.65,
        vmax=1.0,
        center=0,
        square=True,
        linewidths=2.0,
        linecolor="#FFFFFF",
        cbar_kws={
            "label": "Pearson Correlation Coefficient (r)",
            "shrink": 0.78,
            "aspect": 22,
            "pad": 0.03
        },
        annot_kws={"size": 12.5, "weight": "bold"},
        ax=ax
    )

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10, fontweight="bold", color="#1E293B")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10, fontweight="bold", color="#1E293B")
    ax.tick_params(colors="#64748B", labelsize=10)

    plt.tight_layout()
    save_fig(fig, "reception_detailed_correlation_heatmap.png")


# -----------------------------------------------------------------------------
# 5. p.12: 현장 소요시간 도넛 (slide10_field_donut_breakdown.png)
#    - 카드 컨테이너 배경색 #FFFFFF 명시적 채움
#    - 실사 방문 대기(78.2%)만 강조색(#E11D48), 나머지 슬레이트 그레이 계열
#    - 밝은 슬레이트 섹터 내부 수치: 어두운 색상 (#0F172A) 적용
# -----------------------------------------------------------------------------
def render_p12_field_donut():
    fig, ax = plt.subplots(figsize=(9.2, 6.8), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    sizes = [fs("wait1"), fs("wait2_res"), fs("rep_work"), fs("survey_work")]
    pct_labels = [f"{F['wait1_pct']['s']}%", f"{F['wait2_res_pct']['s']}%", f"{F['rep_work_pct']['s']}%", ""]

    labels = [
        f"① 실사 방문 대기 (Wait 1: {F['wait1']['s']}h, {F['wait1_pct']['s']}%)",
        f"② 수리 착수 및 공정 대기 (Wait 2: {F['wait2_res']['s']}h, {F['wait2_res_pct']['s']}%)",
        f"③ 실제 본수리 실작업 (Repair Work: {F['rep_work']['s']}h, {F['rep_work_pct']['s']}%)",
        f"④ 실사 점검 실작업 (Survey Work: {F['survey_work']['s']}h, {F['survey_work_pct']['s']}%)"
    ]

    colors = ["#E11D48", "#CBD5E1", "#E2E8F0", "#F1F5F9"]
    explode = (0.04, 0.0, 0.0, 0.0)

    _ctr = {"i": -1}
    def _autopct(p):
        _ctr["i"] += 1
        return pct_labels[_ctr["i"]] if _ctr["i"] < len(pct_labels) else ""

    wedges, texts, autotexts = ax.pie(
        sizes,
        explode=explode,
        autopct=_autopct,
        startangle=140,
        colors=colors,
        pctdistance=0.76,
        wedgeprops=dict(width=0.44, edgecolor="white", linewidth=2.5)
    )

    for i, autotext in enumerate(autotexts):
        if i == 0:
            autotext.set_color("#FFFFFF")
            autotext.set_fontweight("bold")
            autotext.set_fontsize(12)
        elif i == 1:
            autotext.set_color("#0F172A")    # 밝은 슬레이트 막대 내부 수치 텍스트: #0F172A (대비 확보)
            autotext.set_fontweight("bold")
            autotext.set_fontsize(10.5)
        else:
            autotext.set_color("#0F172A")
            autotext.set_fontweight("bold")
            autotext.set_fontsize(9.5)

    ax.text(0, 0.15, "현장 총 소요시간", ha="center", va="center", fontsize=12, fontweight="bold", color="#64748B")
    ax.text(0, -0.04, f"{F['field_total']['s']} 시간", ha="center", va="center", fontsize=20, fontweight="bold", color="#0F172A")
    ax.text(0, -0.21, f"(단순 대기 {F['field_wait_pct']['s']}% vs 실작업 {F['field_work_pct']['s']}%)", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#E11D48")

    ax.legend(wedges, labels, loc="lower center", bbox_to_anchor=(0.5, -0.12), fontsize=10, ncol=2, frameon=False)

    plt.tight_layout()
    save_fig(fig, "slide10_field_donut_breakdown.png", also_deck=True)


# -----------------------------------------------------------------------------
# 6. p.13: 유입 vs CAPA 콤보 (slide10_field_bottleneck_wip.png)
#    - 카드 컨테이너 배경색 #FFFFFF 명시적 채움
#    - WIP 라인: 두께 2.5px 다크 로즈(#E11D48) 및 마커 최적화
#    - X축 눈금: #1E293B, Left Y축: #64748B, Right Y축: #E11D48
# -----------------------------------------------------------------------------
def render_p13_field_bottleneck_wip():
    piv = pd.read_csv("case_pivot_table.csv")
    for col in ["inform_survey_time", "survey_start"]:
        piv[col] = pd.to_datetime(piv[col], errors="coerce")
    vdf = piv[piv.objectKey.notna()].copy()

    cohort = vdf.copy()
    cohort["inform_dt"] = cohort["inform_survey_time"].dt.normalize()
    cohort["survey_dt"] = cohort["survey_start"].dt.normalize()

    handoff = cohort.groupby("inform_dt").size().rename("handoff")
    survey = cohort.groupby("survey_dt").size().rename("survey")

    all_dates = sorted(list(set(handoff.index) | set(survey.index)))
    daily = pd.DataFrame(index=pd.to_datetime(all_dates))
    daily = daily.join(handoff).fillna(0).join(survey).fillna(0)

    daily["cum_handoff"] = daily["handoff"].cumsum()
    daily["cum_survey"] = daily["survey"].cumsum()
    daily["field_wip"] = daily["cum_handoff"] - daily["cum_survey"]

    focus_dates = daily.loc["1970-01-01":"1970-01-14"].copy()
    x_labels = [f"Day {i+1}\n({d.strftime('%m/%d')})" for i, d in enumerate(focus_dates.index)]
    x = np.arange(len(focus_dates))
    width = 0.36

    fig, ax1 = plt.subplots(figsize=(12.0, 5.2), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax1.set_facecolor(BG_COLOR)

    bars1 = ax1.bar(x - width / 2, focus_dates["handoff"], width, color="#2563EB", alpha=0.90, edgecolor="none", zorder=3)
    bars2 = ax1.bar(x + width / 2, focus_dates["survey"], width, color="#94A3B8", alpha=0.88, edgecolor="none", zorder=3)

    ax1.axhline(134.3, color="#2563EB", linestyle="--", linewidth=1.5, alpha=0.7, zorder=2)
    ax1.axhline(68.0, color="#475569", linestyle=":", linewidth=1.8, alpha=0.7, zorder=2)

    ax1.set_ylabel("일일 처리 건수 (건/일)", color="#64748B", fontsize=10, fontweight="bold")
    ax1.set_ylim(0, 180)
    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels, fontsize=9.0, color="#1E293B")
    ax1.grid(axis="y", linestyle=":", alpha=0.5, color="#CBD5E1", zorder=1)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#CBD5E1")
    ax1.spines["bottom"].set_color("#CBD5E1")
    ax1.tick_params(colors="#64748B", labelsize=9.5)

    ax2 = ax1.twinx()
    ax2.set_facecolor(BG_COLOR)
    line = ax2.plot(
        x,
        focus_dates["field_wip"],
        color="#E11D48",
        linewidth=2.5,
        marker="o",
        markersize=6.0,
        markerfacecolor="#E11D48",
        markeredgecolor="#FFFFFF",
        markeredgewidth=1.5,
        zorder=5
    )
    ax2.set_ylabel("미처리 현장 적체 대기열 (누적 WIP, 건)", color="#E11D48", fontsize=10, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#E11D48", labelsize=9.5)
    ax2.set_ylim(0, 480)
    ax2.spines["top"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_color("#E11D48")

    t1 = TextArea("■ 현장 이관 유입   ", textprops=dict(color="#2563EB", fontsize=9.5, fontweight="bold"))
    t2 = TextArea("■ 현장 실사 착수   ", textprops=dict(color="#64748B", fontsize=9.5, fontweight="bold"))
    t3 = TextArea("● 미처리 적체 대기열 WIP (건)", textprops=dict(color="#E11D48", fontsize=9.5, fontweight="bold"))
    box = HPacker(children=[t1, t2, t3], align="baseline", pad=0, sep=4)
    anchored_box = AnchoredOffsetbox(
        loc="upper right",
        child=box,
        pad=0.2,
        frameon=False,
        bbox_to_anchor=(0.985, 0.98),
        bbox_transform=fig.transFigure,
        borderpad=0.0
    )
    fig.add_artist(anchored_box)

    plt.tight_layout()
    save_fig(fig, "slide10_field_bottleneck_wip.png")


# -----------------------------------------------------------------------------
# 14. p.14: 수리 방식별 착수 대기 + 사내 재수리 루프 (hypothesis 노트북 Cell 17 의 형태 그대로)
#    - 형태·색·배치 불변, 라벨의 '하자 재방문'만 '재수리'로 교체, 수치는 facts.json 주입
#    - 사용자 PNG(outputs/figures/slide11_repair_delay_rework.png)는 덮어쓰지 않고 deck/ 에만 저장
# -----------------------------------------------------------------------------
def render_p14_rework():
    fs_ = lambda k: F[k]["s"]
    n_all = float(fs_("n_surveyed"))
    n_ie = int(fs_("n_imm1")) + int(fs_("n_ext1"))
    n_in = int(fs_("n_intern1"))
    n_rw = int(fs_("n_rework"))
    cats = [
        f"즉시 완결 / 외주 위탁\n(Immediate & Extern)\n[{n_ie}건, {n_ie / n_all * 100:.1f}%]",
        f"사내 수리 1차 착수\n(InternRepair 1차)\n[{n_in}건, {n_in / n_all * 100:.1f}%]",
        f"사내 재수리 루프\n(Intern Rework Loop)\n[{n_rw}건, {n_rw / n_all * 100:.1f}%]",
    ]
    delays = [fs("wait2_imm"), fs("wait2_intern"), fs("rework_gap_mean")]
    colors = ["#10B981", "#DC2626", "#991B1B"]

    fig, ax = plt.subplots(figsize=(10.5, 5.0), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAFAFA")
    bars = ax.bar(cats, delays, color=colors, width=0.45, edgecolor="none", alpha=0.92)
    ax.set_title("수리 방식별 대기시간 및 사내 재수리 루프 지연 충격 (단일 통합 분석)", fontsize=13, fontweight="bold", pad=16, color="#0F172A", loc="left")
    ax.set_ylabel("착수 대기시간 (시간, h)", fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, 42)
    ax.grid(axis="y", linestyle=":", alpha=0.5, color="#CBD5E1")

    ax.text(bars[0].get_x() + bars[0].get_width() / 2.0, 1.2, f"대기 {fs_('wait2_imm')}h\n(현장 완결 / 전산 즉시 이관)", ha="center", va="bottom", fontsize=10.5, fontweight="bold", color="#059669")
    ax.text(bars[1].get_x() + bars[1].get_width() / 2.0, delays[1] + 1.2, f"평균 {fs_('wait2_intern')}시간 ({delays[1] / 24:.1f}일)\n(자재 조달 및 일정 조율 대기)", ha="center", va="bottom", fontsize=10.5, fontweight="bold", color="#DC2626")
    ax.text(bars[2].get_x() + bars[2].get_width() / 2.0, delays[2] + 1.2, f"추가 대기 +{fs_('rework_gap_mean')}h (최대 {fs_('rework_gap_max_d')}일)\n[재수리군 평균 총 리드타임 {fs_('rework_lead_mean')}h]", ha="center", va="bottom", fontsize=10.5, fontweight="bold", color="#991B1B")

    plt.tight_layout()
    out = os.path.join(DECK_DIR, "slide11_repair_delay_rework.png")
    fig.savefig(out, facecolor=fig.get_facecolor(), edgecolor="none", transparent=False, dpi=300, bbox_inches="tight")
    print(f"✅ [저장 완료] {out} (300 DPI)")
    plt.close(fig)


# -----------------------------------------------------------------------------
# 16. p.16: 접수 사전 분류(B·P·E) 도넛 — 원본 slide12_intake_matching_donut.png 와 같은 형태
#    - 도넛 구성·색·배치 불변. 라벨만 '정합도/적합도(87.3%)' → 실제 1차 수리 방식 일치율로 교체
#    - 사용자 PNG(outputs/figures/slide12_intake_matching_donut.png)는 덮어쓰지 않고 deck/ 에만 저장
# -----------------------------------------------------------------------------
def render_p16_match_donut():
    fs_ = lambda k: F[k]["s"]
    n_E, n_P, n_B = int(fs_("n_E")), int(fs_("n_P")), int(fs_("n_B"))
    n_all = n_E + n_P + n_B
    vals = [n_P, n_E, n_B]
    colors = ["#059669", "#2563EB", "#94A3B8"]
    names = [
        f"P형\n({n_P}건)",
        f"E형\n({n_E}건)",
        f"B형\n({n_B}건)",
    ]
    fig, ax = plt.subplots(figsize=(7.72, 6.2), dpi=100)
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")
    wedges, _ = ax.pie(vals, colors=colors, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.38, edgecolor="white", linewidth=3), radius=1.0)
    for w, val, name in zip(wedges, vals, names):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2.0)
        x, y = np.cos(ang), np.sin(ang)
        ax.text(0.81 * x, 0.81 * y, f"{val / n_all * 100:.1f}%", ha="center", va="center", color="white", fontsize=12, fontweight="bold")
        ax.text(1.12 * x, 1.12 * y, name, ha="left" if x > 0 else "right", va="center", fontsize=16, color="#0F172A")
    ax.text(0, 0.10, f"{fs_('match_upper_pct')}%", ha="center", va="center", fontsize=34, fontweight="bold", color="#0F172A")
    ax.text(0, -0.13, "E·P 사전 분류", ha="center", va="center", fontsize=12, color="#64748B")
    ax.text(0, -0.27, f"({fs_('match_upper_n')} / {n_all}건)", ha="center", va="center", fontsize=12, color="#64748B")
    ax.set_title("접수 사전 분류와 실제 1차 수리 방식", fontsize=17, fontweight="bold", color="#0F172A", pad=18)
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.2, 1.25)
    ax.set_aspect("equal")
    out = os.path.join(DECK_DIR, "slide12_intake_matching_donut.png")
    fig.savefig(out, facecolor=fig.get_facecolor(), edgecolor="none", transparent=False, dpi=300, bbox_inches="tight")
    print(f"✅ [저장 완료] {out} (300 DPI)")
    plt.close(fig)


def main():
    print("🎨 [시작] 카드 컨테이너 명시적 배경(#FFFFFF, transparent=False) 차트 재생성...")
    render_p04_eda_missing()
    render_p08_leadtime_breakdown()
    render_p09_reception_3panel()
    render_p10_correlation_heatmap()
    render_p12_field_donut()
    render_p13_field_bottleneck_wip()
    render_p14_rework()
    render_p16_match_donut()
    print("🎉 [완료] 전 차트 명시적 배경(#FFFFFF) 및 고대비 파라미터 적용 완료!")


if __name__ == "__main__":
    main()
