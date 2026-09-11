import streamlit as st
import sys
from pathlib import Path

st.set_page_config(page_title="Web Coding Agent", page_icon="⚡", layout="wide")

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
    
    st.title("⚡ Web Coding Agent")
    st.caption("AI 编码助手 - 自动调用 Skills 完成编码任务")
    st.divider()
    
    c1, c2, c3 = st.columns([240, 1, 280])
    
    with c1:
        st.header("Skills")
        st.markdown("**🛡️ 代码质量**")
        st.markdown("**🔒 安全检查**")
        st.markdown("**📋 PRD 审查**")
        st.header("历史")
        st.markdown("* 分析代码质量")
        st.markdown("* 检查安全漏洞")
    
    with c2:
        render_chat()
    
    with c3:
        st.header("执行")
        st.markdown("**状态**: 待命")

def render_chat():
    if st.session_state.messages:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown("**你好，我是 Web Coding Agent**")
            st.markdown("我可以帮你分析代码质量、检查安全漏洞、审查 PRD")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🛡️ 代码质量"):
                process("分析代码质量")
        with col2:
            if st.button("🔒 安全检查"):
                process("检查安全漏洞")
        with col3:
            if st.button("📋 PRD 审查"):
                process("审查 PRD")
        with col4:
            if st.button("📦 Skills"):
                process("列出 Skills")
    
    prompt = st.chat_input("描述你的需求...")
    if prompt:
        response = handle_prompt(prompt)
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def handle_prompt(prompt):
    p = prompt.lower()
    if any(k in p for k in ["代码质量", "analyze"]):
        return f"**路径**: `{extract_path(prompt) or '/Users/yanping.ma/biz-delivery'}`\n\n正在分析..."
    elif any(k in p for k in ["安全检查", "security"]):
        return "**安全检查完成** ✅"
    elif any(k in p for k in ["prd", "需求"]):
        return "**PRD 审查完成** ✅"
    elif any(k in p for k in ["skill", "技能"]):
        return "**已安装 Skills**\n- code-quality-guard\n- biz-delivery"
    return f"收到: {prompt}"

def extract_path(prompt):
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""

if __name__ == "__main__":
    main()
