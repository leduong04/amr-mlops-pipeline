import streamlit as st
import pandas as pd
import duckdb
import time

# 1. Cấu hình giao diện chuẩn Dashboard
st.set_page_config(page_title="AMR MLOps Dashboard", layout="wide")
st.title("🤖 AMR Edge-to-Cloud Monitoring")

DB_PATH = "/app/data/warehouse.duckdb"

# 2. Xử lý Concurrency (Đồng thời) với DuckDB
@st.cache_data(ttl=5) # Cache tự động làm mới mỗi 5 giây
def fetch_data():
    for _ in range(5): # Thử tối đa 5 lần nếu chạm trúng khoảnh khắc Worker đang ghi
        try:
            # Kết nối ở chế độ Read-Only để không block ETL Worker
            conn = duckdb.connect(DB_PATH, read_only=True)
            df = conn.execute("SELECT * FROM detections ORDER BY timestamp DESC").df()
            conn.close()
            return df
        except duckdb.IOException:
            time.sleep(0.5)
    return pd.DataFrame()

df = fetch_data()

# 3. Trực quan hóa dữ liệu (Visualization)
if df.empty:
    st.warning("Đang chờ đồng bộ dữ liệu từ Cloud Data Lake...")
else:
    # Tính toán các Metrics quan trọng
    total_detections = len(df)
    ood_count = len(df[df['is_ood'] == True])
    ood_ratio = (ood_count / total_detections) * 100 if total_detections > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số suy luận (Inferences)", total_detections)
    col2.metric("Số lượng vật thể OOD", ood_count)
    col3.metric("Tỷ lệ dị thường (Anomaly Rate)", f"{ood_ratio:.1f}%")
    
    st.markdown("---")
    st.subheader("Bảng cấp dữ liệu (Real-time Feed)")
    
    # Định dạng lại bảng cho đẹp mắt
    display_df = df[['timestamp', 'robot_id', 'class_name', 'confidence', 'is_ood']].copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)
