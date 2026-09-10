"""
web-coding - AI Code Agent Platform
类似 Codex 的 agent 工作台
"""
import streamlit as st
import sys
from pathlib import Path

# 页面配置
st.set_page_config(
    page_title="Web Coding Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自定义样式
st.markdown("""
<style>
/* Main theme */
:root {
  --bg-primary: #0F172A;
  --bg-secondary: #1E293B;
  --accent: #38BDF8;
  --text-primary: #F8FAFC;
  --text-secondary: #94A3B8;
}

/* Override Streamlit defaults */
.stApp {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
  background-color: var(--bg-secondary);
  border-right: 1px solid #334155;
}

[data-testid="stSidebar"] .stMarkdown {
  color: var(--text-primary);
}

/* Main content */
main {
  background-color: var(--bg-primary);
}

/* Buttons */
.stButton > button {
  background-color: var(--accent);
  color: var(--bg-primary);
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
}

.stButton > button:hover {
  opacity: 0.9;
}

/* Chat input */
.stChatInput {
  background-color: var(--bg-secondary);
  border: 1px solid #334155;
  border-radius: 12px;
}

/* Text colors */
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
  color: var(--text-primary);
}

/* Quick action chips */
.quick-action {
  display: inline-block;
  padding: 6px 14px;
  margin: 4px;
  background: #334155;
  border: 1px solid #475569;
  border-radius: 20px;
  color: #94A3B8;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.quick-action:hover {
  background: var(--accent);
  color: var(--bg-primary);
  border-color: var(--accent);
}

/* Message bubbles */
.message {
  display: flex;
  gap: 12px;
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 12px;
  background: #1E293B;
}

.message-user {
  background: #334155;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message-user .message-avatar {
  background: #475569;
}

.message-assistant .message-avatar {
  background: linear-gradient(135deg, #38BDF8, #818CF8);
}

/* Stats cards */
.stat-card {
  background: #1E293B;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #38BDF8;
}

.stat-label {
  font-size: 13px;
  color: #94A3B8;
  margin-top: 4px;
}

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #38BDF8, #818CF8);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.empty-subtitle {
  font-size: 15px;
  color: #94A3B8;
}
</style>
""", unsafe_allow_html=True)

# 路径设置
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

# 导入核心模块
try:
    from skill_registry import SkillRegistry
    from skill_runner import SkillRunner
except ImportError:
    SkillRegistry = None
    SkillRunner = None


def main():
    # 初始化
    if 'registry' not in st.session_state:
        if SkillRegistry:
            st.session_state.registry = SkillRegistry()
        else:
            st.session_state.registry = None
    if 'runner' not in st.session_state:
        if SkillRunner and st.session_state.registry:
            st.session_state.runner = SkillRunner(st.session_state.registry)
        else:
            st.session_state.runner = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # 渲染布局
    render_layout()


def render_layout():
    """渲染主布局"""
    render_sidebar()
    render_main()


def render_sidebar():
    """渲染侧边栏"""
    st.markdown("### 🤖 Web Coding")
    st.markdown("---")
    
    # 导航
    st.markdown("**导航**")
    nav_items = [
        ("💬", "对话", True),
        ("📊", "历史记录", False),
        ("⚙️", "设置", False),
    ]
    for icon, text, active in nav_items:
        if active:
            st.markdown(f"{icon} **{text}**")
        else:
            st.markdown(f"{icon} {text}")
    
    st.markdown("---")
    
    # Skills
    st.markdown("**已安装 Skills**")
    if st.session_state.registry:
        skills = st.session_state.registry.list_skills()
        for skill in skills:
            status = "✅" if skill.get("enabled") else "❌"
            st.markdown(f"{status} {skill['name']}")
    else:
        st.markdown("❌ code-quality-guard")
        st.markdown("✅ biz-delivery")
    
    st.markdown("---")
    
    # 快速操作
    st.markdown("**快速操作**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛡️ 代码分析", use_container_width=True):
            process_prompt("分析代码质量")
    with col2:
        if st.button("🔒 安全检查", use_container_width=True):
            process_prompt("检查安全漏洞")
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("📋 PRD 审查", use_container_width=True):
            process_prompt("审查 PRD")
    with col4:
        if st.button("📦 列出 Skills", use_container_width=True):
            process_prompt("列出所有 Skills")
    
    st.markdown("---")
    
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


def render_main():
    """渲染主内容区"""
    # Header
    st.markdown("## Web Coding Agent")
    st.markdown("输入你的需求，AI 将调用相应的 Skills 完成编码任务")
    st.markdown("---")
    
    # Quick actions
    st.markdown("**快速开始：**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🛡️ 分析代码质量", use_container_width=True):
            process_prompt("分析代码质量")
    with col2:
        if st.button("🔒 安全检查", use_container_width=True):
            process_prompt("检查安全漏洞")
    with col3:
        if st.button("📋 PRD 审查", use_container_width=True):
            process_prompt("审查 PRD")
    with col4:
        if st.button("📦 列出 Skills", use_container_width=True):
            process_prompt("列出所有 Skills")
    
    st.markdown("")
    
    # Chat messages
    if st.session_state.messages:
        for msg in st.session_state.messages:
            render_message(msg)
    else:
        render_empty_state()
    
    st.markdown("---")
    
    # Input area
    prompt = st.chat_input("输入你的需求，例如：分析 biz-delivery 代码质量...")
    if prompt:
        response = process_task(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


def render_message(msg: dict):
    """渲染单条消息"""
    is_user = msg["role"] == "user"
    avatar = "👤" if is_user else "🤖"
    role = "你" if is_user else "Web Coding Agent"
    
    with st.container():
        st.markdown(f"""
        <div style="display: flex; gap: 12px; padding: 16px; margin-bottom: 12px; border-radius: 12px; background: {'#334155' if is_user else '#1E293B'};">
            <div style="width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; background: {'#475569' if is_user else 'linear-gradient(135deg, #38BDF8, #818CF8)'};">
                {avatar}
            </div>
            <div style="flex: 1;">
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 6px; font-weight: 600;">{role}</div>
                <div style="font-size: 15px; line-height: 1.6;">{msg['content']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_empty_state():
    """渲染空状态"""
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 20px; text-align: center;">
        <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #38BDF8, #818CF8); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 28px; margin-bottom: 16px;">
            🤖
        </div>
        <div style="font-size: 24px; font-weight: 600; margin-bottom: 8px;">你好，我是 Web Coding Agent</div>
        <div style="font-size: 15px; color: #94A3B8; max-width: 400px;">
            我可以帮你分析代码质量、检查安全漏洞、审查 PRD，或者管理你的 Skills
        </div>
    </div>
    """, unsafe_allow_html=True)


def process_task(prompt: str) -> str:
    """处理任务"""
    prompt_lower = prompt.lower()
    
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
    
    if not st.session_state.runner:
        return f"⚠️ 请安装 code-quality-guard skill\n\n路径: `{path}`"
    
    result = st.session_state.runner.analyze_directory(path, "python")
    
    if "error" in result:
        return f"❌ 分析失败: {result['error']}"
    
    score = result.get('score', 0)
    summary = result.get('summary', {})
    findings = result.get('findings', [])
    
    lines = [
        f"## 📊 代码质量分析结果",
        f"",
        f"**目标路径**: `{path}`",
        f"",
        f"**质量得分**: **{score}/100**",
        f"",
        f"**统计**: 错误 {summary.get('errors', 0)} | 警告 {summary.get('warnings', 0)}",
    ]
    
    if findings:
        lines.append("\n### 🔍 发现的问题\n")
        for f in findings[:5]:
            icon = "🔴" if f.get('severity') == 'error' else "🟡"
            lines.append(f"- {icon} **{f.get('message', 'Unknown')}** (Line {f.get('line', '?')})")
    else:
        lines.append("\n✅ 未发现重大问题!")
    
    return "\n".join(lines)


def run_security_check(prompt: str) -> str:
    """运行安全检查"""
    path = extract_path(prompt) or str(Path.home() / "biz-delivery")
    
    if not st.session_state.runner:
        return f"⚠️ 请安装 code-quality-guard skill\n\n路径: `{path}`"
    
    result = st.session_state.runner.run_security_check(path)
    
    if "error" in result:
        return f"❌ 检查失败: {result['error']}"
    
    lines = [f"## 🔒 OWASP 安全检查结果", f"", f"**目标路径**: `{path}`", ""]
    
    for item in result.get('checks', []):
        icon = "✅" if item.get('passed') else "❌"
        lines.append(f"- {icon} **{item.get('name', 'Unknown')}**")
        if not item.get('passed'):
            lines.append(f"  - ⚠️ {item.get('detail', '')}")
    
    lines.append(f"\n**风险评分**: {result.get('risk_score', 0)}/100")
    return "\n".join(lines)


def run_prd_review(prompt: str) -> str:
    """运行 PRD 审查"""
    biz_delivery_path = Path("/Users/yanping.ma/biz-delivery")
    expert_script = biz_delivery_path / "scripts" / "expert_system.py"
    
    if not expert_script.exists():
        return "❌ biz-delivery skill 未找到，请先安装"
    
    prd_content = extract_prd_content(prompt)
    if not prd_content:
        return "⚠️ 请提供 PRD 内容，例如:\n\n```\n# 项目名称\n## 背景\n...\n## 功能需求\n...\n```"
    
    import subprocess
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
    if not st.session_state.registry:
        return "⚠️ Registry 未初始化"
    
    skills = st.session_state.registry.list_skills()
    lines = ["## 📦 已安装的 Skills\n", ""]
    
    for s in skills:
        status = "✅ 启用" if s.get("enabled") else "❌ 禁用"
        langs = s.get("metadata", {}).get("languages", [])
        lines.append(f"- **{s['name']}** v{s.get('version', '?')} - {status}")
        if langs:
            lines.append(f"  - 支持语言: {', '.join(langs)}")
        lines.append(f"  - {s.get('description', 'N/A')}\n")
    
    return "\n".join(lines)


def generate_capabilities_response() -> str:
    lines = [
        "## 🤖 Web Coding Agent 能力",
        "",
        "我可以帮你完成以下编码任务：",
        "",
        "### 🛡️ 代码质量",
        "- 分析 Python/TypeScript/Go/Java/Rust/C#/PHP 代码",
        "- OWASP Top 10 安全检查",
        "- 识别代码坏味道",
        "- 提供修复建议",
        "",
        "### 📋 PRD 审查",
        "- 专家级 PRD 审查",
        "- 技术可行性评估",
        "- 业务价值分析",
        "",
        "### 📦 Skills 管理",
        "- 列出已安装 Skills",
        "- 安装/卸载 Skills",
        "- 查看 Skill 详情",
        "",
        "### 💬 使用示例",
        '- 输入 "分析 /Users/yanping.ma/biz-delivery 的代码质量"',
        '- 输入 "检查 /path/to/project 的安全漏洞"',
        '- 输入 "审查这个 PRD: ..."',
        '- 输入 "列出所有已安装的 Skills"',
    ]
    return "\n".join(lines)


def generate_default_response(prompt: str) -> str:
    lines = [
        f"收到你的需求: \"{prompt}\"",
        "",
        "我可以帮你：",
        "- 🛡️ **代码质量分析** - 调用 code-quality-guard",
        "- 🔒 **安全检查** - OWASP Top 10 扫描",
        "- 📋 **PRD 审查** - 专家系统审查",
        "- 📦 **Skills 管理** - 查看/安装 Skills",
        "",
        "请提供更多细节，或选择具体功能。",
    ]
    return "\n".join(lines)


def extract_path(prompt: str) -> str:
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""


def extract_prd_content(prompt: str) -> str:
    import re
    code_blocks = re.findall(r'```[\s\S]*?```', prompt)
    return code_blocks[0].replace('```', '').strip() if code_blocks else prompt


def process_prompt(prompt: str):
    """处理快速操作"""
    response = process_task(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()


if __name__ == "__main__":
    main()
