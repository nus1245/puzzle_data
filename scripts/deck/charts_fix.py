"""원장에서 정정이 확정된 차트 및 Modern Tech Light 테마 통합 렌더러.

`scripts/deck/render_deck_charts.py`의 메인 렌더 파이프라인을 호출하여
outputs/figures/ 및 outputs/figures/deck/ 전역에 슬라이드 테마와 통일된
투명 배경·축정리·헤더 중복제거 고해상도(300 DPI) 차트를 생성한다.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_deck_charts

if __name__ == "__main__":
    render_deck_charts.main()
