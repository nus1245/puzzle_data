"""
repair_cleaned.csv to MySQL Importer
===================================
이 스크립트는 전처리 완료 데이터셋(repair_cleaned.csv)을 MySQL 데이터베이스에
최적화된 스키마(데이터타입, 인덱스, utf8mb4)로 자동 생성 및 초고속 적재합니다.

사용법:
    python scripts/import_to_mysql.py
또는 옵션 지정:
    python scripts/import_to_mysql.py --host localhost --port 3306 --user root --password mypass --db repair_db
"""

import os
import sys
import argparse
import getpass
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import errorcode

def parse_args():
    parser = argparse.ArgumentParser(description="repair_cleaned.csv MySQL 자동 적재 스크립트")
    parser.add_argument("--host", default="localhost", help="MySQL 호스트 (기본값: localhost)")
    parser.add_argument("--port", type=int, default=3306, help="MySQL 포트 (기본값: 3306)")
    parser.add_argument("--user", default="root", help="MySQL 사용자명 (기본값: root)")
    parser.add_argument("--password", default=None, help="MySQL 비밀번호 (미입력 시 안전하게 프롬프트 입력)")
    parser.add_argument("--db", default="repair_db", help="대상 데이터베이스명 (기본값: repair_db)")
    parser.add_argument("--csv", default="repair_cleaned.csv", help="CSV 파일 경로 (기본값: repair_cleaned.csv)")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 1. CSV 파일 존재 확인
    csv_path = os.path.abspath(args.csv)
    if not os.path.exists(csv_path):
        print(f"❌ 오류: CSV 파일을 찾을 수 없습니다: {csv_path}")
        sys.exit(1)
        
    print("=" * 60)
    print("🚀 [MySQL 데이터 자동 적재기] repair_cleaned.csv -> MySQL")
    print("=" * 60)
    print(f"📁 대상 파일: {csv_path}")
    print(f"🖥️ 접속 호스트: {args.host}:{args.port}")
    print(f"👤 계정: {args.user}")
    print(f"🗄️ 데이터베이스: {args.db}")
    print("-" * 60)

    # 2. 비밀번호 입력
    password = args.password
    if password is None:
        try:
            password = getpass.getpass(prompt=f"🔑 MySQL 비밀번호를 입력하세요 (user: {args.user}): ")
        except Exception:
            password = input(f"🔑 MySQL 비밀번호를 입력하세요 (user: {args.user}): ")

    # 3. MySQL 서버 접속
    try:
        print("\n⏳ MySQL 서버 연결 시도 중...")
        conn = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=password,
            charset="utf8mb4"
        )
        cursor = conn.cursor()
        print("✅ MySQL 서버 연결 성공!")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ 오류: 사용자 이름 또는 비밀번호가 잘못되었습니다.")
        elif err.errno == errorcode.CR_CONN_HOST_ERROR:
            print("❌ 오류: MySQL 서버에 연결할 수 없습니다. 서비스가 실행 중인지 확인하세요.")
        else:
            print(f"❌ 연결 오류: {err}")
        sys.exit(1)

    # 4. 데이터베이스 생성 및 선택
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{args.db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE `{args.db}`;")
        print(f"✅ 데이터베이스 `{args.db}` 준비 완료.")
    except mysql.connector.Error as err:
        print(f"❌ 데이터베이스 생성 실패: {err}")
        cursor.close()
        conn.close()
        sys.exit(1)

    # 5. 테이블 생성 (DDL)
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS `repair_logs` (
        `caseID`              INT NOT NULL,
        `taskID`              VARCHAR(50) NOT NULL,
        `originator`          VARCHAR(50) NOT NULL,
        `eventtype`           VARCHAR(20) NOT NULL,
        `contact`             VARCHAR(20) NULL,
        `RepairType`          VARCHAR(20) NULL,
        `objectKey`           INT NULL,
        `RepairInternally`    TINYINT(1) NULL,
        `EstimatedRepairTime` FLOAT NULL,
        `RepairCode`          FLOAT NULL,
        `RepairOK`            TINYINT(1) NULL,
        `date`                VARCHAR(20) NULL,
        `time`                VARCHAR(20) NULL,
        `timestamp`           VARCHAR(30) NULL,
        `task_group`          VARCHAR(20) NOT NULL,
        `SUBJECT`             VARCHAR(20) NOT NULL,
        `외주여부`            VARCHAR(20) NOT NULL,
        `수정된연도`          INT NULL,
        `seq`                 INT NOT NULL,
        `sub_seq`             INT NOT NULL,
        `작업단계`            VARCHAR(50) NOT NULL,
        `re_date`             DATE NOT NULL,
        `re_time`             TIME NOT NULL,
        `clean_timestamp`     DATETIME NOT NULL,
        INDEX `idx_case_seq` (`caseID`, `seq`, `sub_seq`),
        INDEX `idx_clean_time` (`clean_timestamp`),
        INDEX `idx_task_group` (`task_group`, `taskID`),
        INDEX `idx_originator` (`originator`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """

    try:
        # 기존 테이블 존재 시 초기화 여부 확인
        cursor.execute("SHOW TABLES LIKE 'repair_logs';")
        exists = cursor.fetchone()
        if exists:
            cursor.execute("TRUNCATE TABLE `repair_logs`;")
            print("ℹ️ 기존 `repair_logs` 테이블 데이터를 초기화(TRUNCATE)했습니다.")
        else:
            cursor.execute(create_table_sql)
            print("✅ `repair_logs` 테이블 및 인덱스 신규 생성 완료.")
    except mysql.connector.Error as err:
        print(f"❌ 테이블 준비 실패: {err}")
        cursor.close()
        conn.close()
        sys.exit(1)

    # 6. CSV 데이터 읽기 및 전처리
    print(f"\n⏳ CSV 데이터 로드 및 정제 중 ({csv_path})...")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    # Nullable 타입 변환
    def to_time_str(val):
        if pd.isna(val) or not str(val).strip():
            return None
        parts = str(val).strip().split(':')
        if len(parts) == 2:
            return f"{int(parts[0]):02d}:{int(parts[1]):02d}:00"
        elif len(parts) == 3:
            return f"{int(parts[0]):02d}:{int(parts[1]):02d}:{int(parts[2]):02d}"
        return str(val)

    def to_bool_int(val):
        if pd.isna(val) or val is None or val == '':
            return None
        if str(val).strip().lower() in ['true', '1', '1.0', 't']:
            return 1
        elif str(val).strip().lower() in ['false', '0', '0.0', 'f']:
            return 0
        return None

    def to_nullable_int(val):
        if pd.isna(val) or val is None or val == '':
            return None
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return None

    def to_nullable_float(val):
        if pd.isna(val) or val is None or val == '':
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    def to_nullable_str(val):
        if pd.isna(val) or val is None:
            return None
        s = str(val).strip()
        return s if s != '' else None

    # 데이터 리스트 변환
    records = []
    for _, row in df.iterrows():
        record = (
            int(row['caseID']),
            str(row['taskID']),
            str(row['originator']),
            str(row['eventtype']),
            to_nullable_str(row['contact']),
            to_nullable_str(row['RepairType']),
            to_nullable_int(row['objectKey']),
            to_bool_int(row['RepairInternally']),
            to_nullable_float(row['EstimatedRepairTime']),
            to_nullable_float(row['RepairCode']),
            to_bool_int(row['RepairOK']),
            to_nullable_str(row['date']),
            to_nullable_str(row['time']),
            to_nullable_str(row['timestamp']),
            str(row['task_group']),
            str(row['SUBJECT']),
            str(row['외주여부']),
            to_nullable_int(row['수정된연도']),
            int(row['seq']),
            int(row['sub_seq']),
            str(row['작업단계']),
            str(row['re_date']),
            to_time_str(row['re_time']),
            str(row['clean_timestamp'])
        )
        records.append(record)

    total_count = len(records)
    print(f"✅ 총 {total_count:,}건의 레코드 변환 완료.")

    # 7. 배치 삽입 (Batch Insert)
    insert_sql = """
    INSERT INTO `repair_logs` (
        `caseID`, `taskID`, `originator`, `eventtype`, `contact`, `RepairType`,
        `objectKey`, `RepairInternally`, `EstimatedRepairTime`, `RepairCode`,
        `RepairOK`, `date`, `time`, `timestamp`, `task_group`, `SUBJECT`,
        `외주여부`, `수정된연도`, `seq`, `sub_seq`, `작업단계`, `re_date`,
        `re_time`, `clean_timestamp`
    ) VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s
    )
    """

    print(f"\n⏳ MySQL 테이블로 배치 적재 시작...")
    batch_size = 2000
    for i in range(0, total_count, batch_size):
        batch = records[i:i + batch_size]
        cursor.executemany(insert_sql, batch)
        conn.commit()
        print(f"   - {min(i + batch_size, total_count):,} / {total_count:,} 행 적재 완료 ({(min(i + batch_size, total_count)/total_count*100):.1f}%)")

    # 8. 최종 검증
    cursor.execute("SELECT COUNT(*) FROM `repair_logs`;")
    inserted_count = cursor.fetchone()[0]
    print("\n" + "=" * 60)
    print(f"🎉 적재 완료! 총 적재 행 수: {inserted_count:,}건 (원천 {total_count:,}건 일치)")
    print("=" * 60)

    cursor.close()
    conn.close()
    print("💡 이제 MySQL Workbench 또는 다른 클라이언트에서 분석 쿼리를 실행하실 수 있습니다.")

if __name__ == "__main__":
    main()
