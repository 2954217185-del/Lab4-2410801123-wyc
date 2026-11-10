import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = r"d:\大学\机器视觉算法与应用\lab4"
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
RESULTS_PATH = os.path.join(BASE_DIR, "output", "experiment_results.json")
DOCX_OUT = os.path.join(BASE_DIR, "Lab4-2410801123-王弈淳.docx")

with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    exp_results = json.load(f)

doc = docx.Document()

# Margins: 0.75 inch (1.9 cm)
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    
    # Header & Footer setup
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("机器视觉算法与应用 · Lab4 理论综合回顾与校园视频目标检测开源实战  |  王弈淳 (2410801123)")
    hrun.font.name = "Microsoft YaHei"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(120, 120, 120)
    
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = fp.add_run("南京林业大学 · 信息科学技术学院、人工智能学院 · 机器视觉课程组")
    frun.font.name = "Microsoft YaHei"
    frun.font.size = Pt(8.5)
    frun.font.color.rgb = RGBColor(120, 120, 120)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_run_font(run, font_name="Microsoft YaHei", size_pt=9.5, bold=False, color_rgb=(0,0,0), italic=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:eastAsia'), font_name)
    rPr.append(rFonts)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    set_run_font(run, "Microsoft YaHei", 15, bold=True, color_rgb=(24, 76, 120))

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    set_run_font(run, "Microsoft YaHei", 10.5, bold=True, color_rgb=(60, 60, 60))

def add_meta(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_run_font(run, "Microsoft YaHei", 8.5, bold=False, color_rgb=(100, 100, 100))

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    set_run_font(run, "Microsoft YaHei", 11.5, bold=True, color_rgb=(24, 76, 120))

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    set_run_font(run, "Microsoft YaHei", 10, bold=True, color_rgb=(46, 91, 136))

def add_body(text, bold_prefix=None, indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if indent and not bold_prefix:
        p.paragraph_format.first_line_indent = Pt(16)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        set_run_font(r_pre, "Microsoft YaHei", 9, bold=True, color_rgb=(30, 30, 30))
    run = p.add_run(text)
    set_run_font(run, "Microsoft YaHei", 9, bold=False, color_rgb=(40, 40, 40))

def add_inline_img(img_path, caption, width_inch=6.2):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(1.5)
        p_img.paragraph_format.keep_with_next = True
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inch))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(5)
        run_cap = p_cap.add_run(caption)
        set_run_font(run_cap, "Microsoft YaHei", 8.2, bold=True, color_rgb=(80, 80, 80))

# ==================== Document Content ====================

add_title("《机器视觉算法与应用》课程实验报告")
add_subtitle("Lab4 · 前 13 讲理论综合回顾与校园视频目标检测开源实战")
add_meta("学生学号：2410801123  |  学生姓名：王弈淳  |  依托平台：校园 3D 拼建平台 (Job #419)  |  完成日期：2026 年 11 月 9 日")

# ==================== Section 1 ====================
add_h1("一、 前 13 讲理论体系精炼总结：信息压缩、物理约束与归纳偏置")
add_body("机器视觉的核心是从含噪光学投影中逆解三维空间与语义的病态问题。前 13 讲围绕“信息压缩与重建”主线递进：光子 → 像素 → 局部特征 → 几何约束 → 空间结构 → 语义感知，由不确定性传递、物理几何约束与数据驱动归纳偏置三条暗线贯穿：")

add_body("曝光三角决定通光量，光电转换服从泊松分布，散粒噪声信噪比满足 SNR ∝ √N。提高 ISO 仅放大数值增益，过曝与欠曝丢失的信息物理不可逆。本讲将连续光学信号量化为数字阵列，输入带物理偏见。最深方法：信噪比平方根法则；局限：纯硬件极限，单次曝光无法突破动态范围。", "1. 成像与像素表示（第 02 讲）：")

add_body("空域卷积等价于频域乘积。低通滤波平滑噪声必然损伤高频边缘，双边滤波与引导滤波通过值域相似度实现保边抗噪，为高斯金字塔与 DoG 多尺度表达奠基。最深方法：双边滤波平坦区低通、边缘放行机制；局限：仅基于低阶像素灰度相似性，无法区分真实物体边缘与高频噪声。", "2. 空域/频域滤波与图像表示（第 03 讲）：")

add_body("SIFT 在 DoG 空间搜索极值点，结合梯度直方图生成 128 维光照鲁棒描述子；匹配阶段通过 Lowe 比值检验（最近邻/次近邻 ≤ 0.75）与双向检验初筛。本讲将稠密像素压缩为稀疏特征点。最深方法：Lowe's Ratio Test；局限：依赖局部纹理梯度，在弱纹理大白墙与周期性重复纹理下易产生大量误匹配。", "3. 局部特征提取与鲁棒匹配（第 04–05 讲）：")

add_body("针孔模型 x_cam ~ K[R|t]X 将 3D 映射至像素平面；对极约束 x2^T F x1 = 0 将 2D 匹配面搜索降至 1D 极线搜索。针对外点，RANSAC 依据 k = ln(1 - p) / ln(1 - w^s) 鲁棒拟合基础矩阵 F。最深方法：RANSAC 极大似然估计；局限：纯旋转运动或共面场景下几何矩阵秩亏退化，极线约束失效。", "4. 相机模型、对极几何与 RANSAC（第 06–07 讲）：")

add_body("双目视差 ΔZ ≈ Z²·Δd / (fb) 指向远距离视差衰减；增量 SfM 通过 EPnP 注册新视点、DLT 三角化新点，调用 Schur 补消元的 BA 优化重投影误差；MVS 平面扫描聚合稠密点云。最深方法：利用 Schur 补消元的稀疏 BA 优化；局限：无绝对尺度，误差单向累积发散，弱纹理形成点云空洞。", "5. 双目立体、增量 SfM 与 MVS（第 08–09 讲）：")

add_body("NeRF/3DGS 转向连续辐射场或高斯显式微元；SLAM 引入前端因果建图与回环优化。第 12–13 讲突破解析几何局限：CNN 引入局部连接、权重共享与平移等变强归纳偏置；ViT 则打破局部性，以全局自注意力换取海量数据表征容量。核心感悟：几何模型依赖强物理约束换精度，深度模型依赖数据规模换泛化，现代视觉走向几何底座与语义感知的深层融合。", "6. 神经隐式表征、SLAM 与深度学习（第 10–13 讲）：")

# ==================== Section 2 ====================
add_h1("二、 高级语义任务与开源算法选型理由")
add_body("Lab3 基于校园平台重建了主楼几何网格，但缺乏实例级认知。选定开放场景目标检测（Object Detection）识别行人、车辆与校园设施，实现从“静态几何重建”到“动态时空语义感知”的闭环。", "1. 任务合理性：")

add_body("选用业界标杆开源 Ultralytics YOLOv8。其采用 Anchor-Free 无锚框机制、CSPDarknet 骨干（C2f/SPPF）、PAN-FPN 双向特征金字塔、解耦检测头与分布焦点损失（DFL）。尺度家族完备（Nano 至 X-Large），严格支撑多模型规模与分辨率消融对比。", "2. 算法选型理由：")

# ==================== Section 3 ====================
add_h1("三、 视频输入数据源与前处理管线")
add_body("校园 3D 拼建平台 Job #419 (platform-419)，本人于晴朗午后手持后置主摄（1080p, 1080×1920 竖屏, 30fps）沿主楼录制的 3 段视频：南侧人行道（v108）、西侧竹林转角（v109）、北侧广场（v110），共 308 帧（约 10.3s）。", "1. 数据来源：")

add_body("平台依据拉普拉斯清晰度均值（368.4）自适应抽取 48 关键帧（0000.jpg ~ 0047.jpg），间隔约 0.5s。", "2. 关键帧抽取：")

add_body("BGR 转 RGB；保持 9:16 高宽比自适应 Letterbox 补灰边对齐 32 像素步长；归一化至 [0, 1] 并重排为 (1, C, H, W) 张量加载至 GPU。", "3. 预处理管线：")

# ==================== Section 4 ====================
add_h1("四、 开源代码逐模块深度解析与架构调用关系")
add_body("YOLOv8 源码构建于 PyTorch 架构之上，各模块高度解耦（调用拓扑如图 1 所示）：\n"
         "1. 骨干网络（Backbone - CSPDarknet）：输入经 Stem 卷积下采样，堆叠 4 个 C2f 跨阶段局部瓶颈模块。C2f 先通过 1×1 Conv 压缩通道并均等拆分（chunk(2)）：一半残差直通，另一半经 n 个 Bottleneck 并跳跃级联；末端引入 SPPF 串行 3 个 5×5 MaxPool 融合多感受野，输出 P3(80×80), P4(40×40), P5(20×20) 三尺度特征图。\n"
         "2. 颈部融合（Neck - PAN-FPN）：Top-Down 路径将 P5 深层语义上采样注入浅层；Bottom-Up 路径通过步长 2 卷积将浅层高分辨率空间几何细节回传深层，平衡语义与定位精度。\n"
         "3. 解耦检测头（Head & DFL）：分类与边框回归彻底解耦。分类分支利用 Sigmoid 预测 80 类后验概率；回归分支引入分布焦点损失（DFL），将边框坐标建模为 [0, 16] 上的离散概率分布 P(y_i)，积分求期望 y_hat = Σ i · P(y_i) 建模不确定性。配以 TaskAlignedAssigner 动态匹配正样本与 NMS (IoU 门限 0.7) 滤除冗余框。")

add_inline_img(os.path.join(FIGURES_DIR, "fig1_yolo_arch.png"), "图 1：YOLOv8 开源目标检测算法核心模块调用拓扑与训练/推理全流程解析图", 6.2)

# ==================== Section 5 ====================
add_h1("五、 实验结果与量化指标对比分析")
add_body("在配备 NVIDIA RTX 4060 Laptop GPU（8GB 满血版）与 AMD R7 8845H CPU 的真实环境下跑通 5 组实验。在无人工逐帧真值标注下，引入跨帧时序 IoU 重叠率（Temporal IoU）与轨迹留存率（Persistence Rate）作为稳定性无监督评价指标（数据见表 5-1）：")

# Table 5-1
t_headers = ["实验设置组", "模型规模 / 权重", "输入分辨率", "置信门限", "平均耗时", "实时帧率", "显存峰值", "总检出数", "平均置信度", "时序 IoU", "留存率"]
t_rows = [
    ["第 1 组 (Nano基线)", "YOLOv8n (3.2M)", "640×384", "conf=0.25", "10.46 ms", "95.6 FPS", "179.4 MB", "321", "0.505", "0.252", "0.273"],
    ["第 2 组 (Small平衡)", "YOLOv8s (11.2M)", "640×384", "conf=0.25", "9.77 ms", "102.4 FPS", "247.7 MB", "374", "0.558", "0.297", "0.319"],
    ["第 3 组 (X-Large高精)", "YOLOv8x (68.2M)", "640×384", "conf=0.25", "32.19 ms", "31.1 FPS", "767.9 MB", "433", "0.620", "0.311", "0.336"],
    ["第 4 组 (超分辨率)", "YOLOv8x (68.2M)", "1280×768", "conf=0.25", "106.99 ms", "9.3 FPS", "1226.9 MB", "538", "0.643", "0.311", "0.342"],
    ["第 5 组 (严格门限)", "YOLOv8x (68.2M)", "640×384", "conf=0.50", "31.45 ms", "31.8 FPS", "1293.9 MB", "291", "0.746", "0.294", "0.361"],
]

t_table = doc.add_table(rows=len(t_rows) + 1, cols=len(t_headers))
t_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for col_idx, h in enumerate(t_headers):
    cell = t_table.cell(0, col_idx)
    cell.text = h
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_background(cell, "184C78")
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    set_run_font(p.runs[0], "Microsoft YaHei", 8.2, bold=True, color_rgb=(255, 255, 255))

for row_idx, row in enumerate(t_rows):
    bg_color = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
    for col_idx, val in enumerate(row):
        cell = t_table.cell(row_idx + 1, col_idx)
        cell.text = val
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_background(cell, bg_color)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(1.5)
        set_run_font(p.runs[0], "Microsoft YaHei", 8, bold=False, color_rgb=(30, 30, 30))

p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.paragraph_format.space_before = Pt(2)
p_cap.paragraph_format.space_after = Pt(5)
rcap = p_cap.add_run("表 5-1：Job #419 校园视频数据集在 5 组实验设置下的软硬件性能与时序稳定性实测对比表")
set_run_font(rcap, "Microsoft YaHei", 8.2, bold=True, color_rgb=(80, 80, 80))

add_inline_img(os.path.join(FIGURES_DIR, "fig2_representative_detections.png"), "图 2：YOLOv8x 在校园视频 4 个典型路段代表性关键帧（#0000, #0016, #0032, #0047）上的高精度检测可视化全貌图", 6.2)

add_inline_img(os.path.join(FIGURES_DIR, "fig3_model_and_res_comparison.png"), "图 3：北侧广场关键帧 #0032 在模型规模（Nano vs X-Large）、分辨率（640p vs 1280p）及置信度门限下的检测敏感性消融对比图", 6.0)

add_inline_img(os.path.join(FIGURES_DIR, "fig4_temporal_curves.png"), "图 4：48 帧检测目标数量时序波动曲线 (a)、跨帧边界框 IoU 一致性 (b) 及算力/显存/检出量 Pareto 权衡气泡图 (c)", 6.2)

add_h2("量化结果核心研判：")
add_body("Nano 到 X-Large 参数量扩增 21 倍，总检出数从 321 增至 433（+34.9%），平均置信度从 0.505 升至 0.620，时序 IoU 从 0.252 升至 0.311，且在 RTX 4060 上达 31.1 FPS，满足实时在线要求。", "(1) 模型规模增益：")

add_body("分辨率提升至 1280p 后总检出数跃升至 538 个（+24.2%），远景微小自行车从 139 增至 174 辆（+25.2%），背包从 2 增至 12 个，证实高频细节对微弱小目标的重要性。", "(2) 超分采样增益：")

add_body("图 4(b) 显示 #15 → #16 帧间 IoU 暴跌至 0.05，对应南主立面急转至西竹林的 90° 纯旋转，验证了第 08 讲纯旋转导致几何视差退化的理论。", "(3) 时序视差突变：")

# ==================== Section 6 ====================
add_h1("六、 典型失败案例与物理/机理深度归因")
add_body("在真实非受控校园场景下，算法暴露出其理论与工程边界（图 5 所示）：")

add_inline_img(os.path.join(FIGURES_DIR, "fig5_failure_cases.png"), "图 5：校园视频典型失败案例切片与物理/深度学习机理深度诊断分析图", 6.2)

add_body("手持快速转向导致光轴角速度过大，单帧曝光时间内传感器感光单元发生横向位移积分，频域上表现为 sinc 样低通退化核抹平高频边缘；加之逆光散射光晕冲刷对比度，浅层卷积响应微弱导致远端目标漏检。", "1. 转弯运动模糊与逆光光晕（关键帧 #0017，图 5 左）：")

add_body("人行道灌木横向切断行人下肢，破坏了 CNN 局部空间连续性归纳偏置；缺乏骨骼拓扑显式约束，DFL 回归分支输出双峰离散概率分布，检测框高度收缩且跨帧抖动。", "2. 前景常青灌木横向严重遮挡（关键帧 #0008，图 5 中）：")

add_body("远景自行车宽度不足 15 像素，下采样 32 倍后在 P5 特征图上小于半个单元网格，特征严重混叠；贪心 NMS 固定 IoU 门限（0.7）将紧挨并排的真实邻近目标误当成重复重叠框清除。", "3. 远景小目标极端尺度失调与密集粘连（关键帧 #0035，图 5 右）：")

# ==================== Section 7 ====================
add_h1("七、 运行环境配置与一键复现说明")
add_body("NVIDIA GeForce RTX 4060 Laptop GPU (8GB GDDR6), AMD Ryzen 7 8845H CPU, 16GB RAM.", "1. 硬件平台：")
add_body("Windows 11, Python 3.11, PyTorch 2.2.2 (CUDA 12.1), Torchvision 0.17.2, Ultralytics 8.4.208, OpenCV 5.0.0, NumPy 1.26.4, ReportLab 5.0.1, python-docx 1.2.0.", "2. 软件运行栈：")
add_body("全局设定 torch.manual_seed(42) 与 np.random.seed(42) 消除随机抖动。", "3. 随机种子固化：")
add_body("依次运行以下命令即可实现全流程自动化复现与双版本报告生成：\n"
         "  python run_experiments.py          # 运行 5 组推理并持久化指标\n"
         "  python generate_visualizations.py  # 生成 5 张高分辨率研究级图表\n"
         "  python generate_pdf.py             # 编译生成精炼版实验报告 PDF\n"
         "  python generate_docx.py            # 编译生成精炼版实验报告 Word 文档", "4. 一键复现指令：")

try:
    doc.save(DOCX_OUT)
    print(f"Word document successfully generated: {DOCX_OUT}")
except PermissionError:
    alt_out = os.path.join(BASE_DIR, "Lab4-2410801123-王弈淳_精简版.docx")
    doc.save(alt_out)
    print(f"Original file is locked by Word/WPS. Successfully saved to: {alt_out}")
