import os
import glob
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager as fm

# Setup Chinese font
font_path = 'C:/Windows/Fonts/simhei.ttf'
zh_font = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = r"d:\大学\机器视觉算法与应用\lab4"
FRAMES_DIR = os.path.join(BASE_DIR, "data", "frames")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
RESULTS_PATH = os.path.join(BASE_DIR, "output", "experiment_results.json")
os.makedirs(FIGURES_DIR, exist_ok=True)

with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    results = json.load(f)

# Helper to load image
def load_rgb(fname):
    p = os.path.join(FRAMES_DIR, fname)
    buf = np.fromfile(p, dtype=np.uint8)
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Colors for bounding boxes
CLASS_COLORS = {
    'person': (235, 60, 60),      # Red
    'bicycle': (40, 160, 240),    # Blue
    'car': (50, 200, 100),        # Green
    'motorcycle': (240, 160, 40), # Orange
    'backpack': (180, 80, 240),   # Purple
    'handbag': (240, 80, 180),    # Pink
    'bottle': (100, 220, 220),    # Cyan
    'kite': (200, 200, 50),       # Yellow
    'potted plant': (80, 160, 80) # Dark green
}

def draw_detections(img, dets, min_conf=0.25):
    vis = img.copy()
    h, w, _ = vis.shape
    for d in dets:
        if d['conf'] < min_conf:
            continue
        box = [int(v) for v in d['box']]
        cls_name = d['cls']
        conf = d['conf']
        color = CLASS_COLORS.get(cls_name, (200, 200, 200))
        
        # Bounding box
        cv2.rectangle(vis, (box[0], box[1]), (box[2], box[3]), color, 3)
        
        # Label text
        label = f"{cls_name} {conf:.2f}"
        (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        y1 = max(0, box[1] - th - 6)
        cv2.rectangle(vis, (box[0], y1), (box[0] + tw + 6, y1 + th + 6), color, -1)
        cv2.putText(vis, label, (box[0] + 3, y1 + th + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    return vis

# ----------------- Fig 1: YOLOv8 Architecture -----------------
def generate_fig1_architecture():
    print("Generating Fig 1: Architecture Diagram...")
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 75)
    ax.axis('off')
    
    # Title
    ax.text(60, 71, "YOLOv8 开源目标检测算法核心模块调用关系与推理/训练全流程", 
            ha='center', va='center', fontsize=14, fontweight='bold', fontproperties=zh_font, color='#1a2332')
    
    def draw_box(x, y, w, h, title, subtitle, bg='#e8f2ff', border='#3273dc'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8", 
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.65, title, ha='center', va='center', 
                fontsize=10, fontweight='bold', fontproperties=zh_font, color='#111827')
        ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', 
                fontsize=8, fontproperties=zh_font, color='#4b5563')

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#4b5563", lw=1.5))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 1.2, label, ha='center', va='bottom', 
                    fontsize=8, fontproperties=zh_font, color='#1f2937')

    # Backbone column
    ax.text(18, 64, "【骨干网络 Backbone】\nCSPDarknet 跨尺度分层特征提取", ha='center', va='center', 
            fontsize=10.5, fontweight='bold', fontproperties=zh_font, color='#1e3a8a')
    draw_box(6, 48, 24, 10, "Conv 卷积下采样", "k=3, s=2, p=1 (P1/2)", bg='#eff6ff', border='#3b82f6')
    draw_box(6, 34, 24, 10, "C2f 跨阶段局部瓶颈", "梯度分流 + n个Bottleneck", bg='#eff6ff', border='#3b82f6')
    draw_box(6, 20, 24, 10, "SPPF 空间金字塔池化", "多尺度最大池化 (5×5, 9×9, 13×13)", bg='#eff6ff', border='#3b82f6')
    draw_box(6, 6, 24, 10, "多尺度特征图输出", "P3(80×80), P4(40×40), P5(20×20)", bg='#eff6ff', border='#3b82f6')
    
    draw_arrow(18, 48, 18, 44)
    draw_arrow(18, 34, 18, 30)
    draw_arrow(18, 20, 18, 16)
    
    # Neck column
    ax.text(58, 64, "【特征融合 Neck】\nPAN-FPN 双向特征金字塔路径", ha='center', va='center', 
            fontsize=10.5, fontweight='bold', fontproperties=zh_font, color='#065f46')
    draw_box(46, 44, 24, 12, "Top-Down 自顶向下分支", "上采样 (Nearest) + 高低层Concat\n引入丰富深层语义上下文", bg='#ecfdf5', border='#10b981')
    draw_box(46, 16, 24, 12, "Bottom-Up 自底向上分支", "步长2卷积下采样 + Concat\n强化浅层空间位置与几何细节", bg='#ecfdf5', border='#10b981')
    draw_arrow(46+12, 44, 46+12, 28, "自顶向下融合")
    draw_arrow(30, 25, 46, 50, "P5/P4 注入")
    draw_arrow(30, 11, 46, 22, "P3 浅层注入")

    # Head & Loss column
    ax.text(98, 64, "【解耦检测头 Head 与损失】\nDecoupled Head & Task-Aligned", ha='center', va='center', 
            fontsize=10.5, fontweight='bold', fontproperties=zh_font, color='#9a3412')
    draw_box(86, 48, 26, 11, "分类分支 Cls Head", "BCE / Varifocal Loss\n预测多类别后验概率", bg='#fff7ed', border='#f97316')
    draw_box(86, 32, 26, 11, "回归分支 Reg Head (DFL)", "CIoU 几何损失 + DFL 分布焦损\n回归坐标概率分布连续积分", bg='#fff7ed', border='#f97316')
    draw_box(86, 16, 26, 11, "动态样本匹配 Assigner", "TaskAlignedAssigner\nt = s^α × IoU^β 联合动态门限", bg='#fef3c7', border='#f59e0b')
    draw_box(86, 2, 26, 9, "后处理与输出 (NMS)", "非极大值抑制 (IoU>0.7) 过滤重叠框", bg='#f3f4f6', border='#6b7280')

    draw_arrow(70, 50, 86, 53)
    draw_arrow(70, 22, 86, 37)
    draw_arrow(99, 32, 99, 27)
    draw_arrow(99, 16, 99, 11)

    plt.tight_layout()
    out_file = os.path.join(FIGURES_DIR, "fig1_yolo_arch.png")
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_file}")

