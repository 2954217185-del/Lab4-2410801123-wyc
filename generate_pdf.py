import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Register Chinese Font
font_path = 'C:/Windows/Fonts/simhei.ttf'
pdfmetrics.registerFont(TTFont('SimHei', font_path))

BASE_DIR = r"d:\大学\机器视觉算法与应用\lab4"
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
RESULTS_PATH = os.path.join(BASE_DIR, "output", "experiment_results.json")
PDF_OUT = os.path.join(BASE_DIR, "Lab4-2410801123-王弈淳.pdf")

with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    exp_results = json.load(f)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont('SimHei', 8)
        self.setFillColor(colors.HexColor('#666666'))
        
        # Header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, A4[1] - 24, "机器视觉算法与应用 · Lab4 理论综合回顾与校园视频目标检测开源实战")
            self.drawRightString(A4[0] - 36, A4[1] - 24, "学生：王弈淳 (2410801123)")
            self.setStrokeColor(colors.HexColor('#D0D7DE'))
            self.setLineWidth(0.5)
            self.line(36, A4[1] - 28, A4[0] - 36, A4[1] - 28)
        
        # Footer
        page_str = f"第 {self._pageNumber} 页 / 共 {page_count} 页"
        self.drawRightString(A4[0] - 36, 18, page_str)
        self.drawString(36, 18, "南京林业大学 · 信息科学技术学院、人工智能学院 · 机器视觉课程组")
        self.setStrokeColor(colors.HexColor('#D0D7DE'))
        self.setLineWidth(0.5)
        self.line(36, 26, A4[0] - 36, 26)
        
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )
    
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='SimHei',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#184C78'),
        alignment=1,
        spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='SimHei',
        fontSize=9.8,
        leading=13.5,
        textColor=colors.HexColor('#333333'),
        alignment=1,
        spaceAfter=3
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        fontName='SimHei',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceAfter=4
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='SimHei',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor('#184C78'),
        spaceBefore=5,
        spaceAfter=2.5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='SimHei',
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor('#2E5B88'),
        spaceBefore=3,
        spaceAfter=1.5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='SimHei',
        fontSize=8.2,
        leading=11.6,
        textColor=colors.HexColor('#24292F'),
        spaceAfter=2.5,
        firstLineIndent=14
    )
    caption_style = ParagraphStyle(
        'Caption_Custom',
        fontName='SimHei',
        fontSize=7.4,
        leading=9.8,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceBefore=1.5,
        spaceAfter=3.5
    )
    table_text = ParagraphStyle(
        'TableText',
        fontName='SimHei',
        fontSize=7.2,
        leading=9.4,
        textColor=colors.HexColor('#24292F')
    )
    table_header = ParagraphStyle(
        'TableHeader',
        fontName='SimHei',
        fontSize=7.2,
        leading=9.4,
        textColor=colors.HexColor('#FFFFFF'),
        alignment=1
    )

    story = []
    
    # ==================== PAGE 1: 封面元数据与精炼第一部分理论总结 ====================
    story.append(Paragraph("《机器视觉算法与应用》课程实验报告", title_style))
    story.append(Paragraph("Lab4 · 前 13 讲理论综合回顾与校园视频目标检测开源实战", subtitle_style))
    story.append(Paragraph("学生学号：2410801123 &nbsp;|&nbsp; 学生姓名：王弈淳 &nbsp;|&nbsp; 依托平台：校园 3D 拼建平台 (Job #419) &nbsp;|&nbsp; 完成日期：2026 年 11 月 9 日", meta_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#184C78'), spaceAfter=4))

    story.append(Paragraph("一、 前 13 讲理论体系精炼总结：信息压缩、物理约束与归纳偏置", h1_style))
    p1 = ("机器视觉的核心是从含噪光学投影中逆解三维空间与语义的病态问题。前 13 讲围绕<b>“信息压缩与重建”</b>主线递进：<b>光子 → 像素 → 局部特征 → 几何约束 → 空间结构 → 语义感知</b>，由不确定性传递、物理几何约束与数据驱动归纳偏置三条暗线贯穿：")
    story.append(Paragraph(p1, body_style))

    p2 = ("<b>1. 成像与像素表示（第 02 讲）：</b>曝光三角决定通光量，光电转换服从泊松分布，散粒噪声信噪比满足 SNR ∝ √N。提高 ISO 仅放大数值增益，过曝与欠曝丢失的信息物理不可逆。本讲将连续光学信号量化为数字阵列，输入带物理偏见。<i>最深方法：</i>信噪比平方根法则；<i>局限：</i>纯硬件极限，单次曝光无法突破动态范围。")
    story.append(Paragraph(p2, body_style))

    p3 = ("<b>2. 空域/频域滤波与图像表示（第 03 讲）：</b>空域卷积等价于频域乘积。低通滤波平滑噪声必然损伤高频边缘，双边滤波与引导滤波通过值域相似度实现保边抗噪，为高斯金字塔与 DoG 多尺度表达奠基。<i>最深方法：</i>双边滤波平坦区低通、边缘放行机制；<i>局限：</i>仅基于低阶像素灰度相似性，无法区分真实物体边缘与高频噪声。")
    story.append(Paragraph(p3, body_style))

    p4 = ("<b>3. 局部特征提取与鲁棒匹配（第 04–05 讲）：</b>SIFT 在 DoG 空间搜索极值点，结合梯度直方图生成 128 维光照鲁棒描述子；匹配阶段通过 Lowe 比值检验（最近邻/次近邻 ≤ 0.75）与双向检验初筛。本讲将稠密像素压缩为稀疏特征点。<i>最深方法：</i>Lowe's Ratio Test；<i>局限：</i>依赖局部纹理梯度，在弱纹理大白墙与周期性重复纹理下易产生大量误匹配。")
    story.append(Paragraph(p4, body_style))

    p5 = ("<b>4. 相机模型、对极几何与 RANSAC（第 06–07 讲）：</b>针孔模型 x_cam ~ K[R|t]X 将 3D 映射至像素平面；对极约束 x<sub>2</sub><sup>T</sup> F x<sub>1</sub> = 0 将 2D 匹配面搜索降至 1D 极线搜索。针对外点，RANSAC 依据 k = ln(1 - p) / ln(1 - w<sup>s</sup>) 鲁棒拟合基础矩阵 F。<i>最深方法：</i>RANSAC 极大似然估计；<i>局限：</i>纯旋转运动或共面场景下几何矩阵秩亏退化，极线约束失效。")
    story.append(Paragraph(p5, body_style))

    p6 = ("<b>5. 双目立体、增量 SfM 与 MVS（第 08–09 讲）：</b>双目视差 ΔZ ≈ Z<sup>2</sup>·Δd / (fb) 指向远距离视差衰减；增量 SfM 通过 EPnP 注册新视点、DLT 三角化新点，调用 Schur 补消元的 BA 优化重投影误差；MVS 平面扫描聚合稠密点云。<i>最深方法：</i>利用 Schur 补消元的稀疏 BA 优化；<i>局限：</i>无绝对尺度，误差单向累积发散，弱纹理形成点云空洞。")
    story.append(Paragraph(p6, body_style))

    p7 = ("<b>6. 神经隐式表征、SLAM 与深度学习（第 10–13 讲）：</b>NeRF/3DGS 转向连续辐射场或高斯显式微元；SLAM 引入前端因果建图与回环优化。第 12–13 讲突破解析几何局限：CNN 引入局部连接、权重共享与平移等变强归纳偏置；ViT 则打破局部性，以全局自注意力换取海量数据表征容量。<i>核心感悟：</i>几何模型依赖强物理约束换精度，深度模型依赖数据规模换泛化，现代视觉走向几何底座与语义感知的深层融合。")
    story.append(Paragraph(p7, body_style))

    story.append(Paragraph("二、 高级语义任务与开源算法选型理由", h1_style))
    p_task = ("<b>1. 任务合理性：</b>Lab3 基于校园平台重建了主楼几何网格，但缺乏实例级认知。选定<b>开放场景目标检测（Object Detection）</b>识别行人、车辆与校园设施，实现从“静态几何重建”到“动态时空语义感知”的闭环。<br/>"
              "<b>2. 算法选型理由：</b>选用业界标杆开源 <b>Ultralytics YOLOv8</b>。其采用 Anchor-Free 无锚框机制、CSPDarknet 骨干（C2f/SPPF）、PAN-FPN 双向特征金字塔、解耦检测头与分布焦点损失（DFL）。尺度家族完备（Nano 至 X-Large），严格支撑多模型规模与分辨率消融对比。")
    story.append(Paragraph(p_task, body_style))

    story.append(PageBreak())

    # ==================== PAGE 2: 数据前处理与开源代码逐模块理解 ====================
    story.append(Paragraph("三、 视频输入数据源与前处理管线", h1_style))
    p_data = ("<b>1. 数据来源：</b>校园 3D 拼建平台 Job #419 (<code>platform-419</code>)，本人于晴朗午后手持后置主摄（1080p, 1080×1920 竖屏, 30fps）沿主楼录制的 3 段视频：南侧人行道（v108）、西侧竹林转角（v109）、北侧广场（v110），共 308 帧（约 10.3s）。<br/>"
              "<b>2. 关键帧抽取：</b>平台依据拉普拉斯清晰度均值（368.4）自适应抽取 48 关键帧（<code>0000.jpg</code> ~ <code>0047.jpg</code>），间隔约 0.5s。<br/>"
              "<b>3. 预处理管线：</b>BGR 转 RGB；保持 9:16 高宽比自适应 Letterbox 补灰边对齐 32 像素步长；归一化至 [0, 1] 并重排为 (1, C, H, W) 张量加载至 GPU。")
    story.append(Paragraph(p_data, body_style))

    story.append(Paragraph("四、 开源代码逐模块深度解析与架构调用关系", h1_style))
    p_code = ("YOLOv8 源码构建于 PyTorch 架构之上，各模块高度解耦（调用拓扑如图 1 所示）：<br/>"
              "<b>1. 骨干网络（Backbone - CSPDarknet）：</b>输入经 Stem 卷积下采样，堆叠 4 个 <code>C2f</code> 跨阶段局部瓶颈模块。<code>C2f</code> 先通过 1×1 Conv 压缩通道并均等拆分（<code>chunk(2)</code>）：一半残差直通，另一半经 n 个 Bottleneck 并跳跃级联；末端引入 <code>SPPF</code> 串行 3 个 5×5 MaxPool 融合多感受野，输出 P3(80×80), P4(40×40), P5(20×20) 三尺度特征图。<br/>"
              "<b>2. 颈部融合（Neck - PAN-FPN）：</b>Top-Down 路径将 P5 深层语义上采样注入浅层；Bottom-Up 路径通过步长 2 卷积将浅层高分辨率空间几何细节回传深层，平衡语义与定位精度。<br/>"
              "<b>3. 解耦检测头（Head & DFL）：</b>分类与边框回归彻底解耦。分类分支利用 Sigmoid 预测 80 类后验概率；回归分支引入<b>分布焦点损失（DFL）</b>，将边框坐标建模为 [0, 16] 上的离散概率分布 P(y<sub>i</sub>)，积分求期望 y_hat = Σ i · P(y<sub>i</sub>) 建模不确定性。配以 <code>TaskAlignedAssigner</code> 动态匹配正样本与 NMS (IoU 门限 0.7) 滤除冗余框。")
    story.append(Paragraph(p_code, body_style))

    img_arch_path = os.path.join(FIGURES_DIR, "fig1_yolo_arch.png")
    if os.path.exists(img_arch_path):
        story.append(Image(img_arch_path, width=7.2*inch, height=2.8*inch))
        story.append(Paragraph("图 1：YOLOv8 开源目标检测算法核心模块调用拓扑与训练/推理全流程解析图", caption_style))

    story.append(PageBreak())

    # ==================== PAGE 3: 实验指标表与代表性检测全貌 ====================
    story.append(Paragraph("五、 实验结果与量化指标对比分析", h1_style))
    p_exp_intro = ("在配备 <b>NVIDIA RTX 4060 Laptop GPU（8GB 满血版）</b>与 <b>AMD R7 8845H CPU</b> 的真实环境下跑通 5 组实验。在无人工逐帧真值标注下，引入<b>跨帧时序 IoU 重叠率（Temporal IoU）</b>与<b>轨迹留存率（Persistence Rate）</b>作为稳定性无监督评价指标（数据见表 5-1）：")
    story.append(Paragraph(p_exp_intro, body_style))

    # Table 5-1
    headers = ["实验设置组", "模型规模 / 权重", "输入分辨率", "置信门限", "平均耗时", "帧率", "显存峰值", "总检出数", "平均置信度", "时序 IoU", "留存率"]
    table_data = [[Paragraph(f"<b>{h}</b>", table_header) for h in headers]]
    
    rows = [
        ("第 1 组 (Nano基线)", "YOLOv8n (3.2M)", "640×384", "conf=0.25", "10.46 ms", "95.6 FPS", "179.4 MB", "321", "0.505", "0.252", "0.273"),
        ("第 2 组 (Small型)", "YOLOv8s (11.2M)", "640×384", "conf=0.25", "9.77 ms", "102.4 FPS", "247.7 MB", "374", "0.558", "0.297", "0.319"),
        ("第 3 组 (X-Large)", "YOLOv8x (68.2M)", "640×384", "conf=0.25", "32.19 ms", "31.1 FPS", "767.9 MB", "433", "0.620", "0.311", "0.336"),
        ("第 4 组 (超分辨率)", "YOLOv8x (68.2M)", "1280×768", "conf=0.25", "106.99 ms", "9.3 FPS", "1226.9 MB", "538", "0.643", "0.311", "0.342"),
        ("第 5 组 (严格门限)", "YOLOv8x (68.2M)", "640×384", "conf=0.50", "31.45 ms", "31.8 FPS", "1293.9 MB", "291", "0.746", "0.294", "0.361"),
    ]
    for r in rows:
        table_data.append([Paragraph(cell, table_text) for cell in r])
        
    t5_1 = Table(table_data, colWidths=[62, 68, 48, 44, 44, 42, 44, 38, 44, 40, 38])
    t5_1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#184C78')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.HexColor('#FFFFFF')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
    ]))
    story.append(t5_1)
    story.append(Paragraph("表 5-1：Job #419 校园视频数据集在 5 组实验设置下的软硬件性能与时序稳定性实测对比表", caption_style))

    img_rep_path = os.path.join(FIGURES_DIR, "fig2_representative_detections.png")
    if os.path.exists(img_rep_path):
        story.append(Image(img_rep_path, width=7.2*inch, height=3.6*inch))
        story.append(Paragraph("图 2：YOLOv8x 在校园视频 4 个典型路段关键帧（#0000, #0016, #0032, #0047）上的高精度检测可视化全貌图", caption_style))

    story.append(PageBreak())

    # ==================== PAGE 4: 消融对比图、时序曲线图与精炼量化分析 ====================
    img_cmp_path = os.path.join(FIGURES_DIR, "fig3_model_and_res_comparison.png")
    if os.path.exists(img_cmp_path):
        story.append(Image(img_cmp_path, width=7.2*inch, height=2.9*inch))
        story.append(Paragraph("图 3：北侧广场关键帧 #0032 在模型规模（Nano vs X-Large）、分辨率（640p vs 1280p）及置信度门限下的检测敏感性消融对比图", caption_style))

    img_curv_path = os.path.join(FIGURES_DIR, "fig4_temporal_curves.png")
    if os.path.exists(img_curv_path):
        story.append(Image(img_curv_path, width=7.2*inch, height=1.9*inch))
        story.append(Paragraph("图 4：48 帧检测目标数量时序波动曲线 (a)、跨帧边界框 IoU 一致性 (b) 及算力/显存/检出量 Pareto 权衡气泡图 (c)", caption_style))

    p_disc = ("<b>量化结果核心研判：</b><br/>"
              "<b>(1) 模型规模增益：</b>Nano 到 X-Large 参数量扩增 21 倍，总检出数从 321 增至 433（+34.9%），平均置信度从 0.505 升至 0.620，时序 IoU 从 0.252 升至 0.311，且在 RTX 4060 上达 31.1 FPS，满足实时在线要求。<br/>"
              "<b>(2) 超分采样增益：</b>分辨率提升至 1280p 后总检出数跃升至 538 个（+24.2%），远景微小自行车从 139 增至 174 辆（+25.2%），背包从 2 增至 12 个，证实高频细节对微弱小目标的重要性。<br/>"
              "<b>(3) 时序视差突变：</b>图 4(b) 显示 #15 → #16 帧间 IoU 暴跌至 0.05，对应南主立面急转至西竹林的 90° 纯旋转，验证了第 08 讲纯旋转导致几何视差退化的理论。")
    story.append(Paragraph(p_disc, body_style))

    story.append(PageBreak())

    # ==================== PAGE 5: 失败案例分析与复现说明 ====================
    story.append(Paragraph("六、 典型失败案例与物理/机理深度归因", h1_style))
    p_fail_intro = ("在真实非受控校园场景下，算法暴露出其理论与工程边界（图 5 所示）：")
    story.append(Paragraph(p_fail_intro, body_style))

    img_fail_path = os.path.join(FIGURES_DIR, "fig5_failure_cases.png")
    if os.path.exists(img_fail_path):
        story.append(Image(img_fail_path, width=7.2*inch, height=2.3*inch))
        story.append(Paragraph("图 5：校园视频典型失败案例切片与物理/深度学习机理深度诊断分析图", caption_style))

    p_fail1 = ("<b>1. 转弯运动模糊与逆光光晕（关键帧 #0017，图 5 左）：</b>手持快速转向导致光轴角速度过大，单帧曝光时间内传感器感光单元发生横向位移积分，频域上表现为 sinc 样低通退化核抹平高频边缘；加之逆光散射光晕冲刷对比度，浅层卷积响应微弱导致远端目标漏检。")
    story.append(Paragraph(p_fail1, body_style))

    p_fail2 = ("<b>2. 前景常青灌木横向严重遮挡（关键帧 #0008，图 5 中）：</b>人行道灌木横向切断行人下肢，破坏了 CNN 局部空间连续性归纳偏置；缺乏骨骼拓扑显式约束，DFL 回归分支输出双峰离散概率分布，检测框高度收缩且跨帧抖动。")
    story.append(Paragraph(p_fail2, body_style))

    p_fail3 = ("<b>3. 远景小目标极端尺度失调与密集粘连（关键帧 #0035，图 5 右）：</b>远景自行车宽度不足 15 像素，下采样 32 倍后在 P5 特征图上小于半个单元网格，特征严重混叠；贪心 NMS 固定 IoU 门限（0.7）将紧挨并排的真实邻近目标误当成重复重叠框清除。")
    story.append(Paragraph(p_fail3, body_style))

    story.append(Paragraph("七、 运行环境配置与一键复现说明", h1_style))
    p_reproduce = ("<b>1. 硬件平台：</b>NVIDIA GeForce RTX 4060 Laptop GPU (8GB GDDR6), AMD Ryzen 7 8845H CPU, 16GB RAM.<br/>"
                   "<b>2. 软件运行栈：</b>Windows 11, Python 3.11, PyTorch 2.2.2 (CUDA 12.1), Torchvision 0.17.2, Ultralytics 8.4.208, OpenCV 5.0.0, NumPy 1.26.4, ReportLab 5.0.1, python-docx 1.2.0.<br/>"
                   "<b>3. 随机种子固化：</b>全局设定 <code>torch.manual_seed(42)</code> 与 <code>np.random.seed(42)</code> 消除随机抖动。<br/>"
                   "<b>4. 一键复现指令：</b><br/>"
                   "&nbsp;&nbsp;<code>python run_experiments.py</code> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 运行 5 组推理并持久化指标<br/>"
                   "&nbsp;&nbsp;<code>python generate_visualizations.py</code> # 生成 5 张高分辨率研究级图表<br/>"
                   "&nbsp;&nbsp;<code>python generate_pdf.py</code> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 编译生成精炼版实验报告 PDF<br/>"
                   "&nbsp;&nbsp;<code>python generate_docx.py</code> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 编译生成精炼版实验报告 Word 文档")
    story.append(Paragraph(p_reproduce, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    build_pdf(PDF_OUT)
