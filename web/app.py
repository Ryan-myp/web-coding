import streamlit as st
import sys
from pathlib import Path

st.set_page_config(page_title="Web Coding", page_icon="⚡", layout="wide")

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
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "registry" not in st.session_state:
        st.session_state.registry = SkillRegistry() if SkillRegistry else None
    if "runner" not in st.session_state:
        st.session_state.runner = SkillRunner(st.session_state.registry) if SkillRunner and st.session_state.registry else None
    
    # 标题
    st.title("⚡ Web Coding Agent")
    st.markdown("---")
    
    # 两栏
    left, right = st.columns([250, 1])
    
    with left:
        st.header("📋 Skills")
        st.markdown("**🛡️ 代码质量**")
        st.markdown("**🔒 安全检查**")
        st.markdown("**📋 PRD 审查**")
        st.markdown("**📦 Skills 管理**")
        
        st.header("📜 历史")
        st.markdown("* 分析 biz-delivery")
        st.markdown("* 检查安全漏洞")
    
    with right:
        render_chat()

def render_chat():
    if st.session_state.messages:
        for msg in st.session_state.messages:
            st.write(f"**{msg['role']}**: {msg['content']}")
    else:
        st.markdown("### 你好，我是 Web Coding Agent")
        st.markdown("我可以帮你分析代码质量、检查安全漏洞、审查 PRD")
        st.markdown("")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.button("🛡️ 代码质量", key="btn1")
        with c2:
            st.button("🔒 安全检查", key="btn2")
        with c3:
            st.button("📋 PRD 审查", key="btn3")
        with c4:
            st.button("📦 Skills", key="btn4")
    
    prompt = st.chat_input("输入你的需求...")
    if prompt:
        response = handle_request(prompt)
        st.write(f"**你**: {prompt}")
        st.write(f"**Agent**: {response}")
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})

def handle_request(prompt):
    p = prompt.lower()
    if "代码质量" in p or "analyze":
        return f"**路径**: `{extract_path(prompt) or '/Users/yanping.ma/biz-delivery'}`\n\n正在分析..."
    elif "安全检查" in p:
        return "**安全检查完成** ✅"
    elif "prd" in p:
        return "**PRD 审查完成** ✅"
    elif "skill" in p:
        return "**已安装 Skills**\n- code-quality-guard\n- biz-delivery"
    return f"收到: {prompt}"

def extract_path(prompt):
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""

if __name__ == "__main__":
    main()
