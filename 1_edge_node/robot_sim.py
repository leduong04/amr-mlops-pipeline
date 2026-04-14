import cv2
import json
import os
import uuid
from datetime import datetime, timezone
from ultralytics import YOLO
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv

# ==========================================
# 1. KHỞI TẠO HỆ THỐNG VÀ BẢO MẬT
# ==========================================
load_dotenv()  # Load các biến bảo mật từ file .env

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET = os.getenv("MINIO_SECRET_KEY")
BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

MODEL_PATH = 'yolov8n.pt'
ROBOT_ID = "AMR_01"
OOD_CONF_MIN = 0.3  
OOD_CONF_MAX = 0.6  

print("[HỆ THỐNG] Đang khởi động AI & Kết nối Data Lake...")
model = YOLO(MODEL_PATH)

# Khởi tạo kết nối API lên DigitalOcean
client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS,
    secret_key=MINIO_SECRET,
    secure=False  # Dùng False vì HTTP nội bộ, nếu có HTTPS (SSL) thì đổi thành True
)

# ==========================================
# 2. LOGIC SUY LUẬN & TỐI ƯU BĂNG THÔNG
# ==========================================
def process_and_upload(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"❌ Lỗi: Không thể đọc ảnh {image_path}")
        return

    # 1. Chạy Edge AI Inference
    results = model(frame, verbose=False)[0]
    
    # Tạo ID duy nhất cho phiên giao dịch này
    trace_id = uuid.uuid4().hex[:8]
    timestamp_str = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    file_prefix = f"{ROBOT_ID}_{timestamp_str}_{trace_id}"

    payload = {
        "trace_id": trace_id,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "robot_id": ROBOT_ID,
        "detections": [],
        "is_ood": False
    }

    # 2. Phân tích kết quả và Bắt OOD
    for box in results.boxes:
        conf = float(box.conf[0])
        cls_name = model.names[int(box.cls[0])]
        
        payload["detections"].append({
            "class": cls_name,
            "confidence": round(conf, 3),
            "bbox": list(map(int, box.xyxy[0]))  # <-- Bọc thêm list() ở đây
        })

        # Uncertainty Sampling
        if OOD_CONF_MIN <= conf <= OOD_CONF_MAX:
            payload["is_ood"] = True

    # ==========================================
    # 3. GIAO TIẾP VỚI CLOUD (MINIO API)
    # ==========================================
    try:
        # A. Luôn luôn gửi Log JSON lên thư mục /logs/
        json_file_path = f"{file_prefix}.json"
        with open(json_file_path, 'w') as f:
            json.dump(payload, f)
            
        client.fput_object(
            BUCKET_NAME, 
            f"logs/{json_file_path}", 
            json_file_path,
            content_type="application/json"
        )
        os.remove(json_file_path) # Xóa file tạm ở máy tính

        # B. Tối ưu: CHỈ tải ảnh lên Cloud nếu phát hiện vật thể lạ (OOD)
        if payload["is_ood"]:
            image_cloud_path = f"anomaly_images/{file_prefix}.jpg"
            client.fput_object(
                BUCKET_NAME,
                image_cloud_path,
                image_path,
                content_type="image/jpeg"
            )
            print(f"⚠️ [CẢNH BÁO OOD] Đã tải ảnh nghi ngờ lên Cloud: {image_cloud_path}")
        else:
            print("✅ [BÌNH THƯỜNG] AI tự tin với kết quả. Chỉ gửi JSON log, bỏ qua upload ảnh.")

        print(f"🚀 Thành công đẩy JSON Log lên Data Lake: logs/{json_file_path}\n")

    except S3Error as exc:
        print("❌ Lỗi kết nối MinIO:", exc)

# ==========================================
# CHẠY THỰC NGHIỆM
# ==========================================
if __name__ == "__main__":
    IMAGE_DIR = "test_images"
    # Định nghĩa các định dạng ảnh được hỗ trợ
    VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

    # 1. Đảm bảo thư mục tồn tại
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    # 2. Lấy danh sách file và lọc theo định dạng ảnh
    image_files = [f for f in os.listdir(IMAGE_DIR) 
                   if f.lower().endswith(VALID_EXTENSIONS)]
    
    # 3. Xử lý trường hợp thư mục trống
    if not image_files:
        sample_path = os.path.join(IMAGE_DIR, "sample.jpg")
        import numpy as np
        # Tạo ảnh đen giả lập để kiểm tra kết nối API
        cv2.imwrite(sample_path, np.zeros((480, 640, 3), dtype=np.uint8))
        print(f"⚠️ Thư mục '{IMAGE_DIR}' đang trống. Đã tạo ảnh mẫu: {sample_path}")
        image_files = ["sample.jpg"]

    print(f"🚀 Tìm thấy {len(image_files)} tệp tin ảnh. Bắt đầu luồng Pipeline...")

    # 4. Vòng lặp xử lý tuần tự (Sequential processing)
    for filename in sorted(image_files):
        full_path = os.path.join(IMAGE_DIR, filename)
        print(f"\n[TIẾN TRÌNH] Đang phân tích: {filename}...")
        process_and_upload(full_path)

    print(f"\n✅ Đã hoàn tất xử lý {len(image_files)} ảnh. Kiểm tra kết quả tại MinIO Console.")