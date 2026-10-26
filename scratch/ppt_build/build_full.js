const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const SKILL = "C:/Users/nextb/.claude/skills/synced/987d6139-e616-4cee-8655-caebbe5dfdb9_839f932a-f7e9-41d6-939a-3f1377246a4e/pptx";
const { applyTheme } = require(SKILL + "/scripts/apply_theme.js");

const OUT = process.argv[2];
const ROOT = "C:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/";
const FIG = ROOT + "outputs/figures/";
const MAP_IMG = ROOT + "scratch/ppt_build/process_map_crop.png";

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
pres.title = "수리 프로세스 진단 보고서 (Slide 01-19)";

const C = pres.SchemeColor;
const K = {
  navy: C.text1, slate: C.text2, white: C.background1, paper: C.background2,
  orange: C.accent1, green: C.accent2, red: C.accent3, blue: C.accent4,
  gray: C.accent5, mist: C.accent6,
};
const X0 = 0.5, W = 12.333;
const warn = [];

// ---------- text measurement / manual wrapping (Korean wraps per character in PowerPoint) ----------
function cw(ch) {
  const c = ch.charCodeAt(0);
  if ((c >= 0xAC00 && c <= 0xD7A3) || (c >= 0x3130 && c <= 0x318F) || (c >= 0x4E00 && c <= 0x9FFF) || c >= 0xFF00) return 1.0;
  if (ch === " ") return 0.3;
  if (/[0-9]/.test(ch)) return 0.58;
  if (/[A-Z]/.test(ch)) return 0.68;
  if (/[a-z]/.test(ch)) return 0.55;
  if (".,:;·'|!".includes(ch)) return 0.35;
  if ("()[]/-".includes(ch)) return 0.42;
  if (ch === "%") return 0.9;
  return 0.85;
}
function textW(str, pt, bold) {
  let u = 0;
  for (const ch of String(str)) u += cw(ch);
  return u * pt / 72 * (bold ? 1.02 : 1);
}
function wrap(text, wIn, pt, bold = false) {
  text = String(text).replace(/Slide (\d+)/g, "Slide $1");
  const lim = wIn * 0.96, out = [];
  for (const para of String(text).split("\n")) {
    let line = "";
    for (const wd of para.split(" ")) {
      const trial = line ? line + " " + wd : wd;
      if (textW(trial, pt, bold) <= lim) { line = trial; continue; }
      if (line) out.push(line);
      if (textW(wd, pt, bold) > lim) {
        let part = "";
        for (const ch of wd) {
          if (textW(part + ch, pt, bold) > lim) { out.push(part); part = ch; } else part += ch;
        }
        line = part;
      } else line = wd;
    }
    out.push(line);
  }
  return out;
}
function wrapRuns(text, wIn, pt, bold, base = {}) {
  return wrap(text, wIn, pt, bold).map((l, i) => ({ text: l, options: Object.assign({}, base, i > 0 ? { softBreakBefore: true } : {}) }));
}
const LH = 1.22; // line height factor
function lineH(pt) { return pt * LH / 72; }

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "COVER",
  background: { color: "0F172A" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 1.85, w: 7.6, h: 2.5, fontSize: 36, bold: true, color: K.white, align: "left", valign: "top", margin: 0 }, text: "" } },
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

// ---------- primitives ----------
function T(s, text, x, y, w, h, o = {}) {
  const pt = o.fontSize || 14;
  const base = { fontSize: pt, color: o.color || K.navy, bold: !!o.bold, italic: !!o.italic };
  let content = text;
  if (typeof text === "string") {
    content = wrapRuns(text, w, pt, o.bold, base);
    const need = wrap(text, w, pt, o.bold).length * lineH(pt);
    if (need > h + 0.04) warn.push(`overflow? "${text.slice(0, 24)}" need ${need.toFixed(2)} > h ${h.toFixed(2)}`);
  }
  const opts = Object.assign({}, o);
  delete opts.fontSize; delete opts.color; delete opts.bold; delete opts.italic;
  s.addText(content, Object.assign({ x, y, w, h, isTextBox: true, margin: 0, valign: "top", fontSize: pt, color: base.color, bold: base.bold }, opts));
}
function B(s, items, x, y, w, h, o = {}) {
  const pt = o.fontSize || 12, ind = 0.2;
  const runs = [];
  let lines = 0;
  items.forEach((it) => {
    const ws = wrap(it, w - ind, pt, false);
    lines += ws.length;
    ws.forEach((l, j) => {
      const op = { fontSize: pt, color: o.color || K.slate };
      if (j === 0) op.bullet = { indent: 14 };
      else op.softBreakBefore = true;
      runs.push({ text: l, options: op });
    });
  });
  const need = lines * lineH(pt) + (items.length - 1) * (o.gap ?? 3) / 72;
  if (need > h + 0.04) warn.push(`bullets overflow "${items[0].slice(0, 20)}" need ${need.toFixed(2)} > ${h.toFixed(2)}`);
  s.addText(runs, { x, y, w, h, isTextBox: true, margin: 0, valign: "top", fontSize: pt, color: o.color || K.slate, paraSpaceAfter: o.gap ?? 3 });
  return need;
}
function card(s, x, y, w, h, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign({ x, y, w, h, rectRadius: 0.08, fill: { color: K.paper }, line: { type: "none" } }, o));
}
function pill(s, text, x, y, w, h, fill, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: h / 2, fill: { color: fill }, line: { type: "none" } });
  s.addText(text, Object.assign({ x, y, w, h, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 12, bold: true, color: K.white }, o));
}
function kicker(s, text) { T(s, text, X0, 0.3, W, 0.28, { fontSize: 12, bold: true, color: K.orange }); }
function source(s, text) { T(s, text, X0, 7.05, 11.4, 0.3, { fontSize: 10, color: K.gray, valign: "middle" }); }
function title(s, text) {
  let lines = wrap(text, W, 24, true);
  if (lines.length === 2) { // balance the two lines
    let lo = W * 0.4, hi = W;
    for (let i = 0; i < 20; i++) { const mid = (lo + hi) / 2; if (wrap(text, mid, 24, true).length <= 2) hi = mid; else lo = mid; }
    lines = wrap(text, hi, 24, true);
  }
  if (lines.length > 2) warn.push("title >2 lines: " + text.slice(0, 30));
  s.addText(lines.join("\n"), { placeholder: "title" });
}
function newSlide(layout, section) { return pres.addSlide({ masterName: layout, sectionTitle: section }); }
function pngSize(p) { const b = fs.readFileSync(p); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; }
function fitImg(s, p, bx, by, bw, bh, alt, alignX = "center") {
  const sz = pngSize(p), ar = sz.w / sz.h;
  let iw = bw, ih = bw / ar;
  if (ih > bh) { ih = bh; iw = bh * ar; }
  const x = alignX === "left" ? bx : bx + (bw - iw) / 2;
  const y = by + (bh - ih) / 2;
  s.addImage({ path: p, x, y, w: iw, h: ih, altText: alt });
  return { x, y, w: iw, h: ih };
}
function infoCard(s, x, y, w, h, o) {
  card(s, x, y, w, h);
  const px = x + 0.2, pw = w - 0.4;
  let cy = y + 0.1;
  if (o.big) { T(s, o.big, px, cy, pw, 0.5, { fontSize: o.bigPt || 28, bold: true, color: o.bigColor || K.navy, valign: "middle" }); cy += 0.52; }
  if (o.tag) { pill(s, o.tag, px, cy, Math.max(1.0, textW(o.tag, 11, true) + 0.3), 0.26, o.tagFill || K.slate, { fontSize: 11 }); cy += 0.33; }
  if (o.title) {
    const n = wrap(o.title, pw, 13, true).length;
    T(s, o.title, px, cy, pw, n * lineH(13), { fontSize: 13, bold: true });
    cy += n * lineH(13) + 0.06;
  }
  if (o.bullets) B(s, o.bullets, px, cy, pw, y + h - cy - 0.06, { fontSize: o.fs || 11.5 });
}
function kpi(s, x, y, w, h, o) {
  card(s, x, y, w, h);
  T(s, o.big, x + 0.2, y + 0.12, w - 0.4, 0.62, { fontSize: o.bigPt || 32, bold: true, color: o.color, valign: "middle" });
  T(s, o.label, x + 0.2, y + 0.8, w - 0.4, 0.5, { fontSize: 13, bold: true });
  if (o.sub) T(s, o.sub, x + 0.2, y + 0.8 + wrap(o.label, w - 0.4, 13, true).length * lineH(13) + 0.04, w - 0.4, h - 1.2, { fontSize: 11, color: K.slate });
}
function stdTable(s, rows, x, y, w, colW, rowH, o = {}) {
  s.addTable(rows, Object.assign({
    x, y, w, colW, rowH, border: { type: "solid", pt: 0.75, color: "E2E8F0" }, fill: { color: "F8FAFC" }, margin: [0.03, 0.08, 0.03, 0.08], fontFace: "Malgun Gothic",
  }, o));
}
const hdrC = (t, fill = "0F172A", o = {}) => ({ text: t, options: Object.assign({ bold: true, color: "FFFFFF", fill: { color: fill }, fontSize: 11, align: "center", valign: "middle" }, o) });
const cel = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 11, color: "334155", valign: "middle", align: "left" }, o) });

// figure-centric slide: image on the left, 2 KPI cards on the right, 3 insight cards below
function figSlide(s, o) {
  const imgBox = o.noKpi ? { x: X0, y: 1.55, w: W, h: o.imgH || 3.6 } : { x: X0, y: 1.55, w: 9.7, h: 3.55 };
  fitImg(s, FIG + o.img, imgBox.x, imgBox.y, imgBox.w, imgBox.h, o.alt, o.noKpi ? "center" : "left");
  if (!o.noKpi) {
    o.kpis.forEach((k, i) => kpi(s, 10.4, 1.55 + i * 1.85, 2.433, 1.7, k));
  }
  const cy = o.noKpi ? 5.3 : 5.25, ch = o.noKpi ? 1.65 : 1.7;
  const cwid = 3.95, gap = (W - 3 * cwid) / 2;
  o.cards.forEach((c, i) => infoCard(s, X0 + i * (cwid + gap), cy, cwid, ch, c));
}

