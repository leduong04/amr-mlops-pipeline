Sau khi đọc toàn bộ các file:

* `robot_sim_video.py` → Edge AI + Robot Simulator + OOD Detection + Model Update (CD) 
* `etl_worker.py` → ETL Pipeline từ MinIO → DuckDB 
* `dashboard.py` → Dashboard giám sát tập trung + Analytics + OOD Monitoring 
* `ct_pipeline.py` → Active Learning + Pseudo Labeling + Continuous Training + Model Registry 
* Docker Compose → triển khai toàn bộ hệ thống dạng microservice/container

Tôi thấy đề tài của bạn thực chất không phải:

> "Xây dựng mô hình YOLO phát hiện vật cản"

mà là:

> "Xây dựng hệ thống MLOps Edge-to-Cloud cho đội robot AMR sử dụng YOLOv8"

Đó mới là điểm mạnh nhất của đề tài.

---

# MỤC LỤC ĐỀ XUẤT CUỐI CÙNG

## DANH MỤC HÌNH ẢNH

## DANH MỤC BẢNG BIỂU

## DANH MỤC TỪ VIẾT TẮT

## LỜI MỞ ĐẦU

### 1. Lý do chọn đề tài

### 2. Mục tiêu nghiên cứu

### 3. Đối tượng và phạm vi nghiên cứu

### 4. Phương pháp nghiên cứu

### 5. Cấu trúc báo cáo

---

# CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI

## 1.1. Giới thiệu về nhà máy thông minh và Industry 4.0

## 1.2. Robot di động tự hành AMR trong logistics nội bộ

## 1.3. Bài toán giám sát đội robot AMR quy mô lớn

## 1.4. Hạn chế của các hệ thống AI truyền thống

### 1.4.1. Model Decay

### 1.4.2. Data Drift

### 1.4.3. Thiếu vòng phản hồi dữ liệu

## 1.5. Đề xuất hướng tiếp cận

## 1.6. Mục tiêu và đóng góp của đề tài

## 1.7. Tổng kết chương

---

# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT

## 2.1. Robot di động tự hành (AMR)

### 2.1.1. Kiến trúc AMR

### 2.1.2. Cảm biến và hệ thống nhận thức

### 2.1.3. Vai trò của thị giác máy tính

---

## 2.2. Thị giác máy tính và nhận diện vật thể

### 2.2.1. CNN

### 2.2.2. Object Detection

### 2.2.3. Kiến trúc YOLO

### 2.2.4. YOLOv8

---

## 2.3. Trí tuệ nhân tạo tại biên (Edge AI)

### 2.3.1. Khái niệm Edge Computing

### 2.3.2. Edge AI trong robot công nghiệp

### 2.3.3. Đánh đổi giữa độ chính xác và độ trễ

---

## 2.4. Data Engineering

### 2.4.1. Data Lake

### 2.4.2. ETL Pipeline

### 2.4.3. In-process OLAP

### 2.4.4. DuckDB

---

## 2.5. MLOps

### 2.5.1. Vòng đời mô hình AI

### 2.5.2. Model Registry

### 2.5.3. Continuous Training

### 2.5.4. Continuous Deployment

### 2.5.5. Active Learning

---

## 2.6. Dữ liệu ngoài phân phối (Out-of-Distribution)

### 2.6.1. Khái niệm OOD

### 2.6.2. Uncertainty Sampling

### 2.6.3. Confidence Score

---

## 2.7. Tổng kết chương

---

# CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

## 3.1. Phân tích yêu cầu

### 3.1.1. Yêu cầu chức năng

### 3.1.2. Yêu cầu phi chức năng

---

## 3.2. Kiến trúc tổng thể hệ thống

### 3.2.1. Kiến trúc Edge-to-Cloud

### 3.2.2. Luồng dữ liệu tổng thể

### 3.2.3. Data Flywheel

---

## 3.3. Thiết kế phân hệ Edge AI

### 3.3.1. Robot Video Simulator

### 3.3.2. YOLOv8 Inference Engine

### 3.3.3. OOD Detection Module

### 3.3.4. JSON Logging Module

---

## 3.4. Thiết kế Data Lake

### 3.4.1. MinIO Storage

### 3.4.2. Cấu trúc Bucket

### 3.4.3. Quản lý dữ liệu bất thường

---

## 3.5. Thiết kế ETL Pipeline

### 3.5.1. Extract

### 3.5.2. Transform

### 3.5.3. Load

### 3.5.4. Lưu trữ bằng DuckDB

---

