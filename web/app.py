"""
web-coding - AI Code Agent Platform
参考 AI Ops Agent 的三栏布局设计
"""
import streamlit as st
import sys
from pathlib import Path

st.set_page_config(
    page_title="Web Coding Agent",
    page_icon="⚡",
    layout="wide",
)

# 全局样式
st.markdown("""
<style>
/* 基础变量 */
:root {
  --bg-primary: #0F1419;
  --bg-secondary: #1A1F26;
  --bg-tertiary: #242B33;
  --bg-card: #1E252D;
  --border: #2D3741;
  --accent: #10B981;
  --accent-hover: #059669;
  --text-primary: #F3F4F6;
  --text-secondary: #9CA3AF;
  --text-muted: #6B7280;
}

/* 全局样式 */
.stApp {
  background: var(--bg-primary);
  color: var(--text-primary);
}

/* 隐藏 Streamlit 默认元素 */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none !important;}

/* 顶部导航 */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.topbar-brand-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #10B981, #059669);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.topbar-actions {
  display: flex;
  gap: 8px;
}

.topbar-btn {
  padding: 6px 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}

.topbar-btn:hover {
  background: var(--border);
  color: var(--text-primary);
}

.topbar-btn.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

/* 三栏布局 */
.layout {
  display: grid;
  grid-template-columns: 240px 1fr 320px;
  height: calc(100vh - 57px);
}

/* 左栏 - 导航 */
.sidebar-left {
  background: var(--bg-secondary);
  border-right: 1px solid var(--border);
  padding: 16px;
  overflow-y: auto;
}

.new-chat-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #10B981, #059669);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.15s;
}

.new-chat-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.nav-section {
  margin-bottom: 24px;
}

.nav-section-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
  margin-bottom: 8px;
  padding: 0 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}

.nav-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--bg-tertiary);
  color: var(--accent);
}

.history-item {
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 4px;
  transition: all 0.15s;
}

.history-item:hover {
  background: var(--bg-tertiary);
}

.history-title {
  font-size: 13px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* 中栏 - 主内容 */
.main-content {
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
}

/* 聊天气泡 */
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.message {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.message-user .message-avatar {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
}

.message-assistant .message-avatar {
  background: linear-gradient(135deg, #10B981, #059669);
}

.message-content {
  flex: 1;
}

.message-role {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.message-text {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-primary);
  background: var(--bg-card);
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid var(--border);
}

.message-text code {
  background: var(--bg-tertiary);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #7DD3FC;
}

.message-text pre {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  overflow-x: auto;
  margin: 8px 0;
}

.message-text pre code {
  background: none;
  padding: 0;
  color: var(--text-primary);
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #10B981, #059669);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  max-width: 400px;
  line-height: 1.6;
}

/* 功能卡片 */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 32px;
  width: 100%;
  max-width: 500px;
}

.feature-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.feature-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.feature-icon {
  font-size: 20px;
  margin-bottom: 8px;
}

.feature-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.feature-desc {
  font-size: 11px;
  color: var(--text-muted);
}

/* 输入区域 */
.input-area {
  padding: 16px 24px 24px;
  background: var(--bg-primary);
}

.input-container {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  transition: border-color 0.2s;
}

.input-container:focus-within {
  border-color: var(--accent);
}

/* 右栏 - 执行面板 */
.sidebar-right {
  background: var(--bg-secondary);
  border-left: 1px solid var(--border);
  padding: 16px;
  overflow-y: auto;
}

.panel-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-status {
  font-size: 11px;
  color: var(--accent);
  background: rgba(16, 185, 129, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
}

.tool-call {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
}

.tool-call-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.tool-call-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--accent);
}

.tool-call-status {
  font-size: 11px;
  color: var(--text-muted);
  margin-left: auto;
}

.tool-call-param {
  font-size: 11px;
  color: var(--text-secondary);
  padding: 4px 0;
}

.tool-call-param code {
  color: #7DD3FC;
  font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# 路径设置
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

try:
    from skill_registry import SkillRegistry
    from skill_runner import SkillRunner
except ImportError:
    SkillRegistry = None
    SkillRunner = None


def main():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'registry' not in st.session_state:
        st.session_state.registry = SkillRegistry() if SkillRegistry else None
    if 'runner' not in st.session_state:
        st.session_state.runner = SkillRunner(st.session_state.registry) if SkillRunner and st.session_state.registry else None
    
    render_topbar()
    render_layout()


def render_topbar():
    """渲染顶部导航"""
    st.markdown(f'''
    <div class="topbar">
        <div class="topbar-brand">
            <div class="topbar-brand-icon">⚡</div>
            <span>Web Coding Agent</span>
        </div>
        <div class="topbar-actions">
            <button class="topbar-btn active">● Live</button>
            <button class="topbar-btn">▼ 筛选</button>
            <button class="topbar-btn">🔧 系统运维</button>
            <button class="topbar-btn">🌙 深色</button>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_layout():
    """渲染三栏布局"""
    col1, col2, col3 = st.columns([240, 1, 320])
    
    with col1:
        render_sidebar_left()
    
    with col2:
        render_main_content()
    
    with col3:
        render_sidebar_right()


def render_sidebar_left():
    """渲染左侧导航"""
    st.markdown('<button class="new-chat-btn">+ 新对话</button>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nav-section">
        <div class="nav-section-title">Skills 管理</div>
        <div class="nav-item active">
            <span>🛡️</span>
            <span>代码质量</span>
        </div>
        <div class="nav-item">
            <span>🔒</span>
            <span>安全检查</span>
        </div>
        <div class="nav-item">
            <span>📋</span>
            <span>PRD 审查</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nav-section">
        <div class="nav-section-title">最近对话</div>
        <div class="history-item">
            <div class="history-title">分析 biz-delivery 代码质量</div>
            <div class="history-time">今天 09:56</div>
        </div>
        <div class="history-item">
            <div class="history-title">检查安全漏洞</div>
            <div class="history-time">昨天 14:30</div>
        </div>
        <div class="history-item">
            <div class="history-title">PRD 审查 - 广告投放</div>
            <div class="history-time">9/8</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_main_content():
    """渲染主内容区"""
    messages_container = st.container()
    with messages_container:
        if st.session_state.messages:
            for msg in st.session_state.messages:
                render_message(msg)
        else:
            render_empty_state()
    
    render_input()


def render_message(msg: dict):
    """渲染消息"""
    is_user = msg["role"] == "user"
    avatar = "👤" if is_user else "⚡"
    role = "你" if is_user else "Web Coding Agent"
    
    st.markdown(f'''
    <div class="message {'message-user' if is_user else 'message-assistant'}">
        <div class="message-avatar">{avatar}</div>
        <div class="message-content">
            <div class="message-role">{role}</div>
            <div class="message-text">{msg['content']}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_empty_state():
    """渲染空状态"""
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">⚡</div>
        <div class="empty-title">你好，我是 Web Coding Agent</div>
        <div class="empty-subtitle">我可以帮你分析代码质量、检查安全漏洞、审查 PRD，或者管理你的 Skills</div>
        
        <div class="feature-grid">
            <div class="feature-card" onclick="setPrompt('分析代码质量')">
                <div class="feature-icon">🛡️</div>
                <div class="feature-title">代码质量分析</div>
                <div class="feature-desc">Python/TS/Go/Java/Rust/C#/PHP</div>
            </div>
            <div class="feature-card" onclick="setPrompt('检查安全漏洞')">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">安全检查</div>
                <div class="feature-desc">OWASP Top 10 扫描</div>
            </div>
            <div class="feature-card" onclick="setPrompt('审查 PRD')">
                <div class="feature-icon">📋</div>
                <div class="feature-title">PRD 审查</div>
                <div class="feature-desc">专家级技术评估</div>
            </div>
            <div class="feature-card" onclick="setPrompt('列出 Skills')">
                <div class="feature-icon">📦</div>
                <div class="feature-title">Skills 管理</div>
                <div class="feature-desc">查看已安装 Skills</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_input():
    """渲染输入区域"""
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    prompt = st.chat_input("描述你的需求，例如：帮我创建一个 Meta 广告系列...", key="main_input")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if prompt:
        response = process_task(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


def render_sidebar_right():
    """渲染右侧执行面板"""
    st.markdown(f'''
    <div class="panel-title">
        <span>执行轨迹</span>
        <span class="panel-status">待命</span>
    </div>
    <div style="background: var(--bg-tertiary); border: 1px dashed var(--border); border-radius: 8px; padding: 20px; text-align: center; color: var(--text-muted); font-size: 12px;">
        本回合未产生 Tool 执行<br><br>
        发送请求后，这里显示真实计划与 Tool 状态
    </div>
    """, unsafe_allow_html=True)


