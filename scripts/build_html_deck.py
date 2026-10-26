# -*- coding: utf-8 -*-
"""build_deck_v4.py(기본) 의 슬라이드 정의를 그대로 실행하되 deck_common 을 HTML 백엔드(deck_html)로 바꿔
단일 HTML 프레젠테이션(outputs/html/puzzledata_repair_report.html)을 만든다.

PPTX 와 HTML 이 같은 소스에서 나오므로 좌표·텍스트·차트·발표 대본이 항상 일치한다.
사용: python scripts/build_html_deck.py [build_deck_v3.py]
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import deck_html  # noqa: E402  (내부에서 실제 deck_common 을 먼저 import 한다)

sys.modules["deck_common"] = deck_html
runpy.run_path(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "build_deck_v4.py"), run_name="__main__")
