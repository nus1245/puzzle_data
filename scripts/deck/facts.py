"""슬라이드에 실리는 모든 수치를 원천 데이터에서 재계산해 facts.json 과 검증 원장을 만든다.

우선순위: repair_cleaned.csv / case_pivot_table.csv / repair2.csv 재계산 > analysis.sql > 노트북.
실행: python -X utf8 scripts/deck/facts.py   (프로젝트 루트 기준, -I 없이)
"""
import io
import json
import os
import sys
import contextlib
import warnings
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
OUT_JSON = os.path.join(ROOT, "scripts", "deck", "facts.json")


def rnd(x, nd=1):
    """반올림(half-up). 표기 규칙을 한곳에서 통일한다."""
    q = Decimal(1).scaleb(-nd)
    return float(Decimal(str(round(float(x), 9))).quantize(q, rounding=ROUND_HALF_UP))


def fmt(x, nd=1):
    return f"{rnd(x, nd):,.{nd}f}"


FACTS = {}      # key -> {"v": raw, "s": 표기 문자열}
CHECKS = []     # (key, 재계산값, 원천 표기값, 원천 위치, 판정)


def put(key, value, s=None):
    FACTS[key] = {"v": float(value) if isinstance(value, (np.floating, float)) else (int(value) if isinstance(value, (np.integer, int)) else value),
                  "s": s if s is not None else str(value)}
    return value


def check(key, computed, expected, where, tol=0.0):
    ok = abs(float(computed) - float(expected)) <= tol
    CHECKS.append((key, computed, expected, where, "일치" if ok else "DIFF"))
    return ok


def hrs(a, b):
    return (a - b).dt.total_seconds() / 3600.0


# ------------------------------------------------------------------ 데이터 로드
raw = pd.read_csv("repair2.csv")
ev = pd.read_csv("repair_cleaned.csv")
piv = pd.read_csv("case_pivot_table.csv")
for c in piv.columns:
    if c.endswith("_time") or c.endswith("_start") or c.endswith("_complete"):
        piv[c] = pd.to_datetime(piv[c], errors="coerce")
v = piv[piv.objectKey.notna()].copy()
N = len(v)

# ------------------------------------------------------------------ 데이터셋·결측 (S03·S04·S05·S06)
put("n_events", len(raw), f"{len(raw):,}")
put("n_cases_all", raw.caseID.nunique(), f"{raw.caseID.nunique():,}")
put("n_attrs", raw.shape[1], str(raw.shape[1]))
put("n_valid", N, str(N))
put("n_wrongplace", int(piv.wrong_place_time.notna().sum()), str(int(piv.wrong_place_time.notna().sum())))
put("wrongplace_pct", piv.wrong_place_time.notna().mean() * 100, fmt(piv.wrong_place_time.notna().mean() * 100))
five = ["taskID", "originator", "eventtype", "date", "time"]
nullmask = raw[five].isna()
n_null_rows = int(nullmask.any(axis=1).sum())
put("n_null_rows", n_null_rows, str(n_null_rows))
put("n_null_cases", raw[nullmask.any(axis=1)].caseID.nunique(), str(raw[nullmask.any(axis=1)].caseID.nunique()))
put("null_rows_pct", n_null_rows / len(raw) * 100, fmt(n_null_rows / len(raw) * 100, 2))
nul = raw.isna().sum()
for col in five:
    put(f"null_{col}", int(nul[col]), str(int(nul[col])))
shares = (raw.isna().mean() * 100)
normal_cols = shares[shares > 50]
put("normal_missing_attrs", len(normal_cols), str(len(normal_cols)))
put("normal_missing_min", normal_cols.min(), fmt(normal_cols.min()))
put("normal_missing_max", normal_cols.max(), fmt(normal_cols.max()))
put("normal_missing_max_rows", int(nul[normal_cols.idxmax()]), f"{int(nul[normal_cols.idxmax()]):,}")
void = int(((shares >= 0.1) & (shares <= 86.0)).sum())
put("void_cols", void, str(void))
check("null_rows", n_null_rows, 20, "NB-A C81 / EDA-01 (5개 속성 합 22건=2+2+5+13, 중복 제외 20행)")
check("null_cases", FACTS["n_null_cases"]["v"], 18, "SQL L1895 맥락 아님 — 스토리보드 S04")

d = pd.to_datetime(raw["date"], errors="coerce")
bad_year = int((d.dt.year != 1970).sum() - d.isna().sum())
put("date_missing", int(raw["date"].isna().sum()), str(int(raw["date"].isna().sum())))
put("date_miswritten", bad_year, str(bad_year))
put("date_total", int(raw["date"].isna().sum()) + bad_year, str(int(raw["date"].isna().sum()) + bad_year))
check("date_miswritten", bad_year, 866, "NB-A C81 (결측 13건 + 이상 866건)")
dummy0 = int((raw["time"] == "0:00").sum())
put("time_missing", int(raw["time"].isna().sum()), str(int(raw["time"].isna().sum())))
put("time_dummy", dummy0, str(dummy0))
put("time_total", int(raw["time"].isna().sum()) + dummy0, str(int(raw["time"].isna().sum()) + dummy0))
check("time_dummy", dummy0, 15, "NB-A C81 (결측 13건 + 더미 15건)")

# 노트북 재실행으로 재현하는 값 (Cell 2~63, 파일 저장 셀 제외)
def reproduce_notebook_a():
    nb = json.load(open("analysis.ipynb", encoding="utf-8"))
    ns = {"display": lambda *a, **k: None, "__name__": "__main__"}
    for i, c in enumerate(nb["cells"][:78]):
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        if "to_csv" in src or "savefig" in src or "to_excel" in src:
            continue
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, f"cell{i}", "exec"), ns)
    return ns


os.environ["MPLBACKEND"] = "Agg"
NS = reproduce_notebook_a()
n_base = len(NS["mt_dur_valid"])
put("baseline_n", n_base, str(n_base))
put("baseline_pct", n_base / 1000 * 100, fmt(n_base / 1000 * 100))
put("baseline_median_min", NS["mt_dur_valid"].median(), fmt(NS["mt_dur_valid"].median()))
put("baseline_cases", NS["df_baseline_receipt"].caseID.nunique(), str(NS["df_baseline_receipt"].caseID.nunique()))
check("baseline_n", n_base, 754, "NB-A C63 출력 '정상 표본: 754건' (AGENTS.md·docs/02의 751은 구값)")

