# -*- coding: utf-8 -*-
"""PPT 스토리보드(docs/03_ppt_storyboard.md) 수치를 원천 데이터에서 재계산해 대조한다.

원천: case_pivot_table.csv(케이스 피벗, 927건 코호트), repair_cleaned.csv(이벤트 로그)
실행: python scripts/verify_deck_facts.py   (UTF-8 출력)
각 행: [상태] 항목 | 스토리보드 값 | 재계산 값
  OK   = 반올림 범위 내 일치
  DIFF = 불일치 (덱에서는 재계산 값을 채택)
"""
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

piv = pd.read_csv(os.path.join(BASE, "case_pivot_table.csv"))
ev = pd.read_csv(os.path.join(BASE, "repair_cleaned.csv"))
for col in piv.columns:
    if col.endswith(("_time", "_start", "_complete")):
        piv[col] = pd.to_datetime(piv[col])
m = piv[piv.objectKey.notna()].copy()  # 927건 정상 수리 코호트


def hrs(a, b):
    return (m[b] - m[a]).dt.total_seconds() / 3600.0


ROWS = []


def check(name, claimed, actual, tol=0.051, fmt="{:.1f}"):
    """claimed/actual 이 수치면 tol 이내일 때 OK."""
    ok = abs(claimed - actual) <= tol
    ROWS.append((("OK  " if ok else "DIFF"), name, fmt.format(claimed), fmt.format(actual)))


# ---------------- A. 데이터 프로파일 ----------------
check("전체 이벤트 행", 13262, len(ev), 0, "{:,.0f}")
check("전체 케이스", 1000, ev.caseID.nunique(), 0, "{:,.0f}")
check("정상 수리 코호트", 927, len(m), 0, "{:,.0f}")
check("오접수 격리", 73, 1000 - len(m), 0, "{:,.0f}")
check("고유 주택", 890, m.objectKey.nunique(), 0, "{:,.0f}")
check("케이스당 이벤트 중앙값", 14, piv.total_events.median(), 0, "{:,.0f}")
ch = m.contact_channel.value_counts()
for k, v in (("Phone", 251), ("Web", 241), ("Personal", 228), ("Letter", 207)):
    check(f"채널 {k}", v, ch[k], 0, "{:,.0f}")

# ---------------- B. 거시 리드타임 ----------------
total = hrs("contact_time", "ticket_ready_time")
field = hrs("inform_survey_time", "repair_ready_time")
survey = hrs("survey_start", "survey_complete")
rep_work = sum(hrs(f"rep{i}_start", f"rep{i}_complete").fillna(0) for i in (1, 2, 3))
field_work = survey + rep_work
settle = hrs("repair_ready_time", "ticket_ready_time")
reception = hrs("contact_time", "inform_survey_time")
check("E2E 리드타임(h)", 105.9, total.mean())
check("현장 국면(h)", 98.3, field.mean())
check("현장 비중(%)", 92.8, field.mean() / total.mean() * 100)
check("현장 실작업(h)", 4.6, field_work.mean())
check("현장 대기(h)", 93.7, (field - field_work).mean())
check("현장 대기 비중(%)", 95.3, (field - field_work).mean() / field.mean() * 100)
w1 = hrs("inform_survey_time", "survey_start")
w2 = hrs("survey_complete", "rep1_start")
check("Wait1 실사 대기(h)", 76.8, w1.mean())
check("Wait1 비중(%)", 78.2, w1.mean() / field.mean() * 100)
check("Wait2 수리 착수 대기(h)", 15.9, w2.mean())
check("정산 구간(h)", 5.5, settle.mean())
check("접수 구간(h)", 2.1, reception.mean())
# 90.5% = (총 - 현장 실작업 - 정산) / 총  (정산 5.5h를 시스템 처리 시간으로 간주)
wait_conservative = total.mean() - field_work.mean() - settle.mean()
check("E2E 대기(h) [정산=처리]", 95.8, wait_conservative)
check("E2E 대기 비율(%) [정산=처리]", 90.5, wait_conservative / total.mean() * 100)
check("현장 대기 / E2E 대기(%)", 98.0, (field - field_work).mean() / wait_conservative * 100)
# 엄격 정의: start→complete 구간만 작업
ev_c = ev[ev.caseID.isin(m.caseID)].copy()
ev_c["t"] = pd.to_datetime(ev_c["clean_timestamp"])
ev_c = ev_c.sort_values(["caseID", "t", "seq", "sub_seq"])
work_strict = []
for _, g in ev_c.groupby("caseID", sort=False):
    t, task, et = g.t.values, g.taskID.values, g.eventtype.values
    w = 0.0
    for i in range(len(g) - 1):
        if et[i] == "start" and et[i + 1] == "complete" and task[i] == task[i + 1]:
            w += (t[i + 1] - t[i]) / np.timedelta64(1, "h")
    work_strict.append(w)
