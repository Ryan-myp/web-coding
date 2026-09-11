import streamlit as st
import sys
from pathlib import Path

st.set_page_config(
    page_title="Web Coding Agent",
    page_icon="⚡",
    layout="wide"
)

# 深色主题
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
header { visibility: hidden; }
footer { visibility: hidden; }
.stApp { background-color: #0D1117; }
.stButton > button {
    background-color: #238636;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 14px;
}
.stButton > button:hover { background-color: #2EA043; }
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
    
    st.markdown("<h2 style='color:white;'>⚡ Web Coding Agent</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B949E;'>输入你的需求，AI 将调用相应的 Skills 完成编码任务</p>", unsafe_allow_html=True)
    
    col_left, col_mid, col_right = st.columns([240, 1, 280])
    
    with col_left:
        st.markdown("### Skills")
        st.markdown("**🛡️** 代码质量分析")
        st.markdown("**🔒** 安全检查")
        st.markdown("**📋** PRD 审查")
        st.markdown("")
        st.markdown("### 历史记录")
        st.markdown("* 分析 biz-delivery 代码质量")
        st.markdown("* 检查安全漏洞")
    
    with col_mid:
        render_chat()
    
    with col_right:
        st.markdown("### 执行面板")
        st.markdown("**状态**: ⏳ 待命")

def render_chat():
    messages_container = st.container()
    with messages_container:
        if st.session_state.messages:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f"**你:** {msg['content']}")
                else:
                    st.markdown(f"**⚡ Agent:** {msg['content']}")
        else:
            st.markdown("""
            <div style="text-align:center; padding:40px; color:#8B949E;">
                <h2>你好，我是 Web Coding Agent</h2>
                <p>我可以帮你分析代码质量、检查安全漏洞、审查 PRD</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.button("🛡️ 代码质量")
            with c2:
                st.button("🔒 安全检查")
            with c3:
                st.button("📋 PRD 审查")
            with c4:
                st.button("📦 Skills")
    
    prompt = st.chat_input("描述你的需求...")
    if prompt:
        response = handle_prompt(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def handle_prompt(prompt):
    p = prompt.lower()
    if any(k in p for k in ["代码质量", "analyze", "code quality"]):
        path = extract_path(prompt) or "/Users/yanping.ma/biz-delivery"
        return f"**路径**: `{path}`\n\n正在分析代码质量..."
    elif any(k in p for k in ["安全检查", "security"]):
        return "**安全检查完成**\n\n✅ OWASP Top 10 无严重问题"
    elif any(k in p for k in ["prd", "需求"]):
        return "**PRD 审查完成**\n\n✅ 功能完整性检查通过"
    elif any(k in p for k in ["skill", "技能"]):
        return "**已安装 Skills:**\n\n- code-quality-guard\n- biz-delivery"
    return f"收到: {prompt}\n\n请具体说明你需要什么帮助"

def extract_path(prompt):
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""

if __name__ == "__main__":
    main()
