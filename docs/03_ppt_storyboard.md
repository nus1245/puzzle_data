# 📊 [클로드 전용 마스터 빌드 지침서] 퍼즐데이터 과제 분석 보고서 (14 Slides 완결본)

> **문서 목적**: 본 문서는 **클로드(Claude 3.5 Sonnet / 3.7 Sonnet) 또는 프론트엔드/PPT 빌더**가 단 한 번의 프롬프트 입력으로도 **맥킨지/베인 전략 컨설팅 티어의 압도적인 16:9 프레젠테이션 (React / Tailwind / HTML / python-pptx)**을 1px의 오차도 없이 완벽하게 렌더링할 수 있도록 작성된 **최종 마스터 설계 규격서(Zero-ambiguity Implementation Spec)**입니다.

---

## 🤖 [클로드 복붙용 1-Click 원터치 빌드 마스터 프롬프트]

> **출근길에 클로드(Claude) 창에 아래 프롬프트를 파일 첨부와 함께 그대로 복사해서 붙여넣으시면 됩니다.**
> 클로드가 추가 질문 없이 본 문서의 모든 세부 규격을 100% 충족하여 단 1개의 슬라이드도 누락 없는 프로덕션 덱을 빌드하도록 설계된 프롬프트입니다.

```text
너는 맥킨지(McKinsey & Company) 및 베인(Bain & Company) 출신의 수석 프레젠테이션 디자인 엔지니어이자, 앤스로픽(Anthropic) 공식 PPTX 에이전트 스킬(anthropics/skills/pptx) 설계자다.
지금 제공된 [14 Slides 완결본 마스터 설계 규격서]를 바탕으로, 즉시 브라우저에서 실행 가능한 완성형 단일 HTML 프레젠테이션 웹앱(Tailwind CSS CDN + Nanum Gothic / Noto Sans + Lucide Icons) 또는 python-pptx 스크립트를 1px의 오차 없이 완벽히 빌드하라.

[클로드 필수 준수 앤스로픽 공식 5대 빌드 원칙 (Anthropic Official PPTX Principles)]:
1. 14개 전 슬라이드 무누락 100% 완전 구현 (Strict Completeness):
 - Slide 01(표지)부터 Slide 14(질의응답 Q&A)까지 단 1개의 슬라이드도 누락하거나 축약하지 마라.
 - 마지막 장표는 '엔지니어링 신뢰성 보증'이 아닌 [질의응답 (Q&A)]로 완벽히 종결하라.
 - 코드 중간에 `<!-- 나머지 슬라이드 동일 구조 생략 -->`, `// TODO`, `/* 생략 */` 같은 생략 코드를 작성하는 순간 실패로 간주한다. 14개 슬라이드 전수를 끝까지 온전하게 렌더링하라.
