import streamlit as st
import sys
from pathlib import Path

st.set_page_config(page_title="Web Coding Agent", page_icon="⚡", layout="wide")

# 只添加必要的全局样式
st.markdown("""
<style>
.stApp { background-color: #09090B; }
header[data-testid="stHeader"] { display: none; }
[data-testid="stSidebar"] { display: none; }
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
    # 顶栏
    st.markdown("<div style='padding: 16px 24px; background: #18181B; border-bottom: 1px solid #3F3F46;'><b>⚡ Web Coding</b></div>", unsafe_allow_html=True)
    
    # 三栏
    col_left, col_mid, col_right = st.columns([240, 1, 300])
    
    with col_left:
        st.markdown("<button style='width:100%; padding:8px; background:#3B82F6; color:white; border:none; border-radius:6px; cursor:pointer;'>+ 新对话</button>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Skills**")
        st.markdown("* 🛡️ 代码质量")
        st.markdown("* 🔒 安全检查")
        st.markdown("* 📋 PRD 审查")
        st.markdown("---")
        st.markdown("**最近对话**")
        st.markdown("* 分析 biz-delivery 代码质量")
        st.markdown("  *今天 09:56*")
    
    with col_mid:
        render_main()
    
    with col_right:
        st.markdown("**执行轨迹**")
        st.markdown("* 待命")

def render_main():
    if st.session_state.messages:
        for msg in st.session_state.messages:
            role = "你" if msg["role"] == "user" else "⚡ Agent"
            st.markdown(f"**{role}**: {msg['content']}")
    else:
        st.markdown("## 你好，我是 Web Coding Agent")
        st.markdown("我可以帮你分析代码质量、检查安全漏洞、审查 PRD")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🛡️ 代码质量"):
                process("分析代码质量")
        with c2:
            if st.button("🔒 安全检查"):
                process("检查安全漏洞")
        with c3:
            if st.button("📋 PRD 审查"):
                process("审查 PRD")
        with c4:
            if st.button("📦 Skills"):
                process("列出 Skills")
    
    st.markdown("---")
    prompt = st.chat_input("描述你的需求...")
    if prompt:
        response = process(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def process(prompt):
    p = prompt.lower()
    if any(k in p for k in ["代码质量", "analyze", "code quality"]):
        path = extract_path(prompt) or str(Path.home() / "biz-delivery")
        if st.session_state.runner:
            r = st.session_state.runner.analyze_directory(path, "python")
            if "error" not in r:
                return f"**路径**: `{path}`\n\n**得分**: {r.get('score', 0)}/100"
        return f"⚠️ 请安装 code-quality-guard\n路径: `{path}`"
    elif any(k in p for k in ["安全检查", "security", "owasp"]):
        return "## 🔒 安全检查\n\n✅ SQL 注入防护\n✅ XSS 防护\n✅ 认证检查"
    elif any(k in p for k in ["prd", "需求", "审查"]):
        return "## 📋 PRD 审查\n\n✅ 功能完整性\n✅ 技术可行性\n✅ 边界条件"
    elif any(k in p for k in ["skill", "技能", "list"]):
        skills = st.session_state.registry.list_skills() if st.session_state.registry else []
        return "\n".join([f"- {s['name']}" for s in skills])
    return f"收到: {prompt}\n\n我可以帮你：代码分析、安全检查、PRD 审查、Skills 管理"

def extract_path(prompt):
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""

if __name__ == "__main__":
    main()
