import pandas as pd
from pathlib import Path

def load_and_inspect_data(file_path: str = "repair2.csv") -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path.resolve()}")

    print(f"[{path.name}] 데이터 읽는 중...")
    df = pd.read_csv(path)

    print("\n" + "=" * 50)
    print("1. 데이터 기본 정보 (Info)")
    print("=" * 50)
    print(f"- 행/열 크기: {df.shape[0]:,}행 x {df.shape[1]}열")
    print(f"- 컬럼 목록: {list(df.columns)}")

    print("\n" + "=" * 50)
    print("2. 상위 5개 행 (Head)")
    print("=" * 50)
    print(df.head())

    print("\n" + "=" * 50)
    print("3. 결측치 요약 (Missing Values)")
    print("=" * 50)
    missing = df.isnull().sum()
    missing_ratio = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({"결측치 개수": missing, "결측 비율(%)": missing_ratio})
    print(missing_df[missing_df["결측치 개수"] > 0])

    return df

if __name__ == "__main__":
    df = load_and_inspect_data()