def process_task(prompt: str) -> str:
    """处理任务"""
    prompt_lower = prompt.lower()
    
    if any(kw in prompt_lower for kw in ["代码质量", "分析代码", "code quality", "analyze"]):
        return run_code_analysis(prompt)
    elif any(kw in prompt_lower for kw in ["安全检查", "security", "owasp"]):
        return run_security_check(prompt)
    elif any(kw in prompt_lower for kw in ["prd", "需求", "review", "审查"]):
        return run_prd_review(prompt)
    elif any(kw in prompt_lower for kw in ["skill", "技能", "list"]):
        return run_skill_management()
    elif any(kw in prompt_lower for kw in ["能做什么", "help", "capabilities"]):
        return generate_capabilities_response()
    else:
        return generate_default_response(prompt)


def run_code_analysis(prompt: str) -> str:
    path = extract_path(prompt) or str(Path.home() / "biz-delivery")
    if not st.session_state.runner:
        return f"⚠️ 请安装 code-quality-guard\n\n路径: `{path}`"
    result = st.session_state.runner.analyze_directory(path, "python")
    if "error" in result:
        return f"❌ {result['error']}"
    score = result.get('score', 0)
    findings = result.get('findings', [])
    lines = [f"## 📊 代码质量分析", f"", f"**路径**: `{path}`", f"**得分**: **{score}/100**", ""]
    if findings:
        lines.append("### 🔍 发现问题")
        for f in findings[:5]:
            lines.append(f"- {'🔴' if f.get('severity')=='error' else '🟡'} {f.get('message', 'Unknown')} (L{f.get('line', '?')})")
    else:
        lines.append("✅ 未发现重大问题")
    return "\n".join(lines)


