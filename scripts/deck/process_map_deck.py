"""슬라이드 7 프로세스 맵 덱 전용 복사본.

docs/repair_process_map.html 의 SVG 를 구성·색·배치 그대로 두고, 글자 크기와 폰트만 슬라이드 영역에 맞게 손본다.
  - 폰트: Geist/Geist Mono/Instrument Serif → 한글 맑은 고딕, 영문 노드명·수치 Consolas
  - 크기: 구간 제목 14→18, 노드명 12→14, 수치·보조 9→12, 간선 라벨 8→11, 하단 설명 14→17
  - 영역: 슬라이드 카드 폭(비율 3.5:1)에 맞게 위·옆 여백과 설명선 간격을 줄여 잘라 낸다. 범례는 원본 PNG 와 동일하게 제외.
원본 HTML 은 수정하지 않는다.
실행: python -X utf8 scripts/deck/process_map_deck.py   (프로젝트 루트 기준, Edge/Chrome 필요)
"""
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "docs", "repair_process_map.html")
OUT_DIR = os.path.join(ROOT, "outputs", "figures", "deck")
HTML = os.path.join(ROOT, "scripts", "deck", "process_map_deck.html")
PNG = os.path.join(OUT_DIR, "process_map_deck.png")

KO = "'Malgun Gothic','맑은 고딕',sans-serif"
MONO = "Consolas,'Courier New',monospace"
VB = (24, 98, 1368, 390)               # 잘라 낼 영역 x, y, w, h (원본 viewBox 1416×600 기준)
HANGUL = re.compile(r"[가-힣]")


def retype_text(m):
    tag, body = m.group(1), m.group(2)
    size = float(re.search(r'font-size="([\d.]+)"', tag).group(1))
    plain = re.sub(r"<[^>]+>", "", body)
    ko = bool(HANGUL.search(plain))
    if size == 14:                                           # 구간 제목(01 접수…) / 하단 설명
        fam, new = KO, (18 if "font-weight" in tag else 17)
    elif size == 12:                                         # 노드명
        fam, new = (KO if ko else MONO), 14
    elif size == 9:                                          # 노드 수치·구간 부제
        fam, new = MONO, 12
    else:                                                    # 8: 간선 라벨
        fam, new = MONO, 11
    tag = re.sub(r'font-size="[\d.]+"', f'font-size="{new}"', tag)
    tag = re.sub(r'font-family="[^"]*"', f'font-family="{fam}"', tag)
    # 노드명은 굵게, 하단 설명(원래 세리프)은 한글 600 으로
    if size == 12 and 'font-weight' in tag:
        tag = re.sub(r'font-weight="\d+"', 'font-weight="700"', tag)
    if size == 14 and "font-weight" not in tag:
        tag = tag.replace("<text ", '<text font-weight="600" ', 1)
    return tag + body + "</text>"


def build():
    h = open(SRC, encoding="utf-8").read()
    svg = re.search(r"<svg .*?</svg>", h, re.S).group(0)
    svg = re.sub(r"(<text[^>]*>)(.*?)</text>", retype_text, svg, flags=re.S)
    # 간선 라벨 뒷배경 사각형을 커진 글자에 맞춰 넓힌다
    svg = svg.replace('<rect x="492" y="278" width="76" height="14" rx="2" fill="#f5f5f5"/>', '<rect x="480" y="274" width="100" height="18" rx="2" fill="#f5f5f5"/>')
    svg = svg.replace('<rect x="496" y="308" width="68" height="14" rx="2" fill="#f5f5f5"/>', '<rect x="484" y="305" width="92" height="18" rx="2" fill="#f5f5f5"/>')
    for x, y in [(746, 249), (746, 337), (846, 249)]:
        svg = svg.replace(f'<rect x="{x}" y="{y}" width="16" height="14" rx="2" fill="#f5f5f5"/>', f'<rect x="{x-3}" y="{y-2}" width="24" height="18" rx="2" fill="#f5f5f5"/>')
    # InformClientWrongPlace 노드명이 상자에 꽉 차서 좌우를 8씩 넓힌다
    svg = svg.replace('x="56" y="360" width="176"', 'x="48" y="360" width="192"')
    # 하단 설명을 구간 가까이로 당긴다(원본 y 504 → 478)
    svg = svg.replace('y="504"', 'y="478"').replace("M 252 484 V 336", "M 252 458 V 336").replace("M 782 484 V 424", "M 782 458 V 424")
    # 설명 텍스트 색·내용은 그대로. 범례 이하는 잘려 나간다
    x, y, w, hh = VB
    svg = re.sub(r'viewBox="0 0 1416 600"', f'viewBox="{x} {y} {w} {hh}" width="{w}" height="{hh}"', svg, count=1)
    svg = svg.replace('<rect width="100%" height="100%" fill="#f5f5f5"/>', f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" fill="#ffffff"/>')
    return f'<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>html,body{{margin:0;padding:0;background:#fff}}svg{{display:block;min-width:0;width:{w}px;height:{hh}px}}</style></head><body>{svg}</body></html>'


def find_browser():
    for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe"]:
        if os.path.exists(p):
            return p
    raise SystemExit("Edge/Chrome 을 찾지 못했습니다")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    open(HTML, "w", encoding="utf-8").write(build())
    w, hh = VB[2], VB[3]
    cmd = [find_browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2.4",
           f"--window-size={w},{hh}", f"--screenshot={PNG}", "file:///" + HTML.replace("\\", "/")]
    subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    print("->", PNG)


if __name__ == "__main__":
    main()