// =====================================================================
// Part 00
// =====================================================================
pres.addSection({ title: "Part 00. 인트로" });
{ // 01
  const s = newSlide("COVER", "Part 00. 인트로");
  pill(s, "채용 과제 전형 최종 보고서", 0.7, 0.75, 3.3, 0.42, "334155");
  s.addText("프로세스 마이닝 기반\n공공임대주택 수리 프로세스\n진단 및 운영 최적화 방안", { placeholder: "title" });
  T(s, "5대 무손실 전처리, 실사 대기 병목(76.8h) 원인 규명 및\n3대 데이터 기반 TO-BE 전략", 0.7, 4.45, 7.6, 0.9, { fontSize: 18, color: "CBD5E1" });
  T(s, "퍼즐데이터 수리 프로세스 데이터 분석 과제   |   제출일 2026. 10. 27", 0.7, 6.55, 7.6, 0.35, { fontSize: 14, color: "94A3B8" });
  [["13,262행", "이벤트 로그 · 1,000 케이스", "#ProcessMining", K.white],
   ["90.5%", "리드타임 중 공정 간 단순 대기", "#LeadTime_90.5%_Wait", K.orange],
   ["65%", "TO-BE 리드타임 단축 목표", "#TO-BE_ROI_65%", "34D399"]].forEach(([big, label, tag, col], i) => {
    const y = 1.55 + i * 1.8;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.0, y, w: 3.83, h: 1.6, rectRadius: 0.1, fill: { color: "1E293B" }, line: { type: "none" } });
    T(s, big, 9.25, y + 0.12, 3.4, 0.62, { fontSize: 36, bold: true, color: col, valign: "middle" });
    T(s, label, 9.25, y + 0.84, 3.4, 0.3, { fontSize: 13, color: "E2E8F0" });
    pill(s, tag, 9.25, y + 1.2, textW(tag, 11, true) + 0.35, 0.28, "334155", { fontSize: 11, color: "CBD5E1" });
  });
  s.addNotes("안녕하십니까, 퍼즐데이터 수리 프로세스 데이터 분석 결과 발표를 맡은 지원자입니다. 본 보고서는 네덜란드 공공임대주택 1,000건의 수리 로그를 바탕으로, 단순 통계를 넘어 프로세스 마이닝 관점에서 대기시간 약 90%의 구조적 원인을 밝히고 실질적 개선안을 제시합니다.\n\n[수치 근거] E2E 리드타임 105.9h 중 대기 95.8h = 90.5%. (94.4%는 현장 국면 98.3h 내 Wait1+Wait2 비중이라 분모가 달라 사용하지 않음)");
}
{ // 02
  const s = newSlide("CONTENT", "Part 00. 인트로");
  kicker(s, "Agenda");
  title(s, "원천 데이터 전처리부터 TO-BE 전략까지, 4개 파트로 보고합니다");
  const parts = [
    ["01", "데이터 진단\n및 전처리", "질문 1", ["이벤트 로그 프로파일링", "5대 인과 복원 (CASE 1~5)", "927건 클린 코호트 확립"]],
    ["02", "프로세스 마이닝\n심층 분석", "질문 2", ["E2E 프로세스 흐름 (맵)", "3대 대기 병목 심층 규명", "품질 리스크 & 영향 요인 회귀"]],
    ["03", "프로세스\n최적화 방안", "질문 3", ["소통 통제 (Web 자가 예약)", "대기 단축 (1회 방문 패스트트랙)", "정량적 ROI (리드타임 65% 감축)"]],
    ["04", "엔지니어링\n신뢰성 보증", "검증", ["1,878행 SQL 및 파이프라인 검증", "재현성 보증 체크리스트", "질의응답 (Q&A)"]],
  ];
  const cwid = 2.9, gap = 0.24;
  parts.forEach(([no, ttl, tag, items], i) => {
    const x = X0 + i * (cwid + gap), y = 1.85;
    card(s, x, y, cwid, 4.5);
    T(s, no, x + 0.3, y + 0.3, cwid - 0.6, 0.75, { fontSize: 44, bold: true, color: i === 1 ? K.orange : K.navy });
    T(s, ttl, x + 0.3, y + 1.15, cwid - 0.6, 0.8, { fontSize: 18, bold: true });
    pill(s, tag, x + 0.3, y + 2.1, 1.0, 0.32, K.slate, { fontSize: 11 });
    B(s, items, x + 0.3, y + 2.65, cwid - 0.55, 1.7, { fontSize: 13, gap: 6 });
  });
  s.addNotes("오늘 발표는 4개 파트로 진행됩니다. 질문 1의 데이터 무손실 전처리를 거쳐, 질문 2의 프로세스 병목과 원인을 규명하고, 질문 3에서 실질적 개선안과 정량적 ROI를 제시하며 마무리하겠습니다.");
}
{ // 03
  const s = newSlide("CONTENT", "Part 00. 인트로");
  kicker(s, "Executive Summary");
  title(s, "현장의 '대기시간'을 줄이고, 이해관계자 간의 '소통'을 통제하면 프로세스 리드타임을 획기적으로 개선할 수 있다");
  const cards = [
    ["1", "원천 진단", "13,262행", "100% 무손실 복원", "이벤트 로그 특성을 반영한 2원화 전처리로 임의 행 삭제 0건, 20행의 비정상 시스템 결측만 정밀 인과 복원 달성", K.navy],
    ["2", "병목 가설", "대기 90.5%", "+ 비동기 소통 지연", "리드타임 지연의 본질은 작업자 속도가 아닌 공정 간 단순 대기(95.8h)와 접수 단계의 비동기 소통 핑퐁에 집중", K.orange],
    ["3", "개선 방향", "소통 통제", "+ 대기시간 단축", "'Web 자가 예약 기반 소통 통제'와 '패스트트랙 1회 방문 직행'을 핵심 레버로 수리 리드타임 65% 대폭 감축", K.green],
  ];
  const cwid = 3.95, gap = (W - 3 * cwid) / 2;
  cards.forEach(([n, label, big, sub, body, col], i) => {
    const x = X0 + i * (cwid + gap), y = 1.95;
    card(s, x, y, cwid, 4.4);
    s.addShape(pres.shapes.OVAL, { x: x + 0.35, y: y + 0.35, w: 0.55, h: 0.55, fill: { color: col }, line: { type: "none" } });
    T(s, n, x + 0.35, y + 0.35, 0.55, 0.55, { align: "center", valign: "middle", fontSize: 18, bold: true, color: K.white });
    T(s, label, x + 1.1, y + 0.35, cwid - 1.4, 0.55, { fontSize: 18, bold: true, color: K.slate, valign: "middle" });
    T(s, big, x + 0.35, y + 1.25, cwid - 0.7, 0.7, { fontSize: 32, bold: true, color: col });
    T(s, sub, x + 0.35, y + 1.95, cwid - 0.7, 0.4, { fontSize: 16, bold: true, color: K.slate });
    T(s, body, x + 0.35, y + 2.6, cwid - 0.7, 1.6, { fontSize: 14, color: K.slate });
  });
  s.addNotes("본 분석을 관통하는 핵심 가설은 명확합니다. 수리가 늦어지는 것은 현장 기사가 느려서가 아니라, 공정 사이의 단순 대기와 접수 단계의 비동기 소통 지연 때문입니다. 이 두 가지를 통제하여 전체 프로세스를 획기적으로 개선하는 여정을 보여드리겠습니다.");
}

