import os
import glob
import time
import json
import torch
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ultralytics import YOLO

# Set random seed
torch.manual_seed(42)
np.random.seed(42)

BASE_DIR = r"d:\大学\机器视觉算法与应用\lab4"
FRAMES_DIR = os.path.join(BASE_DIR, "data", "frames")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# Helper to read image with unicode path
def read_image(path):
    data = np.fromfile(path, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return img

def save_image(img, path):
    ext = os.path.splitext(path)[1]
    ret, buf = cv2.imencode(ext, img)
    if ret:
        buf.tofile(path)

# Compute box IoU
def box_iou(box1, box2):
    # box: [x1, y1, x2, y2]
    xA = max(box1[0], box2[0])
    yA = max(box1[1], box2[1])
    xB = min(box1[2], box2[2])
    yB = min(box1[3], box2[3])
    interW = max(0.0, xB - xA)
    interH = max(0.0, yB - yA)
    interArea = interW * interH
    boxAArea = (box1[2] - box1[0]) * (box1[3] - box1[1])
    boxBArea = (box2[2] - box2[0]) * (box2[3] - box2[1])
    unionArea = boxAArea + boxBArea - interArea
    if unionArea <= 0:
        return 0.0
    return interArea / unionArea

# Match consecutive frames detections
def compute_temporal_consistency(detections_per_frame):
    # detections_per_frame: list of list of dict(box, cls, conf)
    consecutive_ious = []
    matched_counts = []
    total_prev_counts = []
    
    for t in range(len(detections_per_frame) - 1):
        dets_t = detections_per_frame[t]
        dets_next = detections_per_frame[t+1]
        total_prev_counts.append(len(dets_t))
        if len(dets_t) == 0 or len(dets_next) == 0:
            consecutive_ious.append(0.0)
            matched_counts.append(0)
            continue
        
        # Match by class and max IoU
        matched_ious = []
        used_next = set()
        for d1 in dets_t:
            best_iou = 0.0
            best_idx = -1
            for j, d2 in enumerate(dets_next):
                if j in used_next:
                    continue
                if d1['cls'] == d2['cls']:
                    iou = box_iou(d1['box'], d2['box'])
                    if iou > best_iou:
                        best_iou = iou
                        best_idx = j
            if best_iou > 0.1:  # match threshold
                matched_ious.append(best_iou)
                used_next.add(best_idx)
        
        matched_counts.append(len(matched_ious))
        if matched_ious:
            consecutive_ious.append(np.mean(matched_ious))
        else:
            consecutive_ious.append(0.0)
            
    mean_temp_iou = float(np.mean(consecutive_ious)) if consecutive_ious else 0.0
    persistence_rate = float(np.sum(matched_counts) / max(1, np.sum(total_prev_counts)))
    return {
        "mean_temporal_iou": mean_temp_iou,
        "persistence_rate": persistence_rate,
        "frame_ious": consecutive_ious
    }

def run_all_experiments():
    frame_files = sorted(glob.glob(os.path.join(FRAMES_DIR, "*.jpg")))
    print(f"Loaded {len(frame_files)} campus frames.")
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    experiments = [
        {"name": "YOLOv8n_640", "weights": "yolov8n.pt", "imgsz": 640, "conf": 0.25, "desc": "轻量级基线 (Nano, 640p)"},
        {"name": "YOLOv8s_640", "weights": "yolov8s.pt", "imgsz": 640, "conf": 0.25, "desc": "平衡型规模 (Small, 640p)"},
        {"name": "YOLOv8x_640", "weights": "yolov8x.pt", "imgsz": 640, "conf": 0.25, "desc": "高精度大模型 (X-Large, 640p)"},
        {"name": "YOLOv8x_1280", "weights": "yolov8x.pt", "imgsz": 1280, "conf": 0.25, "desc": "超分辨率大模型 (X-Large, 1280p)"},
        {"name": "YOLOv8x_conf50", "weights": "yolov8x.pt", "imgsz": 640, "conf": 0.50, "desc": "严格置信门限 (X-Large, 640p, conf=0.5)"},
    ]
    
    all_results = {}
    
    for exp in experiments:
        name = exp["name"]
        print(f"\n================ Running Experiment: {name} ================")
        model = YOLO(exp["weights"])
        model.to(device)
        
        # Warmup
        dummy = np.zeros((640, 640, 3), dtype=np.uint8)
        for _ in range(5):
            _ = model.predict(dummy, imgsz=exp["imgsz"], device=device, verbose=False)
            
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats(device)
            torch.cuda.synchronize()
            
        times = []
        frame_detections = []
        class_counts = {}
        confidence_list = []
        
        t0 = time.time()
        for idx, fpath in enumerate(frame_files):
            img = read_image(fpath)
            
            t_start = time.time()
            res = model.predict(
                img,
                imgsz=exp["imgsz"],
                conf=exp["conf"],
                iou=0.7,
                device=device,
                verbose=False
            )[0]
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            t_end = time.time()
            
            times.append((t_end - t_start) * 1000) # ms
            
            dets = []
            boxes = res.boxes
            if boxes is not None and len(boxes) > 0:
                xyxy = boxes.xyxy.cpu().numpy()
                confs = boxes.conf.cpu().numpy()
                clss = boxes.cls.cpu().numpy().astype(int)
                names = res.names
                
                for b, c, cl in zip(xyxy, confs, clss):
                    cname = names[cl]
                    dets.append({
                        "box": [float(x) for x in b],
                        "conf": float(c),
                        "cls": cname,
                        "cls_id": int(cl)
                    })
                    class_counts[cname] = class_counts.get(cname, 0) + 1
                    confidence_list.append(float(c))
            
            frame_detections.append(dets)
            
        total_time = time.time() - t0
        peak_vram = torch.cuda.max_memory_allocated(device) / (1024**2) if torch.cuda.is_available() else 0.0
        
        temp_metrics = compute_temporal_consistency(frame_detections)
        
        mean_lat = float(np.mean(times))
        std_lat = float(np.std(times))
        fps = 1000.0 / mean_lat if mean_lat > 0 else 0.0
        
        exp_summary = {
            "name": name,
            "desc": exp["desc"],
            "weights": exp["weights"],
            "imgsz": exp["imgsz"],
            "conf": exp["conf"],
            "latency_mean_ms": round(mean_lat, 2),
            "latency_std_ms": round(std_lat, 2),
            "fps": round(fps, 1),
            "peak_vram_mb": round(peak_vram, 1),
            "total_detections": sum(class_counts.values()),
            "class_distribution": class_counts,
            "mean_confidence": round(float(np.mean(confidence_list)), 3) if confidence_list else 0.0,
            "temporal_iou": round(temp_metrics["mean_temporal_iou"], 3),
            "persistence_rate": round(temp_metrics["persistence_rate"], 3),
            "per_frame_counts": [len(d) for d in frame_detections],
            "frame_ious": [round(x, 3) for x in temp_metrics["frame_ious"]],
            "detections": frame_detections
        }
        
        print(f"Summary for {name}:")
        print(f"  Latency: {exp_summary['latency_mean_ms']} ms ± {exp_summary['latency_std_ms']} ms (FPS: {exp_summary['fps']})")
        print(f"  Peak VRAM: {exp_summary['peak_vram_mb']} MB")
        print(f"  Total Detections: {exp_summary['total_detections']} (Mean Conf: {exp_summary['mean_confidence']})")
        print(f"  Classes: {class_counts}")
        print(f"  Temporal IoU: {exp_summary['temporal_iou']}, Persistence: {exp_summary['persistence_rate']}")
        
        all_results[name] = exp_summary
        
    # Save results to json
    results_path = os.path.join(OUTPUT_DIR, "experiment_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\nAll experiment metrics saved to {results_path}")
    return all_results

if __name__ == "__main__":
    run_all_experiments()