def run_security_check(prompt: str) -> str:
    path = extract_path(prompt) or str(Path.home() / "biz-delivery")
    if not st.session_state.runner:
        return "⚠️ 请安装 code-quality-guard"
    result = st.session_state.runner.run_security_check(path)
    if "error" in result:
        return f"❌ {result['error']}"
    lines = [f"## 🔒 OWASP 安全检查", f"", f"**路径**: `{path}`", ""]
    for item in result.get('checks', []):
        lines.append(f"- {'✅' if item.get('passed') else '❌'} **{item.get('name', 'Unknown')}**")
    return "\n".join(lines)


def run_prd_review(prompt: str) -> str:
    import subprocess
    script = Path("/Users/yanping.ma/biz-delivery/scripts/expert_system.py")
    if not script.exists():
        return "❌ biz-delivery 未找到"
    content = extract_prd_content(prompt)
    if not content:
        return "⚠️ 请提供 PRD 内容"
    try:
        result = subprocess.run(["python3", str(script), "review", content], capture_output=True, text=True, timeout=60)
        return f"## 📋 PRD 审查结果\n\n{result.stdout[:500]}" if result.returncode == 0 else f"❌ {result.stderr[:200]}"
    except Exception as e:
        return f"❌ {str(e)[:200]}"


def run_skill_management() -> str:
    if not st.session_state.registry:
        return "⚠️ Registry 未初始化"
    skills = st.session_state.registry.list_skills()
    lines = ["## 📦 已安装 Skills\n", ""]
    for s in skills:
        lines.append(f"- **{s['name']}** v{s.get('version', '?')} - {'✅' if s.get('enabled') else '❌'}")
        lines.append(f"  {s.get('description', 'N/A')}\n")
    return "\n".join(lines)


def generate_capabilities_response() -> str:
    return """## 🤖 我能做什么

**代码质量**
- 分析 Python/TypeScript/Go/Java/Rust/C#/PHP 代码
- OWASP Top 10 安全检查
- 提供修复建议

**PRD 审查**
- 专家级技术可行性评估
- 业务价值分析

**Skills 管理**
- 查看已安装 Skills

**使用示例**
- "分析 /path/to/project 的代码质量"
- "检查安全漏洞"
- "审查这个 PRD: ..."
"""


def generate_default_response(prompt: str) -> str:
    return f'''收到你的需求: "{prompt}"

我可以帮你：
• 🛡️ 代码质量分析
• 🔒 安全检查
• 📋 PRD 审查
• 📦 Skills 管理'''


def extract_path(prompt: str) -> str:
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""


def extract_prd_content(prompt: str) -> str:
    import re
    blocks = re.findall(r'```[\s\S]*?```', prompt)
    return blocks[0].replace('```', '').strip() if blocks else prompt


if __name__ == "__main__":
    main()