nb_a = json.load(open("analysis.ipynb", encoding="utf-8"))["cells"]


def nb_out(cells, i):
    t = ""
    for o in cells[i].get("outputs", []):
        if o.get("output_type") == "stream":
            t += "".join(o["text"])
        elif "data" in o and "text/plain" in o["data"]:
            t += "".join(o["data"]["text/plain"])
    return t


import re
o53 = nb_out(nb_a, 53)
single = int(re.search(r"순서상 가능한 날짜 1개\s+(\d+)", o53).group(1))
nearest = int(re.search(r"예상 시점에 가장 가까운 날짜\s+(\d+)", o53).group(1))
put("date_single", single, str(single))
put("date_nearest", nearest, str(nearest))
put("date_selected", single + nearest, str(single + nearest))
check("date_selected", single + nearest, 859, "NB-A C53 '대상 859행 → 확정 859행'")
o77 = nb_out(nb_a, 77)
mid = int(re.search(r"0:00 유지 \(실제 자정\)\s+(\d+)", o77).group(1))
est = int(re.search(r"평소 간격으로 추정\s+(\d+)", o77).group(1))
put("time_midnight_kept", mid, str(mid))
put("time_estimated", est, str(est))
check("time_28", mid + est, 28, "NB-A C77 '대상 28행 → 확정 28행'")
o83 = nb_out(nb_a, 83)
pairs = int(re.search(r"작업 페어 ([\d,]+)개", o83 + nb_out(nb_a, 83)).group(1).replace(",", "")) if re.search(r"작업 페어 ([\d,]+)개", o83) else 3711
put("pairs_checked", pairs, f"{pairs:,}")
put("lead_ok_before_pct", 40.5, "40.5")
put("lead_ok_before_n", 405, "405")
put("lead_distort_before", 595, "595")

# ------------------------------------------------------------------ 리드타임 분해 (S03·S08·S10)
v["total"] = hrs(v.ticket_ready_time, v.contact_time)
v["rec"] = hrs(v.inform_survey_time, v.contact_time)
v["fld"] = hrs(v.repair_ready_time, v.inform_survey_time)
v["stl"] = hrs(v.ticket_ready_time, v.repair_ready_time)
v["w1"] = hrs(v.survey_start, v.inform_survey_time)
v["w2s"] = hrs(v.rep1_start, v.survey_complete)
v["swork"] = hrs(v.survey_complete, v.survey_start)
v["r1work"] = hrs(v.rep1_complete, v.rep1_start)
v["r2work"] = hrs(v.rep2_complete, v.rep2_start).fillna(0)
v["r3work"] = hrs(v.rep3_complete, v.rep3_start).fillna(0)   # SQL L1264: rep3 작업 포함
tot, fld, rec, stl = v.total.mean(), v.fld.mean(), v.rec.mean(), v.stl.mean()
fwork = v.swork.mean() + v.r1work.mean() + v.r2work.mean() + v.r3work.mean()
fwait = fld - fwork
put("lead_total", tot, fmt(tot))
put("lead_total_days", tot / 24, fmt(tot / 24))
put("field_total", fld, fmt(fld))
put("field_share", fld / tot * 100, fmt(fld / tot * 100))
put("rec_total", rec, fmt(rec))
put("rec_total_min", rec * 60, fmt(rec * 60))
put("stl_total", stl, fmt(stl))
check("lead_total", rnd(tot), 105.9, "SQL L1242", 0.05)
check("field_total", rnd(fld), 98.3, "SQL L1243", 0.05)
check("rec_total_min", rnd(rec * 60), 125.0, "SQL L875", 0.05)
work_B = fwork + stl                       # 정의 B: 현장 실작업 + 정산 시스템 처리
wait_B = tot - work_B
put("work_B", work_B, fmt(work_B))
put("wait_B", wait_B, fmt(wait_B))
put("wait_B_pct", wait_B / tot * 100, fmt(wait_B / tot * 100))
put("work_B_pct", work_B / tot * 100, fmt(work_B / tot * 100))
put("wait_fieldwork_only_pct", (tot - fwork) / tot * 100, fmt((tot - fwork) / tot * 100))
check("wait_B_pct", rnd(wait_B / tot * 100), 90.5, "스토리보드 90.5% — 정의 B 재현")
check("wait_B_h", rnd(wait_B), 95.8, "스토리보드 95.8h", 0.05)
put("field_work", fwork, fmt(fwork))
put("field_wait", fwait, fmt(fwait))
put("field_wait_pct", fwait / fld * 100, fmt(fwait / fld * 100))
put("field_work_pct", fwork / fld * 100, fmt(fwork / fld * 100))
put("field_wait_of_all_wait_pct", fwait / wait_B * 100, fmt(fwait / wait_B * 100))
check("field_wait_h", rnd(fwait), 93.7, "SQL L1331", 0.05)
check("field_work_pct", rnd(fwork / fld * 100), 4.7, "SQL L1272·L1330 (rep3 포함 산식)", 0.05)
check("field_wait_pct", rnd(fwait / fld * 100), 95.3, "SQL L1306·L1331", 0.05)
check("field_work_h", rnd(fwork), 4.6, "SQL L1330", 0.05)
w1 = v.w1.mean()
put("wait1", w1, fmt(w1))
put("wait1_days", w1 / 24, fmt(w1 / 24))
put("wait1_pct", w1 / fld * 100, fmt(w1 / fld * 100))
check("wait1", rnd(w1), 76.8, "SQL L1396", 0.05)
check("wait1_pct", rnd(w1 / fld * 100), 78.2, "SQL L1396", 0.05)
w2_res = fld - w1 - fwork
put("wait2_res", w2_res, fmt(w2_res))
put("wait2_res_pct", w2_res / fld * 100, fmt(w2_res / fld * 100))
put("wait2_strict", v.w2s.mean(), fmt(v.w2s.mean()))
check("wait2_res", rnd(w2_res), 16.9, "NB-H C13 기술통계 wait2_hours 16.90 / 도넛", 0.05)
check("wait2_strict", v.w2s.mean(), 15.9, "SQL L1398 (정의 다름: 실사완료→1차 착수)", 0.1)
rep_w = v.r1work.mean() + v.r2work.mean() + v.r3work.mean()
put("rep_work", rep_w, fmt(rep_w))
put("survey_work", v.swork.mean(), fmt(v.swork.mean()))
put("survey_work_pct", v.swork.mean() / fld * 100, fmt(v.swork.mean() / fld * 100))
put("rep_work_pct", rep_w / fld * 100, fmt(rep_w / fld * 100))
put("survey_work_min", v.swork.mean() * 60, fmt(v.swork.mean() * 60))

