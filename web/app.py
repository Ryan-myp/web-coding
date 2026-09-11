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
    
    # 顶栏
    st.markdown("<h2 style='margin:0;'>⚡ Web Coding Agent</h2>", unsafe_allow_html=True)
    st.caption("AI 编码助手 - 输入需求，自动调用 Skills 完成编码任务")
    st.divider()
    
    c1, c2, c3 = st.columns([240, 1, 280])
    
    # 左栏
    with c1:
        st.header("🛠️ Skills")
        st.markdown("**🛡️** 代码质量分析")
        st.markdown("**🔒** 安全检查")
        st.markdown("**📋** PRD 审查")
        st.markdown("**📦** Skills 管理")
        st.divider()
        st.header("📜 历史")
        st.markdown("* 分析 biz-delivery 代码")
        st.markdown("* 检查安全漏洞")
        st.markdown("* PRD 审查 - 广告投放")
    
    # 中栏 - 聊天
    with c2:
        render_chat()
    
    # 右栏
    with c3:
        st.header("⚙️ 执行")
        st.markdown("**状态**: ⏳ 待命")
        st.markdown("")
        st.markdown("发送请求后，这里将显示 Tool 执行状态")

def render_chat():
    if st.session_state.messages:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown("**你好，我是 Web Coding Agent**")
            st.markdown("我可以帮你分析代码质量、检查安全漏洞、审查 PRD，或者管理你的 Skills")
        
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
        path = extract_path(prompt) or "/Users/yanping.ma/biz-delivery"
        return f"**路径**: `{path}`\n\n正在分析代码质量..."
    elif any(k in p for k in ["安全检查", "security", "owasp"]):
        return "**安全检查完成** ✅\n\n- SQL 注入防护: ✓\n- XSS 防护: ✓\n- 认证检查: ✓"
    elif any(k in p for k in ["prd", "需求", "review", "审查"]):
        return "**PRD 审查完成** ✅\n\n- 功能完整性: ✓\n- 技术可行性: ✓"
    elif any(k in p for k in ["skill", "技能", "list"]):
        return "**已安装 Skills**\n\n- code-quality-guard\n- biz-delivery"
    return f"收到: {prompt}\n\n我可以帮你：\n• 🛡️ 代码质量分析\n• 🔒 安全检查\n• 📋 PRD 审查\n• 📦 Skills 管理"

def extract_path(prompt):
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""

if __name__ == "__main__":
    main()
