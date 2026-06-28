import matplotlib.pyplot as plt
import os
import markdown

# 全局配置：只用一次，后续所有渲染都使用这套样式
plt.rcParams['mathtext.fontset'] = 'stix'  # 使用 STIX 字体，更美观

def render_latex(latex_code, output_path="formula.svg", fontsize=28, fig_width=16, dpi=300):
    """
    将 LaTeX 公式渲染为 SVG 文件
    
    Args:
        latex_code (str): LaTeX 公式代码，需包含 $...$ 或 $$...$$ 包裹
        output_path (str): 输出文件路径，默认 "formula.svg"
        fontsize (int): 字号大小，默认 28
        fig_width (int): 图片宽度（英寸），默认 16
        dpi (int): 输出分辨率，默认 300
    
    Returns:
        bool: 成功返回 True，失败返回 False
    """
    try:
        # 自动补全 $...$ 包裹（如果用户没加）
        latex_code = latex_code.strip()
        if not (latex_code.startswith('$') or latex_code.startswith('\\')):
            latex_code = f'${latex_code}$'
        
        # 创建画布
        fig, ax = plt.subplots(figsize=(fig_width, 1.8))
        ax.text(0.5, 0.5, latex_code, fontsize=fontsize, 
                ha='center', va='center', transform=ax.transAxes)
        ax.axis('off')
        
        # 保存
        plt.savefig(output_path, bbox_inches='tight', dpi=dpi, format='svg')
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 渲染失败: {e}")
        return False

def render_from_text(text, output_dir="./formulas/"):
    """
    从文本中提取 LaTeX 公式并批量渲染为 SVG
    
    Args:
        text (str): 包含公式的文本
        output_dir (str): 输出目录，默认 "./formulas/"
    
    Returns:
        list: 生成的 SVG 文件路径列表
    """
    import re
    os.makedirs(output_dir, exist_ok=True)
    
    # 匹配 \[ ... \] 和 \( ... \) 中的公式
    pattern = r'\\\[(.*?)\\\]|\\\((.*?)\\)'
    matches = re.findall(pattern, text, re.DOTALL)
    
    if not matches:
        print("⚠️ 未找到 LaTeX 公式")
        return []
    
    files = []
    for i, match in enumerate(matches):
        latex_code = match[0] or match[1]
        if not latex_code:
            continue
        
        # 包裹完整公式
        full_latex = r'\[' + latex_code.strip() + r'\]'
        
        filepath = os.path.join(output_dir, f"formula_{i+1}.svg")
        success = render_latex(full_latex, filepath)
        
        if success:
            files.append(filepath)
            print(f"✅ 公式 {i+1} 已保存: {filepath}")
        else:
            print(f"❌ 公式 {i+1} 渲染失败")
    
    return files

def MD_to_HTML():
    try:
        with open(".md","r",encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        print(".md文件不存在！现在没有需要转换的AI回答")
    data = markdown.markdown(data, extensions=['fenced_code', 'tables'])
    with open("a.html","w",encoding="utf-8") as f:
        f.write(data)
    os.remove(".md")
