"""
web-coding - AI Code Agent Platform
类似 Codex 的简洁对话式界面
"""
import streamlit as st
import sys
from pathlib import Path

# 页面配置 - 全屏模式，无边框
st.set_page_config(
    page_title="Web Coding",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 全局样式
st.markdown("""
<style>
/* 全屏背景 */
.stApp {
  background: linear-gradient(180deg, #0D1117 0%, #161B22 100%);
  color: #E6EDF3;
}

/* 隐藏 Streamlit 默认元素 */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none !important;}

/* 主容器 */
.main-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* 顶部标题 */
.header {
  text-align: center;
  margin-bottom: 40px;
}

.header-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.header-title {
  font-size: 32px;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0;
  letter-spacing: -0.5px;
}

.header-subtitle {
  font-size: 16px;
  color: #8B949E;
  margin-top: 8px;
}

/* 消息区域 */
.messages {
  min-height: 300px;
  max-height: 60vh;
  overflow-y: auto;
  padding: 20px 0;
}

.message {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message-user .message-avatar {
  background: #21262D;
  border: 1px solid #30363D;
}

.message-assistant .message-avatar {
  background: linear-gradient(135deg, #1F6FFB 0%, #58A6FF 100%);
}

.message-content {
  flex: 1;
  padding-top: 6px;
}

.message-text {
  font-size: 15px;
  line-height: 1.7;
  color: #E6EDF3;
  white-space: pre-wrap;
}

.message-text code {
  background: #21262D;
  border: 1px solid #30363D;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: #79C0FF;
}

.message-text pre {
  background: #161B22;
  border: 1px solid #30363D;
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 12px 0;
}

.message-text pre code {
  background: none;
  border: none;
  padding: 0;
  color: #E6EDF3;
}

/* 输入区域 */
.input-area {
  position: sticky;
  bottom: 0;
  background: linear-gradient(to top, #0D1117 60%, transparent);
  padding: 20px 0 10px;
}

.input-container {
  background: #161B22;
  border: 1px solid #30363D;
  border-radius: 16px;
  padding: 16px;
  transition: border-color 0.2s;
}

.input-container:focus-within {
  border-color: #1F6FFB;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #1F6FFB 0%, #58A6FF 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 28px;
  font-weight: 700;
  color: #FFFFFF;
  margin-bottom: 8px;
}

.empty-subtitle {
  font-size: 16px;
  color: #8B949E;
  max-width: 500px;
  line-height: 1.6;
}

/* 功能卡片 */
.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 40px;
  width: 100%;
  max-width: 700px;
}

.feature-card {
  background: #161B22;
  border: 1px solid #30363D;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.feature-card:hover {
  border-color: #1F6FFB;
  transform: translateY(-2px);
}

.feature-icon {
  font-size: 24px;
  margin-bottom: 12px;
}

.feature-title {
  font-size: 14px;
  font-weight: 600;
  color: #E6EDF3;
  margin-bottom: 4px;
}

.feature-desc {
  font-size: 12px;
  color: #8B949E;
}
</style>
""", unsafe_allow_html=True)

# 路径设置
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

# 导入模块
try:
    from skill_registry import SkillRegistry
    from skill_runner import SkillRunner
except ImportError:
    SkillRegistry = None
    SkillRunner = None


def main():
    # 初始化 session state
    init_state()
    
    # 渲染界面
    render_header()
    render_messages()
    render_input()


def init_state():
    """初始化会话状态"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'registry' not in st.session_state:
        st.session_state.registry = SkillRegistry() if SkillRegistry else None
    if 'runner' not in st.session_state:
        st.session_state.runner = SkillRunner(st.session_state.registry) if SkillRunner and st.session_state.registry else None


def render_header():
    """渲染顶部标题"""
    st.markdown("""
    <div class="header">
        <div class="header-icon">⚡</div>
        <h1 class="header-title">Web Coding</h1>
        <p class="header-subtitle">AI 编码助手 - 输入你的需求，让 AI 帮你完成</p>
    </div>
    """, unsafe_allow_html=True)


def render_messages():
    """渲染消息列表"""
    messages_container = st.container()
    with messages_container:
        if st.session_state.messages:
            for msg in st.session_state.messages:
                render_message(msg)
        else:
            render_empty_state()


def render_message(msg: dict):
    """渲染单条消息"""
    is_user = msg["role"] == "user"
    avatar = "👤" if is_user else "🤖"
    
    col1, col2 = st.columns([1, 10])
    with col1:
        st.markdown(f'''
        <div style="width: 36px; height: 36px; border-radius: 50%; 
                    background: {'#21262D' if is_user else 'linear-gradient(135deg, #1F6FFB, #58A6FF)'};
                    display: flex; align-items: center; justify-content: center;
                    font-size: 18px;">
            {avatar}
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div style="font-size: 15px; line-height: 1.7; color: #E6EDF3; white-space: pre-wrap;">
            {msg['content']}
        </div>
        ''', unsafe_allow_html=True)


def render_empty_state():
    """渲染空状态"""
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🤖</div>
        <div class="empty-title">你好，我是 Web Coding Agent</div>
        <div class="empty-subtitle">我可以帮你分析代码质量、检查安全漏洞、审查 PRD，或者管理你的 Skills</div>
        
        <div class="features">
            <div class="feature-card" onclick="setPrompt('分析代码质量')">
                <div class="feature-icon">🛡️</div>
                <div class="feature-title">代码质量分析</div>
                <div class="feature-desc">Python/TS/Go/Java/Rust</div>
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
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_input():
    """渲染输入区域"""
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    
    prompt = st.chat_input("输入你的需求，例如：分析 biz-delivery 代码质量...", key="main_input")
    
    if prompt:
        response = process_task(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


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
        return f"⚠️ 请安装 code-quality-guard skill\n\n目标路径: `{path}`"
    
    result = st.session_state.runner.analyze_directory(path, "python")
    
    if "error" in result:
        return f"❌ 分析失败: {result['error']}"
    
    score = result.get('score', 0)
    summary = result.get('summary', {})
    findings = result.get('findings', [])
    
    lines = [
        f"## 📊 代码质量分析",
        f"",
        f"**路径**: `{path}`",
        f"**得分**: **{score}/100**",
        f"",
    ]
    
    if findings:
        lines.append("### 🔍 发现问题")
        for f in findings[:5]:
            icon = "🔴" if f.get('severity') == 'error' else "🟡"
            lines.append(f"- {icon} {f.get('message', 'Unknown')} (L{f.get('line', '?')})")
    else:
        lines.append("✅ 未发现重大问题")
    
    return "\n".join(lines)


def run_security_check(prompt: str) -> str:
    """运行安全检查"""
    path = extract_path(prompt) or str(Path.home() / "biz-delivery")
    
    if not st.session_state.runner:
        return f"⚠️ 请安装 code-quality-guard skill"
    
    result = st.session_state.runner.run_security_check(path)
    
    if "error" in result:
        return f"❌ 检查失败: {result['error']}"
    
    lines = [f"## 🔒 OWASP 安全检查", f"", f"**路径**: `{path}`", ""]
    
    for item in result.get('checks', []):
        icon = "✅" if item.get('passed') else "❌"
        lines.append(f"- {icon} **{item.get('name', 'Unknown')}**")
    
    return "\n".join(lines)


def run_prd_review(prompt: str) -> str:
    """运行 PRD 审查"""
    import subprocess
    biz_delivery_path = Path("/Users/yanping.ma/biz-delivery")
    expert_script = biz_delivery_path / "scripts" / "expert_system.py"
    
    if not expert_script.exists():
        return "❌ biz-delivery skill 未找到"
    
    prd_content = extract_prd_content(prompt)
    if not prd_content:
        return "⚠️ 请提供 PRD 内容"
    
    try:
        result = subprocess.run(
            ["python3", str(expert_script), "review", prd_content],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return f"## 📋 PRD 审查结果\n\n{result.stdout[:500]}"
        else:
            return f"❌ 审查失败: {result.stderr[:200]}"
    except Exception as e:
        return f"❌ 异常: {str(e)[:200]}"


def run_skill_management() -> str:
    """运行 Skills 管理"""
    if not st.session_state.registry:
        return "⚠️ Registry 未初始化"
    
    skills = st.session_state.registry.list_skills()
    lines = ["## 📦 已安装 Skills\n", ""]
    
    for s in skills:
        status = "✅ 启用" if s.get("enabled") else "❌ 禁用"
        lines.append(f"- **{s['name']}** v{s.get('version', '?')} - {status}")
        lines.append(f"  {s.get('description', 'N/A')}\n")
    
    return "\n".join(lines)


def generate_capabilities_response() -> str:
    return """## 🤖 我能做什么

**代码质量**
- 分析 Python/TypeScript/Go/Java/Rust/C#/PHP 代码
- OWASP Top 10 安全检查
- 识别代码坏味道并提供修复建议

**PRD 审查**
- 专家级 PRD 技术可行性评估
- 业务价值分析
- 架构建议

**Skills 管理**
- 查看已安装 Skills
- 管理 Skill 状态

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
• 📦 Skills 管理

请提供更多细节。'''


def extract_path(prompt: str) -> str:
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""


def extract_prd_content(prompt: str) -> str:
    import re
    code_blocks = re.findall(r'```[\s\S]*?```', prompt)
    return code_blocks[0].replace('```', '').strip() if code_blocks else prompt


if __name__ == "__main__":
    main()
