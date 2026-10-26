const pptxgen = require("pptxgenjs");
const path = require("path");
const SKILL = "C:/Users/nextb/.claude/skills/synced/987d6139-e616-4cee-8655-caebbe5dfdb9_839f932a-f7e9-41d6-939a-3f1377246a4e/pptx";
const { applyTheme } = require(SKILL + "/scripts/apply_theme.js");

const OUT = process.argv[2];
const MAP_IMG = path.join(__dirname, "process_map_crop.png");

const THEME = {
  name: "PuzzleData Repair",
  headFontFace: "Malgun Gothic",
  bodyFontFace: "Malgun Gothic",
  colors: {
    dk1: "0F172A", lt1: "FFFFFF", dk2: "334155", lt2: "F1F5F9",
    accent1: "EA580C", accent2: "059669", accent3: "DC2626",
    accent4: "2563EB", accent5: "64748B", accent6: "94A3B8",
    hlink: "2563EB", folHlink: "64748B",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "수리 프로세스 진단 보고서 (Slide 01-08)";

const C = pres.SchemeColor;
const K = {
  navy: C.text1, slate: C.text2, white: C.background1, paper: C.background2,
  orange: C.accent1, green: C.accent2, red: C.accent3, blue: C.accent4,
  gray: C.accent5, mist: C.accent6,
};
const X0 = 0.5, W = 12.333;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "COVER",
  background: { color: "0F172A" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 1.85, w: 7.6, h: 2.7, fontSize: 36, bold: true, color: K.white, align: "left", valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.7, y: 4.45, w: 7.6, h: 0.95, fontSize: 18, color: "CBD5E1", align: "left", valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: "FFFFFF" },
  slideNumber: { x: 12.2, y: 7.05, w: 0.63, h: 0.3, fontSize: 10, color: "64748B", align: "right" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.62, w: W, h: 0.95, fontSize: 24, bold: true, color: K.navy, align: "left", valign: "top", margin: 0 }, text: "" } },
  ],
});

// ---------- helpers ----------
function txt(s, text, x, y, w, h, o = {}) {
  s.addText(text, Object.assign({ x, y, w, h, isTextBox: true, margin: 0, valign: "top", fontSize: 14, color: K.navy }, o));
}
function card(s, x, y, w, h, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign({ x, y, w, h, rectRadius: 0.08, fill: { color: K.paper }, line: { type: "none" } }, o));
}
function kicker(s, text) {
  txt(s, text, X0, 0.3, W, 0.28, { fontSize: 12, bold: true, color: K.orange });
}
function source(s, text) {
  txt(s, text, X0, 7.05, 11.4, 0.3, { fontSize: 10, color: K.gray, valign: "middle" });
}
function newSlide(layout, section) {
  return pres.addSlide({ masterName: layout, sectionTitle: section });
}
function pill(s, text, x, y, w, h, fill, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: h / 2, fill: { color: fill }, line: { type: "none" } });
  txt(s, text, x, y, w, h, Object.assign({ align: "center", valign: "middle", fontSize: 12, bold: true, color: K.white }, o));
}

// =====================================================================
// Slide 01. 표지
// =====================================================================
pres.addSection({ title: "Part 00. 인트로" });
{
  const s = newSlide("COVER", "Part 00. 인트로");
  pill(s, "채용 과제 전형 최종 보고서", 0.7, 0.75, 3.3, 0.42, "334155");
  s.addText("프로세스 마이닝 기반\n공공임대주택 수리 프로세스\n진단 및 운영 최적화 방안", { placeholder: "title" });
  s.addText("5대 무손실 전처리, 실사 대기 병목(76.8h) 원인 규명 및\n3대 데이터 기반 TO-BE 전략", { placeholder: "body" });
  txt(s, "퍼즐데이터 수리 프로세스 데이터 분석 과제   |   제출일 2026. 10. 27", 0.7, 6.55, 7.6, 0.35, { fontSize: 14, color: "94A3B8" });

  const stats = [
    ["13,262행", "이벤트 로그 · 1,000 케이스", "#ProcessMining", K.white],
    ["90.5%", "리드타임 중 공정 간 단순 대기", "#LeadTime_90.5%_Wait", K.orange],
    ["65%", "TO-BE 리드타임 단축 목표", "#TO-BE_ROI_65%", "34D399"],
  ];
  stats.forEach(([big, label, tag, col], i) => {
    const y = 1.55 + i * 1.8;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.0, y, w: 3.83, h: 1.6, rectRadius: 0.1, fill: { color: "1E293B" }, line: { type: "none" } });
    txt(s, big, 9.25, y + 0.15, 3.4, 0.7, { fontSize: 36, bold: true, color: col, valign: "middle" });
    txt(s, label, 9.25, y + 0.87, 3.4, 0.3, { fontSize: 13, color: "E2E8F0" });
    txt(s, tag, 9.25, y + 1.2, 3.4, 0.28, { fontSize: 12, color: "94A3B8" });
  });
  s.addNotes(
    "안녕하십니까, 퍼즐데이터 수리 프로세스 데이터 분석 결과 발표를 맡은 지원자입니다. 본 보고서는 네덜란드 공공임대주택 1,000건의 수리 로그를 바탕으로, 단순 통계를 넘어 프로세스 마이닝 관점에서 대기시간 약 90%의 구조적 원인을 밝히고 실질적 개선안을 제시합니다.\n\n" +
    "[수치 기준 주석] 리드타임(105.9h) 중 대기 95.8h = 90.5%가 E2E 기준입니다. 94.4%는 현장 국면(98.3h) 내 Wait1+Wait2 비중(analysis.sql 2-3절)으로 분모가 달라 표지에는 쓰지 않았습니다."
  );
}

