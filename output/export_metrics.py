import json
import csv
import os

with open('output/experiment_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

params_map = {
    'YOLOv8n_640': '3.2M',
    'YOLOv8s_640': '11.2M',
    'YOLOv8x_640': '68.2M',
    'YOLOv8x_1280': '68.2M',
    'YOLOv8x_conf50': '68.2M'
}

header = [
    '实验配置', '模型权重', '参数量', '输入尺寸', '置信度阈值', 
    '单帧推理时延(ms)', '吞吐帧率(FPS)', '显存峰值(MB)', 
    '48帧累计检出数', '平均置信度', '相邻帧时序IoU', '时序持续率'
]

md_lines = [
    '# 实验定量评测指标汇总表 (Lab4 Quantitative Evaluation Metrics Table)',
    '',
    f'**测试硬件环境**: NVIDIA GeForce RTX 4060 Laptop GPU (8GB VRAM) / Intel Core i7 / CUDA 12.1',
    f'**测试数据集**: 校园真实场景漫游视频 (48帧, 1080×1920@2fps, 来自平台 Job #419)',
    '',
    '| ' + ' | '.join(header) + ' |',
    '| ' + ' | '.join([':---:'] * len(header)) + ' |'
]

csv_rows = [header]

for k, v in data.items():
    row = [
        v['name'],
        v['weights'],
        params_map.get(k, '-'),
        f"{v['imgsz']}x{v['imgsz']}",
        f"{v['conf']:.2f}",
        f"{v['latency_mean_ms']:.2f} ± {v['latency_std_ms']:.2f}",
        f"{v['fps']:.1f}",
        f"{v['peak_vram_mb']:.1f}",
        str(v['total_detections']),
        f"{v['mean_confidence']:.3f}",
        f"{v['temporal_iou']:.3f}",
        f"{v['persistence_rate']:.1%}"
    ]
    csv_rows.append(row)
    md_lines.append('| ' + ' | '.join(row) + ' |')

# Save CSV with UTF-8 BOM so Excel opens it with Chinese characters perfectly
with open('output/metrics_table.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)

with open('output/指标表_定量实验评测结果.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines) + '\n')

print('Generated output/metrics_table.csv and output/指标表_定量实验评测结果.md successfully!')