// =====================================================================
// Part 01
// =====================================================================
const P1 = "Part 01. 질문 1 — 데이터 진단 및 전처리";
pres.addSection({ title: P1 });
{ // 04
  const s = newSlide("CONTENT", P1);
  kicker(s, "Part 01 · 질문 1  |  Before Profiling");
  title(s, "정상 결측은 그대로 보존하고, 시스템 에러 20행(0.15%)만 수사 타겟으로 특정했다");
  card(s, X0, 1.75, 3.9, 5.1);
  [["13,262", "원천 이벤트 행"], ["1,000", "분석 대상 케이스"], ["13", "전체 속성 수"]].forEach(([big, lab], i) => {
    const y = 2.0 + i * 1.2;
    T(s, big, X0 + 0.35, y, 3.2, 0.65, { fontSize: 40, bold: true });
    T(s, lab, X0 + 0.35, y + 0.65, 3.2, 0.32, { fontSize: 14, color: K.slate });
  });
  T(s, "1건 1행의 정형 데이터가 아닌 세부 작업 단위로 기록되는 공정 이벤트 로그", X0 + 0.35, 5.7, 3.2, 0.95, { fontSize: 13, color: K.slate });
  fitImg(s, FIG + "EDA-01.png", 4.65, 1.70, 8.18, 3.15, "컬럼별 결측률 2원화 분포 (EDA-01)");
  [["정상 결측", "059669", "구조적 Null 86.0~93.0% · 7개 속성 (12,335행)", "후속 공정이 없어 비어 있는 값 → [무죄] 임의 대체 없이 100% 보존", 4.98],
   ["비정상 결측", "DC2626", "시스템 에러 0.015~0.098% · 5개 속성 (taskID·orig·event·date·time)", "필수 값 누락 → [유죄] 18개 케이스, 단 20행을 정밀 복원 대상으로 특정", 5.62],
   ["진공 구간", "64748B", "0.1% ~ 86.0% 구간에 걸치는 컬럼 0개 (Void Zone)", "완벽한 양극단 이봉분포 → 정상/비정상 판별의 객관성 입증", 6.26]].forEach(([lab, col, a, b, y]) => {
    card(s, 4.65, y, 8.18, 0.58);
    pill(s, lab, 4.78, y + 0.1, 1.35, 0.38, col, { fontSize: 12 });
    T(s, [{ text: a, options: { bold: true, breakLine: true, fontSize: 11, color: K.navy } }, { text: b, options: { fontSize: 11, color: K.slate } }], 6.3, y + 0.05, 6.4, 0.5, { valign: "middle" });
  });
  source(s, "출처: repair2.csv 원천 프로파일링 (EDA-01) · 20행 = 5개 속성 결측이 포함된 18개 케이스의 실제 행");
  s.addNotes("데이터를 열어보았을 때 가장 먼저 확인한 것은 구조였습니다. 본 데이터는 공정마다 행이 쌓이는 이벤트 로그로, 90% 안팎의 결측치는 후속 수리가 발생하지 않아 생긴 자연스러운 정상 결측입니다. 반면 필수 속성임에도 비어 있는 값은 13,262행 중 단 20행에 불과했습니다. 이 20행만을 정밀 복원 타겟으로 특정했습니다.");
}
{ // 05
  const s = newSlide("CONTENT", P1);
  kicker(s, "Part 01 · 질문 1  |  CASE 1 ~ 5");
  title(s, "행 삭제와 단순 대체 없이, 업무 인과 근거로 20행을 100% 무손실 복원했다");
  T(s, "결측 속성 및 규모", 0.75, 1.6, 2.6, 0.25, { fontSize: 11, bold: true, color: K.gray });
  T(s, "현장 업무 인과 단서 (Ground Truth)", 3.6, 1.6, 4.4, 0.25, { fontSize: 11, bold: true, color: K.gray });
  T(s, "복원 판정 (5개 속성 모두 누락 0건)", 8.5, 1.6, 4.3, 0.25, { fontSize: 11, bold: true, color: K.gray });
  const rows = [
    ["CASE 1", "taskID", "결측 2건", "contact 속성은 FirstContact에만 기록되는 고유 도메인 속성", "FirstContact · InformClientSurvey 확정 복원"],
    ["CASE 2", "originator", "결측 2건", "동일 작업의 시작(start)-완료(complete) 담당자 100.0% 일치", "짝 이벤트 담당자(Anne, Paul) 상호 승계"],
    ["CASE 3", "eventtype", "결측 5건", "기간 작업은 1:1 페어(start→complete), 마일스톤은 단독 발생", "1:1 페어 3건 + 마일스톤 2건 100% 복원"],
    ["CASE 4", "date", "총 879건 · 결측 13 + 오기입 866", "시각 정상 859건 선별, 선·후행 업무 순서 구간 제약 적용", "단일 후보 640건 + 앵커 최근접 219건 매핑 (1970년 통일)"],
    ["CASE 5", "time", "총 28건 · 결측 13 + 더미 15", "표본 34% 한계 극복 → 접수 정상 표본 751건(75.1%) 확보 (중앙값 4.0분)", "정상 자정 7건 보존 + 기준 앵커 역산 21건 (역전 0건)"],
  ];
  rows.forEach(([tag, attr, amt, clue, fix], i) => {
    const y = 1.9 + i * 0.88;
    card(s, X0, y, W, 0.8);
    T(s, [{ text: tag + "  ", options: { fontSize: 11, bold: true, color: K.orange } }, { text: attr, options: { fontSize: 16, bold: true, breakLine: true, color: K.navy } }, { text: amt, options: { fontSize: 11, bold: true, color: K.red } }], 0.75, y, 2.75, 0.8, { valign: "middle" });
    T(s, clue, 3.6, y, 4.4, 0.8, { fontSize: 12, color: K.slate, valign: "middle" });
    T(s, "→", 8.0, y, 0.4, 0.8, { fontSize: 16, bold: true, color: K.gray, valign: "middle", align: "center" });
    T(s, fix, 8.5, y, 4.2, 0.8, { fontSize: 12, bold: true, color: K.green, valign: "middle" });
  });
  [["데이터 무손실", "임의 삭제 0건 · 13,262행 (100.0%) 완전 보존"], ["통계적 강건성", "34% 한계 극복 → 정상 표본 751건(75.1%)"], ["인과 무결성", "시간 역전 0건 달성 · 927건 정상 분석 코호트 확립"]].forEach(([h, b], i) => {
    const x = X0 + i * (3.95 + 0.24);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 6.35, w: 3.95, h: 0.62, rectRadius: 0.08, fill: { color: K.green }, line: { type: "none" } });
    T(s, [{ text: h, options: { bold: true, fontSize: 13, breakLine: true } }, { text: b, options: { fontSize: 11 } }], x + 0.2, 6.35, 3.55, 0.62, { color: K.white, valign: "middle" });
  });
  source(s, "출처: analysis.ipynb Cell 18·20·51·53·77·81, analysis.sql");
  s.addNotes("복원 시 단 한 행도 버리지 않았습니다. 시작-완료 담당자의 100% 일치성, 태스크 고유 속성을 활용했고, 일시는 표본 34% 축소 한계를 극복하여 확보한 751건 정상 모수의 대표값을 앵커로부터 역산 적용했습니다. 덕분에 시간 역전 0건의 완벽한 데이터셋을 완성했습니다.");
}
{ // 06
  const s = newSlide("CONTENT", P1);
  kicker(s, "Part 01 · 질문 1  |  After Profiling");
  title(s, "시간 역전 0건을 입증했고, 오접수 73건을 격리해 927건 클린 코호트를 확립했다");
  const g = (t) => cel(t, { bold: true, color: "059669", align: "center", fontSize: 13 });
  const l = (t) => cel(t, { bold: true, color: "0F172A", fontSize: 13 });
  const m = (t) => cel(t, { align: "center", fontSize: 13 });
  stdTable(s, [
    [hdrC("검증 항목", "0F172A", { fontSize: 13 }), hdrC("Before (원천)", "64748B", { fontSize: 13 }), hdrC("After (정제)", "059669", { fontSize: 13 })],
    [l("총 이벤트 수"), m("13,262행"), g("13,262행 (100% 보존)")],
    [l("필수 속성 결측"), m("20건"), g("0건 (100% 복원)")],
    [l("일자 연도 오기입"), m("866건"), g("0건 (1970년 주기 통일)")],
    [l("시간 역전"), m("음수 소요시간"), g("0건 (3,711 페어 양수)")],
  ], X0, 1.8, 6.3, [2.2, 1.7, 2.4], [0.5, 0.85, 0.85, 0.85, 0.95]);
  card(s, X0, 6.0, 6.3, 0.85, { fill: { color: "ECFDF5" } });
  T(s, "전처리 전 구간 결과: 결측 20건 → 0건, 임의 행 삭제 0건 (무결성 100%)", X0 + 0.25, 6.0, 5.8, 0.85, { fontSize: 14, bold: true, color: K.green, valign: "middle" });
  const rx = 7.15, rw = 5.683, chw = (rw - 3 * 0.15) / 4;
  [["1,000", "케이스"], ["890", "고유 주택"], ["13", "속성"], ["14행", "케이스 중앙값"]].forEach(([b, lb], i) => {
    const x = rx + i * (chw + 0.15);
    card(s, x, 1.8, chw, 1.0);
    T(s, b, x, 1.9, chw, 0.5, { fontSize: 20, bold: true, align: "center" });
    T(s, lb, x, 2.42, chw, 0.3, { fontSize: 11, color: K.slate, align: "center" });
  });
  card(s, rx, 3.1, rw, 1.2, { fill: { color: "ECFDF5" } });
  s.addShape(pres.shapes.OVAL, { x: rx + 0.25, y: 3.25, w: 0.2, h: 0.2, fill: { color: K.green }, line: { type: "none" } });
  T(s, "정상 수리 완결 코호트", rx + 0.55, 3.2, 3.0, 0.3, { fontSize: 13, bold: true });
  T(s, "927건 (92.7%)", rx + 0.25, 3.5, 3.0, 0.45, { fontSize: 22, bold: true, color: K.green, valign: "middle" });
  T(s, "순수 현장수리 분석 모수 → 질문 2 코호트 확립", rx + 3.35, 3.5, rw - 3.5, 0.7, { fontSize: 11, color: K.slate });
  card(s, rx, 4.45, rw, 1.2);
  s.addShape(pres.shapes.OVAL, { x: rx + 0.25, y: 4.6, w: 0.2, h: 0.2, fill: { color: K.mist }, line: { type: "none" } });
  T(s, "오접수 조기 종결", rx + 0.55, 4.55, 3.0, 0.3, { fontSize: 13, bold: true });
  T(s, "73건 (7.3%)", rx + 0.25, 4.85, 3.0, 0.45, { fontSize: 22, bold: true, color: K.gray, valign: "middle" });
  T(s, "타 기관 관할 주택 (InformClientWrongPlace) → 분석 노이즈 격리", rx + 3.35, 4.85, rw - 3.5, 0.7, { fontSize: 11, color: K.slate });
  T(s, "927건 코호트의 접수 채널 분포", rx, 5.85, rw, 0.28, { fontSize: 12, bold: true, color: K.gray });
  [["Phone", "251건 (27.1%)"], ["Web", "241건 (26.0%)"], ["Personal", "228건 (24.6%)"], ["Letter", "207건 (22.3%)"]].forEach(([n, c], i) => {
    const x = rx + i * (chw + 0.15);
    card(s, x, 6.15, chw, 0.75);
    T(s, [{ text: n, options: { bold: true, fontSize: 12, breakLine: true, color: K.navy } }, { text: c, options: { fontSize: 10, color: K.slate } }], x, 6.18, chw, 0.7, { align: "center", valign: "middle" });
  });
  source(s, "출처: repair_cleaned.csv (13,262행) 직접 집계 · 코호트 = RepairReady 927건");
  s.addNotes("5대 전처리를 완료한 결과, 단 한 건의 결측과 시간 역전도 없는 완전무결한 13,262행 정제 데이터셋이 완성되었습니다.\n\n정제된 데이터를 프로파일링하여 타 기관 관할 오접수 73건을 격리하고, 실제 현장 수리가 이루어진 '927건의 클린 분석 코호트'를 확립했습니다.\n\n접수 채널은 Phone 27.1%, Web 26.0%, Personal 24.6%, Letter 22.3%로 고르게 유입되고, 시스템 정산은 자동화되어 있습니다. 그렇다면 대체 왜 전체 프로세스는 평균 4.4일(105.9시간)이나 걸릴까요?\n\n정상화된 927건의 클린 로그를 바탕으로, 대기가 집중된 현장의 진짜 병목을 파헤치는 질문 2, 프로세스 마이닝 심층 분석으로 넘어가겠습니다.");
}

