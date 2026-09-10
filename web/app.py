"""
web-coding - AI Code Agent Platform
使用 Streamlit 原生组件
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
/* 基础样式 */
.stApp { background-color: #09090B; color: #FAFAFA; }
css
""")

# 隐藏 Streamlit chrome
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none !important;}
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
    # 顶栏
    col_brand, col Spacer, col_actions = st.columns([1, 4, 2])
    with col_brand:
        st.markdown("**⚡ Web Coding**")
    with col_actions:
        st.button("● Live", key="btn_live", help="Live mode")
        st.button("▼ 筛选", key="btn_filter")
        st.button("🔧 系统运维", key="btn_ops")
        st.button("🌙 深色", key="btn_dark")
    
    st.markdown("---")
    
    # 三栏布局
    col_left, col_main, col_right = st.columns([240, 1, 300])
    
    with col_left:
        render_sidebar_left()
    
    with col_main:
        render_main()
    
    with col_right:
        render_sidebar_right()


def render_sidebar_left():
    st.markdown("**+ 新对话**")
    st.markdown("---")
    st.markdown("**Skills**")
    st.markdown("* 🛡️ 代码质量")
    st.markdown("* 🔒 安全检查")
    st.markdown("* 📋 PRD 审查")
    st.markdown("---")
    st.markdown("**最近对话**")
    st.markdown("* 分析 biz-delivery 代码质量")
    st.markdown("  *今天 09:56*")
    st.markdown("* 检查安全漏洞")
    st.markdown("  *昨天 14:30*")


def render_main():
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"**你:** {msg['content']}")
            else:
                st.markdown(f"**⚡ Web Coding Agent:**\n\n{msg['content']}")
    else:
        st.markdown("## 你好，我是 Web Coding Agent")
        st.markdown("我可以帮你分析代码质量、检查安全漏洞、审查 PRD，或者管理你的 Skills")
        
        st.markdown("**快速开始：**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🛡️ 代码质量"):
                process_task("分析代码质量")
        with c2:
            if st.button("🔒 安全检查"):
                process_task("检查安全漏洞")
        with c3:
            if st.button("📋 PRD 审查"):
                process_task("审查 PRD")
        with c4:
            if st.button("📦 Skills"):
                process_task("列出所有 Skills")
    
    st.markdown("---")
    prompt = st.chat_input("描述你的需求...")
    if prompt:
        response = process_task(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


def render_sidebar_right():
    st.markdown("**执行轨迹**")
    st.markdown("* 待命")
    st.divider()
    st.markdown("本回合未产生 Tool 执行")
    st.caption("发送请求后，这里显示真实计划与 Tool 状态")


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
    return "\n".join(lines)


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


def generate_default(prompt: str) -> str:
    return f"收到你的需求: \"{prompt}\"\n\n我可以帮你：\n• 🛡️ 代码质量分析\n• 🔒 安全检查\n• 📋 PRD 审查\n• 📦 Skills 管理"


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
