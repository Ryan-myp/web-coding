"""
web-coding - AI Code Agent Platform
类似 Codex 的 agent 工作台，支持多 Skills 协作完成编码任务
"""
import streamlit as st
import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 页面配置
st.set_page_config(
    page_title="Web Coding Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自定义样式
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{}
</style>
""".format(open(Path(__file__).parent / "static" / "styles.css").read()), unsafe_allow_html=True)

# 路径设置
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

# 导入核心模块
from skill_registry import SkillRegistry
from skill_runner import SkillRunner


def main():
    # 初始化
    if 'registry' not in st.session_state:
        st.session_state.registry = SkillRegistry()
    if 'runner' not in st.session_state:
        st.session_state.runner = SkillRunner(st.session_state.registry)
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # 渲染布局
    render_layout()


def render_layout():
    """渲染主布局"""
    col1, col2 = st.columns([260, 1])
    
    with col1:
        render_sidebar()
    
    with col2:
        render_main()


def render_sidebar():
    """渲染侧边栏"""
    st.markdown("""
    <div class="sidebar">
        <div class="sidebar-header">
            <a href="#" class="sidebar-logo">
                <div class="sidebar-logo-icon">🤖</div>
                <span class="sidebar-logo-text">Web Coding</span>
            </a>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-section-title">导航</div>
            <a href="#" class="sidebar-item active">
                <span class="sidebar-item-icon">💬</span>
                <span class="sidebar-item-text">对话</span>
            </a>
            <a href="#" class="sidebar-item">
                <span class="sidebar-item-icon">📊</span>
                <span class="sidebar-item-text">历史记录</span>
            </a>
            <a href="#" class="sidebar-item">
                <span class="sidebar-item-icon">⚙️</span>
                <span class="sidebar-item-text">设置</span>
            </a>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-section-title">已安装 Skills</div>
    """, unsafe_allow_html=True)
    
    # 动态添加 Skills
    skills = st.session_state.registry.list_skills()
    for skill in skills:
        status = "✅" if skill.get("enabled") else "❌"
        st.markdown(f'''
        <a href="#" class="sidebar-item">
            <span class="sidebar-item-icon">{status}</span>
            <span class="sidebar-item-text">{skill['name']}</span>
        </a>
        ''', unsafe_allow_html=True)
    
    st.markdown("""
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-section-title">快速操作</div>
            <button class="sidebar-item" onclick="setPrompt('分析代码质量')">
                <span class="sidebar-item-icon">🛡️</span>
                <span class="sidebar-item-text">代码分析</span>
            </button>
            <button class="sidebar-item" onclick="setPrompt('检查安全漏洞')">
                <span class="sidebar-item-icon">🔒</span>
                <span class="sidebar-item-text">安全检查</span>
            </button>
            <button class="sidebar-item" onclick="setPrompt('审查 PRD')">
                <span class="sidebar-item-icon">📋</span>
                <span class="sidebar-item-text">PRD 审查</span>
            </button>
        </div>
        
        <div class="sidebar-section" style="margin-top: auto;">
            <button class="sidebar-item" onclick="clearChat()">
                <span class="sidebar-item-icon">🗑️</span>
                <span class="sidebar-item-text">清空对话</span>
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_main():
    """渲染主内容区"""
    # Header
    st.markdown(f'''
    <div class="header">
        <div>
            <div class="header-title">Web Coding Agent</div>
            <div class="header-subtitle">输入你的需求，AI 将调用相应的 Skills 完成编码任务</div>
        </div>
        <div class="header-actions">
            <button class="btn btn-secondary">📤 导出</button>
            <button class="btn btn-primary">✨ 新功能</button>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Chat Container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('''
    <div class="quick-actions">
        <span class="quick-action-chip" onclick="setPrompt('分析代码质量')">🛡️ 分析代码质量</span>
        <span class="quick-action-chip" onclick="setPrompt('检查安全漏洞')">🔒 安全检查</span>
        <span class="quick-action-chip" onclick="setPrompt('审查 PRD')">📋 PRD 审查</span>
        <span class="quick-action-chip" onclick="setPrompt('列出所有 Skills')">📦 列出 Skills</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Messages
    if st.session_state.messages:
        for msg in st.session_state.messages:
            render_message(msg)
    else:
        render_empty_state()
    
    # Input Area
    render_input_area()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_message(msg: dict):
    """渲染单条消息"""
    role_class = "message-user" if msg["role"] == "user" else "message-assistant"
    avatar = "👤" if msg["role"] == "user" else "🤖"
    role_name = "你" if msg["role"] == "user" else "Web Coding Agent"
    
    st.markdown(f'''
    <div class="message {role_class}">
        <div class="message-avatar">{avatar}</div>
        <div class="message-content">
            <div class="message-role">{role_name}</div>
            <div class="message-text">{msg["content"]}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_empty_state():
    """渲染空状态"""
    st.markdown('''
    <div class="empty-state">
        <div class="empty-state-icon">🤖</div>
        <div class="empty-state-title">你好，我是 Web Coding Agent</div>
        <div class="empty-state-subtitle">我可以帮你分析代码质量、检查安全漏洞、审查 PRD，或者管理你的 Skills</div>
    </div>
    ''', unsafe_allow_html=True)


def render_input_area():
    """渲染输入区域"""
    # 使用 Streamlit 的 chat_input
    prompt = st.chat_input("输入你的需求，例如：分析 biz-delivery 代码质量...")
    
    if prompt:
        # 处理用户输入
        response = process_task(prompt)
        
        # 添加到会话历史
        st.session_state.messages.append({"role": "user", "content": format_user_message(prompt)})
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # 重新渲染
        st.rerun()


def process_task(prompt: str) -> str:
    """处理任务"""
    prompt_lower = prompt.lower()
    
    # 检测意图
    if any(kw in prompt_lower for kw in ["代码质量", "分析代码", "检查代码", "code quality", "analyze"]):
        return run_code_analysis(prompt)
    elif any(kw in prompt_lower for kw in ["安全检查", "安全扫描", "security", "owasp"]):
        return run_security_check(prompt)
    elif any(kw in prompt_lower for kw in ["prd", "需求", "review", "审查"]):
        return run_prd_review(prompt)
    elif any(kw in prompt_lower for kw in ["skill", "技能", "安装", "manage", "list"]):
        return run_skill_management()
    elif any(kw in prompt_lower for kw in ["能做什么", "有什么功能", "capabilities", "help"]):
        return generate_capabilities_response()
    else:
        return generate_default_response(prompt)


def run_code_analysis(prompt: str) -> str:
    """运行代码分析"""
    path = extract_path(prompt) or str(Path.home() / "biz-delivery")
    runner = st.session_state.runner
    
    result = runner.analyze_directory(path, "python")
    
    if "error" in result:
        return f"❌ 分析失败: {result['error']}"
    
    score = result.get('score', 0)
    summary = result.get('summary', {})
    findings = result.get('findings', [])
    
    response = f"""## 📊 代码质量分析结果

**目标路径**: `{path}`

**质量得分**: **{score}/100**

**统计**: 错误 {summary.get('errors', 0)} | 警告 {summary.get('warnings', 0)}
"""
    
    if findings:
        response += "\n### 🔍 发现的问题\n\n"
        for f in findings[:5]:
            icon = "🔴" if f.get('severity') == 'error' else "🟡"
            response += f"- {icon} **{f.get('message', 'Unknown')}** (Line {f.get('line', '?')})\n"
    else:
        response += "\n✅ 未发现重大问题!"
    
    return response


def run_security_check(prompt: str) -> str:
    """运行安全检查"""
    path = extract_path(prompt) or str(Path.home() / "biz-delivery")
    runner = st.session_state.runner
    
    result = runner.run_security_check(path)
    
    if "error" in result:
        return f"❌ 检查失败: {result['error']}"
    
    response = f"""## 🔒 OWASP 安全检查结果

**目标路径**: `{path}`

"""
    
    for item in result.get('checks', []):
        icon = "✅" if item.get('passed') else "❌"
        response += f"- {icon} **{item.get('name', 'Unknown')}**\n"
        if not item.get('passed'):
            response += f"  - ⚠️ {item.get('detail', '')}\n"
    
    response += f"\n**风险评分**: {result.get('risk_score', 0)}/100"
    return response


def run_prd_review(prompt: str) -> str:
    """运行 PRD 审查"""
    biz_delivery_path = Path("/Users/yanping.ma/biz-delivery")
    expert_script = biz_delivery_path / "scripts" / "expert_system.py"
    
    if not expert_script.exists():
        return "❌ biz-delivery skill 未找到，请先安装"
    
    prd_content = extract_prd_content(prompt)
    if not prd_content:
        return """⚠️ 请提供 PRD 内容

例如：
```
# 项目名称
## 背景
...
## 功能需求
...
```"""
    
    try:
        result = subprocess.run(
            ["python3", str(expert_script), "review", prd_content],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return f"## 📋 PRD 审查结果\n\n{result.stdout}"
        else:
            return f"❌ 审查失败: {result.stderr}"
    except Exception as e:
        return f"❌ 审查异常: {str(e)}"


def run_skill_management() -> str:
    """运行 Skills 管理"""
    registry = st.session_state.registry
    skills = registry.list_skills()
    
    response = "## 📦 已安装的 Skills\n\n"
    for s in skills:
        status = "✅ 启用" if s.get("enabled") else "❌ 禁用"
        langs = s.get("metadata", {}).get("languages", [])
        response += f"- **{s['name']}** v{s.get('version', '?')} - {status}\n"
        if langs:
            response += f"  - 支持语言: {', '.join(langs)}\n"
        response += f"  - {s.get('description', 'N/A')}\n\n"
    
    return response


def generate_capabilities_response() -> str:
    """生成能力说明"""
    return """## 🤖 Web Coding Agent 能力

我可以帮你完成以下编码任务：

### 🛡️ 代码质量
- 分析 Python/TypeScript/Go/Java/Rust/C#/PHP 代码
- OWASP Top 10 安全检查
- 识别代码坏味道
- 提供修复建议

### 📋 PRD 审查
- 专家级 PRD 审查
- 技术可行性评估
- 业务价值分析

### 📦 Skills 管理
- 列出已安装 Skills
- 安装/卸载 Skills
- 查看 Skill 详情

### 💬 使用示例
- "分析 /Users/yanping.ma/biz-delivery 的代码质量"
- "检查 /path/to/project 的安全漏洞"
- "审查这个 PRD: ..."
- "列出所有已安装的 Skills""


def generate_default_response(prompt: str) -> str:
    """生成默认回复"""
    return f"""收到你的需求: "{prompt}"

我可以帮你：
- 🛡️ **代码质量分析** - 调用 code-quality-guard
- 🔒 **安全检查** - OWASP Top 10 扫描
- 📋 **PRD 审查** - 专家系统审查
- 📦 **Skills 管理** - 查看/安装 Skills

请提供更多细节，或选择具体功能。"""


def extract_path(prompt: str) -> str:
    """从 prompt 提取路径"""
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""


def extract_prd_content(prompt: str) -> str:
    """从 prompt 提取 PRD 内容"""
    import re
    code_blocks = re.findall(r'```[\s\S]*?```', prompt)
    return code_blocks[0].replace('```', '').strip() if code_blocks else prompt


def format_user_message(prompt: str) -> str:
    """格式化用户消息"""
    return f"<p>{prompt}</p>"


if __name__ == "__main__":
    main()