// =====================================================================
// Part 02
// =====================================================================
const P2 = "Part 02. 질문 2 — 프로세스 마이닝 심층 분석";
pres.addSection({ title: P2 });
{ // 07
  const s = newSlide("CONTENT", P2);
  kicker(s, "Part 02 · 질문 2-1  |  AS-IS 기준 프로세스 모델");
  title(s, "단방향 에스컬레이션과 병렬 정산이 입증된 E2E 기준 프로세스 모델");
  fitImg(s, MAP_IMG, X0, 1.60, W, 3.78, "접수·현장·정산 3개 국면의 E2E 수리 프로세스 맵");
  [["01 접수 국면", "오접수 격리 & 시스템 앵커", "73건(7.3%)이 InformClientWrongPlace로 조기 이탈. InformClientSurvey가 0초에 자동 발송되어 접수 국면의 종료 앵커로 작동."],
   ["02 현장 국면 (단방향)", "역류 0건 & 완료 커밋 앵커", "수리는 즉시 → 사내 → 외주로만 전이되며, 외주 후 사내 역류는 0건(0.0%). 사내/외주 기사의 완료 커밋 시 시스템이 RepairReady(927건)를 자동 발행."],
   ["03 정산 국면 (병렬 AND)", "대칭 병렬 & 완벽한 AND-Join", "고객통보 선행 50.6%(469건) vs 재무전송 선행 49.2%(456건)의 대칭 병렬. TicketReady는 후행 완료 시각과 99.8%(925건) 일치, 0초에 자동 종결."]].forEach(([tag, ttl, desc], i) => {
    const x = X0 + i * (3.95 + 0.24), y = 5.58;
    card(s, x, y, 3.95, 1.37);
    pill(s, tag, x + 0.15, y + 0.08, Math.max(1.4, textW(tag, 10.5, true) + 0.3), 0.24, i === 1 ? K.orange : K.slate, { fontSize: 10.5 });
    T(s, ttl, x + 0.15, y + 0.36, 3.65, 0.24, { fontSize: 12, bold: true });
    T(s, desc, x + 0.15, y + 0.62, 3.65, 0.74, { fontSize: 10.5, color: K.slate });
  });
  source(s, "출처: repair_cleaned.csv 프로세스 맵 (노드 수치는 이벤트 기준, 국면 머리말은 케이스 기준)");
  s.addNotes("상세 병목 분석에 앞서, 모든 분석의 기준선이 될 'E2E 기준 프로세스 모델'입니다. 이 모델은 데이터의 3가지 명확한 실측 근거를 바탕으로 도출되었습니다.\n\n첫째, 접수 단계는 1,000건 중 관할 외 73건의 조기 이탈과 시스템 자동 알림 앵커로 경계가 확립되었습니다.\n\n둘째, 현장 수리 흐름은 철저한 단방향 에스컬레이션입니다. 외주로 넘어간 후 사내로 되돌아온 역류 케이스는 단 0건입니다.\n\n셋째, 정산 공정은 고객 통보와 재무 처리가 50.6% 대 49.2%로 대칭 선행하는 병렬(AND) 구조이며, 최종 티켓 마감은 두 작업 중 늦게 끝난 시각과 99.8% 일치합니다.\n\n이처럼 검증된 기준 지도를 토대로, 다음 장부터 90.5%의 대기시간이 어디서 발생하는지 거시적 분해로 들어가겠습니다.\n\n[참고] 맵 하단의 '교차 인계 123건 — 건당 +5.11h'는 맵 에셋의 지표이며, 본문 6.6배(1.2h→7.9h, 순지연 +6.7h)와 산출 기준이 다릅니다.");
}
{ // 08
  const s = newSlide("CONTENT", P2);
  kicker(s, "Part 02 · 질문 2-2  |  거시 리드타임 분해");
  title(s, "리드타임 105.9시간의 90.5%는 공정 간 단순 대기이며, 98.0%가 현장 국면에 집중된다");
  fitImg(s, FIG + "slide08_macro_leadtime_breakdown.png", 0.5, 1.65, 7.9, 3.2, "국면별 실작업 대 단순 대기 누적 막대", "left");
  kpi(s, 8.7, 1.65, 4.133, 1.5, { big: "90.5%", color: K.orange, label: "공정 간 단순 대기", sub: "95.8h / 105.9h (실작업 9.5%)" });
  kpi(s, 8.7, 3.3, 4.133, 1.55, { big: "98.0%", color: K.red, label: "현장 국면 집중도", sub: "현장 대기 93.9h / 전체 95.8h · 정산 0.0h" });
  const cs = [
    { tag: "01 접수 · 일정 조율 병목", tagFill: K.slate, title: "접수 대기 1.9h (접수의 90.4%)", bullets: ["전화·대면 479건: 지연율 0%", "웹·우편 448건: 비동기 회신 핑퐁 지체", "교차 인계 123건 → 6.6배 폭증 (1.2h→7.9h)"] },
    { tag: "02 현장 · 실사 방문 대기 (1위)", tagFill: K.red, title: "76.8h = 현장 국면의 78.2% 독점", bullets: ["일 135건 인입 vs 실사 69건 (소화율 51%)", "매일 약 66건 미처리 적체 누적", "피크 시점 403건 대기열(WIP) 폭증"] },
    { tag: "03 현장 · 수리 준비 & 하자 루프", tagFill: K.orange, title: "착수 대기 15.9h (사내수리 30.5h)", bullets: ["즉시·외주 대기 0h, 사내수리만 지연", "원인: 자재 조달 및 2차 일정 조율 공백", "하자 재방문 26건 → 최대 10.1일 지연"] },
  ];
  cs.forEach((c, i) => infoCard(s, X0 + i * (3.95 + 0.24), 5.0, 3.95, 1.95, c));
  source(s, "출처: analysis.sql 2절, slide08_macro_leadtime_breakdown · 정산 5.5h는 100% 시스템 자동 처리 (실작업·시스템 처리 합산)");
  s.addNotes("수리 프로세스가 지연되는 진짜 원인은 무엇일까요? 기사가 작업을 느리게 해서일까요? 데이터를 쪼개보니 완전히 달랐습니다.\n\n전체 105.9시간(약 4.4일) 중 실작업 시간은 10.1시간(9.5%)에 불과하며, 나머지 95.8시간(90.5%)은 공정 사이에서 멈춰 서 있는 단순 대기시간이었습니다. 정산 국면은 시스템이 100% 자동 처리(5.5h)하므로 대기가 0시간이며, 대기 95.8시간의 98.0%가 '현장 국면'에 집중되어 있었습니다.\n\n이 대기시간의 발원지를 '3대 병목'으로 정리했습니다. 첫째, 웹·우편의 비동기 소통 부재로 일정이 늘어지는 '일정 조율 병목(1.9h)'. 둘째, 현장 국면의 78%가 쏠려 있는 압도적 1위의 '실사 방문 대기 병목(76.8h)'. 셋째, 사내 수리 시 자재 조달과 재작업으로 인한 '수리 준비 대기(30.5h) 및 하자 루프(최대 10일)'입니다.\n\n그렇다면 프로세스의 첫 관문인 접수 국면에서 왜 6.6배의 시간 폭증이 일어났는지, 다음 장에서 살펴보겠습니다.\n\n[수치 주석] 78.2% = 76.8h ÷ 현장 국면 98.3h (analysis.sql L1396). 전체 대기(95.8h) 대비로는 80.2%.");
}
{ // 09
  const s = newSlide("CONTENT", P2);
  kicker(s, "Part 02 · 질문 2-2  |  제1 병목 · 접수");
  title(s, "접수 지연은 물량이 아닌 교차 인계에서 비롯되며, 인계 123건은 전부 웹·우편에서 발생했다");
  fitImg(s, FIG + "slide09_reception_bottleneck_3panel.png", X0, 1.55, W, 3.55, "인계 여부별 소요시간·채널별 완료 속도·15분 내 완료 건 평균");
  const cs = [
    { big: "r = 0.21", bigColor: K.slate, tag: "1. 가설 기각", tagFill: K.slate, title: "물량 과부하가 아니다", bullets: ["일별 인입량-소요시간 상관 미약", "접수 창구 CAPA 부족이 아님"] },
    { big: "6.6배", bigColor: K.red, tag: "2. 핵심 동인", tagFill: K.red, title: "교차 인계 123건이 지연을 만든다", bullets: ["단독 804건 1.2h vs 인계 7.9h (+6.7h)", "인계 전수가 웹 69건·우편 54건"] },
    { big: "6.8분", bigColor: K.green, tag: "3. 반전 통찰", tagFill: K.green, title: "웹 시스템 자체는 가장 빠르다", bullets: ["15분 내 완료 건: 웹 6.8분 최속", "원인은 일정 조율 공백 → Slide 14"] },
  ];
  cs.forEach((c, i) => infoCard(s, X0 + i * (3.95 + 0.24), 5.2, 3.95, 1.75, Object.assign({ bigPt: 24 }, c)));
  source(s, "출처: analysis.sql 접수 국면 (L930~1012) · docs/02_analysis_insights.md (물량-소요시간 r=0.21) · slide09_reception_bottleneck_3panel");
  s.addNotes("접수 국면의 지연은 왜 발생했을까요? 특정 날짜에 접수량이 몰려서였을까요? 데이터를 분석해보니 일별 접수량과 소요시간의 상관은 미약했습니다. 물량 문제가 아니었습니다.\n\n좌측 [Panel 1]을 보시면, 진짜 원인은 상담원 간의 '교차 인계(Handover)'였습니다. 단독으로 처리할 때는 1.2시간이면 끝나던 접수가, 상담원 2명 이상 개입되는 순간 7.9시간으로 6.6배 폭증했습니다.\n\n가운데 [Panel 2]를 보시면 양극화가 나타납니다. 전화와 대면은 거의 100%가 15분 이내에 끝나고 인계가 없었습니다. 반면 웹과 우편은 약 50%가 60분을 초과했고, 인계 123건 전수가 웹(69건)과 우편(54건)에서만 발생했습니다.\n\n우측 [Panel 3]의 반전 통찰을 주목해 주십시오. 15분 이내 완료된 건만 보면 웹은 평균 6.8분으로 전화(8.2분)나 대면(8.5분)보다 오히려 빨랐습니다. 웹 시스템 자체가 느린 게 아니라, 신청 후 실시간으로 방문 일정을 확정하지 못해 고객의 회신을 기다리다 다른 상담원이 티켓을 넘겨받는 '비동기 일정 조율 공백'이 6.6배 지연의 본질입니다.\n\n접수 국면의 병목을 규명했으니, 이제 대기시간의 98%가 집중된 '현장 국면'으로 넘어가겠습니다.\n\n[수치 주석] 스토리보드의 r≈0.08, 웹 275건·우편 173건, 대면 100.0%는 원천과 달라 교체: 상관 r=0.21(docs/02), 웹 241·우편 207건(코호트 실측), 대면 99.6%(그림).");
}
{ // 10
  const s = newSlide("CONTENT", P2);
  kicker(s, "Part 02 · 질문 2-2  |  제2 병목 · 현장 실사 대기");
  title(s, "실사 방문 대기 76.8h는 현장 국면의 78.2%이며, 매일 66건씩 쌓인 403건 대기열이 원인이다");
  figSlide(s, {
    img: "slide10_field_bottleneck_wip.png", alt: "일별 유입량 대 실사 착수량 및 WIP, 일자별 평균 실사 대기시간",
    kpis: [
      { big: "76.8h", color: K.orange, label: "실사 방문 대기", sub: "약 3.2일 · 현장 국면의 78.2%" },
      { big: "403건", color: K.red, label: "피크 적체 대기열 (D7)", sub: "D1 20건 → D7 403건, 20배 폭증" },
    ],
    cards: [
      { tag: "원인 1 · CAPA 불균형", tagFill: K.slate, title: "인입 135건/일 vs 실사 69.2건/일", bullets: ["실사 소화율 51.1%", "기사 11명이 1인당 일 6.0~7.1건 소화"] },
      { tag: "원인 2 · 적체 누적", tagFill: K.red, title: "매일 약 66건 미처리 누적", bullets: ["연초 8일 집중 유입, 첫날 20건 → D7 403건", "이후 소화기에 접어들며 대기열 감소"] },
      { tag: "결과 · 대기 폭증", tagFill: K.orange, title: "첫날 10.7h → 최대 95.5h (D9)", bullets: ["D4~D6 평균 대기 90~94h", "접수 부서가 아닌 '전수 실사' 구조의 문제"] },
    ],
  });
  source(s, "출처: analysis.sql L1583~1620 (WIP·CAPA), slide10_field_bottleneck_wip");
  s.addNotes("전체 프로세스 대기시간 중 압도적 1위 병목은 '실사 방문 대기(76.8시간, 3.2일)'였고, 이는 현장 국면 리드타임의 78.2%에 해당합니다. 조사원이 방문하기까지 왜 3일 넘게 걸렸을까요?\n\n좌측 [Panel A]를 보시면 메커니즘이 드러납니다. 연초 8일간 매일 약 135건의 접수가 쏟아져 들어왔지만, 현장 기사 11명이 하루에 소화할 수 있는 실사는 평균 69건에 불과했습니다. 결국 매일 66건의 미처리 건이 누적되었고, 첫날 20건이던 현장 대기열은 7일째 403건까지 20배 폭증했습니다.\n\n우측 [Panel B]를 보시면, 첫날 접수된 건은 10.7시간 만에 방문했지만 대기열이 쌓인 4~6일 차에는 90시간 이상, 최대 95.5시간(약 4일)이 걸렸습니다. 즉 접수 부서의 문제가 아니라 '기사 CAPA를 초과하는 전수 방문 실사'가 현장 병목의 본질이었습니다.\n\n[수치 주석] 스토리보드의 'D4~6 피크 93.6h'는 그림 기준 D6 93.6h이고 전체 최대는 D9 95.5h입니다. 중앙값 48.8h·최대 241.6h는 SQL에서 확인되지 않아 슬라이드에서 제외했습니다.");
}
{ // 11
  const s = newSlide("CONTENT", P2);
  kicker(s, "Part 02 · 질문 2-2  |  제3 병목 & 품질 리스크");
  title(s, "수리 착수 대기는 사내 수리(30.5h)가 단독 주도하고, 사내 재방문 루프는 최대 10.1일을 지연시킨다");
  figSlide(s, {
    img: "slide11_repair_delay_rework.png", alt: "1차 수리 방식별 착수 대기시간 및 수리 차수별 에스컬레이션 지연",
    kpis: [
      { big: "30.5h", color: K.red, label: "사내 수리 착수 대기", sub: "즉시·외주 0.0h · 전체 평균 15.9h" },
      { big: "10.1일", color: "991B1B", label: "사내 하자 재방문 최대 지연", sub: "26건 · 평균 32.9h" },
    ],
    cards: [
      { tag: "Wait 2 · 사내 수리만 지연", tagFill: K.red, title: "착수 대기 15.9h의 원인", bullets: ["즉시 383건·외주 59건: 대기 0.0h", "사내 485건(52.3%): 30.5h (자재 조달·2차 일정)"] },
      { tag: "수리 차수 · 에스컬레이션", tagFill: K.slate, title: "1차 종결 810건(87.4%)", bullets: ["2차 전환 117건(12.6%): 외주 68 + 사내 재방문 49", "3차 전환 6건(0.6%)"] },
      { tag: "품질 리스크 · 재방문 루프", tagFill: "991B1B", title: "사내 → 사내 재방문 26건", bullets: ["평균 32.9h, 최대 10.1일 대기", "해법: 1차 실패 시 즉시 외주 이관 → Slide 15"] },
    ],
  });
  source(s, "출처: analysis.sql L1365 (Wait 2), L1466~1494 (재작업 루프), slide11_repair_delay_rework");
  s.addNotes("현장의 두 번째 병목은 실사 후 1차 수리에 착수하기까지 걸리는 대기시간(15.9시간)이었습니다.\n\n좌측 [Panel A]를 보시면, 즉시수리와 외주수리는 대기가 0.0시간이었습니다. 오직 사내 수리(InternRepair, 485건)에서만 평균 30.5시간, 즉 1.3일의 대기가 발생했습니다. 기사가 실사 후 돌아와 부품을 신청하고 일정을 다시 잡는 '자재 조달 및 재방문 공백'이 원인이었습니다.\n\n우측 [Panel B]의 '재작업 루프'입니다. 전체의 87.4%는 한 번에 끝났지만, 12.6%인 117건이 2차 수리로 넘어갔습니다. 특히 사내 수리를 시도했다가 고치지 못해 다시 방문하는 26건은 평균 33시간, 최대 10.1일의 치명적인 지연이 발생했습니다. 사내에서 억지로 붙잡고 있다가 일정을 지체시키는 관행이 세입자 만족도를 추락시키는 주범이었습니다.\n\n[수치 주석] 2차 전환 117건 = 외주 이관 68(즉시 38 + 사내 30) + 사내 재방문 49(사내→사내 26 + 즉시→사내 23) 로 repair_cleaned.csv에서 재현됨.");
}
{ // 12
  const s = newSlide("CONTENT", P2);
  kicker(s, "Part 02 · 질문 2-3  |  소요시간 영향 요인");
  title(s, "리드타임은 사내 수리·실사 대기·비실시간 채널이 결정하며, 상담원 전담제는 통계적 착시다");
  const imgBox = { x: X0, y: 1.55, w: 9.7, h: 3.55 };
  fitImg(s, FIG + "slide12_regression_leadtime_drivers.png", imgBox.x, imgBox.y, imgBox.w, imgBox.h, "E2E 및 접수 국면 다변량 회귀계수", "left");
  kpi(s, 10.4, 1.55, 2.433, 1.7, { big: "R² 0.878", bigPt: 28, color: K.navy, label: "E2E 모델 설명력", sub: "3대 인자 모두 p < 0.05" });
  kpi(s, 10.4, 3.4, 2.433, 1.7, { big: "+31.75h", bigPt: 28, color: K.red, label: "사내 수리 배정 효과", sub: "실사 대기 +1.12h/h · 비실시간 +4.98h" });
  [{ big: "96.1%", bigColor: K.navy, tag: "착시 ①", tagFill: K.slate, title: "855/890채는 수리 1회", bullets: ["타 상담원과 겹칠 기회 자체가 없음"] },
   { big: "65.7%", bigColor: K.orange, tag: "착시 ②", tagFill: K.orange, title: "다발 35채 중 23채 교차 접수", bullets: ["타 상담원이 접수 → 전담 지역 없음"] },
   { big: "50:50", bigColor: K.green, tag: "착시 ③", tagFill: K.green, title: "기사 배정도 접수자와 무관", bullets: ["Anne 50:50, Edd 51.8:48.2 → 단일 가용 풀"] }].forEach((c, i) => infoCard(s, X0 + i * (3.95 + 0.24), 5.2, 3.95, 1.75, Object.assign({ bigPt: 24 }, c)));
  source(s, "출처: hypothesis_testing_and_visualization.ipynb (statsmodels OLS) · analysis.sql L420~576, L825 · slide12_regression_leadtime_drivers");
  s.addNotes("과제 질문 2-3인 '소요시간에 영향을 미치는 데이터 요소'를 통계적으로 증명하기 위해 E2E 다변량 OLS 회귀분석을 수행했습니다. 모델 설명력(R²)은 87.8%입니다.\n\n좌측을 보시면, 리드타임을 좌우하는 결정적 요인은 세 가지였습니다. 첫째, 실사 대기시간이 1시간 길어질 때마다 리드타임은 1.12시간씩 늘어났습니다. 둘째, 사내 수리로 배정되는 순간 부품 조달로 인해 전체 소요시간이 31.8시간 증가했습니다. 셋째, 웹이나 우편 등 비실시간 채널로 인입되면 5.0시간의 추가 지연이 발생했습니다. 접수 국면만 따로 보면 교차 인계가 +4.59시간(p<0.001), 비실시간 채널이 +3.41시간(p<0.001)입니다.\n\n반면 '상담원별 전담 지역'은 통계적 착시였습니다. 전체 890채 중 855채(96.1%)는 수리가 1회뿐이라 겹치지 않았을 뿐, 다발 35채 중 23채(65.7%)는 타 상담원에게 교차 접수되었습니다. 즉 사람의 문제가 아니라 채널과 공정 방식이 시간을 결정했습니다.\n\n[수치 주석] E2E 모델에서 교차 인계(−0.66h, p=0.890)와 2차 에스컬레이션(+5.93h, p=0.081)은 유의하지 않습니다. '50:50'은 기사별 접수자(Monica/Dian) 배정 비율(analysis.sql L825)이며, 기사 간 업무량이 같다는 뜻이 아닙니다.");
}
{ // 13
  const s = newSlide("CONTENT", P2);
  kicker(s, "Part 02 · 질문 2-3  |  리소스 생산성");
  title(s, "접수 상담원 2인은 53:47로 균등하게 분담하고, 현장에서는 Anne이 즉시수리를 견인한다");
  figSlide(s, {
    img: "slide13_resource_productivity.png", alt: "접수 상담원 2인 처리 건수 및 현장 기술자 11인 실사·수리 처리량",
    kpis: [
      { big: "53 : 47", color: K.blue, label: "상담원 2인 업무 분담", sub: "Monica 490건 · Dian 437건" },
      { big: "23.5%", color: K.orange, label: "Anne의 실사 점유", sub: "218건 · 1차 수리 204건(22.0%)" },
    ],
    cards: [
      { tag: "접수 상담원 2인", tagFill: K.blue, title: "처리량·인계율이 균등", bullets: ["Monica 인계 63건(12.9%), Dian 60건(13.7%)", "개인 역량 차이 없음 → 단일 룰로 작동"] },
      { tag: "현장 기술자 11인", tagFill: K.orange, title: "실사·수리를 병행", bullets: ["즉시수리 383건 중 Anne 185건(48.3%)", "Anne·Jacky·Barbara 3인이 95.3% 담당"] },
      { tag: "전문성 편차", tagFill: K.red, title: "사내 수리는 4인에 분산", bullets: ["Edd·Paul·John·Cindy 각 약 100건 참여", "즉시 vs 사내 배정이 대기 0h vs 30.5h를 가름"] },
    ],
  });
  source(s, "출처: repair_cleaned.csv 직접 집계 (케이스 기준), analysis.sql L1190, L1590 · slide13_resource_productivity");
  s.addNotes("리소스 생산성 측면을 살펴보겠습니다.\n\n좌측 [Panel A]에서 보시듯, 접수 상담원 Monica와 Dian은 처리 건수(490건 대 437건, 53:47)와 인계율(약 13%)이 균등했습니다. 상담원 개인의 업무 태만이나 역량 부족은 지연의 원인이 아니었습니다.\n\n우측 [Panel B]는 현장 기사 11명의 처리량입니다. 모든 기사가 실사와 수리를 병행하지만 Anne 기사는 전체 실사의 23.5%, 1차 수리의 22.0%를 담당했고, 즉시수리 383건 중 185건(48.3%)을 처리했습니다. 즉시수리는 Anne·Jacky·Barbara 3인이 95%를 맡았고, 사내수리는 Edd·Paul·John·Cindy 4인이 각 100건 안팎을 맡았습니다. 어느 배정을 받느냐에 따라 대기가 0시간 또는 30.5시간으로 갈린다는 점이 핵심입니다.\n\n[수치 주석] 스토리보드의 'Anne 즉시수리 370건 단독 완결(96%)'과 'Paul 사내수리 200건·실사 188건'은 start/complete 이벤트 행 수를 건수로 센 것입니다. 케이스 기준으로 Anne 185건(48.3%), Paul 사내수리 100건·실사 94건입니다. 접수 상담원 인계율은 최초 접수자 기준 Monica 63건(12.9%)/Dian 60건(13.7%)로 재집계했습니다(스토리보드 13.5%/13.1%는 재현 불가).");
}