## 3.6. Thiết kế Dashboard

### 3.6.1. Kiến trúc Streamlit

### 3.6.2. Chỉ số giám sát

### 3.6.3. Trực quan hóa dữ liệu

---

## 3.7. Thiết kế Continuous Training Pipeline

### 3.7.1. Thu thập dữ liệu OOD

### 3.7.2. Pseudo Labeling

### 3.7.3. Fine-tuning

### 3.7.4. Model Registry

### 3.7.5. Continuous Deployment

---

## 3.8. Tổng kết chương

---

# CHƯƠNG 4. TRIỂN KHAI HỆ THỐNG

## 4.1. Môi trường triển khai

### 4.1.1. Phần cứng

### 4.1.2. Phần mềm

### 4.1.3. Docker

---

## 4.2. Xây dựng bộ dữ liệu

### 4.2.1. Thu thập dữ liệu

### 4.2.2. Gán nhãn

### 4.2.3. Tiền xử lý dữ liệu

### 4.2.4. Data Augmentation

### 4.2.5. Chia Train-Val-Test

---

## 4.3. Huấn luyện mô hình YOLOv8

### 4.3.1. Thiết lập tham số

### 4.3.2. Huấn luyện YOLOv8n

### 4.3.3. Huấn luyện YOLOv8s

### 4.3.4. Huấn luyện YOLOv8m

### 4.3.5. Lựa chọn mô hình triển khai

---

## 4.4. Triển khai Edge Node

### 4.4.1. Tích hợp YOLOv8

### 4.4.2. OOD Detection

### 4.4.3. Logging Service

---

## 4.5. Triển khai Data Lake

### 4.5.1. MinIO

### 4.5.2. Bucket Management

---

## 4.6. Triển khai ETL Worker

### 4.6.1. Đồng bộ dữ liệu

### 4.6.2. Xử lý dữ liệu

### 4.6.3. Lưu trữ DuckDB

---

## 4.7. Triển khai Dashboard

### 4.7.1. Monitoring Dashboard

### 4.7.2. OOD Analytics

### 4.7.3. Robot Telemetry

---

## 4.8. Triển khai Continuous Training

### 4.8.1. Thu thập dữ liệu mới

### 4.8.2. Pseudo Labeling

### 4.8.3. Fine-tuning

### 4.8.4. Model Registry

### 4.8.5. Continuous Deployment

---

## 4.9. Tổng kết chương

---

# CHƯƠNG 5. ĐÁNH GIÁ VÀ THẢO LUẬN

## 5.1. Kịch bản thực nghiệm

---

## 5.2. Đánh giá mô hình YOLOv8

### 5.2.1. So sánh YOLOv8n, YOLOv8s và YOLOv8m

### 5.2.2. Precision

### 5.2.3. Recall

### 5.2.4. mAP50

### 5.2.5. mAP50-95

### 5.2.6. FPS

---

## 5.3. Đánh giá Edge AI

### 5.3.1. Tốc độ suy luận

### 5.3.2. Khả năng hoạt động thời gian thực

---

## 5.4. Đánh giá Data Pipeline

### 5.4.1. Độ trễ ETL

### 5.4.2. Hiệu năng DuckDB

### 5.4.3. Tốc độ đồng bộ dữ liệu

---

## 5.5. Đánh giá OOD Detection

### 5.5.1. Tỷ lệ phát hiện dữ liệu bất thường

### 5.5.2. Khả năng thu thập dữ liệu mới

---

## 5.6. Đánh giá Continuous Training

### 5.6.1. Chất lượng dữ liệu pseudo-label

### 5.6.2. Hiệu quả fine-tuning

### 5.6.3. Khả năng cập nhật mô hình tự động

---

## 5.7. Hạn chế của hệ thống

---

## 5.8. Tổng kết chương

---

# CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 6.1. Kết luận

## 6.2. Những đóng góp đạt được

## 6.3. Hướng phát triển

### 6.3.1. Tích hợp ROS2

### 6.3.2. Triển khai trên robot AMR thực

### 6.3.3. Data Drift Detection thực thụ

### 6.3.4. Multi-Robot Fleet Management

### 6.3.5. Federated Learning

---

# TÀI LIỆU THAM KHẢO

# PHỤ LỤC

Đây là phiên bản phù hợp nhất với code hiện tại của bạn và phản ánh đúng những gì bạn thực sự đã xây dựng: **Edge AI + Data Lake + ETL + Dashboard + Continuous Training + Continuous Deployment**, thay vì chỉ là một bài toán YOLO đơn thuần.
