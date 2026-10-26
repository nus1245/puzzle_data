"""17장 PPTX 빌드.  python -X utf8 scripts/deck/build_deck.py  (프로젝트 루트, -I 없이)

선행: python -X utf8 scripts/deck/facts.py  → facts.json
      python -X utf8 scripts/deck/charts_fix.py → outputs/figures/deck/*.png
"""
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lxml import etree                      # noqa: E402

import slides_a as A                        # noqa: E402
import slides_b as B                        # noqa: E402
from kit import *                           # noqa: E402,F401,F403

OUT = os.path.join(ROOT, "outputs", "pptx", "puzzledata_repair_report.pptx")
SECTIONS = [("Part 00 · 인트로", [1, 2, 3]), ("Part 01 · 데이터 진단", [4, 5, 6]), ("Part 02 · 병목 규명", [7, 8, 9, 10, 11, 12, 13, 14, 15]),
            ("Part 03 · 개선 전략", [16, 17, 18]), ("Part 04 · Q&A", [19])]

# 숫자 검사 예외: 출처가 노트북/SQL 출력이거나 구조적 표기인 값 (슬라이드: [토큰])
ALLOW = {
    4: ["0.1"],                 # 진공 구간 0.1~86.0% (EDA-01 기준선)
    5: ["100", "1970"],                 # 시작·완료 담당자 일치율 100% (NB-A C19)
    6: ["23", "100", "1970"],           # 0~23시 (SQL L1141), 100% 정상 산출
    9: ["15.0", "15"],          # 15분 경계
    11: ["0.001"],
    14: ["1.12", "0.001"],      # 계수 1.12(facts 1.12), p < 0.001
    16: ["10", "100"],
    17: ["20", "80"],           # 효과율 가정(20%, 80%)
    18: ["20", "80", "485", "30.5", "100"],
}


def add_sections(prs, sections):
    P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
    pres = prs.part._element
    ids = [e.get("id") for e in pres.find(qn("p:sldIdLst"))]
    ext_lst = pres.find(qn("p:extLst"))
    if ext_lst is None:
        ext_lst = etree.SubElement(pres, qn("p:extLst"))
    ext = etree.SubElement(ext_lst, qn("p:ext"))
    ext.set("uri", "{521415D9-36F7-43E2-AB2F-B90AF26B5E84}")
    lst = etree.SubElement(ext, "{%s}sectionLst" % P14, nsmap={"p14": P14})
    for name, nos in sections:
        sec = etree.SubElement(lst, "{%s}section" % P14)
        sec.set("name", name)
        sec.set("id", "{" + str(uuid.uuid4()).upper() + "}")
        sl = etree.SubElement(sec, "{%s}sldIdLst" % P14)
        for n in nos:
            etree.SubElement(sl, "{%s}sldId" % P14).set("id", ids[n - 1])


def main():
    facts = Facts()
    doc = Doc(facts)
    builders = [A.s01, A.s02, A.s03, A.s04, A.s05, A.s06, A.s07, A.s08, A.s09, A.s10r, A.s11r, B.s10, B.s11, B.s12, B.s13, B.s14, B.s15, B.s16, B.s17]
    problems = []
    for fn in builders:
        try:
            sl = fn(doc, facts)
            sl.finish()
        except LayoutError as e:
            problems.append(str(e))
            continue
        for tok, ctx in check_numbers(sl, facts, ALLOW.get(sl.no, [])):
            problems.append(f"[S{sl.no}] 숫자 리터럴 '{tok}' 가 facts 에 없음: {ctx}")
    if problems:
        print(f"빌드 실패: {len(problems)}건")
        for p_ in problems:
            print("  -", p_)
        sys.exit(1)
    # 목차 링크
    for shape, target in doc.links:
        shape.click_action.target_slide = doc.prs.slides[target - 1] if target - 1 < len(doc.prs.slides._sldIdLst) else None
    add_sections(doc.prs, SECTIONS)
    cp = doc.prs.core_properties
    cp.title = "공공임대주택 수리 프로세스 진단 및 운영 최적화 방안 — 퍼즐데이터 채용 과제"
    cp.author = "조승훈"
    cp.last_modified_by = "조승훈"
    cp.subject = "데이터 분석가(신입) 지원 · 프로세스 마이닝 기반 수리 프로세스 분석"
    cp.keywords = "Process Mining, Lead Time, Bottleneck, OLS, TO-BE"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc.prs.save(OUT)
    json.dump({str(k): sorted(v) for k, v in facts.log.items()}, open(os.path.join(ROOT, "scripts", "deck", "facts_usage.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"저장: {OUT} · 슬라이드 {len(doc.prs.slides._sldIdLst)}장 · 사용 facts {len(facts.used)}개")


if __name__ == "__main__":
    main()
