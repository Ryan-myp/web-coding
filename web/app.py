"""
web-coding - AI Code Agent Platform
设计参考: frontend-design skill 原则
- 避免默认AI设计 (温暖奶油色、SaaS卡片、ALL-CAPS眉标)
- 采用专业开发者工具风格
- 克制使用装饰
- 功能优先
"""
import streamlit as st
import sys
from pathlib import Path

st.set_page_config(
    page_title="Web Coding",
    page_icon="⚡",
    layout="wide",
)

# 设计 Token System
st.markdown("""
<style>
/* Design Tokens */
:root {
  /* Base palette - 避免温暖奶油色 */
  --bg-canvas: #09090B;      /* zinc-950, 真正的黑 */
  --bg-elevated: #18181B;    /* zinc-900 */
  --bg-muted: #27272A;       /* zinc-800 */
  --border-subtle: #3F3F46;  /* zinc-700 */
  --border-default: #52525B; /* zinc-600 */
  
  /* Accent - 避免 acid-green，用 blue */
  --accent-primary: #3B82F6; /* blue-500 */
  --accent-hover: #2563EB;   /* blue-600 */
  --accent-muted: #1E3A5F;   /* blue-900 */
  
  /* Text - 避免 tinted near-black，用 zinc */
  --text-primary: #FAFAFA;   /* neutral-50 */
  --text-secondary: #A1A1AA; /* neutral-400 */
  --text-muted: #71717A;     /* neutral-500 */
  
  /* Semantic */
  --success: #22C55E;
  --warning: #F59E0B;
  --error: #EF4444;
}

/* Reset & Base */
* { box-sizing: border-box; }
.stApp {
  background: var(--bg-canvas);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }

/* Layout Grid */
.app-grid {
  display: grid;
  grid-template-columns: 260px 1fr 300px;
  height: 100vh;
}

/* Top Bar */
.topbar {
  grid-column: 1 / -1;
  height: 56px;
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 16px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 15px;
}

.brand-icon {
  width: 28px;
  height: 28px;
  background: var(--accent-primary);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.topbar-spacer { flex: 1; }

.topbar-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.btn-pill {
  padding: 6px 12px;
  background: var(--bg-muted);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-pill:hover {
  background: var(--border-subtle);
  color: var(--text-primary);
}

.btn-pill.active {
  background: var(--accent-primary);
  border-color: var(--accent-primary);
  color: white;
}

/* Left Sidebar */
.sidebar-left {
  background: var(--bg-elevated);
  border-right: 1px solid var(--border-subtle);
  padding: 16px;
  overflow-y: auto;
}

.new-chat-btn {
  width: 100%;
  padding: 10px 16px;
  background: var(--accent-primary);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.15s;
}

.new-chat-btn:hover {
  background: var(--accent-hover);
}

.section-label {
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
  padding: 8px 10px;
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  margin-bottom: 2px;
  transition: all 0.15s;
}

.nav-item:hover {
  background: var(--bg-muted);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--accent-muted);
  color: var(--accent-primary);
}

.history-item {
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 4px;
  border: 1px solid transparent;
  transition: all 0.15s;
}

.history-item:hover {
  background: var(--bg-muted);
  border-color: var(--border-subtle);
}

.history-title {
  font-size: 13px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-meta {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* Main Content */
.main-content {
  display: flex;
  flex-direction: column;
  background: var(--bg-canvas);
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

/* Chat Messages */
.message {
  display: flex;
  gap: 14px;
  margin-bottom: 24px;
  animation: messageIn 0.2s ease;
}

@keyframes messageIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.message-user .message-avatar {
  background: var(--bg-muted);
  border: 1px solid var(--border-default);
}

.message-assistant .message-avatar {
  background: var(--accent-primary);
}

.message-body {
  flex: 1;
  max-width: 700px;
}

.message-role {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.message-text {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-primary);
}

.message-text code {
  background: var(--bg-muted);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #60A5FA;
}

.message-text pre {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 14px;
  overflow-x: auto;
  margin: 10px 0;
}

.message-text pre code {
  background: none;
  padding: 0;
  color: var(--text-primary);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}

.empty-icon {
  width: 56px;
  height: 56px;
  background: var(--accent-primary);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: -0.3px;
}

.empty-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  max-width: 400px;
  line-height: 1.6;
}

/* Feature Cards - 避免 SaaS 卡片套件 */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 32px;
  width: 100%;
  max-width: 480px;
}

.feature-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.15s;
  text-align: left;
}

.feature-card:hover {
  border-color: var(--accent-primary);
  transform: translateY(-1px);
}

.feature-icon {
  font-size: 18px;
  margin-bottom: 8px;
}

.feature-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.feature-desc {
  font-size: 11px;
  color: var(--text-muted);
}

/* Input Area */
.input-area {
  padding: 20px 32px 24px;
  background: var(--bg-canvas);
}

.input-wrapper {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: border-color 0.15s;
}

.input-wrapper:focus-within {
  border-color: var(--accent-primary);
}

/* Right Sidebar */
.sidebar-right {
  background: var(--bg-elevated);
  border-left: 1px solid var(--border-subtle);
  padding: 16px;
  overflow-y: auto;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.panel-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.status-badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 12px;
  background: var(--accent-muted);
  color: var(--accent-primary);
}

.tool-call {
  background: var(--bg-muted);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.tool-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--accent-primary);
}

.tool-status {
  font-size: 11px;
  color: var(--text-muted);
  margin-left: auto;
}

.tool-params {
  font-size: 11px;
  color: var(--text-secondary);
}

.tool-params code {
  color: #60A5FA;
  font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

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
    render()


def render():
    render_topbar()
    render_layout()


def render_topbar():
    st.markdown(f'''
    <div class="topbar">
        <div class="brand">
            <div class="brand-icon">⚡</div>
            <span>Web Coding</span>
        </div>
        <div class="topbar-spacer"></div>
        <div class="topbar-actions">
            <button class="btn-pill active">● Live</button>
            <button class="btn-pill">▼ 筛选</button>
            <button class="btn-pill">🔧 系统运维</button>
            <button class="btn-pill">🌙 深色</button>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_layout():
    col1, col2, col3 = st.columns([260, 1, 300])
    
    with col1:
        render_sidebar_left()
    
    with col2:
        render_main_content()
    
    with col3:
        render_sidebar_right()


def render_sidebar_left():
    st.markdown('<button class="new-chat-btn">+ 新对话</button>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-label">Skills</div>
    <div class="nav-item active"><span>🛡️</span><span>代码质量</span></div>
    <div class="nav-item"><span>🔒</span><span>安全检查</span></div>
    <div class="nav-item"><span>📋</span><span>PRD 审查</span></div>
    
    <div class="section-label" style="margin-top: 24px;">最近对话</div>
    <div class="history-item">
        <div class="history-title">分析 biz-delivery 代码质量</div>
        <div class="history-meta">今天 09:56</div>
    </div>
    <div class="history-item">
        <div class="history-title">检查安全漏洞</div>
        <div class="history-meta">昨天 14:30</div>
    </div>
    <div class="history-item">
        <div class="history-title">PRD 审查 - 广告投放</div>
        <div class="history-meta">9/8</div>
    </div>
    """, unsafe_allow_html=True)