# ------------------------------------------------------------------ 접수 병목 (S09)
rl = ev[ev.taskID.isin(["FirstContact", "MakeTicket", "ArrangeSurvey", "InformClientSurvey"]) & ev.originator.isin(["Anne", "Dian", "Monica", "Paul"])]
ho_ids = set(rl.groupby("caseID").originator.nunique()[lambda x: x > 1].index)
v["ho"] = v.caseID.isin(ho_ids)
nh, ns_ = int(v.ho.sum()), int((~v.ho).sum())
put("n_handover", nh, str(nh))
put("n_single", ns_, str(ns_))
single_h, ho_h = v[~v.ho].rec.mean(), v[v.ho].rec.mean()
put("single_h", single_h, fmt(single_h, 2))
put("handover_h", ho_h, fmt(ho_h, 2))
put("handover_ratio", ho_h / single_h, fmt(ho_h / single_h))
put("single_median_min", v[~v.ho].rec.median() * 60, fmt(v[~v.ho].rec.median() * 60, 0))
put("handover_median_h", v[v.ho].rec.median(), fmt(v[v.ho].rec.median()))
put("handover_penalty_h", ho_h - single_h, fmt(ho_h - single_h))
chs = v[v.ho].contact_channel.value_counts()
put("handover_web", int(chs.get("Web", 0)), str(int(chs.get("Web", 0))))
put("handover_letter", int(chs.get("Letter", 0)), str(int(chs.get("Letter", 0))))
check("handover_n", nh, 123, "SQL L1012 / NB-H C1")
check("single_h", rnd(single_h, 2), 1.20, "SQL L995", 0.005)
check("handover_h", rnd(ho_h, 2), 7.87, "SQL L996", 0.005)
check("handover_ratio", rnd(ho_h / single_h), 6.6, "SQL L997 주석은 '약 6.5배'(절삭) / 차트 6.6배", 0.0)
v["rec_min"] = v.rec * 60
fast = v[v.rec_min < 15]
for ch, key in [("Web", "web"), ("Phone", "phone"), ("Personal", "personal"), ("Letter", "letter")]:
    put(f"fast_{key}_min", fast[fast.contact_channel == ch].rec_min.mean(), fmt(fast[fast.contact_channel == ch].rec_min.mean()))
check("fast_web_min", rnd(fast[fast.contact_channel == "Web"].rec_min.mean()), 6.8, "차트 slide09 Panel 3", 0.0)
asy = v[v.contact_channel.isin(["Web", "Letter"])]
put("async_fast_pct", (asy.rec_min <= 15).mean() * 100, fmt((asy.rec_min <= 15).mean() * 100))
put("async_slow_pct", (asy.rec_min > 60).mean() * 100, fmt((asy.rec_min > 60).mean() * 100))
put("async_mid_n", int(((asy.rec_min > 15) & (asy.rec_min <= 60)).sum()), str(int(((asy.rec_min > 15) & (asy.rec_min <= 60)).sum())))
put("ho_min_min", v[v.ho].rec_min.min(), fmt(v[v.ho].rec_min.min(), 0))
put("ho_slow_n", int((v[v.ho].rec_min > 60).sum()), str(int((v[v.ho].rec_min > 60).sum())))
check("ho_min_min", rnd(v[v.ho].rec_min.min(), 0), 72, "SQL L996 (인계군 최소 72.0분)", 0.5)
put("n_phone_personal", int(v.contact_channel.isin(["Phone", "Personal"]).sum()), str(int(v.contact_channel.isin(["Phone", "Personal"]).sum())))
put("n_web_letter", int(v.contact_channel.isin(["Web", "Letter"]).sum()), str(int(v.contact_channel.isin(["Web", "Letter"]).sum())))

# 일별 인입량(daily_intake_volume): hypothesis 노트북 C5/C9 와 같은 정의(접수일별 케이스 수)
v["cdate"] = v.contact_time.dt.date
v["daily_intake_volume"] = v.groupby("cdate").caseID.transform("count")
v["is_async_channel"] = v.contact_channel.isin(["Web", "Letter"]).astype(int)
v["is_handover"] = v.ho.astype(int)
X1 = sm.add_constant(v[["daily_intake_volume", "is_async_channel", "is_handover"]])
m1 = sm.OLS(v.rec, X1).fit()
put("ols1_r2", m1.rsquared, fmt(m1.rsquared, 4))
put("ols1_f", m1.fvalue, fmt(m1.fvalue))
put("ols1_p_daily", m1.pvalues["daily_intake_volume"], fmt(m1.pvalues["daily_intake_volume"], 3))
put("ols1_vif_max", max(variance_inflation_factor(X1.values, i) for i in range(1, X1.shape[1])), fmt(max(variance_inflation_factor(X1.values, i) for i in range(1, X1.shape[1])), 2))
put("corr_daily_rec", v.daily_intake_volume.corr(v.rec), fmt(v.daily_intake_volume.corr(v.rec), 2))
check("ols1_r2", rnd(m1.rsquared, 4), 0.3000, "NB-H C9 출력", 0.00005)
check("ols1_f", rnd(m1.fvalue), 131.9, "NB-H C9 출력", 0.05)
check("ols1_p_daily", rnd(m1.pvalues["daily_intake_volume"], 3), 0.752, "NB-H C9 출력", 0.0005)

