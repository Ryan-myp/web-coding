import streamlit as st
st.title("✅ Web Coding Agent 工作台")
st.markdown("---")
st.markdown("## 🎯 功能")
st.markdown("""
1. **🛡️ 代码质量分析** - 调用 code-quality-guard
2. **🔒 安全检查** - OWASP Top 10
3. **📋 PRD审查** - 专家系统
4. **📦 Skills管理** - 安装/卸载

## 💬 对话示例
- "分析 biz-delivery 代码质量"
- "检查 /path/to/project 安全漏洞"
- "列出已安装的 Skills"
""")
st.markdown("---")
st.info("💡 请访问 http://localhost:8501 查看完整界面")
