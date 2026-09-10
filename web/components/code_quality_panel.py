"""
Code Quality Panel - 代码质量分析界面
集成 code-quality-guard 功能
"""
import streamlit as st
import json
from pathlib import Path
from datetime import datetime


def render_code_quality_panel(integration):
    """渲染代码质量面板"""
    st.title("🛡️ 代码质量分析")
    st.markdown("集成 code-quality-guard 进行多维度代码质量分析")
    
    # 选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["📊 分析代码", "🔒 安全检查", "📚 模式库", "⚙️ 配置"])
    
    with tab1:
        render_analysis_tab(integration)
    
    with tab2:
        render_security_tab(integration)
    
    with tab3:
        render_patterns_tab(integration)
    
    with tab4:
        render_config_tab(integration)


def render_analysis_tab(integration):
    """分析代码标签页"""
    st.subheader("📊 代码分析")
    
    # 输入区
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        target_path = st.text_input(
            "目标路径",
            value=str(Path.home() / "biz-delivery"),
            key="cq_target_path"
        )
    with col2:
        language = st.selectbox(
            "语言",
            ["auto", "python", "typescript", "go", "java", "rust", "csharp", "php"],
            key="cq_language"
        )
    with col3:
        if st.button("🔍 分析", type="primary"):
            analyze_code(integration, target_path, language)


def analyze_code(integration, target_path: str, language: str):
    """执行代码分析"""
    path = Path(target_path)
    if not path.exists():
        st.error(f"路径不存在: {target_path}")
        return
    
    with st.spinner(f"正在分析 {target_path}..."):
        if path.is_dir():
            result = integration.analyze_directory(str(path), language)
        else:
            result = integration.analyze_file(str(path), language)
        
        if "error" in result:
            st.error(f"分析失败: {result['error']}")
        else:
            display_analysis_result(result)


def display_analysis_result(result: dict):
    """显示分析结果"""
    # 汇总信息
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        score = result.get('score', 0)
        st.metric("质量得分", f"{score}/100")
    with col2:
        summary = result.get('summary', {})
        st.metric("错误数", summary.get('errors', 0))
    with col3:
        summary = result.get('summary', {})
        st.metric("警告数", summary.get('warnings', 0))
    
    # 问题列表
    findings = result.get('findings', [])
    if findings:
        st.markdown("### 🔍 发现的问题")
        for f in findings[:20]:
            icon = "🔴" if f.get('severity') == 'error' else "🟡" if f.get('severity') == 'warning' else "⚪"
            with st.expander(f"{icon} {f.get('message', 'Unknown')} (Line {f.get('line', '?')})"):
                st.code(f.get('code', ''), language="python")
                st.markdown(f"**规则**: {f.get('rule_id', 'N/A')}")
                
                # 反馈按钮
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ 确认修复", key=f"confirm_{f.get('rule_id')}_{f.get('line', 0)}"):
                        st.success("已记录确认")
                with col2:
                    if st.button("❌ 误报", key=f"reject_{f.get('rule_id')}_{f.get('line', 0)}"):
                        st.warning("已标记为误报")
    else:
        st.success("✅ 未发现重大问题!")


def render_security_tab(integration):
    """安全检查标签页"""
    st.subheader("🔒 OWASP 安全检查")
    
    target = st.text_input("目标路径", value=str(Path.home() / "biz-delivery"), key="sec_target")
    
    if st.button("🔍 运行安全检查"):
        with st.spinner("正在检查安全漏洞..."):
            result = integration.run_security_check(target)
            if "error" in result:
                st.error(f"检查失败: {result['error']}")
            else:
                display_security_result(result)


def display_security_result(result: dict):
    """显示安全检查结果"""
    # OWASP Top 10 检查
    st.markdown("### OWASP Top 10")
    for item in result.get('checks', []):
        icon = "✅" if item.get('passed') else "❌"
        st.markdown(f"- {icon} **{item.get('name', 'Unknown')}**")
        if not item.get('passed'):
            st.markdown(f"  - ⚠️ {item.get('detail', '')}")
    
    # 风险评分
    st.markdown("---")
    st.metric("安全风险评分", f"{result.get('risk_score', 0)}/100")


def render_patterns_tab(integration):
    """模式库标签页"""
    st.subheader("📚 模式库")
    
    # 模式统计
    stats = integration.get_pattern_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总模式数", stats.get('total_patterns', 0))
    with col2:
        st.metric("总使用次数", stats.get('total_usages', 0))
    with col3:
        rate = stats.get('average_success_rate', 0)
        st.metric("平均成功率", f"{rate:.1%}")
    
    # 按类别展示
    by_category = stats.get('by_category', {})
    if by_category:
        st.markdown("### 按类别")
        for cat, count in sorted(by_category.items()):
            st.markdown(f"- **{cat}**: {count} 个模式")


def render_config_tab(integration):
    """配置标签页"""
    st.subheader("⚙️ 配置")
    
    st.markdown("### 质量阈值")
    threshold = st.slider("最低通过分数", 0, 100, 70, key="cq_threshold")
    
    st.markdown("### 语言偏好")
    languages = st.multiselect(
        "分析语言",
        ["python", "typescript", "go", "java", "rust", "csharp", "php"],
        default=["python", "typescript"],
        key="cq_languages"
    )
    
    if st.button("保存配置"):
        st.success("配置已保存!")


def init_session_state():
    """初始化 session state"""
    if 'cq_analysis_result' not in st.session_state:
        st.session_state.cq_analysis_result = None
    if 'sec_result' not in st.session_state:
        st.session_state.sec_result = None
    if 'cq_patterns_list' not in st.session_state:
        st.session_state.cq_patterns_list = []