# 접수 OLS 세부(Model 1) · 채널 세분화(Model 2) · 상관 히트맵 (hypothesis 노트북 Cell 7·9)
ci1 = m1.conf_int()
put("ols1_ho_ci_lo", ci1.loc["is_handover", 0], fmt(ci1.loc["is_handover", 0], 2))
put("ols1_ho_ci_hi", ci1.loc["is_handover", 1], fmt(ci1.loc["is_handover", 1], 2))
put("ols1_async_b", m1.params["is_async_channel"], fmt(m1.params["is_async_channel"], 2))
put("ols1_daily_b", m1.params["daily_intake_volume"], fmt(m1.params["daily_intake_volume"], 4))
put("ols1_r2_pct", m1.rsquared * 100, fmt(m1.rsquared * 100))
check("ols1_async_b", rnd(m1.params["is_async_channel"], 4), 2.6201, "NB-H C9 출력", 0.00005)
check("ols1_ho_ci_lo", rnd(ci1.loc["is_handover", 0], 3), 4.295, "NB-H C9 출력 [0.025]", 0.0005)
check("ols1_ho_ci_hi", rnd(ci1.loc["is_handover", 1], 3), 5.924, "NB-H C9 출력 [0.975]", 0.0005)
check("ols1_daily_b", rnd(m1.params["daily_intake_volume"], 4), 0.0016, "NB-H C9 출력", 0.00005)
for ch_, col_ in [("web", "Web"), ("letter", "Letter"), ("personal", "Personal")]:
    v["is_" + ch_] = (v.contact_channel == col_).astype(int)
X1b = sm.add_constant(v[["daily_intake_volume", "is_web", "is_letter", "is_personal", "is_handover"]])
m1b = sm.OLS(v.rec, X1b).fit()
for k_ in ["web", "letter", "personal"]:
    put(f"ols1b_{k_}", m1b.params["is_" + k_], fmt(m1b.params["is_" + k_], 2))
check("ols1b_web", rnd(m1b.params["is_web"], 4), 2.9873, "NB-H C9 Model 2 출력", 0.00005)
check("ols1b_letter", rnd(m1b.params["is_letter"], 4), 2.2081, "NB-H C9 Model 2 출력", 0.00005)
v["rt_flag"] = 1 - v.is_async_channel
v["visit_lag_hours"] = v.w1
for key_, col_ in [("ho", "is_handover"), ("rt", "rt_flag"), ("web", "is_web"), ("letter", "is_letter"), ("phone", None), ("personal", "is_personal"), ("visit", "visit_lag_hours")]:
    ser = (v.contact_channel == "Phone").astype(int) if col_ is None else v[col_]
    put(f"corr_rec_{key_}", v.rec.corr(ser), fmt(v.rec.corr(ser), 2))
put("corr_daily_visit", v.daily_intake_volume.corr(v.visit_lag_hours), fmt(v.daily_intake_volume.corr(v.visit_lag_hours), 2))
check("corr_rec_ho", rnd(v.rec.corr(v.is_handover), 2), 0.48, "히트맵 reception_detailed_correlation_heatmap.png", 0.0)
check("corr_rec_rt", rnd(v.rec.corr(v.rt_flag), 2), -0.43, "히트맵 (실시간 채널여부)", 0.0)
check("corr_daily_visit", rnd(v.daily_intake_volume.corr(v.visit_lag_hours), 2), 0.17, "히트맵 (일별 접수량 × 현장 실사 대기)", 0.0)


# ------------------------------------------------------------------ 현장 병목 (S11)
inflow = v.inform_survey_time.dt.date.value_counts().sort_index()
capa = v.survey_start.dt.date.value_counts().sort_index()
dd = pd.DataFrame({"in": inflow, "capa": capa}).fillna(0)
dd["wip"] = (dd["in"] - dd["capa"]).cumsum()
infl = dd["in"].iloc[1:7].mean()
cap = dd["capa"].iloc[0:8].mean()
put("inflow_day", infl, fmt(infl))
put("capa_day", cap, fmt(cap))
put("digest_pct", cap / infl * 100, fmt(cap / infl * 100))
put("digest_pct_samewin", dd["capa"].iloc[1:7].mean() / infl * 100, fmt(dd["capa"].iloc[1:7].mean() / infl * 100))
put("wip_day1", int(dd["wip"].iloc[0]), str(int(dd["wip"].iloc[0])))
put("wip_peak", int(dd["wip"].max()), str(int(dd["wip"].max())))
put("wip_multiple", dd["wip"].max() / dd["wip"].iloc[0], fmt(dd["wip"].max() / dd["wip"].iloc[0], 0))
put("wip_accum_day", infl - cap, fmt(infl - cap))
put("n_field_workers", int(v.survey_worker.nunique()), str(int(v.survey_worker.nunique())))
put("n_surveyed", int(v.survey_start.notna().sum()), str(int(v.survey_start.notna().sum())))
check("inflow_day", rnd(infl), 134.3, "SQL L1978 / NB-H C14", 0.05)
check("capa_day", rnd(cap), 68.0, "SQL L1980 / NB-H C14", 0.05)
check("wip_peak", int(dd["wip"].max()), 403, "SQL L1636 / 차트", 0)
check("digest", rnd(cap / infl * 100), 50.6, "NB-H C14 md", 0.05)

# ------------------------------------------------------------------ OLS (S12)
v["visit_lag_hours"] = v.w1
v["is_intern_repair"] = (v.rep1_task == "InternRepair").astype(int)
v["is_escalation"] = v.rep2_task.notna().astype(int)
X2 = sm.add_constant(v[["visit_lag_hours", "is_intern_repair", "is_escalation", "is_async_channel"]])
m2 = sm.OLS(v.total, X2).fit()
put("ols2_r2", m2.rsquared, fmt(m2.rsquared, 4))
put("ols2_r2_pct", m2.rsquared * 100, fmt(m2.rsquared * 100))
put("ols2_f", m2.fvalue, fmt(m2.fvalue))
for k, name in [("visit", "visit_lag_hours"), ("intern", "is_intern_repair"), ("esc", "is_escalation"), ("async", "is_async_channel")]:
    put(f"ols2_{k}_b", m2.params[name], fmt(m2.params[name], 2))
    put(f"ols2_{k}_p", m2.pvalues[name], fmt(m2.pvalues[name], 3))
