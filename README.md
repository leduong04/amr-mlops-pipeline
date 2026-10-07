# Edge-to-Cloud MLOps for AMR

Hệ thống MLOps theo kiến trúc **Edge-to-Cloud** phục vụ giám sát và cập nhật mô hình AI cho **Autonomous Mobile Robot (AMR)** trong môi trường nhà kho.

Đồ án tập trung xây dựng một vòng đời dữ liệu và mô hình khép kín:

**Edge Inference → Data Lake → ETL → Analytics → Monitoring → Continuous Training → Model Registry → Edge Update**

---

## 1. Giới thiệu

Trong môi trường nhà kho, mô hình AI triển khai trên robot có thể suy giảm hiệu năng khi điều kiện vận hành thay đổi hoặc xuất hiện các đối tượng chưa có trong tập huấn luyện.

Đồ án xây dựng một hệ thống MLOps nhằm:

* Triển khai mô hình YOLOv8 tại thiết bị biên.
* Nhận diện các đối tượng trong môi trường nhà kho.
* Phát hiện và thu thập các mẫu có độ tin cậy trung bình để phục vụ cải thiện mô hình.
* Lưu trữ dữ liệu vận hành trên Data Lake.
* Tự động xử lý dữ liệu bằng ETL Pipeline.
* Phân tích dữ liệu bằng DuckDB.
* Giám sát hệ thống thông qua Streamlit Dashboard.
* Thực hiện Continuous Training trên dữ liệu được thu thập.
* Lưu phiên bản mô hình mới vào Model Registry để Edge Node có thể cập nhật.

---

## 2. Kiến trúc hệ thống

```text
                         ┌──────────────────────┐
                         │      Edge Node       │
                         │                      │
                         │  YOLOv8s Inference   │
                         │  OOD Sampling        │
                         └──────────┬───────────┘
                                    │
                       JSON Logs / OOD Images
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │           MinIO           │
                    │         Data Lake         │
                    │                           │
                    │  logs/                    │
                    │  anomaly_images/          │
                    │  model-registry/          │
                    └───────┬───────────┬───────┘
                            │           │
                       JSON Logs    OOD Images
                            │           │
                            ▼           ▼
                    ┌────────────┐  ┌───────────────┐
                    │ ETL Worker │  │ Continuous    │
                    │            │  │ Training      │
                    └─────┬──────┘  └───────┬───────┘
                          │                 │
                          ▼                 │
                    ┌────────────┐          │
                    │   DuckDB   │          │
                    │ Analytics  │          │
                    └─────┬──────┘          │
                          │                 │
                          ▼                 ▼
                    ┌────────────┐     ┌──────────────┐
                    │ Streamlit  │     │ Model        │
                    │ Dashboard  │     │ Registry     │
                    └────────────┘     └──────┬───────┘
                                              │
                                              │ New Model
                                              ▼
                                         Edge Node
```

### Các thành phần chính

| Thành phần          | Vai trò                                          |
| ------------------- | ------------------------------------------------ |
| Edge Node           | Chạy mô hình YOLOv8 và xử lý dữ liệu đầu vào     |
| MinIO               | Lưu trữ dữ liệu dạng object và Model Registry    |
| ETL Worker          | Đọc, làm sạch, biến đổi và nạp dữ liệu           |
| DuckDB              | Lưu trữ và phân tích dữ liệu đã chuẩn hóa        |
| Dashboard           | Giám sát dữ liệu và trạng thái mô hình           |
| Continuous Training | Thu thập dữ liệu OOD và thực hiện tái huấn luyện |
| Model Registry      | Lưu trữ phiên bản mô hình mới                    |

---

## 3. Mô hình AI

Hệ thống sử dụng **YOLOv8** cho bài toán phát hiện đối tượng.

Các lớp đối tượng trong phạm vi đồ án:

1. Person
2. Forklift
3. Carton Box
4. Safety Cone
5. Wet Floor Sign

Mô hình được triển khai tại Edge Node nhằm thực hiện suy luận trực tiếp thay vì gửi toàn bộ luồng video lên Cloud.

### Kết quả mô hình

Mô hình YOLOv8s đạt:

* **mAP@0.5:0.95:** 78.8%
* **Inference speed:** 81.78 FPS

Việc lựa chọn YOLOv8s nhằm cân bằng giữa độ chính xác và tốc độ suy luận trong môi trường tài nguyên hạn chế.

---

## 4. Cơ chế thu thập dữ liệu bất định

Edge Node không gửi toàn bộ video lên Data Lake.

Sau mỗi lần suy luận, hệ thống kiểm tra confidence của các đối tượng được phát hiện.

Các dự đoán nằm trong khoảng:

```text
0.3 ≤ confidence ≤ 0.6
```

