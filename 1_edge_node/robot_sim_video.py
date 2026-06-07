import cv2
import json
import os
import uuid
import argparse
import time

from datetime import datetime, timezone

from ultralytics import YOLO
from minio import Minio
from dotenv import load_dotenv
import urllib3
import time

# ==================================================
# ARGUMENTS
# ==================================================

parser = argparse.ArgumentParser(
    description="AMR Video Simulator"
)

parser.add_argument(
    "--robot_id",
    type=str,
    required=True,
    help="Robot ID"
)

parser.add_argument(
    "--video",
    type=str,
    required=True,
    help="Video file"
)

parser.add_argument(
    "--skip_frames",
    type=int,
    default=30,
    help="Process every N frames"
)

args = parser.parse_args()


# ==================================================
# INIT
# ==================================================

load_dotenv()

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)


def check_and_update_model():
    print("🔄 [CD Pipeline] Đang kiểm tra bản cập nhật Model mới từ Registry...")
    try:
        # Gọi thẳng tới file public hoặc dùng client MinIO để download best_v2.pt
        response = client.stat_object("model-registry", "best_v2.pt")
        last_modified = response.last_modified
        
        # Nếu chưa có file best_v2.pt trên máy, hoặc model trên cloud mới hơn
        if not os.path.exists("best_v2.pt"):
            print("⬇️ Phát hiện trọng số mới (best_v2.pt). Đang tải về Edge Node...")
            client.fget_object("model-registry", "best_v2.pt", "best_v2.pt")
            print("✅ Đã cập nhật xong. Hot-swap thành công sang Model V2!")
            return YOLO('best_v2.pt')
    except Exception as e:
        print("Trọng số hiện tại là mới nhất (V1). Bỏ qua cập nhật.")
        pass
    
    return YOLO("/home/leduong/DO_AN_MLOPS/1_edge_node/models/yolov8s_best.pt") # Dùng bản cũ nếu không có bản mới

# Thay đổi lúc khởi tạo model:
# Mọi khi: model = YOLO('yolov8s.pt')
# Bây giờ:
model = check_and_update_model()


# model = YOLO(
#     "/home/leduong/DO_AN_MLOPS/1_edge_node/models/yolov8s_best.pt"
# )


# ==================================================
# MAIN
# ==================================================

def process_video():

    cap = cv2.VideoCapture(args.video)

    if not cap.isOpened():
        print(
            f"❌ [{args.robot_id}] "
            f"Cannot open video: {args.video}"
        )
        return

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    fps_video = cap.get(
        cv2.CAP_PROP_FPS
    )

    print("=" * 60)
    print(f"Robot      : {args.robot_id}")
    print(f"Video      : {args.video}")
    print(f"Frames     : {total_frames}")
    print(f"FPS        : {fps_video}")
    print("=" * 60)

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            print(
                f"\n🛑 [{args.robot_id}] "
                f"Video ended at frame "
                f"{frame_count}/{total_frames}"
            )
            break

        frame_count += 1

        display_frame = frame.copy()

        # ==========================================
        # SKIP FRAME
        # ==========================================

        if frame_count % args.skip_frames != 0:

            cv2.putText(
                display_frame,
                f"Frame: {frame_count}/{total_frames}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            cv2.imshow(
                f"AMR - {args.robot_id}",
                display_frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            continue

        # ==========================================
        # YOLO INFERENCE
        # ==========================================

        start_time = time.time()

        results = model(
            frame,
            verbose=False
        )[0]

        infer_time = time.time() - start_time

        fps = 1 / infer_time if infer_time > 0 else 0

        trace_id = uuid.uuid4().hex[:8]

        timestamp = datetime.now(
            timezone.utc
        )

        file_prefix = (
            f"{args.robot_id}_"
            f"{timestamp.strftime('%Y%m%d_%H%M%S')}_"
            f"{trace_id}"
        )

        payload = {
            "trace_id": trace_id,
            "timestamp":
                timestamp.isoformat()
                .replace("+00:00", "Z"),
            "robot_id": args.robot_id,
            "detections": [],
            "is_ood": False
        }

        # ==========================================
        # DRAW BOXES
        # ==========================================

        for box in results.boxes:

            conf = float(box.conf[0])

            cls_id = int(box.cls[0])

            class_name = model.names[cls_id]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            payload["detections"].append({
                "class": class_name,
                "confidence": round(conf, 3),
                "bbox": [x1, y1, x2, y2]
            })

            if 0.3 <= conf <= 0.6:
                payload["is_ood"] = True

            cv2.rectangle(
                display_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                display_frame,
                f"{class_name} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        # ==========================================
        # OVERLAY INFO
        # ==========================================

        cv2.putText(
            display_frame,
            f"Frame: {frame_count}/{total_frames}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.putText(
            display_frame,
            f"FPS: {fps:.2f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        cv2.putText(
            display_frame,
            f"Objects: {len(results.boxes)}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        if payload["is_ood"]:

            cv2.putText(
                display_frame,
                "OOD DETECTED",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # ==========================================
        # SHOW VIDEO
        # ==========================================

        cv2.imshow(
            f"AMR - {args.robot_id}",
            display_frame
        )

        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):
            print(
                f"\n🛑 [{args.robot_id}] "
                f"Stopped by user."
            )
            break

        # ==========================================
        # SEND TO CLOUD
        # ==========================================

        try:

            json_path = (
                f"temp_{file_prefix}.json"
            )

            with open(
                json_path,
                "w"
            ) as f:
                json.dump(
                    payload,
                    f,
                    indent=2
                )

            client.fput_object(
                os.getenv(
                    "MINIO_BUCKET_NAME"
                ),
                f"logs/{file_prefix}.json",
                json_path,
                content_type="application/json"
            )

            os.remove(json_path)

            if payload["is_ood"]:

                img_path = (
                    f"temp_{file_prefix}.jpg"
                )

                cv2.imwrite(
                    img_path,
                    frame
                )

                client.fput_object(
                    os.getenv(
                        "MINIO_BUCKET_NAME"
                    ),
                    f"anomaly_images/{file_prefix}.jpg",
                    img_path,
                    content_type="image/jpeg"
                )

                os.remove(img_path)

                print(
                    f"⚠️ [{args.robot_id}] "
                    f"OOD uploaded."
                )

            else:

                print(
                    f"✅ [{args.robot_id}] "
                    f"Frame {frame_count} processed."
                )

        except Exception as e:

            print(
                f"❌ [{args.robot_id}] "
                f"Cloud Error: {e}"
            )

    cap.release()

    cv2.destroyAllWindows()

    print(
        f"🏁 [{args.robot_id}] "
        f"Simulation finished."
    )


# ==================================================
# ENTRY
# ==================================================

if __name__ == "__main__":
    process_video()