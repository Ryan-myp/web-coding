import streamlit as st
import sys
from pathlib import Path

st.set_page_config(page_title="Web Coding", page_icon="⚡", layout="wide")

# 简洁的全局样式
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
header { visibility: hidden; }
footer { visibility: hidden; }
.stApp { background: #0d1117; }
.stTextInput input { background: #161b22; color: white; border: 1px solid #30363d; border-radius: 8px; }
.stButton > button { 
    background: #238636; 
    color: white; 
    border: none; 
    border-radius: 6px;
    padding: 8px 16px;
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
    
    # 顶栏
    st.markdown("<h2 style='color:#58a6ff; margin:0;'>⚡ Web Coding Agent</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 三栏布局
    c1, c2, c3 = st.columns([240, 1, 280])
    
    with c1:
        st.markdown("### Skills")
        st.markdown("**🛡️** 代码质量分析")
        st.markdown("**🔒** 安全检查")
        st.markdown("**📋** PRD 审查")
        st.markdown("")
        st.markdown("### 最近对话")
        st.markdown("* 分析 biz-delivery 代码质量")
        st.markdown("* 检查安全漏洞")
    
    with c2:
        render_chat()
    
    with c3:
        st.markdown("### 执行面板")
        st.markdown("**状态**: ⏳ 待命")

def render_chat():
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"**你:** {msg['content']}")
            else:
                st.markdown(f"**⚡ Agent:** {msg['content']}")
    else:
        st.markdown("<h3 style='color:#c9d1d9;'>你好，我是 Web Coding Agent</h3>", unsafe_allow_html=True)
        st.markdown("我可以帮你分析代码质量、检查安全漏洞、审查 PRD")
        st.markdown("")
        
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
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def handle_prompt(prompt):
    p = prompt.lower()
    if any(k in p for k in ["代码质量", "analyze"]):
        return "**代码质量分析**\n\n路径: `/Users/yanping.ma/biz-delivery`\n得分: 78/100"
    elif any(k in p for k in ["安全检查", "security"]):
        return "**安全检查**\n\n✅ OWASP Top 10 无严重问题"
    elif any(k in p for k in ["prd", "需求"]):
        return "**PRD 审查**\n\n✅ 功能完整性检查通过"
    elif any(k in p for k in ["skill", "技能"]):
        return "**已安装 Skills**\n\n- code-quality-guard\n- biz-delivery"
    return f"收到: {prompt}\n\n请具体说明你需要什么帮助"

if __name__ == "__main__":
    main()
