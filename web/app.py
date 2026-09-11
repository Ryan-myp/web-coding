import streamlit as st

st.set_page_config(page_title="Web Coding", page_icon="⚡", layout="centered")

st.title("⚡ Web Coding Agent")
st.markdown("AI 编码助手 - 输入需求，自动完成编码任务")
st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🛡️ 代码质量"):
        st.info("分析代码质量...")
with col2:
    if st.button("🔒 安全检查"):
        st.info("检查安全漏洞...")
with col3:
    if st.button("📋 PRD 审查"):
        st.info("审查 PRD...")
with col4:
    if st.button("📦 Skills"):
        st.info("列出 Skills...")

st.divider()

prompt = st.chat_input("描述你的需求...")
if prompt:
    st.write(f"你: {prompt}")
    st.write("⚡ Agent: 收到你的需求，正在处理...")