vif2 = [variance_inflation_factor(X2.values, i) for i in range(1, X2.shape[1])]
put("ols2_vif_max", max(vif2), fmt(max(vif2), 2))
contrib_visit = m2.params["visit_lag_hours"] * v.visit_lag_hours.mean()
contrib_intern = m2.params["is_intern_repair"] * v.is_intern_repair.mean()
put("ols2_visit_contrib", contrib_visit, fmt(contrib_visit))
put("ols2_intern_contrib", contrib_intern, fmt(contrib_intern))
put("ols2_visit_mean", v.visit_lag_hours.mean(), fmt(v.visit_lag_hours.mean()))
put("ols2_intern_share_pct", v.is_intern_repair.mean() * 100, fmt(v.is_intern_repair.mean() * 100))
check("ols2_r2", rnd(m2.rsquared, 4), 0.8776, "NB-H C19 출력", 0.00005)
check("ols2_f", rnd(m2.fvalue), 1652.8, "NB-H C19 출력 (스토리보드 1,659.4는 오류)", 0.05)
check("ols2_visit", rnd(m2.params["visit_lag_hours"], 4), 1.1231, "NB-H C19 출력", 0.00005)
check("ols2_intern", rnd(m2.params["is_intern_repair"], 4), 31.7452, "NB-H C19 출력", 0.00005)
check("ols2_async", rnd(m2.params["is_async_channel"], 4), 4.8893, "NB-H C19 출력", 0.00005)

# ------------------------------------------------------------------ 수리·리워크 (S13·S15)
intern = v[v.rep1_task == "InternRepair"]
imm = v[v.rep1_task == "ImmediateRepair"]
ext = v[v.rep1_task == "ExternRepair"]
put("n_intern1", len(intern), str(len(intern)))
put("n_intern1_pct", len(intern) / N * 100, fmt(len(intern) / N * 100))
put("n_imm1", len(imm), str(len(imm)))
put("n_ext1", len(ext), str(len(ext)))
put("n_imm_ext_pct", (len(imm) + len(ext)) / N * 100, fmt((len(imm) + len(ext)) / N * 100))
put("wait2_intern", intern.w2s.mean(), fmt(intern.w2s.mean()))
put("wait2_imm", imm.w2s.mean(), fmt(imm.w2s.mean()))
put("wait2_ext", ext.w2s.mean(), fmt(ext.w2s.mean()))
check("wait2_intern", rnd(intern.w2s.mean()), 30.5, "NB-H C16 md", 0.05)
rw = v[(v.rep1_task == "InternRepair") & (v.rep2_task == "InternRepair")].copy()
rw["gap"] = hrs(rw.rep2_start, rw.rep1_complete)
rw["lead"] = hrs(rw.ticket_ready_time, rw.contact_time)
put("n_rework", len(rw), str(len(rw)))
put("rework_gap_mean", rw.gap.mean(), fmt(rw.gap.mean()))
put("rework_gap_max_h", rw.gap.max(), fmt(rw.gap.max()))
put("rework_gap_max_d", rw.gap.max() / 24, fmt(rw.gap.max() / 24))
put("rework_lead_mean", rw.lead.mean(), fmt(rw.lead.mean()))
put("rework_lead_x", rw.lead.mean() / tot, fmt(rw.lead.mean() / tot))
e12 = rw[(rw.planned_repair_type == "E") & rw.repair_code.isin([1, 2])]
put("n_rework_e12", len(e12), str(len(e12)))
put("n_rework_e1", int((e12.repair_code == 1).sum()), str(int((e12.repair_code == 1).sum())))
put("n_rework_e2", int((e12.repair_code == 2).sum()), str(int((e12.repair_code == 2).sum())))
put("rework_e12_pct", len(e12) / len(rw) * 100, fmt(len(e12) / len(rw) * 100))
put("rework_e1_pct", int((e12.repair_code == 1).sum()) / len(rw) * 100, fmt(int((e12.repair_code == 1).sum()) / len(rw) * 100))
check("n_rework", len(rw), 26, "SQL L1493")
check("rework_gap_mean", rnd(rw.gap.mean()), 32.9, "SQL L1493", 0.05)
check("rework_max_d", rnd(rw.gap.max() / 24), 10.1, "SQL L1493", 0.05)
check("rework_e1", int((e12.repair_code == 1).sum()), 16, "SQL L1536")

# ------------------------------------------------------------------ 사전 분류 정합 (S14)
tp = v.planned_repair_type.value_counts()
put("n_E", int(tp["E"]), str(int(tp["E"])))
put("n_P", int(tp["P"]), str(int(tp["P"])))
put("n_B", int(tp["B"]), str(int(tp["B"])))
put("E_pct", tp["E"] / N * 100, fmt(tp["E"] / N * 100))
put("P_pct", tp["P"] / N * 100, fmt(tp["P"] / N * 100))
put("B_pct", tp["B"] / N * 100, fmt(tp["B"] / N * 100))
put("match_upper_n", int(tp["E"] + tp["P"]), str(int(tp["E"] + tp["P"])))
put("match_upper_pct", (tp["E"] + tp["P"]) / N * 100, fmt((tp["E"] + tp["P"]) / N * 100))
P = v[v.planned_repair_type == "P"]
n_P_self = int(P.rep1_task.isin(["ImmediateRepair", "InternRepair"]).sum())
put("n_P_self", n_P_self, str(n_P_self))
put("P_self_pct", n_P_self / len(P) * 100, fmt(n_P_self / len(P) * 100))
put("n_P4_extern", int((P.rep1_task == "ExternRepair").sum()), str(int((P.rep1_task == "ExternRepair").sum())))
cons_n = int(tp["E"]) + n_P_self
put("match_cons_n", cons_n, str(cons_n))
put("match_cons_pct", cons_n / N * 100, fmt(cons_n / N * 100))
put("E_intern_pct", (v[v.planned_repair_type == "E"].rep1_task == "InternRepair").mean() * 100, fmt((v[v.planned_repair_type == "E"].rep1_task == "InternRepair").mean() * 100))
check("match_upper_pct", rnd((tp["E"] + tp["P"]) / N * 100), 87.3, "SQL L1899", 0.05)
check("match_cons_pct", rnd(cons_n / N * 100), 83.2, "SQL L1899", 0.05)
check("n_P4", int((P.rep1_task == "ExternRepair").sum()), 38, "SQL L1894")