// =====================================================================
// Part 03
// =====================================================================
const P3 = "Part 03. 질문 3 — 프로세스 최적화 방안";
pres.addSection({ title: P3 });
function flowNode(s, text, x, y, w, h, fill, fc = K.white, bold = false, pt = 11.5) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: fill }, line: { type: "none" } });
  T(s, text, x + 0.08, y, w - 0.16, h, { fontSize: pt, color: fc, bold, align: "center", valign: "middle" });
}
function arrowDown(s, x, y, h) {
  s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: "64748B", width: 1.5, endArrowType: "triangle" } });
}
{ // 14
  const s = newSlide("CONTENT", P3);
  kicker(s, "Part 03 · 질문 3  |  TO-BE 전략 1 & 2");
  title(s, "접수 소통을 통제하고 1회 방문으로 직행시키면 실사 대기열 87.3%가 사라진다");
  const py = 1.55, ph = 3.0, pw = 6.05;
  // AS-IS panel
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X0, y: py, w: pw, h: ph, rectRadius: 0.08, fill: { color: "FFFFFF" }, line: { color: "DC2626", width: 2 } });
  pill(s, "AS-IS · 전수 실사 후 수리", X0 + 0.2, py + 0.1, 2.5, 0.3, K.red, { fontSize: 11 });
  const nx = X0 + 0.7, nw = pw - 1.4;
  const as = [["01 접수 · 비동기 핑퐁, 교차 인계 123건 (2.1h)", K.slate], ["전수 실사 대기 76.8h (927건 전부 대기열)", K.red], ["현장 실사 40.5분 (헛걸음 포함)", K.slate], ["수리 착수 대기 15.9h (사내수리 30.5h)", K.orange], ["수리 → 정산 · 총 105.9h (4.4일)", K.navy]];
  as.forEach(([t, f], i) => {
    const y = py + 0.5 + i * 0.48;
    flowNode(s, t, nx, y, nw, 0.34, f, K.white, i === 1);
    if (i < as.length - 1) arrowDown(s, nx + nw / 2, y + 0.34, 0.14);
  });
  // TO-BE panel
  const tx = X0 + pw + 0.233;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: tx, y: py, w: pw, h: ph, rectRadius: 0.08, fill: { color: "FFFFFF" }, line: { color: "059669", width: 2 } });
  pill(s, "TO-BE · 사전 체크 후 1회 방문 직행", tx + 0.2, py + 0.1, 3.3, 0.3, K.green, { fontSize: 11 });
  const mx = tx + 0.35, mw = pw - 0.7;
  flowNode(s, "01 접수 · Web 자가 예약 + 사진 2장 체크리스트 (인계 0%)", mx, py + 0.5, mw, 0.34, K.slate);
  arrowDown(s, mx + mw / 2, py + 0.84, 0.14);
  flowNode(s, "사전 분류 · E·P형 809건(87.3%) / B형 118건(12.7%)", mx, py + 0.98, mw, 0.34, K.navy);
  arrowDown(s, mx + mw * 0.3, py + 1.32, 0.14);
  arrowDown(s, mx + mw * 0.86, py + 1.32, 0.14);
  flowNode(s, "E·P형: 부품 사전 상차, 1회 방문 직행 (실사 생략)", mx, py + 1.46, mw * 0.62, 0.5, K.green, K.white, true);
  flowNode(s, "B형: 선별 실사 큐", mx + mw * 0.66, py + 1.46, mw * 0.34, 0.5, "94A3B8", K.navy);
  arrowDown(s, mx + mw * 0.3, py + 1.96, 0.14);
  arrowDown(s, mx + mw * 0.83, py + 1.96, 0.14);
  flowNode(s, "수리 (사내 1차 미완결 시 외주 패스트트랙)", mx, py + 2.1, mw, 0.34, K.slate);
  arrowDown(s, mx + mw / 2, py + 2.44, 0.12);
  flowNode(s, "정산 · 총 36.0h (1.5일)", mx, py + 2.56, mw, 0.34, K.green, K.white, true);
  // strategy cards
  infoCard(s, X0, 4.7, pw, 1.65, { tag: "전략 1 · 접수 소통 통제", tagFill: K.blue, title: "사진 필수 첨부 + 세입자 자가 일정 확정", bullets: ["부품 라벨 사진 2장 → 고장 부품 해상도 확보", "캘린더 연동 자가 확정 → 핑퐁·교차 인계 123건 원천 소멸 (인계율 0%)"], fs: 11 });
  infoCard(s, tx, 4.7, pw, 1.65, { tag: "전략 2 · 1회 방문 원샷 직행", tagFill: K.green, title: "E·P형 809건이 실사 대기열을 우회", bullets: ["E형 370건(정합도 100%): 사전 키팅, 실사 40분 + 자재대기 38.7h 제거", "P형 439건(즉시 365·사내 36·외주 38, 사내 완결 91.3%) · B형 118건만 실사"], fs: 11 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X0, y: 6.45, w: W, h: 0.52, rectRadius: 0.08, fill: { color: "ECFDF5" }, line: { color: "059669", width: 1.25 } });
  T(s, "546.3시간 기사 공수 회수 & 실사 대기열 87% 제거 (일 유입 135건 → 14.8건, 기사 CAPA 69건 이내)", X0 + 0.2, 6.45, W - 0.4, 0.52, { fontSize: 14, bold: true, color: K.green, valign: "middle", align: "center" });
  s.addNotes("이제 구체적인 프로세스 최적화 방안을 말씀드리겠습니다.\n\n핵심은 '소통 통제와 1회 방문 직행'입니다. 현재는 모든 수리 건에 대해 기사가 먼저 가서 40분 동안 확인만 하고 오는 전수 실사를 고수하고 있습니다. 하지만 접수원이 최초 기록한 유형만으로도 87.3%는 어떤 수리가 필요한지 이미 정확히 맞추고 있었습니다.\n\n따라서 웹 접수 시 부품 사진과 라벨을 필수로 첨부받아 세부 규격을 특정하고, 세입자가 직접 방문 일정을 선택하게 만듭니다. 이렇게 되면 전화 핑퐁으로 인한 인계 123건은 0건으로 사라집니다.\n\n무엇보다 E형과 P형에 해당하는 809건(87.3%)은 헛걸음 실사를 건너뛰고, 부품을 차에 싣고 곧바로 수리에 착수하는 '1회 방문 직행'을 적용합니다. 546시간의 기사 낭비 공수가 회수되고, 하루 135건씩 쏟아지던 실사 대기열이 15건 안팎으로 줄어 76.8시간의 실사 대기 병목은 구조적으로 소멸됩니다.\n\n[수치 주석] P형은 439건(즉시 365 + 사내 36 + 외주 38, analysis.sql L1842~1856)이며 스토리보드의 '365건'은 그중 즉시수리분입니다. E 370 + P 439 = 809 = 927 × 87.3%. 87.3%는 접수원 사전 분류와 최종 수리 방식의 정합도(낙관 기준)이고, 보수 기준은 83.2%(771건)입니다.");
}
{ // 15
  const s = newSlide("CONTENT", P3);
  kicker(s, "Part 03 · 질문 3  |  TO-BE 전략 3 & ROI");
  title(s, "외주 패스트트랙을 더한 3대 전략으로 리드타임이 4.4일에서 1.5일로 65.1% 줄어든다");
  // left: decision rule
  card(s, X0, 1.55, 4.9, 2.85);
  pill(s, "전략 3 · 외주 패스트트랙", X0 + 0.2, 1.65, 2.4, 0.3, K.green, { fontSize: 11 });
  flowNode(s, "사내 1차 수리 (485건)", X0 + 1.2, 2.1, 2.5, 0.36, K.slate);
  arrowDown(s, X0 + 1.55, 2.46, 0.2);
  arrowDown(s, X0 + 3.35, 2.46, 0.2);
  flowNode(s, "완결 → 종결 (429건)", X0 + 0.2, 2.66, 2.0, 0.5, K.green, K.white, true);
  flowNode(s, "미완결 → 즉시 외주 이관 (DoIt·FixIt), 대기 0.0h", X0 + 2.4, 2.66, 2.3, 0.5, K.red, K.white, true, 10.5);
  T(s, "재방문 26건 · 최대 10.1일 루프 원천 차단", X0 + 0.2, 3.5, 4.5, 0.3, { fontSize: 12, bold: true, color: K.green, align: "center" });
  T(s, "외주 이관 시 착수 대기는 0.0시간 (현재 외주 대기 0.0h)", X0 + 0.2, 3.85, 4.5, 0.4, { fontSize: 11, color: K.slate, align: "center" });
  fitImg(s, FIG + "slide15_roi_leadtime_reduction.png", 5.6, 1.55, 7.233, 2.85, "총 리드타임 Before/After 및 공정별 시간 절감 분해", "left");
  const k = [
    { big: "▼ 65.1%", bigColor: K.green, tag: "총 리드타임", tagFill: K.navy, title: "105.9h → 36.0h (4.4일 → 1.5일)", bullets: ["평균 2.9일 · 69.9시간 단축"] },
    { big: "▼ 94.8%", bigColor: K.green, tag: "실사 방문 대기", tagFill: K.red, title: "76.8h → 4.0h 이내", bullets: ["E·P형 809건 직행 → 당일 실사"] },
    { big: "546.3h", bigColor: K.green, tag: "기사 공수 회수", tagFill: K.blue, title: "헛걸음 실사 40.5분 생략", bullets: ["본 수리 작업으로 재배치"] },
    { big: "13.3% → 0%", bigColor: K.green, bigPt: 22, tag: "교차 인계율", tagFill: K.orange, title: "자가 예약으로 123건 소멸", bullets: ["접수 2.1h → 0.5h, 착수 대기 15.9h → 12.0h"] },
  ];
  const kw = (W - 3 * 0.2) / 4;
  k.forEach((c, i) => infoCard(s, X0 + i * (kw + 0.2), 4.6, kw, 2.35, Object.assign({ bigPt: 30, fs: 12 }, c)));
  source(s, "출처: hypothesis_testing_and_visualization.ipynb (Slide 15 ROI), analysis.sql L1830~1878 · slide15_roi_leadtime_reduction");
  s.addNotes("세 번째 전략은 '외주 패스트트랙'입니다. 사내 기사가 1차 수리에서 고치지 못했을 때 억지로 2차 방문 일정을 잡지 않고, 즉시 전문 외주업체로 전산 이관합니다. 외주업체 이관 시 대기는 0시간이므로, 최대 10일 동안 세입자를 방치하던 품질 루프를 원천 차단할 수 있습니다.\n\n3대 전략을 결합한 최종 정량 ROI입니다. 현재 평균 4.4일(105.9시간)이 소요되던 전체 수리 리드타임은 1.5일(36.0시간)로 65.1% 단축됩니다.\n\n세부 내역을 보시면, 76.8시간에 달하던 실사 대기가 4시간 이내로 줄어든 것이 혁신의 핵심 동력입니다. 546시간의 기사 공수를 추가 확보하고 세입자의 주거 만족도를 높일 수 있습니다.\n\n[검증 필요 — ROI 정합성] 36.0h(65.1%)는 노트북 Slide 15 셀에 hours_tot=[105.9, 36.0]로 직접 입력된 값이며, 같은 셀의 공정별 TO-BE(접수 0.5 + 실사대기 4.0 + 수리대기 12.0 + 실작업 5.5 = 22.0h)와 합산이 맞지 않습니다. AS-IS 공정 합도 100.3h로 105.9h와 5.6h 차이가 납니다. 36.0h의 산출식(가정)을 확정하거나, 공정별 합계 기준으로 수치를 통일해야 합니다. 이 슬라이드는 스토리보드 값(36.0h, 65.1%)을 그대로 사용했습니다.");
}

