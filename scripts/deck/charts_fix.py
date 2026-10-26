"""원장에서 정정이 확정된 차트 3종을 '형태 유지' 방식으로 재렌더한다.

hypothesis_testing_and_visualization.ipynb 의 해당 셀 코드를 그대로 실행하되,
하드코딩/CSV 입력값만 case_pivot_table.csv 재계산값(facts.json)으로 치환한다.
출력: outputs/figures/deck/ (사용자의 원본 PNG·노트북은 덮어쓰지 않는다)

  slide08_macro_leadtime_breakdown.png  : 접수 행을 정의 B(접수 전체 대기)로 정정 → 행 합 = E2E 행
  slide09_reception_bottleneck_3panel.png: '15분 이내'를 ≤15분으로 통일(경계 15.0분 2건 오분류 제거) → 막대 합 100%
  slide10_field_donut_breakdown.png     : 쐐기 라벨 78.1% → 78.2% (범례·SQL과 통일)
"""
import io
import json
import os
import re
import sys
import contextlib

os.environ["MPLBACKEND"] = "Agg"
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
OUT = os.path.join("outputs", "figures", "deck")
os.makedirs(OUT, exist_ok=True)

F = json.load(open(os.path.join("scripts", "deck", "facts.json"), encoding="utf-8"))["facts"]
nb = json.load(open("hypothesis_testing_and_visualization.ipynb", encoding="utf-8"))["cells"]


def src(i):
    return "".join(nb[i]["source"])


PRE = src(1).split("# 1. 케이스 피벗")[0]      # import + 폰트 설정 (Malgun Gothic)


def run(code, ns):
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        exec(compile(code, "chart", "exec"), ns)
    return buf.getvalue()


def sub(code, pattern, repl, count=1):
    new, n = re.subn(pattern, lambda m: repl, code, count=count, flags=re.S)
    assert n == count, f"패치 실패: {pattern[:40]}"
    return new


# ------------------------------------------------------------------ 1) slide08
fs = lambda k: float(F[k]["s"])
work = [fs("work_B_pct"), 100.0, fs("field_work_pct"), 0.0]               # E2E / 정산 / 현장 / 접수(정의 B: 전체 대기)
wait = [fs("wait_B_pct"), 0.0, fs("field_wait_pct"), 100.0]
wait_h = [fs("wait_B"), 0.0, fs("field_wait"), fs("rec_total")]
tot_h = [fs("lead_total"), fs("stl_total"), fs("field_total"), fs("rec_total")]
c = src(3)
c = sub(c, r"work_pct = \[[^\]]*\]", f"work_pct = {work}")
c = sub(c, r"wait_pct = \[[^\]]*\]", f"wait_pct = {wait}")
c = sub(c, r"wait_hours = \[[^\]]*\]", f"wait_hours = {wait_h}")
c = sub(c, r"hours_total = \[[^\]]*\]", f"hours_total = {tot_h}")
c = c.replace("outputs/figures/slide08_macro_leadtime_breakdown.png", f"{OUT}/slide08_macro_leadtime_breakdown.png".replace("\\", "/"))
ns = {}
run(PRE + "\n" + c, ns)
print("slide08 ->", work, wait, wait_h, tot_h)

# ------------------------------------------------------------------ 2) slide09
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
    "duration_hours": v.m / 60.0})
df_cohort = pd.DataFrame({
    "contact_channel": v.contact_channel,
    "arrange_duration_minutes": v.m,
    "cohort_group": np.where(v.m <= 15, "15분 이내 (Fast Cohort)", np.where(v.m > 60, "60분 초과 (Slow Cohort)", "15~60분 (Mid Cohort)"))})
c = src(5)
c = sub(c, r"df_leadtime = pd\.read_csv\([^\n]*\)", "pass")
c = sub(c, r"df_cohort = pd\.read_csv\([^\n]*\)", "pass")
c = c.replace("outputs/figures/slide09_reception_bottleneck_3panel.png", f"{OUT}/slide09_reception_bottleneck_3panel.png".replace("\\", "/"))
ns = {"df_leadtime": df_leadtime, "df_cohort": df_cohort}
run(PRE + "\n" + c, ns)
print("slide09 -> mid cohort:", int((df_cohort.cohort_group.str.contains("Mid")).sum()))

# ------------------------------------------------------------------ 3) donut
c = src(11)
pct = [F["wait1_pct"]["s"], F["wait2_res_pct"]["s"], F["rep_work_pct"]["s"], ""]
helper = ("_pl = %r\n_ctr = {'i': -1}\n"
          "def _autopct(p):\n    _ctr['i'] += 1\n    return (_pl[_ctr['i']] + '%%') if _pl[_ctr['i']] else ''\n") % (pct,)
c = sub(c, r"autopct=lambda p: [^\n]*,", "autopct=_autopct,")
c = c.replace("outputs/figures/slide10_field_donut_breakdown.png", f"{OUT}/slide10_field_donut_breakdown.png".replace("\\", "/"))
# 레이블·중심 문구도 facts 로 통일
c = sub(c, r"labels = \[.*?\n\]", "labels = [\n    '① 실사 방문 대기 (Wait 1: %sh, %s%%)',\n    '② 수리 착수 및 공정 대기 (Wait 2: %sh, %s%%)',\n    '③ 실제 본수리 실작업 (Repair Work: %sh, %s%%)',\n    '④ 실사 점검 실작업 (Survey Work: %sh, %s%%)'\n]" % (
    F["wait1"]["s"], F["wait1_pct"]["s"], F["wait2_res"]["s"], F["wait2_res_pct"]["s"],
    F["rep_work"]["s"], F["rep_work_pct"]["s"], F["survey_work"]["s"], F["survey_work_pct"]["s"]))
c = c.replace("(단순 대기 95.3% vs 실작업 4.7%)", f"(단순 대기 {F['field_wait_pct']['s']}% vs 실작업 {F['field_work_pct']['s']}%)")
ns = {}
run(PRE + "\n" + helper + c, ns)
print("donut ->", pct)