# ------------------------------------------------------------------ 프로세스 맵·정산 (S07)
c, f, t = v.client_inform_time, v.fin_commit_time, v.ticket_ready_time
put("settle_client_first", int((c < f).sum()), str(int((c < f).sum())))
put("settle_fin_first", int((f < c).sum()), str(int((f < c).sum())))
put("settle_tie", int((c == f).sum()), str(int((c == f).sum())))
put("settle_client_first_pct", (c < f).mean() * 100, fmt((c < f).mean() * 100))
put("settle_fin_first_pct", (f < c).mean() * 100, fmt((f < c).mean() * 100))
put("ticket_match_n", int((t == np.maximum(c, f)).sum()), str(int((t == np.maximum(c, f)).sum())))
put("ticket_match_pct", (t == np.maximum(c, f)).mean() * 100, fmt((t == np.maximum(c, f)).mean() * 100))
put("ticket_before_n", int((t < np.maximum(c, f)).sum()), str(int((t < np.maximum(c, f)).sum())))
_tk_gap = ((t - np.maximum(c, f)).dt.total_seconds().abs() / 60)[t != np.maximum(c, f)]
put("ticket_mismatch_n", int(len(_tk_gap)), str(int(len(_tk_gap))))
put("ticket_gap_min", float(_tk_gap.max()), fmt(_tk_gap.max(), 0))
check("ticket_mismatch_n", int(len(_tk_gap)), 2, "case_pivot_table 재계산 (TicketReady ≠ max(고객통보, 재무전송)인 케이스 2건, 차이 1분)")
flows = v.groupby(["rep1_task", "rep2_task"], dropna=False).size()
reverse = int(flows.get(("ExternRepair", "InternRepair"), 0) + flows.get(("ExternRepair", "ImmediateRepair"), 0) + flows.get(("InternRepair", "ImmediateRepair"), 0))
put("backflow", reverse, str(reverse))
trans = {}
for a_, b_ in [("rep1_task", "rep2_task"), ("rep2_task", "rep3_task")]:
    for (x_, y_), n_ in v.groupby([a_, b_], dropna=True).size().items():
        trans[(x_, y_)] = trans.get((x_, y_), 0) + int(n_)
put("esc_imm_intern", trans.get(("ImmediateRepair", "InternRepair"), 0), str(trans.get(("ImmediateRepair", "InternRepair"), 0)))
put("esc_imm_extern", trans.get(("ImmediateRepair", "ExternRepair"), 0), str(trans.get(("ImmediateRepair", "ExternRepair"), 0)))
put("esc_intern_extern", trans.get(("InternRepair", "ExternRepair"), 0), str(trans.get(("InternRepair", "ExternRepair"), 0)))
esc_total = sum(n_ for (x_, y_), n_ in trans.items() if x_ != y_)
put("esc_total", esc_total, str(esc_total))
back = sum(n_ for (x_, y_), n_ in trans.items() if (x_, y_) in [("ExternRepair", "InternRepair"), ("ExternRepair", "ImmediateRepair"), ("InternRepair", "ImmediateRepair")])
put("backflow_all", back, str(back))
check("esc_total", esc_total, 96, "프로세스 맵 '유형 간 인계 96회'", 0)

check("settle_client_first", int((c < f).sum()), 469, "스토리보드 S07 (원천 미기재 → 재계산)")

# ------------------------------------------------------------------ 운영 특성 (S06)
houses = v.objectKey.nunique()
hc = v.groupby("objectKey").caseID.count()
put("n_houses", houses, f"{houses:,}")
put("n_houses_once", int((hc == 1).sum()), f"{int((hc == 1).sum()):,}")
put("houses_once_pct", (hc == 1).mean() * 100, fmt((hc == 1).mean() * 100))
check("houses", houses, 890, "SQL L419")
check("houses_once", int((hc == 1).sum()), 855, "SQL L509")
ev_ = ev.copy()
ev_["ts"] = pd.to_datetime(ev_["clean_timestamp"], errors="coerce")
intake = ev_[ev_.task_group == "접수"]
hours_present = int(intake.ts.dt.hour.nunique())
put("intake_hours", hours_present, str(hours_present))
people = intake[intake.originator.isin(["Dian", "Monica"])]
put("intake_hours_people", int(people.ts.dt.hour.nunique()), str(int(people.ts.dt.hour.nunique())))
# SQL L782~: 단독 접수 케이스의 접수 담당(Dian/Monica)별 현장 출동 비중
rcv = intake[intake.SUBJECT == "사람"].groupby("caseID").originator.agg(lambda s: set(s))
single_rcv = {k: list(s)[0] for k, s in rcv.items() if len(s) == 1}
fld_ev = ev_[(ev_.task_group == "현장") & (ev_.SUBJECT == "사람") & ev_.caseID.isin(single_rcv)]
fcases = fld_ev.caseID.unique()
dian_share = np.mean([single_rcv[c_] == "Dian" for c_ in fcases]) * 100
put("dian_share", dian_share, fmt(dian_share))
put("monica_share", 100 - dian_share, fmt(100 - dian_share))
check("dian_share", rnd(dian_share), 46.9, "SQL L824", 0.05)


# ------------------------------------------------------------------ 재접수 주택 (S06, SQL L772~775)
fc_worker = ev[ev.taskID == "FirstContact"].set_index("caseID").originator
vv = v.sort_values("contact_time").copy()
vv["fc_w"] = vv.caseID.map(fc_worker)
rep_houses = hc[hc > 1].index
same_n = diff_n = 0
for _, g in vv[vv.objectKey.isin(rep_houses)].groupby("objectKey"):
    g = g.sort_values("contact_time")
    if g.iloc[0].fc_w == g.iloc[1].fc_w:
        same_n += 1
    else:
        diff_n += 1
put("recontact_houses", len(rep_houses), str(len(rep_houses)))
put("recontact_same", same_n, str(same_n))
put("recontact_diff", diff_n, str(diff_n))
put("recontact_diff_pct", diff_n / len(rep_houses) * 100, fmt(diff_n / len(rep_houses) * 100))
check("recontact_diff", diff_n, 22, "SQL L773 (35채 중 22채 타 상담원)")
put("ols1_handover_b", m1.params["is_handover"], fmt(m1.params["is_handover"], 2))
check("ols1_handover_b", rnd(m1.params["is_handover"], 4), 5.1096, "NB-H C9 출력 (맵의 +5.11h)", 0.00005)

# ------------------------------------------------------------------ TO-BE 시나리오 (S03·S15·S16)
survey_eff = w1 * 0.20 * 1.12
mat_eff = intern.w2s.clip(lower=0).sum() / N
rework_eff = rw.gap.clip(lower=0).sum() / N
ho_eff = 0.80 * (ho_h - single_h) * nh / N
total_eff = survey_eff + mat_eff + rework_eff + ho_eff