được đánh dấu là dữ liệu bất định và được sử dụng để thu thập ảnh OOD phục vụ quá trình Continuous Training.

Dữ liệu được phân thành:

```text
logs/
    └── *.json

anomaly_images/
    └── *.jpg
```

Cách tiếp cận này giúp giảm lượng dữ liệu cần truyền và lưu trữ so với việc gửi toàn bộ video.

> Lưu ý: trong phạm vi đồ án, confidence threshold được sử dụng như một heuristic cho Uncertainty Sampling; đây không phải là một thuật toán OOD Detection hoàn chỉnh theo nghĩa lý thuyết.

---

## 5. Data Lake với MinIO

MinIO đóng vai trò là tầng lưu trữ object trung tâm.

### `logs/`

Lưu các bản ghi JSON được tạo từ Edge Node.

Thông tin chính bao gồm:

* `trace_id`
* `timestamp`
* `robot_id`
* `is_ood`
* danh sách detections
* class
* confidence

### `anomaly_images/`

Lưu các hình ảnh được lựa chọn thông qua cơ chế confidence-based sampling.

### `model-registry/`

Lưu các phiên bản model được tạo sau quá trình Continuous Training.

Ví dụ:

```text
model-registry/
└── best_v2.pt
```

Việc sử dụng MinIO giúp tách biệt dữ liệu gốc khỏi tầng phân tích.

---

## 6. ETL Pipeline

ETL Worker định kỳ quét thư mục `logs/` trên MinIO.

Quy trình:

```text
Extract
   ↓
Đọc JSON từ MinIO
   ↓
Transform
   ↓
Flatten detections
   ↓
Chuẩn hóa dữ liệu
   ↓
Load
   ↓
DuckDB
```

Mỗi detection được chuyển thành một bản ghi độc lập trong bảng `detections`.

Ví dụ:

```text
trace_id
timestamp
robot_id
class_name
confidence
is_ood
processed_at
```

### Idempotency

ETL Worker sử dụng bảng:

```text
processed_files
```

để lưu các file JSON đã được xử lý.

Nhờ đó, cùng một file không bị nạp nhiều lần vào bảng `detections`.

---

## 7. DuckDB

DuckDB được sử dụng làm hệ quản trị cơ sở dữ liệu phân tích cho tầng dữ liệu đã được ETL.

Các bảng chính:

```text
detections
processed_files
```

### `detections`

Lưu dữ liệu detection đã được chuẩn hóa.

### `processed_files`

Theo dõi các file JSON đã được xử lý nhằm đảm bảo tính idempotent của ETL Pipeline.

Dashboard kết nối DuckDB ở chế độ **Read-Only** để truy vấn dữ liệu.

---

## 8. Dashboard

Dashboard được xây dựng bằng **Streamlit**.

Các chỉ số chính:

* Total Inferences
* OOD Objects
* Anomaly Rate
* Data Drift / OOD trend
* Real-time Detection Feed

Dashboard truy vấn dữ liệu từ DuckDB và hiển thị dưới dạng:

* KPI Cards
* Line Chart
* Data Table

Dashboard được thiết kế để phục vụ giám sát dữ liệu và tình trạng hoạt động của hệ thống MLOps.

---

## 9. Continuous Training

Continuous Training Pipeline sử dụng dữ liệu OOD được thu thập từ MinIO.

Quy trình:

```text
OOD Images
     ↓
Dataset
     ↓
Teacher Model
     ↓
Pseudo-labeling
     ↓
Student Model
     ↓
Fine-tuning
     ↓
best_v2.pt
     ↓
Model Registry
```

### Teacher Model

Teacher Model được sử dụng để thực hiện pseudo-labeling trên các ảnh được lựa chọn từ quá trình vận hành.

### Student Model

Student Model là mô hình YOLOv8s được fine-tune từ trọng số hiện tại với dữ liệu mới.

Sau khi huấn luyện, trọng số mới được đưa vào:

```text
model-registry/best_v2.pt
```

---

## 10. Cập nhật mô hình tại Edge

Khi Edge Node khởi động, chương trình kiểm tra Model Registry trên MinIO.

Nếu tìm thấy phiên bản model mới, hệ thống tải model về thiết bị và sử dụng phiên bản đó cho quá trình suy luận.

Nếu không thể truy cập Model Registry, hệ thống sử dụng model cục bộ đã được lưu sẵn.

Luồng cập nhật:

```text
Model Registry
      │
      ▼
Check New Model
      │
      ├── Có model mới
      │       ↓
      │   Download
      │       ↓
      │   Load Model
      │
      └── Không có / lỗi kết nối
              ↓
          Local Model
```

---

## 11. Docker

Các thành phần của hệ thống được triển khai trong môi trường container để thuận tiện cho quá trình cấu hình và vận hành.