# ----------------- Fig 2: Representative Detections -----------------
def generate_fig2_representative():
    print("Generating Fig 2: Representative Detections...")
    key_frames = ["0000.jpg", "0016.jpg", "0032.jpg", "0047.jpg"]
    titles = [
        "(a) 关键帧 #0000 · 南侧主立面起点 (人行道、绿化与行人通行)",
        "(b) 关键帧 #0016 · 西侧竹林转角 (鹅卵石步道、深阴影与强逆光)",
        "(c) 关键帧 #0032 · 北侧广场开阔区 (密集多目标、行人与停放自行车)",
        "(d) 关键帧 #0047 · 终点闭环复访区 (回环回到主立面，远近尺度)"
    ]
    
    # We use YOLOv8x 640 results
    dets_v8x = results["YOLOv8x_640"]["detections"]
    frame_indices = [0, 16, 32, 47]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 13), dpi=300)
    axes = axes.flatten()
    
    for ax, fname, title, f_idx in zip(axes, key_frames, titles, frame_indices):
        img_rgb = load_rgb(fname)
        dets = dets_v8x[f_idx]
        vis = draw_detections(img_rgb, dets, min_conf=0.25)
        ax.imshow(vis)
        ax.set_title(title, fontsize=11, fontweight='bold', fontproperties=zh_font, pad=8)
        ax.axis('off')
        
    plt.tight_layout()
    out_file = os.path.join(FIGURES_DIR, "fig2_representative_detections.png")
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_file}")