// =====================================================================
// Slide 02. 목차
// =====================================================================
{
  const s = newSlide("CONTENT", "Part 00. 인트로");
  kicker(s, "Agenda");
  s.addText("원천 데이터 전처리부터 TO-BE 전략까지, 4개 파트로 보고합니다", { placeholder: "title" });
  const parts = [
    ["01", "데이터 진단\n및 전처리", "질문 1", ["로그 프로파일링", "5대 인과 복원", "927건 클린 코호트"]],
    ["02", "프로세스 마이닝\n심층 분석", "질문 2", ["E2E 프로세스 흐름", "3대 대기 병목", "재작업 루프", "영향 요인 회귀"]],
    ["03", "프로세스\n최적화 방안", "질문 3", ["소통 통제", "대기 단축", "정량적 ROI"]],
    ["04", "엔지니어링\n신뢰성 보증", "검증", ["파이프라인 검증", "Q&A"]],
  ];
  const cw = 2.9, gap = (W - 4 * cw) / 3;
  parts.forEach(([no, title, tag, items], i) => {
    const x = X0 + i * (cw + gap), y = 1.85;
    card(s, x, y, cw, 4.5);
    txt(s, no, x + 0.3, y + 0.3, cw - 0.6, 0.75, { fontSize: 44, bold: true, color: i === 1 ? K.orange : K.navy });
    txt(s, title, x + 0.3, y + 1.15, cw - 0.6, 0.85, { fontSize: 18, bold: true });
    pill(s, tag, x + 0.3, y + 2.1, 1.0, 0.32, K.slate, { fontSize: 11 });
    s.addText(
      items.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < items.length - 1 } })),
      { x: x + 0.3, y: y + 2.65, w: cw - 0.55, h: 2.0, isTextBox: true, margin: 0, valign: "top", fontSize: 14, color: K.slate, paraSpaceAfter: 6 }
    );
  });
  s.addNotes("오늘 발표는 4개 파트로 진행됩니다. 질문 1의 데이터 무손실 전처리를 거쳐, 질문 2의 프로세스 병목과 원인을 규명하고, 질문 3에서 실질적 개선안과 정량적 ROI를 제시하며 마무리하겠습니다.");
}

// =====================================================================
// Slide 03. Executive Summary
// =====================================================================
{
  const s = newSlide("CONTENT", "Part 00. 인트로");
  kicker(s, "Executive Summary");
  s.addText("현장의 '대기시간'을 줄이고, 이해관계자 간의 '소통'을 통제하면\n프로세스 리드타임을 획기적으로 개선할 수 있다", { placeholder: "title" });
  const cards = [
    ["1", "원천 진단", "13,262행", "100% 무손실 복원", "2원화 전처리로 단 한 행도 삭제 없이 비정상 결측을 복원했다."],
    ["2", "병목 가설", "공정 간 대기", "+ 비동기 소통 지연", "리드타임 지연의 본질은 작업자 속도가 아니라 공정 사이의 단순 대기와 접수 단계의 비동기 소통 지연에 있다."],
    ["3", "개선 방향", "소통 통제", "+ 대기 단축", "'Web 자가 예약 기반 소통 통제'와 '패스트트랙 기반 대기시간 단축'을 핵심 레버로 도출한다."],
  ];
  const cw = 3.95, gap = (W - 3 * cw) / 2;
  cards.forEach(([n, label, big, sub, body], i) => {
    const x = X0 + i * (cw + gap), y = 1.95;
    card(s, x, y, cw, 4.4);
    s.addShape(pres.shapes.OVAL, { x: x + 0.35, y: y + 0.35, w: 0.55, h: 0.55, fill: { color: i === 0 ? K.navy : i === 1 ? K.orange : K.green }, line: { type: "none" } });
    txt(s, n, x + 0.35, y + 0.35, 0.55, 0.55, { align: "center", valign: "middle", fontSize: 18, bold: true, color: K.white });
    txt(s, label, x + 1.1, y + 0.35, cw - 1.4, 0.55, { fontSize: 18, bold: true, color: K.slate, valign: "middle" });
    txt(s, big, x + 0.35, y + 1.25, cw - 0.7, 0.7, { fontSize: 32, bold: true, color: i === 1 ? K.orange : i === 2 ? K.green : K.navy });
    txt(s, sub, x + 0.35, y + 1.95, cw - 0.7, 0.4, { fontSize: 16, bold: true, color: K.slate });
    txt(s, body, x + 0.35, y + 2.65, cw - 0.7, 1.6, { fontSize: 16, color: K.slate });
  });
  s.addNotes("본 분석을 관통하는 핵심 가설은 명확합니다. 수리가 늦어지는 것은 현장 기사가 느려서가 아니라, 공정 사이의 단순 대기와 접수 단계의 비동기 소통 지연 때문입니다. 이 두 가지를 통제하여 전체 프로세스를 획기적으로 개선하는 여정을 보여드리겠습니다.");
}

