# 机器视觉算法与应用 · Lab4 实验实战

**实验任务**：Lab4 前 13 讲理论综合回顾与校园视频目标检测开源实战  
**学生姓名**：王弈淳  
**学生学号**：2410801123  
**授课教师**：李成华  
**培养单位**：南京林业大学 · 信息科学技术学院、人工智能学院  
**依托平台**：南京林业大学课程平台 (`http://202.119.209.217:7100`) 与校园 3D 拼建平台 (`http://202.119.209.217:8080`) Job #419 (`platform-419`)

---

## 一、 项目简介与算法选型

本项目基于在 Lab3（P3 阶段）实地采集并上传至校园 3D 拼建平台重建的校园视频数据（Job #419），开展**开放场景目标检测（Object Detection）**开源算法深度实战。

- **算法选型**：Ultralytics YOLOv8（涵盖 Nano, Small, X-Large 模型尺度家族，基于 AGPL-3.0 License）
- **架构特点**：Anchor-Free 无锚框机制、CSPDarknet 骨干网络（含 `C2f` 跨阶段梯度跳跃连接与 `SPPF` 空间金字塔池化模块）、PAN-FPN 双向跨尺度特征金字塔 Neck、分类/回归解耦检测头（Decoupled Head）、分布焦点损失（Distribution Focal Loss, DFL）与动态任务对齐样本分配（TaskAlignedAssigner）。
- **实验环境**：NVIDIA GeForce RTX 4060 Laptop GPU (8GB GDDR6, 140W 满血版), Intel Core i7 / AMD Ryzen 7, CUDA 12.1, Python 3.11, PyTorch 2.2.2+cu121。

---

## 二、 目录结构说明

```
Lab4-2410801123-王弈淳/
├── data/
│   ├── frames/                          # 校园视频抽取的 48 张 1080p 高清关键帧 (0000.jpg ~ 0047.jpg)
│   └── campus_walk.mp4                  # 关键帧序列合成的校园漫游视频 (1080×1920@2fps)
├── figures/                             # 实验报告中引用的 5 组高清科研图表
│   ├── fig1_yolo_arch.png               # 图 1：YOLOv8 模块架构与数据流拓扑图
│   ├── fig2_representative_detections.png # 图 2：4 处代表性路段检测可视化效果图
│   ├── fig3_model_and_res_comparison.png  # 图 3：模型规模与输入分辨率消融对比图
│   ├── fig4_temporal_curves.png          # 图 4：48 帧时序稳定性曲线与 Pareto 权衡气泡图
│   └── fig5_failure_cases.png            # 图 5：3 类典型失败案例切片与物理/机理深度归因图
├── output/
│   ├── metrics_table.csv                # 实验定量评测指标表 (Excel 兼容 CSV 格式)
│   ├── 指标表_定量实验评测结果.md        # 实验定量评测指标 Markdown 格式表
│   └── experiment_results.json          # 5 组实验的完整量化指标与逐帧检测数据
├── run_experiments.py                   # 核心实验推理与量化指标评估评测主脚本
├── generate_visualizations.py           # 科研级对比可视化图表生成脚本
├── generate_pdf.py                      # ReportLab 5 页精美 PDF 报告编译脚本
├── generate_docx.py                     # python-docx 格式规范 Word 报告生成脚本
├── Lab4-2410801123-王弈淳.pdf            # 最终交付的 5 页规范实验报告 PDF
├── Lab4-2410801123-王弈淳.docx           # 最终交付的精简版排版实验报告 Word 文档
├── requirements.txt                     # Python 依赖库清单
└── README.md                            # 项目说明与一键复现指南文档
```

---

## 三、 实验量化指标汇总（实测）

| 实验配置 | 预训练权重 | 参数量 | 输入尺寸 | 置信门限 | 平均耗时 | 实时帧率 | 显存峰值 | 48 帧总检出 | 平均置信度 | 相邻帧时序 IoU | 时序持续率 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLOv8n_640** | `yolov8n.pt` | 3.2M | 640×640 | 0.25 | 10.46 ms | 95.6 FPS | 179.4 MB | 321 | 0.505 | 0.252 | 27.3% |
| **YOLOv8s_640** | `yolov8s.pt` | 11.2M | 640×640 | 0.25 | 9.77 ms | 102.4 FPS | 247.7 MB | 374 | 0.558 | 0.297 | 31.9% |
| **YOLOv8x_640** | `yolov8x.pt` | 68.2M | 640×640 | 0.25 | 32.19 ms | 31.1 FPS | 767.9 MB | 433 | 0.620 | 0.311 | 33.6% |
| **YOLOv8x_1280** | `yolov8x.pt` | 68.2M | 1280×1280 | 0.25 | 106.99 ms | 9.3 FPS | 1226.9 MB | 538 | 0.643 | 0.311 | 34.2% |
| **YOLOv8x_conf50** | `yolov8x.pt` | 68.2M | 640×640 | 0.50 | 31.45 ms | 31.8 FPS | 1293.9 MB | 291 | 0.746 | 0.294 | 36.1% |

---

## 四、 环境依赖与一键复现步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 依次运行实验与编译报告
```bash
# 步骤 1：运行 5 组对比实验并计算时序一致性定量指标（自动生成 output/experiment_results.json）
python run_experiments.py

# 步骤 2：生成报告所需的 5 组科研可视化图表（自动保存至 figures/ 目录）
python generate_visualizations.py

# 步骤 3：一键编译生成 Lab4-2410801123-王弈淳.pdf 实验报告
python generate_pdf.py

# 步骤 4：一键生成 Lab4-2410801123-王弈淳.docx 实验报告
python generate_docx.py
```

---

## 五、 交付成果清单

1. **实验报告 PDF**：`Lab4-2410801123-王弈淳.pdf`（严格 5 页，包含前 13 讲理论回顾、算法架构深解、定量指标表、5 组对比图表及失败机理归因）
2. **实验报告 Word 文档**：`Lab4-2410801123-王弈淳.docx`（精简规范排版，内嵌高清图表与完整指标表，便于二次编辑修改）
3. **结果素材与指标表**：
   - 5 张高分辨率科研可视化图表（`figures/fig1` ~ `figures/fig5`）
   - 定量评测指标表（`output/metrics_table.csv`、`output/指标表_定量实验评测结果.md`、`output/experiment_results.json`）
4. **源码与运行说明压缩包**：`Lab4-2410801123-王弈淳-code.zip`（仅收录 Lab4 必需的源码、说明文档、输入数据、结果图表及交付报告）