// =====================================================================
// Part 04
// =====================================================================
pres.addSection({ title: "Part 04. 마무리" });
{ // 16
  const s = newSlide("CONTENT", "Part 04. 마무리");
  kicker(s, "Part 04 · 마무리  |  Reliability & Q&A");
  title(s, "모든 정량 지표는 1,878행 SQL과 파이썬 파이프라인으로 100% 재현 가능하다");
  const items = [
    ["1", "무손실 전처리 파이프라인", "repair_cleaned.csv · 13,262행 전수 보존, 비정상 결측 20행(18개 케이스) 인과 복원, 시간 역전 0건"],
    ["2", "SQL 프로세스 마이닝 마스터 모델", "analysis.sql · 1,878행, case_master_view 기반으로 리드타임·대기시간·WIP를 산출"],
    ["3", "가설 검정 및 고해상도 시각화", "hypothesis_testing_and_visualization.ipynb · OLS 회귀와 슬라이드 차트 에셋 생성"],
    ["4", "에셋 및 문서 규격화", "outputs/figures 11종 차트 에셋 및 03_ppt_storyboard.md와 동기화"],
  ];
  items.forEach(([n, h, d], i) => {
    const y = 1.75 + i * 1.28;
    card(s, X0, y, 6.4, 1.15);
    s.addShape(pres.shapes.OVAL, { x: X0 + 0.2, y: y + 0.3, w: 0.5, h: 0.5, fill: { color: K.navy }, line: { type: "none" } });
    T(s, n, X0 + 0.2, y + 0.3, 0.5, 0.5, { fontSize: 16, bold: true, color: K.white, align: "center", valign: "middle" });
    T(s, h, X0 + 0.9, y + 0.1, 5.3, 0.3, { fontSize: 14, bold: true });
    T(s, d, X0 + 0.9, y + 0.44, 5.3, 0.65, { fontSize: 11.5, color: K.slate });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.2, y: 1.75, w: 5.633, h: 5.0, rectRadius: 0.1, fill: { color: "0F172A" }, line: { type: "none" } });
  T(s, "Q&A", 7.6, 2.0, 4.8, 1.0, { fontSize: 54, bold: true, color: K.white, valign: "middle" });
  T(s, "현장의 대기시간(90.5%)을 줄이고, 이해관계자 간 소통을 통제하여 리드타임 65% 단축을 달성하겠습니다.", 7.6, 3.25, 4.8, 1.4, { fontSize: 17, bold: true, color: "E2E8F0" });
  [["90.5%", "단순 대기", K.orange], ["76.8h", "실사 대기", "FCA5A5"], ["65.1%", "단축 목표", "34D399"]].forEach(([b, l, c], i) => {
    const x = 7.6 + i * 1.62;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 5.1, w: 1.5, h: 1.2, rectRadius: 0.08, fill: { color: "1E293B" }, line: { type: "none" } });
    T(s, b, x, 5.2, 1.5, 0.5, { fontSize: 20, bold: true, color: c, align: "center", valign: "middle" });
    T(s, l, x, 5.78, 1.5, 0.3, { fontSize: 11, color: "CBD5E1", align: "center" });
  });
  s.addNotes("본 보고서에서 제시된 모든 수치와 분석 결과는 감이나 추정이 아닙니다. 13,262개 이벤트 로그를 한 건의 손실도 없이 복원한 전처리 파이프라인과, 1,878행의 MySQL 마스터 뷰 쿼리, 그리고 파이썬 통계 모델을 통해 재현 가능하도록 엔지니어링되었습니다.\n\n데이터의 엄밀한 진단이 실제 프로세스 혁신으로 이어지는 프로세스 마이닝 엔지니어로서 기여하겠습니다. 경청해 주셔서 감사합니다. 질문을 받겠습니다.\n\n[수치 주석] 스토리보드의 '노트북 19개 셀 전수 무오류 실행 통과'는 확인되지 않았습니다(노트북 19셀 중 코드 9셀, 저장된 실행 결과가 있는 셀은 4개, 오류 0건). 슬라이드에는 해당 문구를 넣지 않았습니다. 요약 메시지의 '94.4%'는 90.5%로 정정했습니다.");
}