// =====================================================================
// Slide 04. 원천 데이터 프로파일링 (Before)
// =====================================================================
pres.addSection({ title: "Part 01. 질문 1 — 데이터 진단 및 전처리" });
{
  const s = newSlide("CONTENT", "Part 01. 질문 1 — 데이터 진단 및 전처리");
  kicker(s, "Part 01 · 질문 1  |  Before Profiling");
  s.addText("정상 결측은 그대로 보존하고,\n시스템 에러 20행(0.15%)만 복원 대상으로 특정했다", { placeholder: "title" });

  card(s, X0, 1.75, 3.9, 5.1);
  [["13,262", "이벤트 행"], ["1,000", "케이스"], ["13", "속성"]].forEach(([big, lab], i) => {
    const y = 2.0 + i * 1.2;
    txt(s, big, X0 + 0.35, y, 3.2, 0.65, { fontSize: 40, bold: true });
    txt(s, lab, X0 + 0.35, y + 0.65, 3.2, 0.32, { fontSize: 14, color: K.slate });
  });
  txt(s, "1건 1행의 정형 데이터가 아니라 세부 작업 단위로 쌓이는 이벤트 로그", X0 + 0.35, 5.7, 3.2, 0.95, { fontSize: 13, color: K.slate });

  const attrs = [
    ["EstimatedRepairTime", 93.0], ["RepairCode", 93.0], ["RepairType", 93.0], ["objectKey", 93.0],
    ["RepairInternally", 93.0], ["contact", 92.5], ["RepairOK", 86.0],
    ["date", 0.098], ["time", 0.098], ["eventtype", 0.038], ["originator", 0.015], ["taskID", 0.015], ["caseID", 0.0],
  ];
  s.addChart(pres.charts.BAR, [{ name: "결측률(%)", labels: attrs.map(a => a[0]), values: attrs.map(a => a[1]) }], {
    x: 4.65, y: 1.7, w: 8.18, h: 3.15, barDir: "bar", catAxisOrientation: "maxMin",
    chartColors: attrs.map(a => (a[1] > 80 ? "94A3B8" : "DC2626")),
    barGapWidthPct: 35,
    showTitle: true, title: "컬럼별 결측률 (%)", titleFontSize: 12, titleColor: "334155", titleFontFace: "+mn-lt",
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.0##"%"', dataLabelFontSize: 10, dataLabelColor: "334155", dataLabelFontFace: "+mn-lt",
    catAxisLabelFontSize: 10, catAxisLabelColor: "334155", catAxisLabelFontFace: "+mn-lt", catAxisLabelFrequency: 1,
    valAxisLabelFontSize: 10, valAxisLabelColor: "64748B", valAxisLabelFontFace: "+mn-lt",
    valAxisMinVal: 0, valAxisMaxVal: 110, valAxisMajorUnit: 20,
    valGridLine: { color: "E2E8F0", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: false,
  });

  const rows = [
    ["정상 결측", "059669", "구조적 Null 86.0~93.0% · 7개 속성(12,335행)", "후속 공정이 없어 비어 있는 값 → 무죄. 임의 대체 없이 100% 보존"],
    ["비정상 결측", "DC2626", "0.015~0.098% · 5개 속성(taskID·originator·eventtype·date·time)", "필수 값의 시스템 에러 → 유죄. 18개 케이스, 단 20행을 복원 대상으로 특정"],
    ["진공 구간", "64748B", "0.1~86.0% 구간에 걸치는 컬럼 0개", "완벽한 양극단 이봉분포 → 정상/비정상 판별의 객관성 입증"],
  ];
  rows.forEach(([lab, col, a, b], i) => {
    const y = 4.98 + i * 0.64;
    card(s, 4.65, y, 8.18, 0.58);
    pill(s, lab, 4.78, y + 0.1, 1.35, 0.38, col, { fontSize: 12 });
    txt(s, [
      { text: a, options: { bold: true, breakLine: true } },
      { text: b, options: { color: K.slate } },
    ], 6.3, y + 0.05, 6.4, 0.5, { fontSize: 11, valign: "middle" });
  });
  source(s, "출처: repair_cleaned.csv 원천 프로파일링 (EDA-01) · 20행 = 5개 속성에 걸친 결측이 몰린 18개 케이스의 행");
  s.addNotes("데이터를 열어보았을 때 가장 먼저 확인한 것은 구조였습니다. 본 데이터는 공정마다 행이 쌓이는 이벤트 로그로, 90% 안팎의 결측치는 후속 수리가 발생하지 않아 생긴 자연스러운 정상 결측입니다. 반면 필수 속성임에도 비어 있는 값은 13,262행 중 단 20행에 불과했습니다. 이 20행만을 정밀 복원 타겟으로 특정했습니다.");
}

// =====================================================================
// Slide 05. 5대 비정상 결측치 복원
// =====================================================================
{
  const s = newSlide("CONTENT", "Part 01. 질문 1 — 데이터 진단 및 전처리");
  kicker(s, "Part 01 · 질문 1  |  CASE 1 ~ 5");
  s.addText("행 삭제와 단순 대체 없이, 업무 인과 근거로 20행을 100% 무손실 복원했다", { placeholder: "title" });
  const cases = [
    ["CASE 1", "taskID", "결측 2건", "contact는 FirstContact에만 기록되는 고유 속성", "FirstContact · InformClientSurvey 확정 복원"],
    ["CASE 2", "originator", "결측 2건", "같은 작업의 start·complete 담당자 100.0% 일치", "짝 이벤트 담당자(Anne, Paul) 승계"],
    ["CASE 3", "eventtype", "결측 5건", "기간 작업은 start→complete 1:1 짝, 마일스톤은 단독", "1:1 페어 3건 + 마일스톤 2건 복원"],
    ["CASE 4", "date", "총 879건|결측 13 + 오기입 866", "1905년 리셋·2020~22년 오기입. 시각이 정상인 859건에 선·후행 순서 구간 제약 적용", "단일 후보 640건 + 앵커 최근접 219건 매핑"],
    ["CASE 5", "time", "총 28건|결측 13 + 더미 15", "완전무결 기준 시 표본 34%로 축소 → 접수 구간 정상 표본 751건(75.1%) 확보, 중앙값 4.0분", "정상 자정 7건 보존 + 앵커 역산 21건"],
  ];
  const colA = X0 + 0.25, colB = X0 + 3.1, colC = X0 + 8.0;
  txt(s, "결측 속성", colA, 1.6, 2.6, 0.25, { fontSize: 11, bold: true, color: K.gray });
  txt(s, "현장 단서", colB, 1.6, 4.4, 0.25, { fontSize: 11, bold: true, color: K.gray });
  txt(s, "복원 판정 (5개 속성 모두 누락 0건)", colC, 1.6, 4.3, 0.25, { fontSize: 11, bold: true, color: K.gray });
  const rh = 0.8, rg = 0.08;
  cases.forEach(([tag, attr, amt, clue, fix], i) => {
    const y = 1.9 + i * (rh + rg);
    card(s, X0, y, W, rh);
    txt(s, [
      { text: tag + "  ", options: { fontSize: 11, bold: true, color: K.orange } },
      { text: attr, options: { fontSize: 16, bold: true, breakLine: true } },
      { text: amt.replace("|", " · "), options: { fontSize: 12, bold: true, color: K.red } },
    ], colA, y, 2.7, rh, { valign: "middle" });
    txt(s, clue, colB, y, 4.4, rh, { fontSize: 12, color: K.slate, valign: "middle" });
    txt(s, "→", colC - 0.45, y, 0.3, rh, { fontSize: 16, bold: true, color: K.gray, valign: "middle", align: "center" });
    txt(s, fix, colC, y, 4.05, rh, { fontSize: 12, bold: true, color: K.green, valign: "middle" });
  });
  const badges = [
    ["데이터 무손실", "임의 삭제 0건 · 13,262행(100.0%) 보존"],
    ["통계적 강건성", "표본 34% 한계 → 정상 표본 751건 활용"],
    ["인과 무결성", "시간 역전 0건 · 927건 클린 코호트 확립"],
  ];
  const bw = 3.95, bg = (W - 3 * bw) / 2;
  badges.forEach(([h, b], i) => {
    const x = X0 + i * (bw + bg);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 6.35, w: bw, h: 0.62, rectRadius: 0.08, fill: { color: K.green }, line: { type: "none" } });
    txt(s, [
      { text: h, options: { bold: true, fontSize: 13, breakLine: true } },
      { text: b, options: { fontSize: 12 } },
    ], x + 0.2, 6.35, bw - 0.4, 0.62, { color: K.white, valign: "middle" });
  });
  source(s, "출처: analysis.ipynb Cell 18·20·51·53·77·81, analysis.sql");
  s.addNotes("복원 시 단 한 행도 버리지 않았습니다. 시작-완료 담당자의 100% 일치성, 태스크 고유 속성을 활용했고, 일시는 표본 34% 축소 한계를 극복하여 확보한 751건 정상 모수의 대표값을 앵커로부터 역산 적용했습니다. 덕분에 시간 역전 0건의 완벽한 데이터셋을 완성했습니다.");
}