check("E2E 대기 비율(%) [엄격: start→complete만 작업]", 94.6, (1 - np.mean(work_strict) / total.mean()) * 100)

# ---------------- C. 현장 병목 동역학 ----------------
day = lambda s: s.dt.normalize()
handoff = day(m.inform_survey_time).value_counts().sort_index()
surv_day = day(m.survey_start).value_counts().sort_index()
idx = handoff.index.union(surv_day.index)
wip = handoff.reindex(idx, fill_value=0).cumsum() - surv_day.reindex(idx, fill_value=0).cumsum()
check("일일 유입(1/2~1/7 현장 이관 평균)", 134.3, handoff["1970-01-02":"1970-01-07"].mean())
check("일일 실사 착수(1/1~1/8 평균)", 68.0, surv_day["1970-01-01":"1970-01-08"].mean())
check("소화율(%)", 50.6, 68.0 / 134.3 * 100)
check("WIP 최초", 20, wip.iloc[0], 0, "{:.0f}")
check("WIP 피크", 403, wip.max(), 0, "{:.0f}")
check("14일 지속 CAPA(건/일)", 63.7, surv_day["1970-01-01":"1970-01-14"].mean())

# ---------------- D. 접수 국면 ----------------
rec_tasks = ["FirstContact", "MakeTicket", "ArrangeSurvey", "InformClientSurvey"]
agents = ["Anne", "Dian", "Monica", "Paul"]
rl = ev[ev.taskID.isin(rec_tasks) & ev.originator.isin(agents)]
ho_cases = set(rl.groupby("caseID").originator.nunique()[lambda x: x > 1].index) & set(m.caseID)
m["is_handover"] = m.caseID.isin(ho_cases).astype(int)
m["receipt_hours"] = reception
check("교차 인계 건수", 123, m.is_handover.sum(), 0, "{:.0f}")
check("단독 처리군 평균(h)", 1.2, m[m.is_handover == 0].receipt_hours.mean())
check("교차 인계군 평균(h)", 7.9, m[m.is_handover == 1].receipt_hours.mean())
check("인계 배수(x)", 6.6, m[m.is_handover == 1].receipt_hours.mean() / m[m.is_handover == 0].receipt_hours.mean())
check("인계군 중앙값(h)", 5.6, m[m.is_handover == 1].receipt_hours.median())
hc = m[m.is_handover == 1].contact_channel.value_counts()
check("인계 Web", 69, hc.get("Web", 0), 0, "{:.0f}")
check("인계 Letter", 54, hc.get("Letter", 0), 0, "{:.0f}")
arrange = hrs("survey_arrange_start", "survey_arrange_complete")
check("일정 조율(ArrangeSurvey) 평균(h) [스토리보드 1.9h]", 1.9, arrange.mean())
check("일정 조율 비중(% of 접수 2.1h) [스토리보드 90.4%]", 90.4, arrange.mean() / reception.mean() * 100)
check("일정 조율 중앙값(분)", 4.0, arrange.median() * 60, 0.3)
check("웹 일정 조율 평균(h)", 4.5, arrange[m.contact_channel == "Web"].mean())
check("우편 일정 조율 평균(h)", 3.6, arrange[m.contact_channel == "Letter"].mean())
m["daily_intake_volume"] = m.groupby(day(m.contact_time)).caseID.transform("count")
check("일별 접수량-소요시간 r", 0.01, np.corrcoef(m.daily_intake_volume, m.receipt_hours)[0, 1], 0.005, "{:.3f}")

# ---------------- E. 사전 분류 정합성 ----------------
ct = pd.crosstab(m.planned_repair_type, m.rep1_task)
check("E형 건수", 370, ct.loc["E"].sum(), 0, "{:.0f}")
check("E형 사내수리", 370, ct.loc["E", "InternRepair"], 0, "{:.0f}")
check("P형 건수", 439, ct.loc["P"].sum(), 0, "{:.0f}")
check("P형 즉시", 365, ct.loc["P", "ImmediateRepair"], 0, "{:.0f}")
check("P형 사내", 36, ct.loc["P", "InternRepair"], 0, "{:.0f}")
check("B형 건수", 118, ct.loc["B"].sum(), 0, "{:.0f}")
check("E+P 비중(%) [낙관 상한]", 87.3, (370 + 439) / 927 * 100)
check("E+P 중 내부 완결(%) [보수]", 83.2, (370 + 365 + 36) / 927 * 100)
check("P형 내부 완결률(%)", 91.3, (365 + 36) / 439 * 100)