# ----------------- Fig 3: Model and Resolution Comparison -----------------
def generate_fig3_comparison():
    print("Generating Fig 3: Model Scale & Resolution Comparison on Frame #0032...")
    fname = "0032.jpg"
    img_rgb = load_rgb(fname)
    
    dets_n = results["YOLOv8n_640"]["detections"][32]
    dets_x_640 = results["YOLOv8x_640"]["detections"][32]
    dets_x_1280 = results["YOLOv8x_1280"]["detections"][32]
    dets_x_conf50 = results["YOLOv8x_conf50"]["detections"][32]
    
    vis_n = draw_detections(img_rgb, dets_n)
    vis_x_640 = draw_detections(img_rgb, dets_x_640)
    vis_x_1280 = draw_detections(img_rgb, dets_x_1280)
    vis_x_conf50 = draw_detections(img_rgb, dets_x_conf50)
    
    # Let's crop a region of interest: distant bicycles in background
    # (crop around top-center / mid-plaza area)
    # img is 1920x1080 (h, w)
    crop_box = (850, 450, 1350, 950) # ymin, xmin, ymax, xmax
    
    fig = plt.figure(figsize=(15, 12), dpi=300)
    gs = fig.add_gridspec(2, 2, hspace=0.15, wspace=0.1)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(vis_n)
    ax1.set_title(f"(a) YOLOv8n (640p, conf=0.25) · 检出 {len(dets_n)} 个目标\n轻量级模型对远景微小自行车与重叠行人存在明显漏检", 
                  fontsize=10.5, fontweight='bold', fontproperties=zh_font)
    ax1.axis('off')
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(vis_x_640)
    ax2.set_title(f"(b) YOLOv8x (640p, conf=0.25) · 检出 {len(dets_x_640)} 个目标\n大参数量提升深层语义表征，行人与中尺度车辆识别准确率显著提高", 
                  fontsize=10.5, fontweight='bold', fontproperties=zh_font)
    ax2.axis('off')
    
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(vis_x_1280)
    ax3.set_title(f"(c) YOLOv8x (1280p 超分辨率, conf=0.25) · 检出 {len(dets_x_1280)} 个目标\n高分辨率保留微弱边缘与微小纹理，远景密集停放自行车召回率大幅跃升", 
                  fontsize=10.5, fontweight='bold', fontproperties=zh_font)
    ax3.axis('off')
    
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.imshow(vis_x_conf50)
    ax4.set_title(f"(d) YOLOv8x (640p, 严格门限 conf=0.50) · 检出 {len(dets_x_conf50)} 个目标\n高置信度门限有效剔除模糊假阳性，但导致部分受遮挡弱纹理目标被滤除", 
                  fontsize=10.5, fontweight='bold', fontproperties=zh_font)
    ax4.axis('off')
    
    out_file = os.path.join(FIGURES_DIR, "fig3_model_and_res_comparison.png")
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_file}")

# ----------------- Fig 4: Temporal Curves & Pareto Tradeoff -----------------
def generate_fig4_temporal_curves():
    print("Generating Fig 4: Temporal Consistency & Performance Tradeoff...")
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.2), dpi=300)
    
    frames = list(range(48))
    
    # 1. Target count curve
    colors = {'YOLOv8n_640': '#2563eb', 'YOLOv8s_640': '#059669', 'YOLOv8x_640': '#d97706', 'YOLOv8x_1280': '#dc2626', 'YOLOv8x_conf50': '#7c3aed'}
    labels = {
        'YOLOv8n_640': 'YOLOv8n (640p)',
        'YOLOv8s_640': 'YOLOv8s (640p)',
        'YOLOv8x_640': 'YOLOv8x (640p)',
        'YOLOv8x_1280': 'YOLOv8x (1280p)',
        'YOLOv8x_conf50': 'YOLOv8x (conf=0.5)'
    }
    
    for key in ['YOLOv8n_640', 'YOLOv8s_640', 'YOLOv8x_640', 'YOLOv8x_1280', 'YOLOv8x_conf50']:
        counts = results[key]['per_frame_counts']
        ax1.plot(frames, counts, label=labels[key], color=colors[key], lw=1.8, alpha=0.85)
        
    ax1.set_title("图 4(a) 48 帧校园视频检测目标总数时序变化", fontsize=11, fontweight='bold', fontproperties=zh_font)
    ax1.set_xlabel("视频关键帧序号 (0 ~ 47)", fontsize=9.5, fontproperties=zh_font)
    ax1.set_ylabel("检出目标数量 (个)", fontsize=9.5, fontproperties=zh_font)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(prop=zh_font, fontsize=8.5, loc='upper left')
    
    # Add vertical line annotations for 3 video segments
    ax1.axvline(x=15.5, color='#9ca3af', linestyle=':', lw=1.2)
    ax1.axvline(x=31.5, color='#9ca3af', linestyle=':', lw=1.2)
    ax1.text(7, 18, "段1: 南立面", ha='center', fontsize=8, fontproperties=zh_font, color='#4b5563')
    ax1.text(23, 18, "段2: 竹林转角", ha='center', fontsize=8, fontproperties=zh_font, color='#4b5563')
    ax1.text(39, 18, "段3: 北侧广场", ha='center', fontsize=8, fontproperties=zh_font, color='#4b5563')
    
    # 2. Temporal IoU curve
    for key in ['YOLOv8n_640', 'YOLOv8x_640', 'YOLOv8x_1280']:
        ious = results[key]['frame_ious']
        ax2.plot(range(len(ious)), ious, label=labels[key], color=colors[key], lw=1.8, alpha=0.85)
    ax2.set_title("图 4(b) 相邻帧间检测边界框 IoU 时序重叠一致性", fontsize=11, fontweight='bold', fontproperties=zh_font)
    ax2.set_xlabel("相邻帧转换对序号 t → t+1", fontsize=9.5, fontproperties=zh_font)
    ax2.set_ylabel("平均匹配 IoU 重叠率", fontsize=9.5, fontproperties=zh_font)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(prop=zh_font, fontsize=8.5, loc='upper right')
    ax2.axvline(x=15.5, color='#ef4444', linestyle='--', lw=1.2, alpha=0.7)
    ax2.text(15.5, 0.45, "拐角剧烈转向\nIoU 发生谷底跌落", ha='center', fontsize=8, fontproperties=zh_font, color='#ef4444')

    # 3. Pareto tradeoff scatter: Latency vs Total Detections vs VRAM Bubble
    for key in ['YOLOv8n_640', 'YOLOv8s_640', 'YOLOv8x_640', 'YOLOv8x_1280', 'YOLOv8x_conf50']:
        lat = results[key]['latency_mean_ms']
        det = results[key]['total_detections']
        vram = results[key]['peak_vram_mb']
        ax3.scatter(lat, det, s=vram * 0.4, color=colors[key], alpha=0.7, edgecolors='black', lw=1.2, label=labels[key])
        ax3.annotate(f"{key}\n({lat}ms, {det}个)", (lat + 2, det - 8), fontsize=8, fontproperties=zh_font)
        
    ax3.set_title("图 4(c) 推理时延 vs 目标总检出量 vs 显存占用 (气泡面积)", fontsize=11, fontweight='bold', fontproperties=zh_font)
    ax3.set_xlabel("单帧平均推理耗时 (ms) [RTX 4060 Laptop]", fontsize=9.5, fontproperties=zh_font)
    ax3.set_ylabel("48 帧总检出目标数 (个)", fontsize=9.5, fontproperties=zh_font)
    ax3.grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    out_file = os.path.join(FIGURES_DIR, "fig4_temporal_curves.png")
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_file}")