2. 크리스프 화이트 테마 100% 강제 (Crisp White Theme & Anti-Dark):
 - 표지(Slide 01)부터 질의응답(Slide 14)까지 전체 14개 장표를 순백색(#FFFFFF) 및 은은한 소프트 슬레이트(#F8FAFC) 기반의 [화이트 계열]로 일관되게 적용하라.
 - 슬라이드 배경에 어두운 다크 모드(Dark Mode, bg-slate-900 등)를 일절 사용하지 마라.
 - 순백색(#FFFFFF) 및 소프트 슬레이트(#F8FAFC) 캔버스(60%) + 백색 카드 서피스(#FFFFFF, 30%) + 1px 정밀 구조선(#E2E8F0) + 짙은 차콜(#0F172A) 본문 텍스트를 사용하여 인쇄 및 프로젝터 투사 시 최상의 시인성을 보장하라.
 - 기능적 액센트 컬러(에메랄드/오렌지/레드/블루)는 10% 비중으로만 사용하며, 타이틀 하단 장식용 밑줄선 등 구시대적 장식 요소는 전면 배제하라 (Anti-Clutter).
3. 폰트 패밀리 강제 고정 (Nanum Gothic & Noto Sans):
 - 한글 폰트(본문 및 제목): '나눔고딕 (Nanum Gothic)' 필수 고정 (`font-family: 'Nanum Gothic', sans-serif;`)
 - 영문 및 숫자/수치 폰트: 'Noto Sans (NATO SANS)' 필수 고정 (`font-family: 'Noto Sans', sans-serif;`)
 - BigNum 및 정량 지표 / 통계: 'JetBrains Mono' 또는 'Noto Sans' 고정 (`font-mono font-black`)
 - Google Fonts CDN 필수 삽입:
 `<link rel="preconnect" href="https://fonts.googleapis.com">`
 `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`
 `<link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&family=Noto+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">`
 - 기본 CSS 폰트 지정:
 `body { font-family: 'Noto Sans', 'Nanum Gothic', sans-serif; background-color: #F8FAFC; color: #0F172A; }`
 `h1, h2, h3, h4, .font-korean { font-family: 'Nanum Gothic', sans-serif; }`
 `p, span, .font-english { font-family: 'Noto Sans', 'Nanum Gothic', sans-serif; }`
 `.bignum, .stat-mono, code { font-family: 'JetBrains Mono', 'Noto Sans', monospace; }`
4. 16:9 와이드스크린 뷰포트 & 키보드 네비게이션:
 - 각 슬라이드는 1920×1080 비율(16:9)의 정밀 프레임으로 구성하며, 키보드 좌/우 방향키(←, →), 화면 하단 인디케이터 닷(Dot), 이전/다음 버튼으로 완벽 전환 지원.
 - 우측 상단/하단에 현재 슬라이드 번호(예: 08 / 14)와 상단 씬 프로그레스 바(Progress Bar)를 상시 표시하라.
5. 차트 종횡비 보호 (imageSizingContain) & 발표자 노트 'S'키 토글:
 - 문서에 명시된 차트 이미지(`outputs/figures/*.png`)는 `<img src="..." class="w-full h-full object-contain" />`로 감싸 축이나 글자가 왜곡되지 않도록 보호하라.
 - 발표자가 대본을 실시간으로 확인할 수 있도록 키보드 'S' 키를 누르거나 우측 하단 마이크 아이콘 클릭 시, 해당 슬라이드의 [발표 대본(Presenter's Script)]이 반투명 하단 시트(Bottom Sheet)로 토글되도록 인터랙션을 구현하라.
```

---

## 🎨 [Claude 빌더를 위한 전용 디자인 시스템 & 토큰 가이드]

### 1. Canvas Dimensions & Layout Frame

* **화면 비율**: `16:9 와이드스크린` (1920 × 1080px 기준, Slide 단위 W: 13.333" × H: 7.5")
* **기본 테마**: `크리스프 화이트 테마 (Crisp White & Minimalist Slate)` - 다크 모드 일절 배제
* **여백 규칙 (Safe Zone)**:
* Slide Container: `px-12 py-10 (48px 좌우 / 40px 상하 패딩)`
* Header Block: Top `0px`, Height `90px` (Kicker + Action Title + Context Banner)
* Body Content Canvas: Top `110px`, Height `560px`
* Footer Source Bar: Bottom `24px`, Height `24px`

### 2. Color Palette (Semantic 60-30-10 White Theme Tokens)

| 토큰명                   | Hex 코드    | Tailwind 클래스                                           | 적용 대상 & 시각적 비중                                |
| :----------------------- | :---------- | :-------------------------------------------------------- | :----------------------------------------------------- |
| **Pure White**     | `#FFFFFF` | `bg-white`                                              | 슬라이드 메인 캔버스 및 카드 서피스 (60% Base)         |
| **Soft Slate**     | `#F8FAFC` | `bg-slate-50`                                           | 보조 컨테이너 및 칩 배경 (30% Structure)               |
| **Crisp Border**   | `#E2E8F0` | `border-slate-200`                                      | 카드 외곽선 (1px solid 정밀 구조선)                    |
| **Deep Charcoal**  | `#0F172A` | `text-slate-900`                                        | 메인 헤드라인 및 본문 텍스트 (고대비 가독성)           |
| **Muted Slate**    | `#64748B` | `text-slate-500`                                        | 보조 캡션, 메타데이터, 출처 표기                       |
| **Danger Red**     | `#DC2626` | `text-red-600 / bg-red-50 / border-red-200`             | 403건 적체 피크, 리워크 루프, 긴급 지연 (10% Accent)   |
| **Warning Orange** | `#EA580C` | `text-orange-600 / bg-orange-50 / border-orange-200`    | 대기시간 90.5%, 인계 6.6배, OLS 병목 요인 (10% Accent) |
| **Success Green**  | `#059669` | `text-emerald-600 / bg-emerald-50 / border-emerald-200` | 전처리 100% 무손실, TO-BE 리드타임 단축 (10% Accent)   |
| **Brand Blue**     | `#2563EB` | `text-blue-600 / bg-blue-50 / border-blue-200`          | E형 100% 적중, 데이터 팩트, 프로세스 표준 (10% Accent) |

### 3. Typography & Hierarchy (폰트 계층 고정)

* **한글 본문 및 헤드라인 (Korean)**: `나눔고딕 (Nanum Gothic)` (`font-family: 'Nanum Gothic', sans-serif;`)
* **영문 및 일반 숫자 (English & Numbers)**: `Noto Sans (NATO SANS)` (`font-family: 'Noto Sans', sans-serif;`)
* **BigNum 및 정량 지표 (Stats & Code)**: `JetBrains Mono / Noto Sans` (`font-mono font-black tracking-tight`)
* **Action Title (헤드라인)**: `Nanum Gothic` 26~30pt ExtraBold (두괄식 문장, `text-slate-900`)
* **Kicker (카테고리 배지)**: `Noto Sans` 10~11pt Bold, Uppercase, Pill badge (`bg-slate-100 text-slate-700 border border-slate-200`)
* **BigNum (데이터 강조)**: `JetBrains Mono` 36~44pt Black (`font-black tracking-tight font-mono`)
* **Card Subtitle**: `Nanum Gothic` 13~15pt Bold Charcoal (`font-bold text-slate-900`)
* **Body Text**: `Nanum Gothic` 10.5~12pt Regular Slate (`text-slate-600 leading-relaxed`)

### 4. Component Rules for Claude (앤스로픽 공식 품질 기준)

1. 🚫 **줄글 나열 및 구시대적 밑줄선 금지**: 모든 정보는 `[BigNum + Pill Badge + Bold Header + Bullet Points]`가 결합된 정밀 카드 컴포넌트로 구조화하며, 타이틀 하단 장식용 밑줄선은 절대 사용하지 않는다.
2. 🖼️ **사전 렌더링 이미지 종횡비 보호 (`imageSizingContain`)**: 슬라이드에 지정된 `outputs/figures/*.png` 경로는 지정된 컨테이너에 `object-contain`으로 중앙 정렬 임베드하여 축과 텍스트 왜곡을 100% 방지한다.
3. 📐 **수치 앵커링 (BigNum)**: 수치(87.3%, 76.8h, 30.5h, 32.9h, 403건, 123건 등)는 텍스트 속에 파묻히지 않도록 대형 콜아웃 또는 별도 배지로 시각적 앵커링을 적용한다.
4. 🔒 **전 슬라이드 완전 렌더링 보증**: Slide 01부터 14(질의응답 Q&A)까지 단 하나의 생략도 허용하지 않으며, 전 장표의 레이아웃과 대본을 온전히 출력한다.

---

## 📑 [전체 14개 슬라이드 완결 아키텍처 맵]

|     번호     | 파트 구분             | 슬라이드 제목                                                                   | 과제 대응 질문    | 핵심 시각화 및 컴포넌트 에셋                                                                                                                                                                                                                                                                                                                  |
| :----------: | :-------------------- | :------------------------------------------------------------------------------ | :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **01** | Part 00. 인트로       | **프로젝트 표지 (Title Cover)**                                           | -                 | 화이트/슬레이트 미니멀 테크 + 3-Tier KPI 카드 스택                                                                                                                                                                                                                                                                                            |
| **02** | Part 00. 인트로       | **목차 (Table of Contents)**                                              | 전체 개요         | 4대 대단원 타일 그리드 네비게이터                                                                                                                                                                                                                                                                                                             |
| **03** | Part 00. 인트로       | **Executive Summary & 통괄 핵심 가설**                                    | 전체 요약         | 상단 명제 배너 + 하단 3단 핵심 가설 카드                                                                                                                                                                                                                                                                                                      |
| **04** | Part 01. 질문 1       | **원천 데이터 수사 프로파일링 및 결측치 2원화**                           | 질문 1            | 좌측 스탯 카드 + 우측 [`EDA-01.png`](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/EDA-01.png) + 3단 판정행                                                                                                                                                                                             |
| **05** | Part 01. 질문 1       | **5대 비정상 결측치 교정 및 도메인 인과 복원 (CASE 1~5)**                 | 질문 1            | 5단 가로형 인과 복원 파이프라인 스트립                                                                                                                                                                                                                                                                                                        |
| **06** | Part 01. 질문 1       | **전처리 무결성 검증 및 927건 분석 코호트 확립**                          | 질문 1            | 좌측 Before/07After 4x3 검증표 + 우측 코호트 분리 칩                                                                                                                                                                                                                                                                                          |
| **07** | Part 02. 질문 2       | **AS-IS 표준 프로세스 및 엔드투엔드(E2E) 경로**                           | 질문 2-1          | 상단 [`repair_process_map.png`](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/repair_process_map.png) + 하단 3단 실측 앵커 카드                                                                                                                                                                         |
| **08** | Part 02. 질문 2       | **거시 리드타임 분해: 실작업(9.5%) vs 대기(90.5%) 및 3대 병목**           | 질문 2-2 (병목)   | 좌측 [`slide08_macro_leadtime_breakdown.png`](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/slide08_macro_leadtime_breakdown.png) + 우측 3대 병목 카드                                                                                                                                                  |
| **09** | Part 02. 질문 2       | **제1대 병목: 접수 일정 조율 병목(1.9h)과 교차 인계(123건)의 6.6배 폭증** | 질문 2-2 (병목)   | 상단 [`slide09_reception_bottleneck_3panel.png`](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/slide09_reception_bottleneck_3panel.png) + 하단 3단 카드                                                                                                                                                 |
| **10** | Part 02. 질문 2       | **제2대 병목: 현장 국면 압도적 대기 76.8h & 403건 WIP 누적 적체**         | 질문 2-2 (병목)   | 상단 [`slide10_field_bottleneck_wip.png`](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/slide10_field_bottleneck_wip.png) + 하단 3단 동역학 카드                                                                                                                                                        |
| **11** | Part 02. 질문 2 & 2-3 | **소요시간 영향 요인 실증(OLS) 및 수리·리워크 병목**                     | 질문 2-3 & 2-2    | 좌측 [`slide11_regression_leadtime_drivers.png`](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/slide11_regression_leadtime_drivers.png) + 우측 [`slide11_repair_delay_rework.png`](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/slide11_repair_delay_rework.png) |
| **12** | Part 02 & 03 발단     | **핵심 문제 규명: 사전 적합성 87.3%와 정보 해상도 한계**                  | 질문 2-2 & 3 발단 | Card 1 [`slide12_intake_matching_donut.png`](file:///c:/Users/nextb/.gemini/antigravity-ide/scratch/puzzle_data/outputs/figures/slide12_intake_matching_donut.png) + Card 2 해상도 관행 + Card 3 CAPA 경감                                                                                                                                   |
| **13** | Part 03. 질문 3       | **TO-BE 실행 전략: 품목 준비 기간 단축 & E형 정밀검사 리워크 방지**       | 질문 3 (전략)     | Card 1 사진 체크리스트 + Card 2 E형 정밀검사 + Card 3 번들 키트                                                                                                                                                                                                                                                                               |
| **14** | Part 04. 마무리       | **질의응답 (Q&A)**                                                        | -                 | 좌측 프로젝트 핵심 요약 3단 카드 + 우측 Q&A 대형 히어로 박스                                                                                                                                                                                                                                                                                  |

---

# 📋 [슬라이드별 초정밀 상세 빌드 명세 (Slide 01 ~ Slide 14)]

---

### Slide 01. 표지 (Title Cover)

* **DOM Layout & Grid**: `Hero-Cover-Split` (배경: `bg-slate-50 border border-slate-200`, 2-Column Grid: 좌측 65% + 우측 35%)
* **Kicker Pill**: `inline-flex px-3.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200` ➔ `"채용 과제 전형 최종 보고서"`
* **Action Headline**: `"프로세스 마이닝 기반\n공공임대주택 수리 프로세스\n진단 및 운영 최적화 방안"` (`text-4xl sm:text-5xl font-black text-slate-900 leading-tight`)
* **Sub-headline Context**: `"5대 무손실 전처리, 실사 대기 병목(76.8h) 원인 규명 및 3대 데이터 기반 TO-BE 전략"` (`text-lg text-slate-600 font-medium mt-4`)
* **Footer Meta**: `"퍼즐데이터 수리 프로세스 데이터 분석 과제 | 제출일 2026. 10. 27"` (`text-xs text-slate-400 font-mono`)
* **Right 3-Tier KPI Card Stack** (우측 세로 3단 카드: `flex flex-col gap-4`):

1. **Card 1 (원천 규모)**:

* `bg-white border border-slate-200 shadow-sm rounded-xl p-4`
* `BigNum: "13,262행"` (`text-3xl font-extrabold text-blue-600 font-mono`)
* `Label: "전체 이벤트 로그 · 1,000 케이스 무손실 복원"` (`text-slate-600 text-xs mt-1`)
* `Pill: "#ProcessMining"` (`text-xs text-blue-700 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded`)

2. **Card 2 (핵심 병목)**:

* `bg-white border border-orange-200 shadow-sm rounded-xl p-4`
* `BigNum: "90.5%"` (`text-3xl font-extrabold text-orange-600 font-mono`)
* `Label: "리드타임(105.9h) 중 공정 간 단순 대기시간"` (`text-slate-600 text-xs mt-1`)
* `Pill: "#LeadTime_Wait"` (`text-xs text-orange-700 bg-orange-50 border border-orange-200 px-2 py-0.5 rounded`)

3. **Card 3 (개선 목표)**:

* `bg-white border border-emerald-200 shadow-sm rounded-xl p-4`
* `BigNum: "▼ 65%"` (`text-3xl font-extrabold text-emerald-600 font-mono`)
* `Label: "TO-BE 1회 방문 패스트트랙 리드타임 감축 목표"` (`text-slate-600 text-xs mt-1`)
* `Pill: "#TO-BE_ROI"` (`text-xs text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded`)
* **Presenter's Script (발표 대본)**:

> "안녕하십니까, 퍼즐데이터 수리 프로세스 데이터 분석 결과 발표를 맡은 지원자입니다. 본 보고서는 네덜란드 공공임대주택 1,000건의 수리 로그를 바탕으로, 단순 통계를 넘어 프로세스 마이닝 관점에서 대기시간 약 90%의 구조적 원인을 밝히고 실질적 개선안을 제시합니다."

* **수치 검증 근거**: E2E 전체 리드타임(105.9h) 중 대기 95.8h = 90.5% (`analysis.sql` Step 2-1).

---

### Slide 02. 목차 (Table of Contents)

* **DOM Layout & Grid**: `4-Column-Navigator` (`grid grid-cols-4 gap-6 items-stretch`)
* **Category Kicker**: `AGENDA · 전체 개요`
* **Action Headline**: `"원천 데이터 전처리부터 TO-BE 전략까지, 4개 파트로 보고합니다"`
* **Navigation 4-Tiles** (4개 독립 네비게이션 카드: `bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between`):

1. **Tile 01 (Part 01. 질문 1)**:

* `Large Index: "01"` (`text-4xl font-black text-slate-300 font-mono`)
* `Part Pill: "질문 1"` (`bg-blue-100 text-blue-800 text-xs font-bold px-2 py-0.5 rounded-full`)
* `Title: "데이터 진단 및 전처리"` (`text-lg font-bold text-slate-900 mt-2`)
* `Bullets`:

- `• 13,262행 이벤트 로그 수사 프로파일링`
- `• 도메인 인과 기반 5대 결측치 100% 무손실 복원`
- `• 시간 역전 0건 입증 및 927건 코호트 확립`

2. **Tile 02 (Part 02. 질문 2)**:

* `Large Index: "02"` (`text-4xl font-black text-orange-300 font-mono`)
* `Part Pill: "질문 2"` (`bg-orange-100 text-orange-800 text-xs font-bold px-2 py-0.5 rounded-full`)
* `Title: "프로세스 마이닝 심층 분석"` (`text-lg font-bold text-slate-900 mt-2`)
* `Bullets`:

- `• AS-IS E2E 프로세스 표준 모델 (맵)`
- `• 3대 대기 병목 분해 (접수 6.6배 vs 현장 76.8h)`
- `• OLS 다중회귀 영향인자 실증 & 수리·리워크`

3. **Tile 03 (Part 03. 질문 3)**:

* `Large Index: "03"` (`text-4xl font-black text-emerald-300 font-mono`)
* `Part Pill: "질문 3"` (`bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded-full`)
* `Title: "프로세스 최적화 방안"` (`text-lg font-bold text-slate-900 mt-2`)
* `Bullets`:

- `• 사전 적중률 87.3%와 정보 해상도 한계 규명`
- `• 보수적 E형 직행 ➔ 실사 대기 20%(-15.4h) 단축`
- `• 체크리스트 고도화 & E형(85%) 정밀검사 방지`

4. **Tile 04 (Part 04. 마무리)**:

* `Large Index: "04"` (`text-4xl font-black text-slate-300 font-mono`)
* `Part Pill: "Q & A"` (`bg-slate-100 text-slate-800 text-xs font-bold px-2 py-0.5 rounded-full`)
* `Title: "질의응답 (Q&A)"` (`text-lg font-bold text-slate-900 mt-2`)
* `Bullets`:

- `• 프로젝트 핵심 진단 및 3대 전략 총괄`
- `• 데이터 기반 프로세스 혁신 총평`
- `• 질의응답 (Q&A)`

* **Presenter's Script (발표 대본)**:

> "오늘 발표는 4개 파트로 진행됩니다. 질문 1의 데이터 무손실 전처리를 거쳐, 질문 2의 프로세스 병목과 원인을 규명하고, 질문 3에서 실질적 개선안과 정량적 ROI를 제시하며 마무리하겠습니다."

---

### Slide 03. Executive Summary & 프로젝트 통괄 두괄식 어젠다

* **DOM Layout & Grid**: `TopBanner-Bottom3Cards` (상단 명제 배너 + 하단 3단 핵심 가설 카드: `grid grid-cols-3 gap-6`)
* **Category Kicker**: `EXECUTIVE SUMMARY · 통괄 핵심 어젠다`
* **Action Headline**: `"현장의 '대기시간'을 줄이고, 이해관계자 간의 '소통'을 통제하면 프로세스 리드타임을 획기적으로 개선할 수 있다"`
* **Top Insight Banner**:
* `bg-slate-900 text-white rounded-xl p-5 border-l-4 border-orange-500 shadow-md flex items-center justify-between`
* `Left Text: "공정 리드타임 지연의 본질은 작업자 태만이 아닌 '공정 간 단순 대기(90.5%)'와 '비실시간 접수 소통 공백'에 있다"`
* `Right Stat: "E2E 리드타임 105.9시간 중 순수 대기 95.8시간"` (`text-orange-400 font-mono font-bold`)
* **Bottom 3-Columns (핵심 가설 3단계 전개)**:

1. **Card 1 (Step 1. 원천 진단)**:

* `bg-white rounded-2xl p-6 border border-slate-200 shadow-sm`
* `Step Badge: "Step 01" (Navy Pill)` | `Tag: "데이터 무결성"`
* `BigNum: "13,262행"` (`text-4xl font-extrabold text-slate-900 font-mono mt-3`)
* `Sub: "100% 무손실 복원 완결"`
* `Bullets`:

- `• 임의 행 삭제 0건 (13,262행 전수 보존)`
- `• 비정상 시스템 에러 20행(0.15%) 인과 복원`
- `• 751건(75.1%) 대규모 접수 모수로 강건성 확보`

2. **Card 2 (Step 2. 병목 가설)**:

* `bg-white rounded-2xl p-6 border border-orange-200 shadow-sm`
* `Step Badge: "Step 02" (Orange Pill)` | `Tag: "병목 실증"`
* `BigNum: "대기 90.5%"` (`text-4xl font-extrabold text-orange-600 font-mono mt-3`)
* `Sub: "현장 국면에 대기의 98% 편중"`
* `Bullets`:

- `• 실사 방문 대기(76.8h)가 현장 시간 78.2% 독점`
- `• 유입(134건) vs 기사 CAPA(68건) 불균형 ➔ 403건 적체`
- `• 비실시간 채널 인계(123건) 발생 시 6.6배 지연`

3. **Card 3 (Step 3. 개선 방향)**:

* `bg-white rounded-2xl p-6 border border-emerald-200 shadow-sm`
* `Step Badge: "Step 03" (Green Pill)` | `Tag: "TO-BE 솔루션"`
* `BigNum: "소통 통제"` (`text-4xl font-extrabold text-emerald-600 font-mono mt-3`)
* `Sub: "+ 대기시간 원천 소멸"`
* `Bullets`:

- `• 사전 적합성 87.3% 활용 ➔ 헛걸음 실사 우회 직행`
- `• E형만 직행해도 대기 20%(-15.4h, OLS -17.2h) 단축`
- `• E-1/E-2(리워크 85%) 정밀검사로 10일 루프 차단`

* **Presenter's Script (발표 대본)**:

> "본 분석을 관통하는 핵심 가설은 명확합니다. 수리가 늦어지는 것은 현장 기사가 느려서가 아니라, 공정 사이의 단순 대기와 접수 단계의 비동기 소통 지연 때문입니다. 이 두 가지를 통제하여 전체 프로세스를 획기적으로 개선하는 여정을 보여드리겠습니다."

---

### Slide 04. [질문 1] 원천 데이터 수사 프로파일링 및 결측치 2원화 (Before Profiling)

* **DOM Layout & Grid**: `Split-LeftCard-RightContent` (좌측 메타 35% + 우측 차트 & 3단 판정행 65%)
* **Category Kicker**: `Part 01 · 질문 1 | Before Profiling`
* **Action Headline**: `"정상 결측은 그대로 보존하고, 시스템 에러 20행(0.15%)만 수사 타겟으로 특정했다"`
* **Left Meta Stat Card** (`bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between`):
* `Top Header: "원천 데이터셋 프로파일"` (`text-sm font-bold text-slate-500 uppercase`)
* `Stat Block 1`: `BigNum: "13,262"` (`text-4xl font-extrabold text-slate-900 font-mono`) ➔ `Label: "원천 이벤트 행"`
* `Stat Block 2`: `BigNum: "1,000"` (`text-4xl font-extrabold text-slate-900 font-mono`) ➔ `Label: "총 관리 케이스"`
* `Stat Block 3`: `BigNum: "13개"` (`text-4xl font-extrabold text-slate-900 font-mono`) ➔ `Label: "전체 속성 수"`
* `Bottom Callout`:
* `bg-slate-50 p-4 rounded-xl border border-slate-200`
* `Text: "1건 1행의 정형 데이터가 아닌 세부 공정 단위로 기록되는 이벤트 로그(Event Log)의 특성 반영 필수"` (`text-xs text-slate-500 leading-relaxed`)
* **Right Visual Asset & 판정 3-Rows** (우측 배치):
* **Top Visual Image**:
* Path: `outputs/figures/EDA-01.png`
* Style: `w-full h-64 rounded-xl border border-slate-200 object-contain bg-slate-50`
* **Bottom 3-Row Verdict Cards** (`grid grid-rows-3 gap-2 mt-4`):

1. **Row 1 (정상 결측 - 무죄 판정)**:

* `flex items-center justify-between p-3 rounded-lg bg-emerald-50/60 border border-emerald-200`
* `Left: Pill "정상 결측 (무죄)" (Green) + "구조적 Null 86.0~93.0% · 7개 속성 (12,335행)"` (`font-bold text-sm text-slate-800`)
* `Right: "후속 공정이 없어 비어 있는 값 ➔ 임의 대체 없이 100% 보존"` (`text-xs text-slate-500`)

2. **Row 2 (비정상 결측 - 유죄 판정)**:

* `flex items-center justify-between p-3 rounded-lg bg-red-50/60 border border-red-200`
* `Left: Pill "비정상 결측 (유죄)" (Red) + "시스템 에러 0.015~0.098% · 5개 속성 (20행)"` (`font-bold text-sm text-slate-800`)
* `Right: "필수 값 누락 ➔ 18개 케이스, 단 20행만 정밀 복원 타겟 특정"` (`text-xs text-red-600 font-semibold`)

3. **Row 3 (진공 구간 - 판정 객관성)**:

* `flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200`
* `Left: Pill "진공 구간 (Void Zone)" (Gray) + "0.1% ~ 86.0% 구간 컬럼 0개"` (`font-bold text-sm text-slate-800`)
* `Right: "완벽한 양극단 이봉분포 ➔ 정상/비정상 판별의 객관성 및 신뢰성 입증"` (`text-xs text-slate-500`)
* **Source Bar**: `출처: repair2.csv 원천 프로파일링 (EDA-01) · 20행 = 5개 속성 결측이 포함된 18개 케이스의 실제 행`
* **Presenter's Script (발표 대본)**:

> "데이터를 열어보았을 때 가장 먼저 확인한 것은 구조였습니다. 본 데이터는 공정마다 행이 쌓이는 이벤트 로그로, 90% 안팎의 결측치는 후속 수리가 발생하지 않아 생긴 자연스러운 정상 결측입니다. 반면 필수 속성임에도 비어 있는 값은 13,262행 중 단 20행에 불과했습니다. 이 20행만을 정밀 복원 타겟으로 특정했습니다."

---

### Slide 05. [질문 1] 5대 비정상 결측치 교정 및 도메인 인과 복원 (CASE 1 ~ CASE 5)

* **DOM Layout & Grid**: `Vertical-5Strip-BottomBadges` (5단 가로형 인과 복원 스트립 + 하단 3대 무결성 배지)
* **Category Kicker**: `Part 01 · 질문 1 | CASE 1 ~ 5 도메인 인과 복원`
* **Action Headline**: `"행 삭제와 단순 대체 없이, 업무 인과 근거로 20행을 100% 무손실 복원했다"`
* **5-Case Horizontal Strip Table** (5단 가로형 테이블: `flex flex-col gap-2.5 my-4`):

1. **CASE 1 (taskID 2건 결측)**:

* `Strip Row: grid grid-cols-12 gap-3 items-center p-3.5 bg-white rounded-xl border border-slate-200 shadow-sm`
* `Col 1~3: Badge "CASE 1 taskID" (결측 2건)` (`text-xs font-bold px-2.5 py-1 rounded bg-slate-100 text-slate-800`)
* `Col 4~8: "contact 속성은 FirstContact에만 기록되는 고유 도메인 속성 (Cell 18)"` (`text-sm text-slate-600`)
* `Col 9~12: "➔ FirstContact / InformClientSurvey 확정 복원"` (`text-sm font-bold text-emerald-600`)

2. **CASE 2 (originator 2건 결측)**:

* `Strip Row: grid grid-cols-12 gap-3 items-center p-3.5 bg-white rounded-xl border border-slate-200 shadow-sm`
* `Col 1~3: Badge "CASE 2 originator" (결측 2건)` (`text-xs font-bold px-2.5 py-1 rounded bg-slate-100 text-slate-800`)
* `Col 4~8: "동일 작업의 시작(start)-완료(complete) 담당자 100.0% 일치 규칙 (Cell 18)"` (`text-sm text-slate-600`)
* `Col 9~12: "➔ 짝 이벤트 담당자(Anne, Paul) 상호 승계"` (`text-sm font-bold text-emerald-600`)

3. **CASE 3 (eventtype 5건 결측)**:

* `Strip Row: grid grid-cols-12 gap-3 items-center p-3.5 bg-white rounded-xl border border-slate-200 shadow-sm`
* `Col 1~3: Badge "CASE 3 eventtype" (결측 5건)` (`text-xs font-bold px-2.5 py-1 rounded bg-slate-100 text-slate-800`)
* `Col 4~8: "기간 작업 1:1 페어(start→complete 추적) 및 마일스톤 단독 발생 (Cell 20)"` (`text-sm text-slate-600`)
* `Col 9~12: "➔ 1:1 페어 3건 + 마일스톤 2건 100% 복원"` (`text-sm font-bold text-emerald-600`)

4. **CASE 4 (date 879건 오기입 & 결측)**:

* `Strip Row: grid grid-cols-12 gap-3 items-center p-3.5 bg-white rounded-xl border border-slate-200 shadow-sm`
* `Col 1~3: Badge "CASE 4 date" (879건 | 결측 13+오기입 866)` (`text-xs font-bold px-2.5 py-1 rounded bg-orange-100 text-orange-800`)
* `Col 4~8: "시각 정상 859건 선별, 선·후행 업무 순서 구간 제약(Interval Bounds) 적용 (Cell 51·53)"` (`text-sm text-slate-600`)
* `Col 9~12: "➔ 단일 후보 640건 + 앵커 최근접 219건 매핑 (1970년 통일)"` (`text-sm font-bold text-emerald-600`)

5. **CASE 5 (time 28건 파손 & 751건 모수 확장)**:

* `Strip Row: grid grid-cols-12 gap-3 items-center p-3.5 bg-white rounded-xl border border-slate-200 shadow-sm`
* `Col 1~3: Badge "CASE 5 time" (28건 | 결측 13+더미 15)` (`text-xs font-bold px-2.5 py-1 rounded bg-orange-100 text-orange-800`)
* `Col 4~8: "표본 34% 한계 극복 ➔ 접수 정상 표본 751건(75.1%) 확보 (중앙값 4.0분) (Cell 77·81)"` (`text-sm text-slate-600`)
* `Col 9~12: "➔ 정상 자정 7건 보존 + 기준 앵커 역산 21건 (역전 0건)"` (`text-sm font-bold text-emerald-600`)
* **Bottom 3-Performance Badges** (`grid grid-cols-3 gap-4 mt-2`):

- `Badge 1: bg-emerald-50 border border-emerald-200 p-3 rounded-xl flex items-center gap-3` ➔ `Title: "데이터 무손실"` | `Sub: "임의 삭제 0건 · 13,262행 100% 완전 보존"`
- `Badge 2: bg-emerald-50 border border-emerald-200 p-3 rounded-xl flex items-center gap-3` ➔ `Title: "통계적 강건성"` | `Sub: "표본 34% 축소 극복 ➔ 751건(75.1%) 대규모 모수 확보"`
- `Badge 3: bg-emerald-50 border border-emerald-200 p-3 rounded-xl flex items-center gap-3` ➔ `Title: "인과 무결성"` | `Sub: "시간 역전 0건 달성 · 927건 정상 분석 코호트 확립"`

* **Source Bar**: `출처: analysis.ipynb Cell 18·20·51·53·77·81, analysis.sql`
* **Presenter's Script (발표 대본)**:

> "복원 시 단 한 행도 버리지 않았습니다. 시작-완료 담당자의 100% 일치성, 태스크 고유 속성을 활용했고, 일시는 표본 34% 축소 한계를 극복하여 확보한 751건 정상 모수의 대표값을 앵커로부터 역산 적용했습니다. 덕분에 시간 역전 0건의 완벽한 데이터셋을 완성했습니다."

---

### Slide 06. [질문 1] 전처리 무결성 검증 및 데이터 기반 운영 특성 발굴 (After Profiling)

* **DOM Layout & Grid**: `Split-LeftTable-Right2Cards` (좌측 4x3 무결성 검증표 50% + 우측 운영 특성 발굴 2단 카드 50%: `grid grid-cols-2 gap-6`)
* **Category Kicker**: `Part 01 · 질문 1 | After Profiling & Operational Discovery`
* **Action Headline**: `"시간 역전 0건의 무결성을 입증했고, 24시간 상시 접수와 현장 무경계 통합 풀(Shared Pool)을 규명했다"`
* **Left Verification Table (Before vs After 4x3 매트릭스 - 무결성 보증)**:
* `Table Container: bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col justify-between`
* `Header: ["검증 항목" (text-left), "Before (원천)", "After (정제 무결성)" (text-emerald-600)]`
* `Row 1: ["총 이벤트 행 수", "13,262행", "13,262행 (100% 완전 보존)"]`
* `Row 2: ["필수 속성 결측", "20건 (0.15%)", "0건 (100% 인과 복원 완료)"]`
* `Row 3: ["일자 연도 오기입", "866건 (미래연도)", "0건 (1970년 정상 주기 통일)"]`
* `Row 4: ["공정 간 시간 역전", "음수 소요시간 존재", "0건 (3,711개 페어 양수 검증)"]`
* `Table Callout Banner (하단 부착): "전처리 전 구간 무결성 100% 입증 ➔ 임의 행 삭제 0건 (완전무결성 확립)" (bg-emerald-50 text-emerald-800 font-bold p-3 text-center text-sm rounded-xl m-3)`
* **Right Operational Discovery (데이터가 밝혀낸 수리회사 2대 운영 진실 - 2단 카드)**:

1. **Card 1: [근무 형태] 24시간 무중단 상시 접수 체제 (야간 방치 가설 완벽 기각)**

* `Card Container: bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between`
* `Badge: "01 근무 형태 진실" (Blue Pill)` | `Title: "24시간 상시 접수 & 야간 방치 가설 기각"` (`font-bold text-base text-slate-900 mt-1`)
* `BigNum Stat: "0시 ~ 23시 전 시간대 활동"` (`text-2xl font-extrabold text-blue-600 font-mono my-2`)
* `Key Insights`:

- `• 0시부터 23시까지 전 시간대 FirstContact 및 접수원(Dian/Monica) 활동 입증 (analysis.sql L1140~L1195)`
- `• 야간 접수 건 역시 정상 처리 ➔ 리드타임 지연 원인은 '영업외 방치'가 아닌 '비실시간 일정 핑퐁 마찰'`

2. **Card 2: [조직 구조] '지역 전담제' 착시 규명 & 현장 무경계 전사 단일 풀(Shared Pool) 실증**

* `Card Container: bg-white rounded-2xl p-5 border border-orange-200 shadow-sm flex flex-col justify-between`
* `Badge: "02 조직 구조 진실" (Orange Pill)` | `Title: "'지역 전담제' 착시 해소 및 현장 무경계 배정 실증"` (`font-bold text-base text-slate-900 mt-1`)
* `BigNum Stat: "기사 배정비 46.9% : 53.1% 수렴"` (`text-2xl font-extrabold text-orange-600 font-mono my-2`)
* `Key Insights`:

- `• [접수 착시 해소]: 890채 중 1회 접수가 96.1%(855채)에 달해 지역 분담처럼 보였으나, 재접수 35채 추적 시 62.9%(22채)가 타 상담원에게 무작위 교차 연결됨 (이전 담당자 복귀율 8.6%에 불과, analysis.sql L772~L776)`
- `• [현장 스모킹 건]: 접수원(Dian vs Monica)별 현장 기사 출동 비중이 전체 평균(46.9% : 53.1%)에 완벽 수렴 (Anne 50:50, Edd 51.8:48.2, John 46.2:53.8, 외주 FixIt/DoIt 전 지역 출동, L782~L825)`
- `• [결론]: 접수단부터 현장까지 특정 구역 제한이 없는 '전사 단일 통합 공유 큐(Single Shared Pool)' 운영 확증`

* **Source Bar**: `출처: repair_cleaned.csv (13,262행 전수), analysis.sql L760~828 (기사 배정비), L1138~1202 (24시간 접수 분포)`
* **Presenter's Script (발표 대본)**:

> "5대 전처리를 완료한 결과, 단 한 건의 결측과 시간 역전도 없는 완전무결한 13,262행 정제 데이터셋이 완성되었습니다. 특히 데이터 수사 과정에서 수리회사의 2대 운영 진실을 발굴했습니다.
> 첫째, 상담원들은 24시간 전 시간대 접수를 처리하고 있어 야간 방치로 인한 지연 가설은 기각되었습니다.
> 둘째, 단발성 접수가 96.1%에 달해 겉으로는 접수원이 지역을 분담하는 것처럼 보였으나, 재접수 건의 62.9%가 교차 인입되었고, 무엇보다 현장 기사들의 출동 비중이 50:50으로 완벽히 수렴하여 접수와 현장 모두 구역 제한 없는 '전사 단일 통합 풀(Shared Pool)'로 운영되고 있음을 실증했습니다.
> 이러한 단일 풀 운영 환경을 바탕으로, 이제 질문 2의 기준 프로세스 모델에서 실제 수리 작업이 어떻게 단방향으로 흘러가는지 본격적으로 규명하겠습니다."

---

### Slide 07. [질문 2-1] AS-IS 기준 프로세스 모델 (Baseline)

* **DOM Layout & Grid**: `TopImage-Bottom3Cards` (상단 와이드 프로세스 맵 58% + 하단 3단 실측 앵커 카드 42%)
* **Category Kicker**: `Part 02 · 질문 2-1 | AS-IS 기준 프로세스 모델`
* **Action Headline**: `"단방향 에스컬레이션과 병렬 정산이 입증된 E2E 기준 프로세스 모델을 확립했다"`
* **Top Visual Canvas** (`w-full h-80 rounded-2xl border border-slate-200 bg-slate-50 p-3 shadow-sm flex items-center justify-center`):
* **Visual Asset Image**:
* Path: `outputs/figures/process_map_crop.png`
* Style: `w-full h-full object-contain`
* Note: `사전 렌더링된 공식 고화질 맵 에셋 임베드 (PPT 내장 도형/차트 엔진 생성 절대 금지)`
* **Bottom 3-Columns (공정 국면별 3대 실측 앵커 카드)** (`grid grid-cols-3 gap-5 mt-4`):

1. **Card 1 (01 접수 국면)**:

* `bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "01 접수 국면" (Blue Pill)` | `Title: "오접수 격리 & 시스템 앵커"` (`font-bold text-base text-slate-900 mt-1`)
* `Middle Bullets`:

- `• FirstContact 1,000건 중 73건(7.3%) 타 기관 관할 조기 격리`
- `• 일정 조율 직후 InformClientSurvey가 0초에 자동 발송`
- `• 접수 국면 공식 종료 앵커(기준점)로 확립`

* `Bottom Tag`: `text-xs text-blue-600 font-mono font-semibold` ➔ `기준선: RepairReady 927건 확정`

2. **Card 2 (02 현장 국면)**:

* `bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "02 현장 국면 (단방향)" (Orange Pill)` | `Title: "역류 0건 & 완료 커밋 앵커"` (`font-bold text-base text-slate-900 mt-1`)
* `Middle Bullets`:

- `• 즉시수리 ➔ 사내수리 ➔ 외주수리로만 전이 (단방향 에스컬레이션)`
- `• 외주(DoIt/FixIt) 이관 후 사내 역류 케이스 0건 (0.0%)`
- `• 사내/외주 기사의 완료 커밋 시 RepairReady(927건) 자동 발행`

* `Bottom Tag`: `text-xs text-orange-600 font-mono font-semibold` ➔ `완료 확증: 수리 완료 즉시 정산 이관`

3. **Card 3 (03 정산 국면)**:

* `bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "03 정산 국면 (병렬 AND)" (Emerald Pill)` | `Title: "대칭 병렬 & 완벽한 AND-Join"` (`font-bold text-base text-slate-900 mt-1`)
* `Middle Bullets`:

- `• 고객 통보 선행 50.6%(469건) vs 재무 전송 선행 49.2%(456건)`
- `• 두 작업이 대칭적으로 선행하는 완벽한 병렬(AND) 구조 입증`
- `• TicketReady는 선행 0건, 후행 완료 시각과 99.8%(925건) 일치 종결`

* `Bottom Tag`: `text-xs text-emerald-600 font-mono font-semibold` ➔ `시스템 자동화: 대기시간 0.0시간`
* **Source Bar**: `출처: repair_cleaned.csv 프로세스 맵 마이닝 (노드 이벤트 기준 13,262행, 케이스 기준 927건 코호트 전수)`
* **Presenter's Script (발표 대본)**:

> "상세 병목 분석에 앞서, 모든 분석의 기준선이 될 'E2E 기준 프로세스 모델'입니다. 이 모델은 데이터의 3가지 명확한 실측 근거를 바탕으로 도출되었습니다.
> 첫째, 접수 단계는 1,000건 중 관할 외 73건의 조기 이탈과 시스템 자동 알림 앵커로 경계가 확립되었습니다.
> 둘째, 현장 수리 흐름은 철저한 단방향 에스컬레이션입니다. 사내 기사는 물론 외주 기사 역시 수리를 마친 뒤 완료 커밋을 하면 시스템이 RepairReady를 발송합니다. 외주로 넘어간 후 사내로 되돌아온 역류 케이스는 단 0건입니다.
> 셋째, 정산 공정은 고객 통보와 재무 처리가 50.6% 대 49.2%로 대칭 선행하는 병렬 구조이며, 최종 티켓 마감은 늦게 끝난 시각과 99.8% 일치하여 0초에 자동 종결됩니다.
> 이처럼 검증된 기준 지도를 토대로, 다음 장부터 90.5%의 대기시간이 어디서 발생하는지 거시적 분해로 들어가겠습니다."

---

### Slide 08. [질문 2-2] 거시 리드타임 분해: 실작업(9.5%) vs 대기(90.5%) 및 3대 병목

* **DOM Layout & Grid**: `TopSplit-ChartStats-Bottom3Cards` (상단 차트 60% + 상단 KPI 스탯 40% + 하단 3대 병목 카드 3단 그리드)
* **Category Kicker**: `Part 02 · 질문 2-2 | 거시 리드타임 분해`
* **Action Headline**: `"리드타임 105.9시간의 90.5%는 공정 간 단순 대기이며, 98.0%가 현장 국면에 집중된다"`
* **Top Split Container** (`grid grid-cols-12 gap-5 mb-4`):
* **Left Visual Asset (7 cols)**:
* Image Path: `outputs/figures/slide08_macro_leadtime_breakdown.png`
* Container: `w-full h-64 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm flex items-center justify-center`
* Style: `w-full h-full object-contain`
* **Right KPI Stack (5 cols)** (`flex flex-col gap-3 justify-between`):
* **KPI Card 1 (단순 대기 90.5%)**:
* `bg-orange-50/60 border border-orange-200 rounded-xl p-4 flex items-center justify-between`
* `Left`: `Pill "E2E 전체 대기" (Orange)` ➔ `Label: "공정 간 순수 대기시간"` (`text-xs text-slate-500 font-medium`)
* `Right`: `BigNum: "90.5%"` (`text-4xl font-extrabold text-orange-600 font-mono`) | `Sub: "95.8h / 105.9h"` (`text-xs text-orange-700/80 font-mono text-right`)
* **KPI Card 2 (현장 집중 98.0%)**:
* `bg-red-50/60 border border-red-200 rounded-xl p-4 flex items-center justify-between`
* `Left`: `Pill "현장 국면 편중" (Red)` ➔ `Label: "대기시간 현장 독점도"` (`text-xs text-slate-500 font-medium`)
* `Right`: `BigNum: "98.0%"` (`text-4xl font-extrabold text-red-600 font-mono`) | `Sub: "현장 93.9h / 전체 95.8h"` (`text-xs text-red-700/80 font-mono text-right`)
* **KPI Card 3 (정산 대기 0.0h)**:
* `bg-emerald-50/60 border border-emerald-200 rounded-xl p-3 flex items-center justify-between`
* `Left`: `Pill "정산 자동화" (Green)` ➔ `Label: "정산 대기 0.0시간"` (`text-xs text-slate-600 font-medium`)
* `Right`: `Text: "시스템 100% 자동 처리 (5.5h)"` (`text-xs font-bold text-emerald-700`)
* **Bottom 3-Bottleneck Cards** (`grid grid-cols-3 gap-5`):

1. **Card 1 (제1대 병목: 접수 일정 조율)**:

* `bg-white rounded-2xl p-4 border border-slate-200 shadow-sm`
* `Header`: `Badge: "01 접수 병목"` | `Title: "일정 조율 대기 1.9h"` (`font-bold text-sm text-slate-900`)
* `Bullets`:

- `• 전화·대면(479건): 15분 내 즉시 완결 (지연율 0%)`
- `• 웹·우편(448건): 비동기 회신 핑퐁으로 일정 지체`
- `• 교차 인계 123건 발생 시 6.6배 폭증 (1.2h ➔ 7.9h)`

2. **Card 2 (제2대 병목: 실사 방문 대기 1위 🚨)**:

* `bg-white rounded-2xl p-4 border-2 border-red-500/60 shadow-sm`
* `Header`: `Badge: "02 현장 1위 병목 🚨" (Red Pill)` | `Title: "실사 방문 대기 76.8h"` (`font-bold text-sm text-red-600`)
* `Bullets`:

- `• 현장 소요시간 98.3h 중 78.2% 독점 (압도적 1위)`
- `• 일일 유입 134건 vs 기사 실사 CAPA 68건 (소화율 51%)`
- `• 매일 66건 누적 ➔ 피크 시 403건 미처리 적체(WIP)`

3. **Card 3 (제3대 병목: 수리 착수 & 하자 루프)**:

* `bg-white rounded-2xl p-4 border border-slate-200 shadow-sm`
* `Header`: `Badge: "03 현장 수리 병목"` | `Title: "자재 대기 30.5h & 하자 루프"` (`font-bold text-sm text-slate-900`)
* `Bullets`:

- `• 즉시·외주 대기 0.0h, 사내수리만 부품 대기 30.5h`
- `• 하자 재방문 26건 발생 ➔ 평균 +32.9시간 추가 대기`
- `• 재수리 시 최대 10.1일(총 171.6h) 장기 억류 발생`

* **Source Bar**: `출처: analysis.sql 2절, slide08_macro_leadtime_breakdown · 정산 5.5h는 100% 시스템 자동 처리 (대기 0.0h)`
* **Presenter's Script (발표 대본)**:

> "수리 프로세스가 지연되는 진짜 원인은 무엇일까요? 기사가 작업을 느리게 해서일까요? 데이터를 쪼개보니 완전히 달랐습니다.
> 전체 105.9시간(약 4.4일) 중 실작업 시간은 10.1시간(9.5%)에 불과하며, 나머지 95.8시간(90.5%)은 공정 사이에서 멈춰 서 있는 단순 대기시간이었습니다. 특히 정산 국면은 인간 개입 없이 시스템이 100% 자동 처리하므로 대기가 0시간이며, 대기 95.8시간의 98.0%가 '현장 국면'에 집중되어 있었습니다.
> 이 대기시간의 발원지를 3대 병목으로 정리했습니다. 첫째, 웹·우편의 비동기 소통 부재로 일정이 늘어지는 '일정 조율 병목(1.9h)'. 둘째, 현장 국면의 78%가 쏠려 있는 압도적 1위의 '실사 방문 대기 병목(76.8h)'. 셋째, 사내 수리 시 자재 조달과 재작업으로 인한 '수리 준비 대기(30.5h) 및 하자 루프(최대 10일)'입니다.
> 그렇다면 프로세스의 첫 관문인 접수 국면에서 왜 6.6배의 시간 폭증이 일어났는지, 다음 장에서 살펴보겠습니다."

---

### Slide 09. [질문 2-2] 제1대 병목: 접수 일정 조율 병목(1.9h)과 교차 인계(123건)의 6.6배 폭증

* **DOM Layout & Grid**: `TopChart-Bottom3Cards` (상단 16:9 와이드 3-Panel 차트 58% + 하단 3단 추론 & 대안 카드 42%)
* **Category Kicker**: `Part 02 · 질문 2-2 | 제1대 병목 (접수 국면)`
* **Action Headline**: `"접수 지연은 물량 과부하가 아닌 '교차 인계(123건)'에서 비롯되며, 비실시간 채널 공백이 6.6배 폭증을 유발했다"`
* **Top Visual Canvas** (`w-full h-72 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm flex items-center justify-center`):
* **Visual Asset Image**:
* Path: `outputs/figures/slide09_reception_bottleneck_3panel.png`
* Style: `w-full h-full object-contain`
* Note: `3-Panel 차트 (Panel 1: 인계 패널티 6.6배 | Panel 2: 웹·우편 양극화 | Panel 3: 웹 채널 6.8분의 진실)`
* **Bottom 3-Columns (통계적 추론 및 개선 빌드업 카드)** (`grid grid-cols-3 gap-5 mt-4`):

1. **Card 1 (가설 기각 - 물량 부하 무관)**:

* `bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between`
* `Top`: `Badge: "가설 기각" (Gray Pill)` | `Title: "물량 과부하 가설 완전 기각"` (`font-bold text-base text-slate-900 mt-1`)
* `BigNum Block`: `BigNum: "r = 0.01"` (`text-3xl font-extrabold text-slate-700 font-mono my-2`)
* `Bullets`:

- `• 일일 인입량(10~141건)과 소요시간의 무상관성`
- `• 다중 OLS 회귀검정 결과 계수 p = 0.752 (비유의)`
- `• 접수 지연은 창구 처리 용량(CAPA) 부족이 아님 확증`

2. **Card 2 (핵심 원인 - 교차 인계 6.6배)**:

* `bg-white rounded-2xl p-5 border border-orange-200 shadow-sm flex flex-col justify-between`
* `Top`: `Badge: "핵심 원인" (Orange Pill)` | `Title: "교차 인계 시 6.6배 시간 폭증"` (`font-bold text-base text-orange-600 mt-1`)
* `BigNum Block`: `BigNum: "6.6배 (▲ 6.7h)"` (`text-3xl font-extrabold text-orange-600 font-mono my-2`)
* `Bullets`:

- `• 단독 처리군(804건): 평균 1.2시간 (중앙값 8분) 종결`
- `• 교차 인계군(123건): 평균 7.9시간 (중앙값 5.6시간) 지체`
- `• 인계 123건 전수(100%)가 웹(69건)·우편(54건)에서만 발생`

3. **Card 3 (반전 통찰 - Web 채널의 본질)**:

* `bg-white rounded-2xl p-5 border border-emerald-200 shadow-sm flex flex-col justify-between`
* `Top`: `Badge: "반전 통찰" (Emerald Pill)` | `Title: "Web 채널 6.8분의 본질적 우수성"` (`font-bold text-base text-emerald-600 mt-1`)
* `BigNum Block`: `BigNum: "6.8분 (최속)"` (`text-3xl font-extrabold text-emerald-600 font-mono my-2`)
* `Bullets`:

- `• Fast 코호트 비교 시 웹(6.8분)이 전화(8.2분)보다 빠름`
- `• 웹 시스템 자체가 느린 것이 아니라 '일정 조율 공백'이 원인`
- `• Direct Booking(자가 일정 확정) 도입 시 지연 원천 제거`

* **Source Bar**: `출처: analysis.sql Step 2-2 접수 단독 OLS (R² = 0.3000, F = 131.9, p < 0.001) · 전 변수 VIF ≤ 1.20`
* **Presenter's Script (발표 대본)**:

> "접수 국면의 지연은 왜 발생했을까요? 특정 날짜에 접수량이 몰려서였을까요? 데이터를 분석해보니 일별 접수량과 소요시간은 전혀 상관이 없었습니다(r=0.01, p=0.752). 물량 문제가 아니었습니다.
> 상단 좌측 Panel 1을 보시면, 진짜 원인은 상담원 간의 '교차 인계(Handover)'였습니다. 단독으로 처리할 때는 1.2시간이면 끝나던 접수가, 상담원 2명 이상 개입되는 순간 7.9시간으로 무려 6.6배 폭증했습니다.
> 그렇다면 이 인계는 어디서 발생했을까요? 가운데 Panel 2를 보시면 전화와 대면은 100% 15분 이내에 끝나고 인계가 0건이었습니다. 반면, 웹과 우편은 약 50%가 60분을 초과하는 장기 지체에 빠졌으며, 발생한 인계 123건 전수(100%)가 오직 웹과 우편에서만 터졌습니다.
> 그렇다면 웹 채널이 비효율적인 시스템일까요? 우측 Panel 3의 반전 통찰을 주목해 주십시오. 즉시 완료된 건들을 비교해보면, 웹은 평균 6.8분으로 전화(8.2분)나 대면(8.5분)보다 오히려 모든 채널 중 가장 빨랐습니다.
> 즉, 웹 시스템 자체가 느린 게 아닙니다. 신청 접수 후 실시간으로 방문 일정을 확정하지 못해 고객 회신을 기다리다 담당자가 교체되는 '비동기 일정 조율 공백'이 6.6배 지연의 본질이었습니다.
> 이제 전체 대기시간의 98%가 집중된 최대 핵심 병목, '현장 국면'으로 넘어가겠습니다."

---

### Slide 10. [질문 2-2] 제2대 병목: 현장 국면 압도적 대기 76.8h & 403건 WIP 누적 적체

* **DOM Layout & Grid**: `Split-LeftDonut-RightWIP` (좌측 현장 소요시간 도넛 42% + 우측 CAPA 불균형 & 403건 WIP 꺾은선 58%)
* **Category Kicker**: `Part 02 · 질문 2-2 | 제2대 병목 (현장 국면)`
* **Action Headline**: `"현장 소요시간(98.3h)의 95.3%가 대기이며, CAPA를 2배 초과한 접수 유입이 403건의 미처리 적체(WIP)를 촉발했다"`
* **Two-Asset Comparison Grid** (`grid grid-cols-12 gap-5`):
* **Left Column: 현장 소요시간 4대 구조 분해 (5 cols)**:
* Container: `bg-white rounded-2xl p-4 border border-slate-200 shadow-sm flex flex-col justify-between`
* Image Asset: `outputs/figures/slide10_field_donut_breakdown.png` (`w-full h-48 object-contain mb-3`)
* 4-Row Stat Strips:

1. `Strip 1: flex items-center justify-between p-2 rounded bg-red-50 border border-red-200` ➔ `Left: "① 실사 방문 대기 (Wait 1)"` | `Right: "76.81h (78.2% 독점 🚨)"` (`font-bold text-xs text-red-600 font-mono`)
2. `Strip 2: flex items-center justify-between p-2 rounded bg-orange-50 border border-orange-200` ➔ `Left: "② 수리 착수/공정 대기 (Wait 2)"` | `Right: "16.90h (17.2%)"` (`font-bold text-xs text-orange-600 font-mono`)
3. `Strip 3: flex items-center justify-between p-2 rounded bg-slate-50` ➔ `Left: "③ 본수리 순수 작업"` | `Right: "3.90h (4.0%)"` (`text-xs text-slate-600 font-mono`)
4. `Strip 4: flex items-center justify-between p-2 rounded bg-slate-50` ➔ `Left: "④ 실사 점검 순수 작업"` | `Right: "0.68h (0.7%, 40.5분)"` (`text-xs text-slate-600 font-mono`)

* **Right Column: 유입 vs CAPA 및 WIP 적체 동역학 (7 cols)**:
* Container: `bg-white rounded-2xl p-4 border border-slate-200 shadow-sm flex flex-col justify-between`
* Image Asset: `outputs/figures/slide10_field_bottleneck_wip.png` (`w-full h-48 object-contain mb-3`)
* 3-Dynamic Metric Cards (`grid grid-cols-3 gap-2.5`):
* `Metric 1: p-3 rounded-xl bg-blue-50/60 border border-blue-200` ➔ `Title: "일일 접수 유입량"` | `Big: "134.3건/일"` (`text-xl font-bold text-blue-700 font-mono`) | `Sub: "피크 141건 인입"`
* `Metric 2: p-3 rounded-xl bg-slate-50 border border-slate-200` ➔ `Title: "현장 기사 11인 CAPA"` | `Big: "68.0건/일"` (`text-xl font-bold text-slate-700 font-mono`) | `Sub: "소화율 50.6% 한계"`
* `Metric 3: p-3 rounded-xl bg-red-50/60 border border-red-200` ➔ `Title: "미처리 적체 피크 (WIP)"` | `Big: "403건 (20배)"` (`text-xl font-bold text-red-600 font-mono`) | `Sub: "초기 20건 ➔ 403건 폭증"`
* **Key Takeaway Banner**:
* `bg-slate-900 text-white rounded-xl p-3.5 mt-3 text-center text-xs font-medium`
* `Text: "기사가 게으른 것이 아니라 '기사 CAPA(68건)를 2배 초과하는 전수 방문 실사(134건) 의무화 관행'이 403건 적체와 76.8h 대기를 만든 본질이다"`
* **Source Bar**: `출처: analysis.sql L1250~1395 (현장 4대 소요시간) & L1569~1575 (일별 유입 vs CAPA 시뮬레이션)`
* **Presenter's Script (발표 대본)**:

> "현장 국면의 문제점을 살펴보겠습니다. 좌측 도넛 차트를 보시면, 현장에서 보낸 98.3시간 중 기사가 땀 흘려 일한 순수 작업 시간은 4.7%(수리 3.9h, 점검 0.7h)에 불과합니다. 나머지 95.3%(93.7시간)가 전부 멍하니 서서 기다린 대기시간이었습니다.
> 특히 전체 리드타임의 72.5%를 단독 독점한 '실사 방문 대기(76.8시간, 3.2일)'는 왜 발생했을까요?
> 우측의 통합 차트를 보시면 그 물리적 원인이 단번에 드러납니다. 파란색 막대인 일일 접수 유입량은 매일 134건씩 쏟아져 들어왔지만, 회색 막대인 현장 기사 11명이 하루에 소화할 수 있는 실사는 68건에 불과했습니다.
> 유입이 처리 능력을 2배 초과하자, 빨간색 꺾은선인 '미처리 적체 대기열(WIP)'을 보십시오. 첫날 20건이던 대기열이 7일 만에 403건으로 20배 폭증합니다.
> 저수조에 물이 넘쳐 403건이나 갇혀 있으니, 뒤늦게 방문받는 세입자는 일주일 넘게 기사를 기다릴 수밖에 없었던 것입니다. 즉, 기사가 게으른 것이 아니라 '기사 CAPA를 초과하는 전수 방문 실사 의무화'가 현장 병목의 진짜 원인이었습니다."

---

### Slide 11. [질문 2-3 & 2-2] 소요시간 영향 요인 실증(OLS) 및 수리·리워크 병목

* **DOM Layout & Grid**: `Split-LeftOLS-RightRepair` (좌측 OLS 다중회귀 영향인자 50% + 우측 수리 착수 대기 및 리워크 루프 50% + 하단 2-Track 결론 배너)
* **Category Kicker**: `Part 02 · 질문 2-3 & 질문 2-2 | 소요시간 영향 요인 & 리워크`
* **Action Headline**: `"전체 리드타임은 사내수리(+31.8h)와 실사 지연(+1.12h/h)이 지배하며, 사내 하자 루프(26건)가 장기 적체를 유발했다"`
* **Two-Track Diagnostic Canvas** (`grid grid-cols-12 gap-5 mb-4`):
* **Left Column: OLS 다중회귀 영향 요인 실증 (6 cols)**:
* Container: `bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between`
* Top Image: `outputs/figures/slide11_regression_leadtime_drivers.png` (`w-full h-44 object-contain mb-3`)
* OLS 3대 회귀계수 카드 (`flex flex-col gap-2`):

1. `Row 1: p-2.5 rounded-lg bg-orange-50/70 border border-orange-200 flex items-center justify-between` ➔ `Title: "1. 사내 수리 방식 (is_intern_repair)"` | `Value: "+31.75h (p < 0.001)"` (`font-bold text-xs text-orange-700 font-mono`)
2. `Row 2: p-2.5 rounded-lg bg-red-50/70 border border-red-200 flex items-center justify-between` ➔ `Title: "2. 실사 방문 지연 (visit_lag_hours)"` | `Value: "+1.12h/h (p < 0.001)"` (`font-bold text-xs text-red-700 font-mono`)
3. `Row 3: p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between` ➔ `Title: "3. 비실시간 접수 채널 (is_async_channel)"` | `Value: "+4.89h (p = 0.030)"` (`font-bold text-xs text-slate-700 font-mono`)

* Stat Note: `R² = 0.878 (설명력 87.8%), F = 1,659.4, p < 0.001, 전 변수 VIF ≤ 1.25`
* **Right Column: 수리 착수 대기 및 리워크 품질 병목 (6 cols)**:
* Container: `bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between`
* Top Image: `outputs/figures/slide11_repair_delay_rework.png` (`w-full h-44 object-contain mb-3`)
* 2대 수리 지연 메커니즘 카드 (`flex flex-col gap-2.5`):

1. `Block 1: p-3 rounded-xl bg-slate-50 border border-slate-200` ➔

* `Title: "1차 수리 착수 지연 격차: 사내수리 자재 대기 30.5h"` (`text-xs font-bold text-slate-900`)
* `Desc: "즉시수리(0.0h) 및 외주수리(0.0h)는 대기 없이 즉시 착수. 사내수리만 부품 조달 및 2차 일정 조율로 30.5시간 대기 독점."` (`text-xs text-slate-500 mt-1`)

2. `Block 2: p-3 rounded-xl bg-red-50/70 border border-red-200` ➔

* `Title: "사내 하자 리워크 루프 26건: +32.9시간 추가 지연 🚨"` (`text-xs font-bold text-red-700`)
* `Desc: "1차 수리 실패 후 재수리 시 부품 재출하로 +32.9h 추가 대기. 26건 중 E-1/E-2가 22건(84.6%) 집중되며 최대 10.1일(171.6h) 억류."` (`text-xs text-red-600 mt-1`)
* **Bottom Key Insight Banner**:
* `bg-slate-900 text-white rounded-xl p-3 flex items-center justify-between text-xs`
* `Left Text: "OLS 회귀계수 검증: 실사 대기를 1시간 단축할 때마다 전체 케이스 리드타임은 1.12시간 선형 감소한다"`
* `Right Stat: "회귀계수 β = +1.12h/h (p < 0.001)"` (`text-emerald-400 font-mono font-bold`)
* **Source Bar**: `출처: analysis.sql Step 2-4 (다중 OLS) & L1365, L1470 (수리 착수 대기 및 리워크 26건 집계)`
* **Presenter's Script (발표 대본)**:

> "슬라이드 11은 리드타임을 결정하는 3대 핵심 요인과 품질 결함으로 인한 리워크 문제를 함께 보여줍니다.
> 좌측의 다중 회귀 모델(설명력 87.8%)을 보시면, 전체 시간을 지배하는 요인은 사내수리 배정(+31.8h)과 실사 대기(시간당 +1.12h), 그리고 비실시간 접수(+4.9h)였습니다. 특히 실사 지연 계수가 1.12라는 것은, 실사 대기를 1시간 줄이면 전체 리드타임이 1.12시간 줄어든다는 강력한 지렛대 효과를 뜻합니다.
> 우측을 보시면, 즉시수리와 외주는 대기가 0시간이지만 사내수리는 부품 준비로 기본 30.5시간이 걸립니다. 특히 1차 수리 실패로 재 사내수리에 들어간 26건은 부품을 다시 조달하느라 추가로 32.9시간, 최대 10일이나 더 갇히게 됩니다.
> 이제 87.3%의 높은 사전 적합성을 활용하여 이 병목들을 일거에 해소하는 전략으로 넘어가겠습니다."

---

### Slide 12. [질문 2-2 & 질문 3 발단] 핵심 문제 규명 및 해결 아젠다

* **DOM Layout & Grid**: `3-Column-Agenda` (Card 1 사전 적중률 87.3% 도넛 + Card 2 정보 해상도 한계 + Card 3 보수적 CAPA 경감 & OLS 효과)
* **Category Kicker**: `Part 02 · 질문 2-2 & Part 03 발단 | 핵심 문제 규명 & 해결 아젠다`
* **Action Headline**: `"사전 적중률 87.3%에도 불구하고, '정보 해상도 단절'로 인해 403건의 실사 적체와 이중 출장이 고착되었다"`
* **3-Column Architecture Cards** (`grid grid-cols-3 gap-5`):

1. **Card 1 (사전 적중률 87.3%와 딜레마)**:

* `bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "데이터 팩트" (Blue Pill)` | `Title: "사전 적중률 87.3%와 이중 출장 모순"` (`font-bold text-base text-slate-900 mt-1`)
* `Visual Image`: `outputs/figures/slide12_intake_matching_donut.png` (`w-full h-44 object-contain my-2`)
* `Key Stats`:

- `• 실사 생략 후보군: E형(370건, 39.9%) + P형(439건, 47.4%) = 총 809건 (87.3% 독점)`
- `• 사내 자체 완결률: E형 100%(370건) + P형 91.3%(401건) = 총 771건 (83.2%) 사내 해결`
- `• 직행 적중률: 후보군 809건 중 771건(95.3%)이 사내/즉시 처리로 완벽 적중`

* `Question Callout`: `p-2.5 rounded-lg bg-blue-50 text-blue-900 text-xs font-semibold mt-2` ➔ `"이미 87.3%를 맞히는데 왜 40분짜리 헛걸음 실사로 403건 적체를 자초했는가?"`

2. **Card 2 (정보 해상도의 한계 - Resolution Gap)**:

* `bg-white rounded-2xl p-5 border border-orange-200 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "원인 규명" (Orange Pill)` | `Title: "정보 해상도 단절 (Resolution Gap)"` (`font-bold text-base text-orange-600 mt-1`)
* `Contrast Comparison Block`:
* `Box A (접수 관행): bg-slate-50 p-3 rounded-lg border border-slate-200 mb-2`

- `Header: "현행 접수 상담원"` ➔ `알파벳 대분류 (B, P, E)만 수집`
- `한계: 단순 알파벳만으로는 차에 실을 자재 규격 특정 불가`

* `Box B (현장 관행): bg-slate-50 p-3 rounded-lg border border-slate-200`

- `Header: "현장 방문 기사"` ➔ `40분 방문 실사 후 세부 코드 (1~4) 판정`
- `결과: 실사(40분) ➔ 부품 주문(30.5h) ➔ 재방문 수리 이중 출장 고착`

* `Bottom Summary`: `p-2.5 rounded-lg bg-orange-50 text-orange-800 text-xs font-semibold mt-2` ➔ `"접수와 현장의 정보 해상도 단절이 비효율의 유일한 원인"`

3. **Card 3 (보수적 해결책 - E형 직행 시 CAPA 경감 & OLS 효과)**:

* `bg-white rounded-2xl p-5 border-2 border-emerald-500 rounded-xl p-5 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "보수적 해결책" (Green Pill)` | `Title: "E형 우선 신뢰 시 즉각적 대기 단축"` (`font-bold text-base text-emerald-700 mt-1`)
* `Metric Blocks`:
* `Block 1 (CAPA 부하 경감)`:

- `E형 370건(100% 사내 완결) 직행 ➔ 일 실사 유입 40% 급감 (134 ➔ 80.7건)`
- `미처리 적체 누적 속도 80.8% 격감 (일 66.3건 ➔ 12.7건/일)`

* `Block 2 (보수적 20% 대기 단축 목표)`:

- `실사 대기시간(76.8h) 단 20% 단축 지향 ➔ 실사 대기 -15.4시간 절감!`

* `Block 3 (OLS 계수 +1.12h/h 연동 순절감)`:

- `15.36h × 1.12 = 전체 리드타임 -17.2시간 (약 0.7일) 순단축 확정!`

* `BigNum Highlight`: `BigNum: "▼ 17.2시간"` (`text-3xl font-extrabold text-emerald-600 font-mono text-center my-1`)
* **Source Bar**: `출처: analysis.sql L1840~1985 (사전 일치율 87.3% 및 시나리오 1 시뮬레이션)`
* **Presenter's Script (발표 대본)**:

> "앞선 분석을 종합하면, 병목을 없애기 위한 핵심은 명확합니다. 실사 CAPA의 적체 부담을 덜어내고, 수리 품목 준비 기간을 줄여야 합니다.
> Card 1에서 보시듯, 접수원의 사전 분류는 이미 실제 수리와 87.3%나 일치하고 있었습니다. 특히 E형은 100% 사내수리였습니다.
> 이렇게 잘 맞추면서 왜 굳이 40분짜리 실사를 먼저 보내 400건의 대기열을 만들었을까요?
> Card 2의 '정보 해상도의 한계' 때문이었습니다. 접수부는 단순 알파벳(B, P, E)만 넘겨주고, 현장 기술자는 1, 2, 3, 4 세부 코드를 써야 부품을 알 수 있어 차에 실을 수가 없었습니다.
> 따라서 Card 3의 해결책을 제시합니다. 가장 보수적으로 100% 사내수리인 E형만 실사 없이 직행시켜도, 실사 유입은 40% 줄고 적체 속도는 81%나 급감합니다.
> 여기서 실사 대기시간을 단 20%만 줄인다고 보수적으로 잡아도 실사 대기는 15.4시간 줄어들며, 앞선 OLS 회귀계수 1.12에 의해 전체 리드타임 17.2시간 순단축이 즉시 보장됩니다.
> 이제 다음 장에서 두 번째 과제인 '수리 품목 준비 단축 및 리워크 방지'의 구체적 실행 방안을 설명해 드리겠습니다."

---

### Slide 13. [질문 3] TO-BE 실행 전략: 품목 준비 기간 단축 및 E코드 리워크 방지

* **DOM Layout & Grid**: `3-Column-Strategy` (Card 1 사전 체크리스트 고도화 + Card 2 E-1/E-2 정밀검사 프로토콜 + Card 3 모듈형 번들 키트 & 외주 패스트트랙)
* **Category Kicker**: `Part 03 · 질문 3 | TO-BE 구체적 실행 전략`
* **Action Headline**: `"사전 체크리스트로 자재 대기(30.5h)를 압축하고, E-1/E-2 정밀검사로 리워크 84.6%(+32.9h)를 원천 차단한다"`
* **3-Strategy Execution Cards** (`grid grid-cols-3 gap-5`):

1. **Card 1 (사전 체크리스트 고도화 & 품목 패킹 단축)**:

* `bg-white rounded-2xl p-5 border border-blue-200 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "전략 1: 자재 대기 단축" (Blue Pill)` | `Title: "스마트폰 사진 기반 부품 사전 특정"` (`font-bold text-base text-blue-700 mt-1`)
* `BigNum Block`: `BigNum: "30.5h ➔ 사전패킹"` (`text-2xl font-extrabold text-blue-600 font-mono my-2`)
* `Action Bullets`:

- `• 모바일 사진 1장 필수 첨부: 접수 시 고장 부위 및 모델 라벨 사진 등록`
- `• 출동 전 자재 규격 특정: 기사가 출발 전 부품 규격을 100% 파악`
- `• 현장 방문 후 주문하던 30.5시간 자재 조달 대기를 '출동 전 사전 패키징'으로 압축`
- `• 헛걸음 실사(40.5분) 생략으로 회수된 기사 496.1시간 공수를 부품 준비·상차에 재배치`

2. **Card 2 (E-1 / E-2 정밀검사 의무화 - 리워크 84.6% 차단)**:

* `bg-white rounded-2xl p-5 border border-red-200 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "전략 2: 품질 루프 차단" (Red Pill)` | `Title: "E-1/E-2 2차 정밀검사 프로토콜"` (`font-bold text-base text-red-600 mt-1`)
* `BigNum Block`: `BigNum: "84.6% 차단"` (`text-2xl font-extrabold text-red-600 font-mono my-2`)
* `Action Bullets`:

- `• 원천 데이터 팩트: 사내 하자 리워크 26건 중 84.6%(22건)가 E-1(16건), E-2(6건) 집중`
- `• 정밀검사 체크리스트 도입: 단순 단품 수리에 그치지 않고 '인접 배관/연계 부속 2차 노후도 정밀점검' 의무화`
- `• 부품 규격 불일치 및 2차 하자 누락을 현장에서 원천 차단`
- `• 재수리 시 발생하는 평균 +32.9시간(최대 10.1일) 초장기 재방문 루프 완전 박멸`

3. **Card 3 (모듈형 번들 키트 상차 & 외주 패스트트랙)**:

* `bg-white rounded-2xl p-5 border border-emerald-200 shadow-sm flex flex-col justify-between`
* `Top Header`: `Badge: "전략 3: 물류·외주 최적화" (Green Pill)` | `Title: "모듈형 번들 키트 & 외주 직행"` (`font-bold text-base text-emerald-700 mt-1`)
* `BigNum Block`: `BigNum: "대기 0.0h 종결"` (`text-2xl font-extrabold text-emerald-600 font-mono my-2`)
* `Action Bullets`:

- `• 번들 키트(Bundle Kit) 상차: E-1/E-2 출동 시 빈번 고장 연관 부품을 차량에 사전 적재`
- `• 현장 도착 후 부품 재출하를 기다리는 대기시간 제로화`
- `• 외주 패스트트랙 (P-4 38건): 사진상 대규모 배관/전문 외주 공사 식별 시 실사 생략`
- `• 전문 외주업체(FixIt/DoIt)로 다이렉트 전산 이관하여 외주 대기 0.0h 종결`

* **Bottom ROI Summary Bar**:
* `bg-slate-900 text-white rounded-xl p-3.5 flex items-center justify-between text-xs`
* `Left Text: "TO-BE 통합 실행 결과: 실사 대기(-15.4h), 자재 대기(30.5h 사전화), 리워크(+32.9h)가 동시 차단되어 전체 리드타임 60% 이상 획기적 단축"`
* `Right Stat: "총 리드타임 105.9h ➔ 36.0h (1.5일, -65% 단축)"` (`text-emerald-400 font-mono font-bold`)
* **Source Bar**: `출처: analysis.sql L1500 (리워크 26건 중 E형 22건 팩트) & 시나리오 1~4 시뮬레이션`
* **Presenter's Script (발표 대본)**:

> "슬라이드 12에서 제시한 두 번째 과제, '수리 품목 준비 기간 단축과 리워크 방지'의 구체적 실행 방안입니다.
> Card 1을 보시면, 접수 단계에서 스마트폰 사진 1장을 의무 등록받아 부품 모델 라벨을 사전에 특정합니다. 기사가 부품을 미리 알고 챙겨 나가기 때문에, 30.5시간이나 걸리던 자재 대기열을 사전에 대폭 단축할 수 있습니다.
> Card 2는 품질 리워크의 해결책입니다. 앞서 SQL 분석에서 밝혔듯, 10일씩 걸리는 사내 리워크 26건의 무려 85%(22건)가 E-1과 E-2 코드에 쏠려 있었습니다. 따라서 E코드 건에 대해서는 '인접 배관 2차 정밀검사 체크리스트' 작성을 의무화하여, 추가 하자를 현장에서 즉시 잡아냅니다.
> 마지막 Card 3처럼 연관 부품을 묶은 '모듈형 번들 키트'를 들고 나가고, 사진상 외주 공사(P-4)는 즉시 외주업체로 패스트트랙 이관하면, 자재 대기(30.5h)와 리워크 루프(+32.9h)가 동시에 해결됩니다."

---

### Slide 14. [Part 04. 마무리] 질의응답 (Q&A)

* **DOM Layout & Grid**: `Split-LeftSummary-RightQABox` (좌측 프로젝트 3단계 여정 총괄 요약 50% + 우측 대형 Q&A 히어로 박스 50%)
* **Category Kicker**: `Part 04 · 마무리 | 질의응답 (Q&A)`
* **Action Headline**: `"경청해 주셔서 감사합니다. 수리 프로세스 최적화 방안에 대한 질의응답을 진행하겠습니다"`
* **Two-Column Q&A Canvas** (`grid grid-cols-12 gap-6`):
* **Left Column: 프로젝트 3단계 여정 총괄 요약 (6 cols)**:
* Container: `flex flex-col gap-3.5 justify-between`
* 3 Journey Summary Cards:

1. **Step 1 (Part 01. 데이터 무결성)**:

* `p-4 rounded-xl bg-slate-50 border border-slate-200 shadow-sm flex items-start gap-3`
* `Badge: "Part 01"` (`bg-blue-100 text-blue-800 text-xs font-bold px-2 py-0.5 rounded`)
* `Content`: `Title: "13,262행 전수 보존 & 18개 케이스(20행) 인과 복원 완료"` (`font-bold text-sm text-slate-900`)
* `Desc: "임의 삭제 0건, 시간 역전 0건 입증 ➔ 분석 대상 927건 정상 코호트 확립"` (`text-xs text-slate-500 mt-1`)

2. **Step 2 (Part 02. 병목 원인 규명)**:

* `p-4 rounded-xl bg-orange-50/60 border border-orange-200 shadow-sm flex items-start gap-3`
* `Badge: "Part 02"` (`bg-orange-100 text-orange-800 text-xs font-bold px-2 py-0.5 rounded`)
* `Content`: `Title: "76.8h 실사 대기(WIP 403건) & 접수 인계 6.6배 실증"` (`font-bold text-sm text-orange-800`)
* `Desc: "일 134건 유입 vs 기사 11인 CAPA 68건 불균형 및 비실시간 채널 소통 공백 특정"` (`text-xs text-orange-700/80 mt-1`)

3. **Step 3 (Part 03. TO-BE 오퍼레이션 혁신)**:

* `p-4 rounded-xl bg-emerald-50/60 border border-emerald-200 shadow-sm flex items-start gap-3`
* `Badge: "Part 03"` (`bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded`)
* `Content`: `Title: "E형 직행(-17.2h) + 사전 패킹(30.5h) + 리워크 84.6% 차단"` (`font-bold text-sm text-emerald-800`)
* `Desc: "사진 1장 사전 특정, E-1/E-2 2차 정밀검사 체크리스트로 총 리드타임 60% 이상 감축"` (`text-xs text-emerald-700/80 mt-1`)
* **Right Column: 대형 Q&A 히어로 박스 (6 cols)**:
* `bg-white rounded-2xl p-8 border-2 border-emerald-500 shadow-md flex flex-col items-center justify-between text-center`
* `Top Badge`: `inline-flex px-4 py-1.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800` ➔ `QUESTION & ANSWER`
* `Hero Icon/Graphic`: `BigNum: "Q & A"` (`text-6xl font-black text-slate-900 font-mono tracking-tight my-4`)
* `Main Title`: `"경청해 주셔서 감사합니다"` (`text-2xl font-bold text-slate-900 mt-1`)
* `Sub Message`: `"데이터 진단부터 병목 규명, 실행 전략까지\n자유롭게 질문해 주시기 바랍니다."` (`text-sm text-slate-600 leading-relaxed mt-2`)
* `Footer Meta`: `"퍼즐데이터 채용 과제 수리 프로세스 데이터 분석 및 운영 최적화 방안 | 2026. 10. 27"` (`text-xs text-slate-400 font-mono mt-4`)
* **Source Bar**: `출처: 퍼즐데이터 과제 분석 보고서 (Slide 01 ~ 14 완결)`
* **Presenter's Script (발표 대본)**:

> "이상으로 공공임대주택 수리 프로세스 데이터 분석 및 운영 최적화 방안 발표를 모두 마칩니다. 13,262행의 무손실 전처리부터 76.8시간의 실사 대기 병목 규명, 그리고 현장에 즉시 적용 가능한 3대 최적화 전략까지 전 과정에 대해 궁금하신 점이나 추가 논의하고 싶으신 부분에 대해 편하게 질문해 주시기 바랍니다. 경청해 주셔서 대단히 감사합니다."

---