Các container được sử dụng trong hệ thống có thể bao gồm:

```text
MinIO
ETL Worker
Dashboard
Continuous Training
```

Mỗi thành phần có môi trường runtime độc lập, giúp giảm sự phụ thuộc giữa các thư viện và môi trường thực thi.

---

## 12. Cấu trúc source code

Cấu trúc thư mục tham khảo:

```text
.
├── robot_sim_video.py
├── etl_worker.py
├── dashboard.py
├── ct_pipeline.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── data/
└── README.md
```

Tùy phiên bản source code, cấu trúc thư mục có thể thay đổi.

---

## 13. Yêu cầu môi trường

Các thành phần chính được xây dựng bằng Python.

Một số thư viện sử dụng:

```text
Python
OpenCV
Ultralytics
PyTorch
Pandas
DuckDB
Boto3
Streamlit
MinIO
Docker
```

---

## 14. Chạy hệ thống

### Bước 1: Clone repository

```bash
git clone <REPOSITORY_URL>
cd <PROJECT_DIRECTORY>
```

### Bước 2: Khởi động các dịch vụ

Nếu repository có `docker-compose.yml`:

```bash
docker compose up -d
```

Kiểm tra container:

```bash
docker compose ps
```

### Bước 3: Kiểm tra MinIO

Đảm bảo MinIO đang hoạt động và các bucket/object cần thiết đã được cấu hình.

### Bước 4: Khởi động ETL Worker

Nếu chạy trực tiếp:

```bash
python etl_worker.py
```

### Bước 5: Khởi động Dashboard

```bash
streamlit run dashboard.py
```

Dashboard mặc định sử dụng cổng:

```text
8501
```

---

## 15. Luồng hoạt động tổng thể

Toàn bộ hệ thống vận hành theo chu trình:

```text
                    ┌──────────────┐
                    │   YOLOv8s    │
                    │ Edge Inference│
                    └──────┬───────┘
                           │
                    Detection Results
                           │
                           ▼
                    ┌──────────────┐
                    │    MinIO     │
                    │   Data Lake  │
                    └──────┬───────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          ┌──────────┐         ┌─────────────┐
          │   ETL    │         │ Continuous  │
          │  Worker  │         │  Training   │
          └────┬─────┘         └──────┬──────┘
               │                      │
               ▼                      ▼
          ┌──────────┐          ┌─────────────┐
          │ DuckDB   │          │Model Registry│
          └────┬─────┘          └──────┬──────┘
               │                       │
               ▼                       │
          ┌──────────┐                 │
          │Dashboard │                 │
          └──────────┘                 │
                                       │
                                       ▼
                                  Edge Node
```

Đây là vòng lặp dữ liệu và mô hình của hệ thống:

**Inference → Data Collection → ETL → Monitoring → Continuous Training → Model Update → Inference**

---

## 16. Hạn chế

Một số giới hạn của phiên bản hiện tại:

* Cơ chế phát hiện dữ liệu bất định chủ yếu dựa trên ngưỡng confidence.
* Edge Node chưa được tích hợp trực tiếp với phần cứng AMR vật lý.
* Hệ thống chưa triển khai cơ chế lưu đệm và đồng bộ lại dữ liệu khi kết nối mạng bị gián đoạn.
* Continuous Training phụ thuộc đáng kể vào tài nguyên tính toán của môi trường huấn luyện.
* Quy mô thử nghiệm hiện tại chưa đại diện cho hệ thống triển khai với hàng trăm AMR.

---

## 17. Hướng phát triển

Các hướng phát triển tiếp theo:

* Tích hợp hệ thống với ROS2 và phần cứng AMR thực tế.
* Xây dựng cơ chế Local Buffer và Retry cho Edge-to-Cloud communication.
* Nghiên cứu các phương pháp OOD Detection chuyên biệt.
* Tối ưu Continuous Training trên GPU.
* Bổ sung Model Versioning và Experiment Tracking.
* Mở rộng kiến trúc để hỗ trợ nhiều robot đồng thời.
* Bổ sung cơ chế xác thực và bảo mật cho các API và object storage.

---

## 18. Thông tin đồ án

**Đề tài:** Thiết kế và triển khai hệ thống MLOps giám sát và cập nhật mô hình AI cho AMR dựa trên kiến trúc Edge-to-Cloud.

**Lĩnh vực:** Artificial Intelligence / Computer Vision / MLOps / Edge Computing / Data Engineering

**Mô hình:** YOLOv8

**Object Storage:** MinIO

**Analytics Database:** DuckDB

**Dashboard:** Streamlit

**Containerization:** Docker

---

## License

Source code được sử dụng cho mục đích học tập và nghiên cứu trong phạm vi đồ án tốt nghiệp.