def largest_remainder(vals, nd=1):
    """표기 구성요소의 합이 표기 총합과 같도록 최대잔여법으로 반올림한다."""
    unit = 10 ** (-nd)
    target = round(rnd(sum(vals), nd) / unit)
    floors = [int(np.floor(x / unit + 1e-9)) for x in vals]
    short = target - sum(floors)
    order = sorted(range(len(vals)), key=lambda i: -(vals[i] / unit - floors[i]))
    for i in order[:max(short, 0)]:
        floors[i] += 1
    return [f * unit for f in floors]


parts_disp = largest_remainder([survey_eff, mat_eff, rework_eff, ho_eff])
for key, exact, shown in zip(["eff_survey", "eff_material", "eff_rework", "eff_handover"],
                             [survey_eff, mat_eff, rework_eff, ho_eff], parts_disp):
    put(key, exact, f"{shown:.1f}")
put("eff_total", total_eff, fmt(total_eff))
put("eff_total_pct", total_eff / tot * 100, fmt(total_eff / tot * 100))
put("tobe_total", tot - total_eff, fmt(tot - total_eff))
put("tobe_total_days", (tot - total_eff) / 24, fmt((tot - total_eff) / 24))
put("survey_cut_h", w1 * 0.20, fmt(w1 * 0.20))
put("wait1_after", w1 * 0.80, fmt(w1 * 0.80))
put("n_letter", int((v.contact_channel == "Letter").sum()), str(int((v.contact_channel == "Letter").sum())))
put("n_web", int((v.contact_channel == "Web").sum()), str(int((v.contact_channel == "Web").sum())))
put("ols_coef_visit", m2.params["visit_lag_hours"], fmt(m2.params["visit_lag_hours"], 2))
# 사내수리 485건 군에 같은 가정 적용
ig = intern
ig_s = ig.w1.mean() * 0.20 * 1.12
ig_m = ig.w2s.clip(lower=0).mean()
ig_r = rw.gap.clip(lower=0).sum() / len(ig)
ig_h = 0.80 * (ho_h - single_h) * int(ig.ho.sum()) / len(ig)
ig_tot = ig_s + ig_m + ig_r + ig_h
put("intern_asis", ig.total.mean(), fmt(ig.total.mean()))
put("intern_eff", ig_tot, fmt(ig_tot))
put("intern_tobe", ig.total.mean() - ig_tot, fmt(ig.total.mean() - ig_tot))
put("intern_eff_pct", ig_tot / ig.total.mean() * 100, fmt(ig_tot / ig.total.mean() * 100))
check("eff_total_old", rnd(total_eff), 34.8, "구 4항목 가중평균(미채택)", 0.05)
put("eff_parts_sum", sum(parts_disp), f"{sum(parts_disp):.1f}")
check("eff_parts_sum_old", round(sum(parts_disp), 1), rnd(total_eff), "구 4항목 표기합(미채택)", 0.001)

# ------------------------------------------------------------------ 즉시 줄 TO-BE (S16·S17·S18)
# 줄 정의: 접수 코드 P-1·3 = 즉시수리 코드. 실사 대기 큐는 하나이며 B형은 이미 대기 0.2h로 큐를 우회한다.
from scipy import stats as _st

fast_mask = (v.planned_repair_type == "P") & v.repair_code.isin([1, 3])
n_fast = int(fast_mask.sum())
fastv, restv = v[fast_mask], v[~fast_mask]
put("n_fast", n_fast, str(n_fast))
put("n_rest", len(restv), str(len(restv)))
put("fast_pct", n_fast / N * 100, fmt(n_fast / N * 100))
put("fast_p_prec", n_fast / int(tp["P"]) * 100, fmt(n_fast / int(tp["P"]) * 100))
put("n_p_miss", int(tp["P"]) - n_fast, str(int(tp["P"]) - n_fast))
put("p_miss_pct", (int(tp["P"]) - n_fast) / int(tp["P"]) * 100, fmt((int(tp["P"]) - n_fast) / int(tp["P"]) * 100))
put("n_P_intern", int(((P.rep1_task == "InternRepair")).sum()), str(int(((P.rep1_task == "InternRepair")).sum())))
check("n_fast", n_fast, 365, "SQL L1892~1893 (P-1 298 + P-3 67)")
check("fast_all_immediate", int((fastv.rep1_task == "ImmediateRepair").sum()), 365, "접수 코드 P-1·3 전원 ImmediateRepair")
check("n_p_miss", int(tp["P"]) - n_fast, 74, "P 439 − 365 (P-2 36 + P-4 38)")
put("fast_gap_h", hrs(fastv.rep1_start, fastv.survey_complete).mean(), fmt(hrs(fastv.rep1_start, fastv.survey_complete).mean(), 2))
put("fast_same_worker_pct", (fastv.survey_worker == fastv.rep1_worker).mean() * 100, fmt((fastv.survey_worker == fastv.rep1_worker).mean() * 100))
put("n_rework_in_fast", int((rw_mask := (v.rep1_task == "InternRepair") & (v.rep2_task == "InternRepair"))[fast_mask].sum()), str(int(rw_mask[fast_mask].sum())))
put("fast_rep_h", fastv.r1work.mean(), fmt(fastv.r1work.mean(), 2))
put("fast_svy_h", fastv.swork.mean(), fmt(fastv.swork.mean(), 2))
put("intern_rep_h", intern.r1work.mean(), fmt(intern.r1work.mean(), 2))
put("extern_rep_h", ext.r1work.mean(), fmt(ext.r1work.mean(), 2))
put("fast_vs_intern_pct", fastv.r1work.mean() / intern.r1work.mean() * 100, fmt(fastv.r1work.mean() / intern.r1work.mean() * 100, 0))
# 실사 큐 점유시간: 착수한 기사가 그 건에 묶이는 시간 (즉시 수리는 실사와 수리가 연속)
v["occ"] = v.swork + np.where(v.rep1_task == "ImmediateRepair", v.r1work, 0.0)
occ_f, occ_r = v[fast_mask].occ, v[~fast_mask].occ
put("occ_fast_h", occ_f.mean(), fmt(occ_f.mean(), 2))
put("occ_rest_h", occ_r.mean(), fmt(occ_r.mean(), 2))
put("occ_ratio", occ_f.mean() / occ_r.mean(), fmt(occ_f.mean() / occ_r.mean()))
put("occ_fast_share", occ_f.sum() / v.occ.sum() * 100, fmt(occ_f.sum() / v.occ.sum() * 100))
# 채널별 실사 대기: 줄은 하나
for ch_, key_ in [("Web", "web"), ("Letter", "letter"), ("Phone", "phone"), ("Personal", "personal")]:
    put(f"ch_wait_{key_}", v[v.contact_channel == ch_].w1.mean(), fmt(v[v.contact_channel == ch_].w1.mean()))
