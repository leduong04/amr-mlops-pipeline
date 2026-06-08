import streamlit as st
import pandas as pd
import duckdb
import time
import random
import numpy as np

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
    st.header("🤖 Trạng thái Vận hành Phần cứng (IoT Telemetry)")

    col_iot1, col_iot2 = st.columns(2)

    with col_iot1:
        st.subheader("Năng lượng & Cảnh báo")
        # Giả lập mức pin giảm dần hoặc ngẫu nhiên
        battery_level = random.randint(45, 100)
        st.metric("🔋 Mức Pin hiện tại", f"{battery_level}%", "-2% so với chu kỳ trước")
        st.progress(battery_level / 100.0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Cảnh báo va chạm: Liên kết logic với mô hình AI
        # Nếu hệ thống AI bắt được object (ood_count > 0), kích hoạt cảnh báo va chạm
        if 'ood_count' in locals() and ood_count > 0:
            st.error(f"⚠️ CẢNH BÁO VA CHẠM: Phát hiện {ood_count} chướng ngại vật trên quỹ đạo!")
        else:
            st.success("✅ Quỹ đạo an toàn. Robot đang di chuyển bình thường.")

    with col_iot2:
        st.subheader("📍 Bản đồ định vị (Mô phỏng)")
        # Giả lập một tọa độ GPS di chuyển nhẹ quanh một điểm cố định trong nhà kho
        # (Tọa độ ví dụ: khu vực Hà Nội)
        base_lat, base_lon = 21.0031, 105.8460 
        map_data = pd.DataFrame(
            np.random.randn(1, 2) / [10000, 10000] + [base_lat, base_lon],
            columns=['lat', 'lon']
        )
        # Vẽ bản đồ bằng widget mặc định của Streamlit
        st.map(map_data, zoom=16, use_container_width=True)

    st.markdown("---")

    st.markdown("---")
    
    # ==========================================
    # THÊM MỚI: BIỂU ĐỒ DATA DRIFT (LINE CHART)
    # ==========================================
    st.subheader("📈 Theo dõi Trôi dạt dữ liệu (Data Drift) theo thời gian")
    
    # Chuyển đổi timestamp sang định dạng datetime của Pandas
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Gom nhóm dữ liệu theo từng phút (hoặc giờ) để vẽ biểu đồ
    # Tính tổng số inference và số OOD trong mỗi khung thời gian
    df_grouped = df.groupby(df['timestamp'].dt.floor('Min')).agg(
        total_inferences=('trace_id', 'count'),
        ood_count=('is_ood', 'sum')
    ).reset_index()
    
    # Tính tỷ lệ % Drift
    df_grouped['Drift_Rate_Percentage'] = (df_grouped['ood_count'] / df_grouped['total_inferences']) * 100
    df_grouped = df_grouped.rename(columns={'timestamp': 'Thời gian'})
    
    # Vẽ Line Chart bằng Streamlit
    if not df_grouped.empty:
        st.line_chart(
            data=df_grouped.set_index('Thời gian'),
            y='Drift_Rate_Percentage',
            use_container_width=True
        )
    else:
        st.info("Chưa đủ dữ liệu chuỗi thời gian để vẽ đồ thị.")

    # ==========================================


    st.markdown("---")
    st.subheader("Bảng cấp dữ liệu (Real-time Feed)")
    
    # Định dạng lại bảng cho đẹp mắt
    display_df = df[['timestamp', 'robot_id', 'class_name', 'confidence', 'is_ood']].copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)
