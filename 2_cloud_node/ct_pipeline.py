import os
import shutil
import boto3
from ultralytics import YOLO
import yaml

# Cấu hình MinIO
MINIO_CONFIG = {
    "endpoint_url": "http://localhost:9000",
    "access_key": "admin_mlops",
    "secret_key": "MLOpsPassword2026!",
    "bucket": "robot-logs"
}

def setup_directories():
    base_dir = "dataset_ood"
    os.makedirs(f"{base_dir}/images/train", exist_ok=True)
    os.makedirs(f"{base_dir}/labels/train", exist_ok=True)
    return base_dir

def pull_ood_data_and_label(base_dir):
    s3 = boto3.client('s3', endpoint_url=MINIO_CONFIG["endpoint_url"],
                      aws_access_key_id=MINIO_CONFIG["access_key"],
                      aws_secret_access_key=MINIO_CONFIG["secret_key"])
    
    # 1. Kéo ảnh từ MinIO
    print("[1] Đang tải ảnh dị thường (OOD) từ Data Lake...")
    response = s3.list_objects_v2(Bucket=MINIO_CONFIG["bucket"], Prefix='anomaly_images/')
    if 'Contents' not in response:
        print("Không có ảnh OOD mới để huấn luyện.")
        return False
        
    for obj in response['Contents']:
        file_key = obj['Key']
        if file_key.endswith('/'): continue
        local_path = f"{base_dir}/images/train/{os.path.basename(file_key)}"
        s3.download_file(MINIO_CONFIG["bucket"], file_key, local_path)

    # 2. Mô phỏng Gán nhãn (Pseudo-labeling) bằng Model Giáo viên (YOLOv8m)
    print("[2] Bắt đầu gán nhãn tự động (Pseudo-labeling)...")
    teacher_model = YOLO('/root/mlops_pipeline/models/yolov8m_best.pt') # Dùng model lớn hơn để tạo nhãn chuẩn
    
    # Tạo file data.yaml cho quá trình re-train
    yaml_content = {
        'path': os.path.abspath(base_dir),
        'train': 'images/train',
        'val': 'images/train', # Tạm dùng train làm val cho demo
        'names': {0: 'person', 1: 'forklift', 2: 'carton_box', 3: 'safety_cone', 4: 'wet_floor_sign'}
    }
    with open(f"{base_dir}/data_ood.yaml", 'w') as f:
        yaml.dump(yaml_content, f)

    # Sinh file .txt chứa bounding box
    for img_name in os.listdir(f"{base_dir}/images/train"):
        img_path = f"{base_dir}/images/train/{img_name}"
        results = teacher_model(img_path, verbose=False)[0]
        label_path = f"{base_dir}/labels/train/{img_name.replace('.jpg', '.txt').replace('.png', '.txt')}"
        
        with open(label_path, 'w') as f:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                # Format YOLO: class x_center y_center width height (chuẩn hóa 0-1)
                x_c, y_c, w, h = box.xywhn[0].tolist()
                f.write(f"{cls_id} {x_c} {y_c} {w} {h}\n")
    return True

def continuous_training(base_dir):
    print("[3] Bắt đầu Transfer Learning (Fine-tuning)...")
    # Tải trọng số tốt nhất hiện tại của robot (YOLOv8s)
    student_model = YOLO('/root/mlops_pipeline/models/yolov8s_best.pt') 
    
    # Chỉ train số epoch nhỏ (Transfer learning) để cập nhật kiến thức mới
    student_model.train(
        data=f"{base_dir}/data_ood.yaml",
        epochs=10, 
        imgsz=640,
        project="MLOps_CT",
        name="retrain_run"
    )
    
    # 4. Model Registry: Đẩy model mới (best.pt) lên MinIO
    print("[4] Cập nhật Model Registry...")
    new_weight_path = "/root/mlops_pipeline/models/best.pt"
    
    s3 = boto3.client('s3', endpoint_url=MINIO_CONFIG["endpoint_url"],
                      aws_access_key_id=MINIO_CONFIG["access_key"],
                      aws_secret_access_key=MINIO_CONFIG["secret_key"])
    
    # Upload đè lên MinIO ở bucket model-registry
    try:
        s3.create_bucket(Bucket="model-registry")
    except: pass # Bỏ qua nếu bucket đã tồn tại
    
    s3.upload_file(new_weight_path, "model-registry", "best_v2.pt")
    print("✅ Đã phát hành phiên bản Model mới: best_v2.pt lên Data Lake!")

if __name__ == "__main__":
    b_dir = setup_directories()
    if pull_ood_data_and_label(b_dir):
        continuous_training(b_dir)