// =====================================================================
// Slide 06. 전처리 무결성 검증 (After)
// =====================================================================
{
  const s = newSlide("CONTENT", "Part 01. 질문 1 — 데이터 진단 및 전처리");
  kicker(s, "Part 01 · 질문 1  |  After Profiling");
  s.addText("시간 역전 0건을 입증했고, 오접수 73건을 격리해 927건 클린 코호트를 확립했다", { placeholder: "title" });

  const hdr = (t, fill) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: fill }, fontSize: 13, align: "center", valign: "middle" } });
  const cell = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 13, color: "334155", valign: "middle", align: "center" }, o) });
  const lab = (t) => cell(t, { align: "left", bold: true, color: "0F172A" });
  const good = (t) => cell(t, { bold: true, color: "059669" });
  s.addTable([
    [hdr("검증 항목", "0F172A"), hdr("Before (원천)", "64748B"), hdr("After (정제)", "059669")],
    [lab("총 이벤트 수"), cell("13,262행"), good("13,262행 (100% 보존)")],
    [lab("필수 속성 결측"), cell("20건"), good("0건 (100% 복원)")],
    [lab("일자 연도 오기입"), cell("866건"), good("0건 (1970년 주기 통일)")],
    [lab("시간 역전"), cell("음수 소요시간"), good("0건 (3,711 페어 양수)")],
  ], {
    x: X0, y: 1.8, w: 6.3, colW: [2.2, 1.7, 2.4], rowH: [0.5, 0.85, 0.85, 0.85, 0.95],
    border: { type: "solid", pt: 0.75, color: "E2E8F0" }, fill: { color: "F8FAFC" }, margin: [0.05, 0.1, 0.05, 0.1],
  });
  card(s, X0, 6.0, 6.3, 0.85, { fill: { color: "ECFDF5" } });
  txt(s, "전처리 전 구간 결과: 결측 20건 → 0건, 임의 행 삭제 0건", X0 + 0.25, 6.0, 5.8, 0.85, { fontSize: 14, bold: true, color: K.green, valign: "middle" });

  // right: meta chips
  const rx = 7.15, rw = 5.683;
  const chips = [["1,000", "케이스"], ["890", "고유 주택"], ["13", "속성"], ["14행", "케이스당 중앙값"]];
  const chw = (rw - 3 * 0.15) / 4;
  chips.forEach(([b, l], i) => {
    const x = rx + i * (chw + 0.15);
    card(s, x, 1.8, chw, 1.0);
    txt(s, b, x, 1.9, chw, 0.5, { fontSize: 20, bold: true, align: "center" });
    txt(s, l, x, 2.42, chw, 0.3, { fontSize: 11, color: K.slate, align: "center" });
  });
  // donut
  s.addChart(pres.charts.DOUGHNUT, [{ name: "코호트", labels: ["정상 수리 완결", "오접수 조기 종결"], values: [927, 73] }], {
    x: rx, y: 3.0, w: 2.7, h: 2.7, holeSize: 62, chartColors: ["059669", "94A3B8"],
    showLegend: false, showPercent: false, showValue: false, showLabel: false, dataBorder: { pt: 1, color: "FFFFFF" },
  });
  txt(s, [{ text: "1,000", options: { bold: true, fontSize: 22, breakLine: true } }, { text: "케이스", options: { fontSize: 12, color: K.slate } }],
    rx + 0.85, 3.95, 1.0, 0.8, { align: "center", valign: "middle" });
  s.addShape(pres.shapes.OVAL, { x: rx + 2.95, y: 3.55, w: 0.2, h: 0.2, fill: { color: K.green }, line: { type: "none" } });
  txt(s, [{ text: "정상 수리 완결", options: { bold: true, breakLine: true } }, { text: "927건 (92.7%)", options: { bold: true, breakLine: true } }, { text: "순수 분석 모수 → 질문 2 코호트", options: { color: K.slate, fontSize: 12 } }],
    rx + 3.25, 3.4, 2.45, 1.0, { fontSize: 13 });
  s.addShape(pres.shapes.OVAL, { x: rx + 2.95, y: 4.65, w: 0.2, h: 0.2, fill: { color: K.mist }, line: { type: "none" } });
  txt(s, [{ text: "오접수 조기 종결", options: { bold: true, breakLine: true } }, { text: "73건 (7.3%)", options: { bold: true, breakLine: true } }, { text: "타 기관 관할 → 노이즈 격리", options: { color: K.slate, fontSize: 12 } }],
    rx + 3.25, 4.5, 2.45, 1.0, { fontSize: 13 });
  // channel
  txt(s, "927건 코호트의 접수 채널", rx, 5.85, rw, 0.28, { fontSize: 12, bold: true, color: K.gray });
  const ch = [["Phone", "251건", "27.1%"], ["Web", "241건", "26.0%"], ["Personal", "228건", "24.6%"], ["Letter", "207건", "22.3%"]];
  ch.forEach(([n, c, p], i) => {
    const x = rx + i * (chw + 0.15);
    card(s, x, 6.15, chw, 0.75);
    txt(s, [{ text: n, options: { bold: true, fontSize: 12, breakLine: true } }, { text: c + " · " + p, options: { fontSize: 11, color: "334155" } }], x, 6.2, chw, 0.65, { align: "center", valign: "middle" });
  });
  source(s, "출처: repair_cleaned.csv (13,262행) 직접 집계 · 코호트 = RepairReady 927건");
  s.addNotes(
    "5대 전처리를 완료한 결과, 단 한 건의 결측과 시간 역전도 없는 완전무결한 13,262행 정제 데이터셋이 완성되었습니다.\n\n" +
    "정제된 데이터를 프로파일링하여 타 기관 관할 오접수 73건을 격리하고, 실제 현장 수리가 이루어진 '927건의 클린 분석 코호트'를 확립했습니다.\n\n" +
    "접수 채널은 Phone 27.1%, Web 26.0%, Personal 24.6%, Letter 22.3%로 고르게 유입되고, 시스템 정산은 자동화되어 있습니다. 그렇다면 대체 왜 전체 프로세스는 평균 4.4일(105.9시간)이나 걸릴까요?\n\n" +
    "정상화된 927건의 클린 로그를 바탕으로, 대기가 집중된 현장의 진짜 병목을 파헤치는 질문 2, 프로세스 마이닝 심층 분석으로 넘어가겠습니다.\n\n" +
    "[수치 주석] 스토리보드 원문의 채널 비율(Phone 25.1 / Web 25.0 / Personal 24.9 / Letter 25.0, '완벽한 25% 균등')은 repair_cleaned.csv 실측과 달라 실측값으로 교체했습니다. 원문의 '지연의 94.4%가 현장에 집중'도 분모 혼선이 있어 '대기가 집중된 현장'으로 바꿨습니다."
  );
}