# ---------------- F. 리워크 / 수리 착수 대기 ----------------
rw = m[(m.rep1_task == "InternRepair") & (m.rep2_task == "InternRepair")]
gap = (rw.rep2_start - rw.rep1_complete).dt.total_seconds() / 3600
check("리워크 건수", 26, len(rw), 0, "{:.0f}")
check("리워크 평균 추가 대기(h)", 32.9, gap.mean())
check("리워크 최대 대기(h)", 171.6, gap.max())  # 스토리보드의 '171.6h'는 10.1일과 모순
check("리워크 최대 대기(일)", 10.1, gap.max() / 24)
check("E-1 리워크", 16, ((rw.planned_repair_type == "E") & (rw.repair_code == 1)).sum(), 0, "{:.0f}")
check("E-2 리워크", 6, ((rw.planned_repair_type == "E") & (rw.repair_code == 2)).sum(), 0, "{:.0f}")
check("E-1/E-2 비중(%)", 84.6, 22 / 26 * 100)
w2g = w2.groupby(m.rep1_task).mean()
check("사내수리 착수 대기(h)", 30.5, w2g["InternRepair"])
check("즉시수리 착수 대기(h)", 0.0, w2g["ImmediateRepair"])
check("외주수리 착수 대기(h)", 0.0, w2g["ExternRepair"])

# ---------------- G. 회귀 ----------------
m["visit_lag_hours"] = w1
m["is_intern_repair"] = (m.rep1_task == "InternRepair").astype(int)
m["is_async_channel"] = m.contact_channel.isin(["Web", "Letter"]).astype(int)
m["is_escalation"] = m.rep2_task.notna().astype(int)
m["total_hours"] = total
X = sm.add_constant(m[["visit_lag_hours", "is_intern_repair", "is_escalation", "is_async_channel"]])
fit = sm.OLS(m.total_hours, X).fit()
check("E2E OLS R²", 0.878, fit.rsquared, 0.0005, "{:.4f}")
check("E2E OLS F", 1659.4, fit.fvalue)  # 노트북 출력은 1652.8
check("계수 visit_lag", 1.12, fit.params["visit_lag_hours"], 0.005, "{:.3f}")
check("계수 is_intern_repair", 31.75, fit.params["is_intern_repair"], 0.005, "{:.2f}")
check("계수 is_async_channel", 4.89, fit.params["is_async_channel"], 0.005, "{:.2f}")
check("p is_async_channel", 0.030, fit.pvalues["is_async_channel"], 0.0005, "{:.3f}")
vifs = [variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])]
check("E2E OLS VIF 최대", 1.25, max(vifs), 0.005, "{:.2f}")

# ---------------- H. TO-BE 시나리오 ----------------
inflow, capa = 134.3, 68.0
check("시나리오1 일 실사 유입(건/일)", 80.7, inflow * (927 - 370) / 927)
check("시나리오1 적체 누적 속도(건/일)", 12.7, inflow * (927 - 370) / 927 - capa)
check("AS-IS 적체 누적 속도(건/일)", 66.3, inflow - capa)
check("적체 속도 감소율(%)", 80.8, (1 - (inflow * (927 - 370) / 927 - capa) / (inflow - capa)) * 100)
check("실사 대기 20% 단축(h)", 15.4, 76.81 * 0.2)
check("OLS 순단축(h)", 17.2, 76.81 * 0.2 * fit.params["visit_lag_hours"])
check("OLS 순단축 비율(%)", 16.2, 76.81 * 0.2 * 1.12 / 105.9 * 100)
check("실사 생략 회수 공수(h) [735건×40.5분]", 496.1, 735 * 40.5 / 60)
check("실사 평균 소요(분)", 40.5, survey.mean() * 60)
check("목표 감축률(%) [105.9→38.0]", 65.0, (1 - 38.0 / 105.9) * 100)
check("노트북 감축률(%) [105.9→36.0]", 65.1, (1 - 36.0 / 105.9) * 100)

width = max(len(r[1]) for r in ROWS)
print(f"{'상태':<5}{'항목':<{width}}  {'스토리보드':>10}  {'재계산':>10}")
for st, name, c, a in ROWS:
    print(f"{st:<5}{name:<{width}}  {c:>10}  {a:>10}")
n_diff = sum(1 for r in ROWS if r[0] == "DIFF")
print(f"\n총 {len(ROWS)}항목 | OK {len(ROWS) - n_diff} | DIFF {n_diff}")