# ----------------- Fig 5: Failure Cases Analysis -----------------
def generate_fig5_failure_cases():
    print("Generating Fig 5: Failure Cases Analysis...")
    fig, axes = plt.subplots(1, 3, figsize=(16, 6.2), dpi=300)
    
    # Failure Case 1: Motion Blur & Backlight in Frame 0017
    img_17 = load_rgb("0017.jpg")
    dets_17 = results["YOLOv8x_640"]["detections"][17]
    vis_17 = draw_detections(img_17, dets_17)
    # Target range around y: 480~750, x: 200~850
    crop_17 = vis_17[480:780, 200:850]
    axes[0].imshow(crop_17)
    axes[0].set_title("失败案例 1：快速转弯运动模糊与逆光光晕 (#0017)\n【成因分析】相机手持快速转向引发曝光积分横向拖影，\n加之西侧竹林逆光造成的高动态光晕冲刷弱纹理，远端行人漏检", 
                      fontsize=9.5, fontweight='bold', fontproperties=zh_font)
    axes[0].axis('off')
    
    # Failure Case 2: Tree / Bush Occlusion in Frame 0008
    img_08 = load_rgb("0008.jpg")
    dets_08 = results["YOLOv8x_640"]["detections"][8]
    vis_08 = draw_detections(img_08, dets_08)
    # Target range around y: 480~820, x: 280:900
    crop_08 = vis_08[480:800, 280:900]
    axes[1].imshow(crop_08)
    axes[1].set_title("失败案例 2：常青灌木与行道树严重前景遮挡 (#0008)\n【成因分析】南侧人行道常青灌木横向切割行人下半身，\n非刚体拓扑断裂破坏了 CNN 局部感受野连通性，边界框高度抖动", 
                      fontsize=9.5, fontweight='bold', fontproperties=zh_font)
    axes[1].axis('off')

    # Failure Case 3: Extreme Scale Disparity & Dense Cluster in Frame 0035
    img_35 = load_rgb("0035.jpg")
    dets_35 = results["YOLOv8x_640"]["detections"][35]
    vis_35 = draw_detections(img_35, dets_35)
    # Target range around y: 500~900, x: 400:1080
    crop_35 = vis_35[500:900, 400:1080]
    axes[2].imshow(crop_35)
    axes[2].set_title("失败案例 3：远景极端尺度微弱目标与密集粘连 (#0035)\n【成因分析】北侧广场远景停放自行车仅占十数个像素，\n多台车身重叠致使降采样后特征高度混叠，NMS 出现错误抑制并漏检", 
                      fontsize=9.5, fontweight='bold', fontproperties=zh_font)
    axes[2].axis('off')

    plt.tight_layout()
    out_file = os.path.join(FIGURES_DIR, "fig5_failure_cases.png")
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {out_file}")

if __name__ == "__main__":
    generate_fig1_architecture()
    generate_fig2_representative()
    generate_fig3_comparison()
    generate_fig4_temporal_curves()
    generate_fig5_failure_cases()
    print("\nAll 5 figures generated successfully!")
