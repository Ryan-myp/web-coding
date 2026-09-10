#!/usr/bin/env python3
"""
Code Quality Panel - Streamlit 组件
"""
import streamlit as st

def render_code_quality_panel(integration):
    st.title("🛡️ 代码质量分析")
    tab1, tab2, tab3, tab4 = st.tabs(["📊 分析代码", "🔒 安全检查", "📚 模式库", "📈 统计"])
    
    with tab1:
        target = st.text_input("目标路径", value="/Users/yanping.ma/biz-delivery")
        lang = st.selectbox("语言", ["python", "typescript", "go", "java", "rust", "csharp", "php"])
        if st.button("🔍 开始分析"):
            with st.spinner("分析中..."):
                result = integration.analyze_directory(target, lang)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"分析完成! 得分: {result.get('score', 0)}/100")
                    st.json(result)
    
    with tab2:
        st.subheader("OWASP 安全检查")
        target = st.text_input("路径", value="/Users/yanping.ma/biz-delivery")
        if st.button("🔒 检查安全"):
            result = integration.run_security_check(target)
            st.json(result)
    
    with tab3:
        st.subheader("模式库")
        stats = integration.get_pattern_stats()
        st.metric("总模式数", stats.get('total_patterns', 0))
        st.metric("平均成功率", f"{stats.get('average_success_rate', 0):.1%}")
    
    with tab4:
        st.subheader("统计")
        skill_stats = integration.get_skill_stats()
        feedback_stats = integration.get_feedback_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("吸收模式", skill_stats.get('total_patterns', 0))
        with col2:
            st.metric("用户反馈", feedback_stats.get('total', 0))

def init_session_state():
    if 'cq_analysis_result' not in st.session_state:
        st.session_state.cq_analysis_result = None