// =====================================================================
// Slide 07. 기준 프로세스 모델
// =====================================================================
pres.addSection({ title: "Part 02. 질문 2 — 프로세스 마이닝 심층 분석" });
{
  const s = newSlide("CONTENT", "Part 02. 질문 2 — 프로세스 마이닝 심층 분석");
  kicker(s, "Part 02 · 질문 2-1  |  AS-IS 기준 프로세스 모델");
  s.addText("단방향 에스컬레이션과 병렬 정산이 입증된 E2E 기준 프로세스 모델", { placeholder: "title" });
  const mw = W, mh = mw * 840 / 2740;
  s.addImage({ path: MAP_IMG, x: X0, y: 1.6, w: mw, h: mh, altText: "접수·현장·정산 3개 국면의 E2E 수리 프로세스 맵" });
  const y0 = 1.6 + mh + 0.2;
  const cards = [
    ["01 접수 국면", "FirstContact 1,000건 중 73건(7.3%)이 InformClientWrongPlace로 조기 이탈. 일정 조율 직후 InformClientSurvey가 0초에 자동 발송되어 국면 종료 앵커로 작동."],
    ["02 현장 국면", "수리는 즉시 → 사내 → 외주로만 전이, 외주 후 사내로의 역류 0건(0.0%). 수리 완료 시 시스템이 RepairReady(927건)를 자동 발행."],
    ["03 정산 국면", "고객통보 선행 50.6%(469건) vs 재무전송 선행 49.2%(456건)의 대칭 병렬. TicketReady는 후행 완료와 99.8%(925건) 일치 → AND-Join."],
  ];
  const cw = 3.95, gap = (W - 3 * cw) / 2, ch = 6.95 - y0;
  cards.forEach(([h, b], i) => {
    const x = X0 + i * (cw + gap);
    card(s, x, y0, cw, ch);
    txt(s, h, x + 0.2, y0 + 0.12, cw - 0.4, 0.28, { fontSize: 14, bold: true, color: i === 1 ? K.orange : K.navy });
    txt(s, b, x + 0.2, y0 + 0.45, cw - 0.4, ch - 0.5, { fontSize: 12, color: K.slate });
  });
  source(s, "출처: repair_cleaned.csv 프로세스 맵 (노드 수치는 이벤트 기준, 국면 머리말은 케이스 기준)");
  s.addNotes(
    "상세 병목 분석에 앞서, 모든 분석의 기준선이 될 'E2E 기준 프로세스 모델'입니다. 이 모델은 데이터의 3가지 명확한 실측 근거를 바탕으로 도출되었습니다.\n\n" +
    "첫째, 접수 단계는 1,000건 중 관할 외 73건의 조기 이탈과 시스템 자동 알림 앵커로 경계가 확립되었습니다.\n\n" +
    "둘째, 현장 수리 흐름은 철저한 단방향 에스컬레이션입니다. 사내 기사는 물론 외주 기사(DoIt, FixIt) 역시 수리를 마친 뒤 완료 커밋을 하면 시스템이 RepairReady를 발송합니다. 외주로 넘어간 후 사내로 되돌아온 역류 케이스는 단 0건입니다.\n\n" +
    "셋째, 정산 공정은 고객 통보와 재무 처리가 50.6% 대 49.2%로 대칭 선행하는 병렬(AND) 구조이며, 최종 티켓 마감은 두 작업 중 늦게 끝난 시각과 99.8% 일치합니다.\n\n" +
    "이처럼 검증된 기준 지도를 토대로, 다음 장부터 90.5%의 대기시간이 어디서 발생하는지 거시적 분해로 들어가겠습니다."
  );
}