// =====================================================================
// Part 05 Appendix
// =====================================================================
pres.addSection({ title: "Part 05. 부록" });
{ // 17
  const s = newSlide("CONTENT", "Part 05. 부록");
  kicker(s, "Appendix 1  |  전처리 알고리즘");
  title(s, "임의 삭제와 평균 대체 없이 인과 규칙과 751건 모수 확장으로 100% 무손실 복원했다");
  const cc = (t, o = {}) => cel(t, Object.assign({ fontSize: 10.5 }, o));
  stdTable(s, [
    [hdrC("CASE"), hdrC("속성 · 규모"), hdrC("인과 단서 · 알고리즘 (Ground Truth)"), hdrC("복원 결과")],
    [cc("1", { bold: true, align: "center" }), cc("taskID 2건", { bold: true }), cc("7124행(caseID 245): contact=Web 보유, MakeTicket start 직전 → FirstContact / 7785행(caseID 15): ArrangeSurvey complete 직후 System 자동 발송 → InformClientSurvey"), cc("확정 복원 2건", { color: "059669", bold: true })],
    [cc("2", { bold: true, align: "center" }), cc("originator 2건", { bold: true }), cc("시작-종료 담당자 일치율 100.0% / 8217행(Survey complete) → Anne 승계, 12880행(InternRepair complete) → Paul 승계"), cc("승계 복원 2건", { color: "059669", bold: true })],
    [cc("3", { bold: true, align: "center" }), cc("eventtype 5건", { bold: true }), cc("1:1 페어 추적: 6953행 ArrangeSurvey start, 8217행 Survey complete, 9843행 ImmediateRepair start / 마일스톤 단독: 8144행 InformClientSurvey, 13159행 TicketReady"), cc("페어 3 + 마일스톤 2", { color: "059669", bold: true })],
    [cc("4", { bold: true, align: "center" }), cc("date 879건", { bold: true }), cc("1905년 리셋 6 + 2020~22년 오기입 860 + 결측 13. 시각 정상 859건 선별 → 선행 완료 ~ 후행 착수 구간 제약 적용"), cc("640 + 219건 매핑 → 1970년 통일", { color: "059669", bold: true })],
    [cc("5", { bold: true, align: "center" }), cc("time 28건", { bold: true }), cc("완전무결 기준 시 표본 34~39%(398건) 축소 → 접수 구간 정상 표본 분리로 751건(75.1%) 확보, 중앙값 4.0분"), cc("자정 7 보존 + 앵커 역산 21 → 역전 0건", { color: "059669", bold: true })],
  ], X0, 1.65, W, [0.7, 1.7, 6.5, 3.433], [0.4, 0.78, 0.7, 0.78, 0.7, 0.7]);
  // sample expansion comparison
  card(s, X0, 5.85, 5.2, 1.1);
  T(s, "34~39%", X0 + 0.25, 5.9, 2.2, 0.55, { fontSize: 30, bold: true, color: K.red, valign: "middle" });
  T(s, "전 공정 완전무결 기준 표본 (398건) · 한계", X0 + 0.25, 6.5, 4.8, 0.35, { fontSize: 11.5, color: K.slate });
  T(s, "→", 5.85, 6.0, 0.8, 0.8, { fontSize: 32, bold: true, color: K.gray, align: "center", valign: "middle" });
  card(s, 6.75, 5.85, 6.083, 1.1, { fill: { color: "ECFDF5" } });
  T(s, "75.1% (751건)", 7.0, 5.9, 5.5, 0.55, { fontSize: 30, bold: true, color: K.green, valign: "middle" });
  T(s, "접수 구간 정상 표본 분리 전략 → 대표값 4.0분 도출", 7.0, 6.5, 5.6, 0.35, { fontSize: 11.5, color: K.slate });
  source(s, "출처: analysis.ipynb Cell 18·20·51·53·77·81 · docs/02_analysis_insights.md (행 번호) · repair2.csv");
  s.addNotes("부록 1번은 5대 전처리의 기술적 디테일입니다. 전 공정을 모두 통과한 표본만 쓰면 34%대로 표본이 급감하지만, 접수 구간의 정상 데이터 751건을 모수로 분리 추출함으로써 4.0분의 통계적 신뢰성을 확보하고 시간 역전 0건을 입증했습니다.");
}
{ // 18
  const s = newSlide("CONTENT", "Part 05. 부록");
  kicker(s, "Appendix 2  |  다변량 OLS 회귀분석");
  title(s, "다변량 OLS 3개 모델: 접수 지연은 인계·채널이, 총 리드타임은 사내 수리·실사 대기가 결정한다");
  const sec = (t, fill) => [{ text: t, options: { colspan: 5, bold: true, color: "FFFFFF", fill: { color: fill }, fontSize: 11, align: "left", valign: "middle" } }];
  const r = (v, b, se, p, sig, hot = false) => [cel(v, { bold: hot }), cel(b, { align: "right", bold: hot, color: hot ? "0F172A" : "334155" }), cel(se, { align: "right" }), cel(p, { align: "right" }), cel(sig, { align: "center", bold: true, color: sig.includes("n.s.") ? "64748B" : "DC2626" })];
  stdTable(s, [
    [hdrC("변수"), hdrC("계수 (h)"), hdrC("표준오차"), hdrC("p값"), hdrC("유의")],
    sec("모델 1 · 접수 국면 (종속: 접수 소요시간, R² = 0.239)", "475569"),
    r("비실시간 채널 (Web/Letter)", "+3.408", "0.279", "< 0.001", "***", true),
    r("교차 인계", "+4.592", "0.567", "< 0.001", "***", true),
    sec("모델 2 · 현장 국면 (종속: 현장 소요시간, R² = 0.8785)", "475569"),
    r("실사 방문 대기 (1시간당)", "+1.122", "0.014", "< 0.001", "***"),
    r("사내 수리 배정", "+31.667", "2.253", "< 0.001", "***", true),
    r("2차 에스컬레이션", "+6.935", "3.368", "0.040", "*"),
    sec("모델 3 · E2E 통합 (종속: 총 리드타임, R² = 0.8776)", "0F172A"),
    r("비실시간 채널 (Web/Letter)", "+4.978", "2.341", "0.034", "*"),
    r("교차 인계", "−0.659", "4.752", "0.890", "n.s."),
    r("실사 방문 대기 (1시간당)", "+1.123", "0.014", "< 0.001", "***"),
    r("사내 수리 배정", "+31.751", "2.269", "< 0.001", "***", true),
    r("2차 에스컬레이션", "+5.935", "3.393", "0.081", "n.s."),
  ], X0, 1.65, 7.4, [2.75, 1.2, 1.2, 1.25, 1.0], [0.34, 0.3, 0.34, 0.34, 0.3, 0.34, 0.34, 0.34, 0.3, 0.34, 0.34, 0.34, 0.34, 0.34]);
  const rx = 8.2, rw = 4.633;
  infoCard(s, rx, 1.65, rw, 1.55, { big: "+4.59h", bigColor: K.orange, tag: "접수 국면 · 교차 인계", tagFill: K.orange, bigPt: 26, bullets: ["비실시간 채널 +3.41h와 함께 접수 지연을 설명 (R² 0.239)"] });
  infoCard(s, rx, 3.35, rw, 1.55, { big: "+31.75h", bigColor: K.red, tag: "E2E · 사내 수리 배정", tagFill: K.red, bigPt: 26, bullets: ["실사 대기 +1.12h/h, 비실시간 채널 +4.98h (p=0.034)"] });
  infoCard(s, rx, 5.05, rw, 1.55, { big: "R² 0.878", bigColor: K.navy, tag: "E2E 설명력", tagFill: K.slate, bigPt: 26, bullets: ["E2E에서 교차 인계(p=0.890)는 채널 변수에 흡수되어 비유의"] });
  source(s, "출처: hypothesis_testing_and_visualization.ipynb OLS 출력 (statsmodels, *** p<0.001, * p<0.05, n.s. 비유의)");
  s.addNotes("부록 2번은 다변량 회귀 분석의 전체 결과표입니다. 접수 국면 모델에서는 교차 인계(+4.59h)와 비실시간 채널(+3.41h)이 모두 유의하고, 현장 국면과 E2E 모델에서는 사내 수리 배정(+31.7h)과 실사 방문 대기(시간당 +1.12h)가 압도적입니다. E2E 모델에서 교차 인계는 채널 변수와 겹쳐 유의성이 사라집니다.\n\n[수치 주석] 스토리보드의 부록 2(R²=0.428, 교차 인계 +6.67, Web +3.82, Letter +4.15, 야간 접수 +1.24, 상담원 더미 p>0.35)는 노트북 출력과 analysis.sql 어디서도 확인되지 않아, 노트북 OLS 3개 모델의 실제 출력으로 교체했습니다. 교차 인계 +6.7h는 회귀계수가 아니라 단순 평균 차이(7.87h − 1.20h)입니다.");
}
{ // 19
  const s = newSlide("CONTENT", "Part 05. 부록");
  kicker(s, "Appendix 3  |  리소스 생산성 크로스탭");
  title(s, "인력 분담은 균등하고, 병목은 사내 수리의 자재 대기와 비실시간 접수 구조에 있다");
  T(s, "접수 상담원 2인 (케이스 기준)", X0, 1.6, 5.2, 0.26, { fontSize: 12, bold: true, color: K.gray });
  const m = (t, o = {}) => cel(t, Object.assign({ align: "center", fontSize: 11 }, o));
  stdTable(s, [
    [hdrC("상담원"), hdrC("접수 건수"), hdrC("점유"), hdrC("인계 발생")],
    [cel("Monica", { bold: true }), m("490건"), m("52.9%"), m("63건 (12.9%)")],
    [cel("Dian", { bold: true }), m("437건"), m("47.1%"), m("60건 (13.7%)")],
  ], X0, 1.9, 5.2, [1.2, 1.1, 1.0, 1.9], [0.34, 0.38, 0.38]);
  T(s, "현장 기술자 11인 (케이스 기준)", 6.0, 1.6, 6.8, 0.26, { fontSize: 12, bold: true, color: K.gray });
  const techs = [["Anne", 218, 204], ["Barbara", 111, 98], ["Jacky", 110, 99], ["John", 101, 89], ["Cindy", 94, 88], ["Paul", 94, 96], ["Edd", 81, 97], ["Ben", 35, 25], ["Nick", 33, 21], ["Lex", 27, 27], ["Eric", 23, 24]];
  const tc = (t, o = {}) => cel(t, Object.assign({ align: "center", fontSize: 10 }, o));
  stdTable(s, [
    [hdrC("", "0F172A", { fontSize: 10 })].concat(techs.map(t => hdrC(t[0], "0F172A", { fontSize: 9 }))),
    [tc("실사", { bold: true })].concat(techs.map(t => tc(String(t[1]), t[0] === "Anne" ? { bold: true, color: "EA580C" } : {}))),
    [tc("1차 수리", { bold: true })].concat(techs.map(t => tc(String(t[2]), t[0] === "Anne" ? { bold: true, color: "EA580C" } : {}))),
  ], 6.0, 1.9, 6.833, [0.7].concat(techs.map(() => 0.557)), [0.34, 0.38, 0.38], { margin: [0.02, 0.02, 0.02, 0.02] });
  T(s, "수리 방식별 성과 대조표 (1차 수리 기준)", X0, 3.2, 8, 0.26, { fontSize: 12, bold: true, color: K.gray });
  const mm = (t, o = {}) => cel(t, Object.assign({ fontSize: 11.5 }, o));
  stdTable(s, [
    [hdrC("수리 방식", "0F172A", { fontSize: 11.5 }), hdrC("1차 수리 건수", "0F172A", { fontSize: 11.5 }), hdrC("착수 대기", "0F172A", { fontSize: 11.5 }), hdrC("2차 전환", "0F172A", { fontSize: 11.5 }), hdrC("주요 담당 (참여 건수)", "0F172A", { fontSize: 11.5 })],
    [mm("즉시 수리 (Immediate)", { bold: true }), mm("383건 (41.3%)"), mm("0.0h", { color: "059669", bold: true }), mm("61건 (15.9%) · 외주 38 + 사내 23"), mm("Anne 185 · Jacky 92 · Barbara 88")],
    [mm("외주 수리 (Extern)", { bold: true }), mm("59건 (6.4%)"), mm("0.0h", { color: "059669", bold: true }), mm("0건 (0.0%)"), mm("DoIt 30 · FixIt 29")],
    [mm("사내 수리 (Intern)", { bold: true }), mm("485건 (52.3%)"), mm("30.5h", { color: "DC2626", bold: true }), mm("56건 (11.5%) · 재방문 26 + 외주 30", { color: "DC2626", bold: true }), mm("Edd 101 · Paul 100 · John 96 · Cindy 95")],
  ], X0, 3.5, W, [2.4, 2.0, 1.4, 3.4, 3.133], [0.4, 0.5, 0.5, 0.5]);
  card(s, X0, 5.8, W, 1.15, { fill: { color: "ECFDF5" } });
  T(s, [
    { text: "개인 편차가 아닌 구조의 문제", options: { bold: true, fontSize: 14, color: "059669", breakLine: true } },
    { text: "상담원 2인의 처리량·인계율과 기사 11인의 실사·수리 분담은 단일 가용 풀 안에서 고르게 작동한다. 지연은 사내 수리 배정 시의 자재 대기(30.5h)와 웹·우편 비동기 접수 구조에서만 발생한다.", options: { fontSize: 12, color: "334155" } },
  ], X0 + 0.25, 5.85, W - 0.5, 1.05, { valign: "middle" });
  source(s, "출처: repair_cleaned.csv 직접 집계 (927건 코호트, 케이스 기준) · analysis.sql");
  s.addNotes("부록 3번의 크로스탭을 보면 상담원과 기사 모두 업무량이 균등하게 분담되어 있어 특정 인력의 태만이 아님을 알 수 있습니다. 병목은 오직 사내 수리의 자재 대기와 비실시간 접수 프로세스 자체에 있었습니다.\n\n[수치 주석] 스토리보드의 부록 3은 repair_cleaned.csv와 일치하지 않아 전면 재집계했습니다. ① 접수 상담원은 Monica·Dian 2인이며(Anne·Paul은 현장 기사), 4인 표(Anne 248/Dian 235/Monica 228/Paul 216)와 '실사 Anne 465 vs Paul 462'는 확인되지 않습니다. 실사는 Anne 218, Paul 94 등 11인 분산입니다. ② 수리 방식은 1차 수리 기준 즉시 383·외주 59·사내 485건(스토리보드 11번과 동일)이며, '사내 412건·외주 132건' 및 즉시수리 재작업률 0%는 맞지 않습니다(즉시수리도 61건이 2차로 전환). ③ 외주 132건은 2차 포함 전체 외주 케이스 수입니다.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
  if (warn.length) console.log("WARNINGS:\n" + warn.join("\n"));
})();
