import os
import time
import json
import pandas as pd
import duckdb
import boto3
from datetime import datetime, timezone

# --- CẤU HÌNH ---
MINIO_CONFIG = {
    "endpoint_url": "http://minio:9000",
    "access_key": "admin_mlops",
    "secret_key": "MLOpsPassword2026!",
    "bucket": "robot-logs"
}
DUCKDB_PATH = "/app/data/warehouse.duckdb"
SLEEP_TIME = 30  # Quét mỗi 30 giây

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=MINIO_CONFIG["endpoint_url"],
        aws_access_key_id=MINIO_CONFIG["access_key"],
        aws_secret_access_key=MINIO_CONFIG["secret_key"]
    )

def init_db():
    conn = duckdb.connect(DUCKDB_PATH)
    # Tạo bảng lưu trữ dữ liệu tập trung
    conn.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            trace_id VARCHAR,
            timestamp TIMESTAMP,
            robot_id VARCHAR,
            is_ood BOOLEAN,
            class_name VARCHAR,
            confidence DOUBLE,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Bảng theo dõi các file đã xử lý để tránh trùng lặp (Idempotency)
    conn.execute("CREATE TABLE IF NOT EXISTS processed_files (file_key VARCHAR PRIMARY KEY)")
    return conn

def etl_process():
    s3 = get_s3_client()
    conn = init_db()
    
    print(f"[{datetime.now()}] Bắt đầu chu kỳ quét MinIO...")
    
    try:
        response = s3.list_objects_v2(Bucket=MINIO_CONFIG["bucket"], Prefix='logs/')
        if 'Contents' not in response:
            return

        for obj in response['Contents']:
            file_key = obj['Key']
            if not file_key.endswith('.json'): continue
            
            # Kiểm tra file đã xử lý chưa
            exists = conn.execute("SELECT 1 FROM processed_files WHERE file_key = ?", [file_key]).fetchone()
            if exists: continue

            print(f"-> Đang xử lý: {file_key}")
            file_obj = s3.get_object(Bucket=MINIO_CONFIG["bucket"], Key=file_key)
            data = json.loads(file_obj['Body'].read().decode('utf-8'))

            # Extract & Transform
            rows = []
            for det in data.get('detections', []):
                rows.append({
                    'trace_id': data.get('trace_id'),
                    'timestamp': data.get('timestamp'),
                    'robot_id': data.get('robot_id'),
                    'is_ood': data.get('is_ood'),
                    'class_name': det.get('class'),
                    'confidence': det.get('confidence')
                })
            
            if rows:
                df = pd.DataFrame(rows)
                # Load vào DuckDB
                # conn.execute("INSERT INTO detections SELECT * EXCLUDE(processed_at), CURRENT_TIMESTAMP FROM df")
                # Load vào DuckDB bằng phương pháp ánh xạ tường minh
                conn.execute("""
                    INSERT INTO detections (trace_id, timestamp, robot_id, is_ood, class_name, confidence) 
                    SELECT * FROM df
                """)
            # Đánh dấu đã xử lý
            conn.execute("INSERT INTO processed_files VALUES (?)", [file_key])
            
        conn.commit()
    except Exception as e:
        print(f"❌ Lỗi ETL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        etl_process()
        time.sleep(SLEEP_TIME)