// =====================================================================
// Slide 08. 거시 리드타임 분해
// =====================================================================
{
  const s = newSlide("CONTENT", "Part 02. 질문 2 — 프로세스 마이닝 심층 분석");
  kicker(s, "Part 02 · 질문 2-2  |  거시 리드타임 분해");
  s.addText("리드타임 105.9시간의 90.5%는 공정 간 단순 대기이고,\n그 98.0%가 현장 국면에 집중된다", { placeholder: "title" });

  const cats = ["01 접수 2.1h (실작업 0.2h)", "02 현장 98.3h (실작업 4.4h)", "03 정산 5.5h (자동 처리)", "E2E 전체 105.9h"];
  s.addChart(pres.charts.BAR, [
    { name: "실작업 / 시스템 처리", labels: cats, values: [0.2, 4.4, 5.5, 10.1] },
    { name: "공정 간 단순 대기", labels: cats, values: [1.9, 93.9, 0, 95.8] },
  ], {
    x: X0, y: 1.65, w: 7.9, h: 3.2, barDir: "bar", barGrouping: "percentStacked", catAxisOrientation: "maxMin",
    chartColors: ["2563EB", "EA580C"], barGapWidthPct: 40,
    showValue: true, dataLabelPosition: "ctr", dataLabelFormatCode: '[<5]"";0.0"h"', dataLabelFontSize: 11, dataLabelColor: "FFFFFF", dataLabelFontBold: true, dataLabelFontFace: "+mn-lt",
    catAxisLabelFontSize: 11, catAxisLabelColor: "334155", catAxisLabelFontFace: "+mn-lt",
    valAxisLabelFontSize: 10, valAxisLabelColor: "64748B", valAxisLabelFontFace: "+mn-lt", valAxisLabelFormatCode: "0%",
    valGridLine: { color: "E2E8F0", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "t", legendFontSize: 11, legendColor: "334155", legendFontFace: "+mn-lt",
  });

  const sx = 8.7, sw = 4.133;
  [["90.5%", "공정 간 단순 대기", "95.8h / 105.9h (실작업 9.5%)"], ["98.0%", "현장 국면 집중도", "대기 93.9h / 95.8h · 정산 대기 0.0h"]].forEach(([b, l, d], i) => {
    const y = 1.65 + i * 1.65;
    card(s, sx, y, sw, 1.5);
    txt(s, b, sx + 0.3, y + 0.12, 1.9, 0.75, { fontSize: 36, bold: true, color: K.orange, valign: "middle" });
    txt(s, l, sx + 2.2, y + 0.12, sw - 2.35, 0.75, { fontSize: 14, bold: true, valign: "middle" });
    txt(s, d, sx + 0.3, y + 0.95, sw - 0.5, 0.4, { fontSize: 12, color: K.slate });
  });

  const cards = [
    ["01 접수 · 일정 조율 병목", "비동기 소통 대기 1.9h (접수의 90.4%)", ["전화·대면 479건: 지연 없음", "웹·우편 448건: 비동기 회신 지체", "교차 인계 123건 → 6.6배 (1.2h→7.9h)"]],
    ["02 현장 · 실사 방문 대기", "76.8h = 현장 국면의 78.2% (압도적 1위)", ["일 135건 인입 vs 실사 69건 (51.1%)", "매일 약 66건 적체", "피크 시점 403건 대기열(WIP)"]],
    ["03 현장 · 수리 준비·하자 루프", "착수 대기 15.9h (사내수리 30.5h)", ["즉시·외주 대기 0h, 사내수리만 지연", "원인: 부품 조달·2차 일정 조율", "하자 재방문 26건, 최대 10.1일"]],
  ];
  const cw = 3.95, gap = (W - 3 * cw) / 2, y0 = 5.0, ch = 1.95;
  cards.forEach(([h, badge, bl], i) => {
    const x = X0 + i * (cw + gap);
    card(s, x, y0, cw, ch);
    txt(s, h, x + 0.2, y0 + 0.12, cw - 0.4, 0.28, { fontSize: 14, bold: true });
    txt(s, badge, x + 0.2, y0 + 0.44, cw - 0.4, 0.28, { fontSize: 12, bold: true, color: K.orange });
    s.addText(
      bl.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < bl.length - 1 } })),
      { x: x + 0.2, y: y0 + 0.82, w: cw - 0.4, h: ch - 0.9, isTextBox: true, margin: 0, valign: "top", fontSize: 12, color: K.slate, paraSpaceAfter: 4 }
    );
  });
  source(s, "출처: analysis.sql 2절, slide08_macro_leadtime_breakdown · 정산 5.5h는 100% 시스템 자동 처리 (실작업·시스템 처리 합산)");
  s.addNotes(
    "수리 프로세스가 지연되는 진짜 원인은 무엇일까요? 기사가 작업을 느리게 해서일까요? 데이터를 쪼개보니 완전히 달랐습니다.\n\n" +
    "전체 105.9시간(약 4.4일) 중 실작업 시간은 10.1시간(9.5%)에 불과하며, 나머지 95.8시간(90.5%)은 공정 사이에서 멈춰 서 있는 단순 대기시간이었습니다. 특히 정산 국면은 인간 개입 없이 시스템이 100% 자동 처리(5.5h)하므로 대기가 0시간이며, 대기 95.8시간의 98.0%가 '현장 국면'에 집중되어 있었습니다.\n\n" +
    "이 대기시간의 발원지를 '3대 병목'으로 정리했습니다. 첫째, 웹·우편의 비동기 소통 부재로 일정이 늘어지는 '일정 조율 병목(1.9h)'. 둘째, 현장 국면의 78%가 쏠려 있는 압도적 1위의 '실사 방문 대기 병목(76.8h)'. 셋째, 사내 수리 시 자재 조달과 재작업으로 인한 '수리 준비 대기(30.5h) 및 하자 루프(최대 10일)'입니다.\n\n" +
    "그렇다면 프로세스의 첫 관문인 접수 국면에서 왜 6.6배의 시간 폭증이 일어났는지, 다음 장에서 살펴보겠습니다.\n\n" +
    "[수치 주석] (1) 스토리보드의 '전체 대기의 78.2%'는 분모가 현장 국면 리드타임(98.3h)입니다(76.8/98.3, analysis.sql L1396). 전체 대기(95.8h) 대비로는 80.2%라 '현장 국면의 78.2%'로 표기했습니다. (2) 94.4%는 현장 국면 내 Wait1+Wait2 비중입니다(analysis.sql L1380). E2E 기준은 90.5%입니다. (3) CAPA는 analysis.sql L1620 기준(69건/일, 인입 대비 51.1%, 일 66건 적체)으로 통일했습니다. 스토리보드의 63.7건/일은 지속 CAPA(L1766)로 66건 적체와 산술이 맞지 않습니다(135−63.7=71.3)."
  );
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