def render_main_content():
    container = st.container()
    with container:
        if st.session_state.messages:
            for msg in st.session_state.messages:
                render_message(msg)
        else:
            render_empty_state()
    render_input()


def render_message(msg: dict):
    is_user = msg["role"] == "user"
    avatar = "👤" if is_user else "⚡"
    role = "你" if is_user else "Web Coding Agent"
    
    st.markdown(f'''
    <div class="message {'message-user' if is_user else 'message-assistant'}">
        <div class="message-avatar">{avatar}</div>
        <div class="message-body">
            <div class="message-role">{role}</div>
            <div class="message-text">{msg['content']}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_empty_state():
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">⚡</div>
        <div class="empty-title">你好，我是 Web Coding Agent</div>
        <div class="empty-subtitle">我可以帮你分析代码质量、检查安全漏洞、审查 PRD，或者管理你的 Skills</div>
        
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🛡️</div>
                <div class="feature-title">代码质量分析</div>
                <div class="feature-desc">Python/TS/Go/Java/Rust/C#/PHP</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">安全检查</div>
                <div class="feature-desc">OWASP Top 10 扫描</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">PRD 审查</div>
                <div class="feature-desc">专家级技术评估</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📦</div>
                <div class="feature-title">Skills 管理</div>
                <div class="feature-desc">查看已安装 Skills</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_input():
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    prompt = st.chat_input("描述你的需求，例如：帮我分析代码质量...", key="main_input")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if prompt:
        response = process_task(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


def render_sidebar_right():
    st.markdown(f'''
    <div class="panel-header">
        <div class="panel-title">执行轨迹</div>
        <span class="status-badge">待命</span>
    </div>
    <div style="background: var(--bg-muted); border: 1px dashed var(--border-subtle); border-radius: 8px; padding: 20px; text-align: center; color: var(--text-muted); font-size: 12px;">
        本回合未产生 Tool 执行<br><br>
        发送请求后，这里显示真实计划与 Tool 状态
    </div>
    ''', unsafe_allow_html=True)


def process_task(prompt: str) -> str:
    p = prompt.lower()
    if any(k in p for k in ["代码质量", "分析代码", "code quality", "analyze"]):
        return run_code_analysis(prompt)
    elif any(k in p for k in ["安全检查", "security", "owasp"]):
        return run_security_check(prompt)
    elif any(k in p for k in ["prd", "需求", "review", "审查"]):
        return run_prd_review(prompt)
    elif any(k in p for k in ["skill", "技能", "list"]):
        return run_skill_management()
    elif any(k in p for k in ["能做什么", "help", "capabilities"]):
        return generate_capabilities()
    return generate_default(prompt)


def run_code_analysis(prompt: str) -> str:
    path = extract_path(prompt) or str(Path.home() / "biz-delivery")
    if not st.session_state.runner:
        return f"⚠️ 请安装 code-quality-guard\n\n路径: `{path}`"
    result = st.session_state.runner.analyze_directory(path, "python")
    if "error" in result:
        return f"❌ {result['error']}"
    score = result.get('score', 0)
    findings = result.get('findings', [])
    lines = [f"## 📊 代码质量分析", "", f"**路径**: `{path}`", f"**得分**: **{score}/100**", ""]
    if findings:
        lines.append("### 🔍 发现问题")
        for f in findings[:5]:
            lines.append(f"- {'🔴' if f.get('severity')=='error' else '🟡'} {f.get('message', 'Unknown')} (L{f.get('line', '?')})")
    else:
        lines.append("✅ 未发现重大问题")
    return "\\n".join(lines)


def run_security_check(prompt: str) -> str:
    path = extract_path(prompt) or str(Path.home() / "biz-delivery")
    if not st.session_state.runner:
        return "⚠️ 请安装 code-quality-guard"
    result = st.session_state.runner.run_security_check(path)
    if "error" in result:
        return f"❌ {result['error']}"
    lines = [f"## 🔒 OWASP 安全检查", "", f"**路径**: `{path}`", ""]
    for item in result.get('checks', []):
        lines.append(f"- {'✅' if item.get('passed') else '❌'} **{item.get('name', 'Unknown')}**")
    return "\\n".join(lines)


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
        return f"## 📋 PRD 审查结果\\n\\n{result.stdout[:500]}" if result.returncode == 0 else f"❌ {result.stderr[:200]}"
    except Exception as e:
        return f"❌ {str(e)[:200]}"


def run_skill_management() -> str:
    if not st.session_state.registry:
        return "⚠️ Registry 未初始化"
    skills = st.session_state.registry.list_skills()
    lines = ["## 📦 已安装 Skills\\n", ""]
    for s in skills:
        lines.append(f"- **{s['name']}** v{s.get('version', '?')} - {'✅' if s.get('enabled') else '❌'}")
        lines.append(f"  {s.get('description', 'N/A')}\\n")
    return "\\n".join(lines)


def generate_capabilities() -> str:
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
- "审查这个 PRD: ...""""


def generate_default(prompt: str) -> str:
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