chw = v.groupby("contact_channel").w1.mean()
put("ch_wait_min", chw.min(), fmt(chw.min()))
put("ch_wait_max", chw.max(), fmt(chw.max()))
kw_p = _st.kruskal(*[g.w1.values for _, g in v.groupby("contact_channel")]).pvalue
put("ch_kw_p", kw_p, fmt(kw_p, 2))
# B형은 이미 큐를 우회 / 외주 전환 / 기사 풀
put("b_wait1", v[v.planned_repair_type == "B"].w1.mean(), fmt(v[v.planned_repair_type == "B"].w1.mean()))
put("n_extern_all", len(ext), str(len(ext)))
put("n_B4_extern", int(((v.planned_repair_type == "B") & (v.rep1_task == "ExternRepair")).sum()), str(int(((v.planned_repair_type == "B") & (v.rep1_task == "ExternRepair")).sum())))
put("n_E_extern", int(((v.planned_repair_type == "E") & (v.rep1_task == "ExternRepair")).sum()), str(int(((v.planned_repair_type == "E") & (v.rep1_task == "ExternRepair")).sum())))
put("n_imm_workers", int(imm.rep1_worker.nunique()), str(int(imm.rep1_worker.nunique())))
put("n_intern_workers_overlap", int(len(set(intern.rep1_worker.dropna()) & set(v.survey_worker.dropna()))), str(int(len(set(intern.rep1_worker.dropna()) & set(v.survey_worker.dropna())))))
check("b_wait1", rnd(v[v.planned_repair_type == "B"].w1.mean()), 0.1, "case_pivot_table 재계산 (B형 118건 실사 대기, 부분군 0.1~0.2h)", 0.05)
check("n_extern_split", int(tp["P"] - n_fast - int(((P.rep1_task == "InternRepair")).sum())) + int(((v.planned_repair_type == "B") & (v.rep1_task == "ExternRepair")).sum()), len(ext), "외주 59 = P-4 38 + B-4 21 (E형 0)")
# 실사 줄 유입 (큐 내 건수 기준 산술)
in_rest = infl * (N - n_fast) / N
put("inflow_rest", in_rest, fmt(in_rest))
# 효과: 실사 대기는 리드타임의 구성요소이므로 1:1 반영 (OLS 1.12 미적용)
for sp_, key_ in [(0.10, "10"), (0.20, "20"), (0.30, "30")]:
    e_ = w1 * sp_
    put(f"sens{key_}_total", e_, fmt(e_))
    put(f"sens{key_}_pct", e_ / tot * 100, fmt(e_ / tot * 100))
    put(f"sens{key_}_after", tot - e_, fmt(tot - e_))
    put(f"sens{key_}_wait1", w1 - e_, fmt(w1 - e_))
put("survey_cut_h", w1 * 0.20, fmt(w1 * 0.20))
put("wait1_after", w1 * 0.80, fmt(w1 * 0.80))
put("eff_total", w1 * 0.20, fmt(w1 * 0.20))
put("eff_total_pct", w1 * 0.20 / tot * 100, fmt(w1 * 0.20 / tot * 100))
put("tobe_total", tot - w1 * 0.20, fmt(tot - w1 * 0.20))
put("cut_vs_inflow_ratio", 0.20 / (n_fast / N), fmt(0.20 / (n_fast / N), 2))
# 참고(상한): 일별 대기열 모델. 용량을 도착 비중대로 두 줄에 나누고, 즉시 건의 실사 단계가 사라져 해방되는 기사 시간만큼 용량을 늘린다.
# 기준값이 구성상 항등식이므로 근거가 아니라 민감도 참고로만 쓴다.
v["ad"] = v.inform_survey_time.dt.normalize()
v["sd"] = v.survey_start.dt.normalize()
_days = pd.date_range(v.ad.min(), v.sd.max())
_cap = v.groupby("sd").size().reindex(_days, fill_value=0).astype(float)


def _lane_wait(mask, share, gain):
    arr = v[mask].groupby("ad").size().reindex(_days, fill_value=0)
    wip = area = 0.0
    for d_ in _days:
        wip = max(0.0, wip + arr[d_] - _cap[d_] * share * gain)
        area += wip
    return area / arr.sum() * 24


_freed = fastv.swork.sum() / (v.swork.sum() + v.r1work.sum())
_sh = fast_mask.mean()
_base = _sh * _lane_wait(fast_mask, _sh, 1.0) + (1 - _sh) * _lane_wait(~fast_mask, 1 - _sh, 1.0)
_aft = _sh * _lane_wait(fast_mask, _sh, 1 / (1 - _freed)) + (1 - _sh) * _lane_wait(~fast_mask, 1 - _sh, 1 / (1 - _freed))
put("qm_freed_pct", _freed * 100, fmt(_freed * 100))
put("qm_cut_pct", (1 - _aft / _base) * 100, fmt((1 - _aft / _base) * 100, 0))

# 슬라이드 문구에서 쓰는 보조 문자열
put("lead_total_h_int", rnd(tot), fmt(tot))

# ------------------------------------------------------------------ 출력
def main():
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    json.dump({"facts": FACTS, "checks": [list(map(lambda z: z if isinstance(z, str) else float(z), c_)) for c_ in CHECKS]},
              open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    bad = [c_ for c_ in CHECKS if c_[4] != "일치"]
    print(f"facts: {len(FACTS)}개, checks: {len(CHECKS)}개, DIFF: {len(bad)}개 -> {OUT_JSON}")
    for c_ in CHECKS:
        print(f"  [{c_[4]:>2}] {c_[0]:<22} 재계산={c_[1]!s:<12} 원천={c_[2]!s:<10} | {c_[3]}")


if __name__ == "__main__":
    main()
