"""
Skill Manager - Skills 管理界面
"""
import streamlit as st
from pathlib import Path


def render_skill_manager(registry):
    """渲染 Skills 管理页面"""
    st.title("📦 Skills 管理")
    
    # 安装 Skill
    st.subheader("安装新 Skill")
    col1, col2 = st.columns([3, 1])
    with col1:
        skill_path = st.text_input("Skill 路径", placeholder="/path/to/skill")
    with col2:
        if st.button("安装"):
            if skill_path:
                result = registry.install_skill(skill_path)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"✅ 已安装: {result['skill']['name']}")
                    st.rerun()
    
    # 已安装列表
    st.subheader("已安装的 Skills")
    skills = registry.list_skills()
    
    if not skills:
        st.info("暂无已安装的 Skills")
        return
    
    for skill in skills:
        with st.expander(f"🔧 {skill['name']} v{skill.get('version', '?')}"):
            st.markdown(f"**描述**: {skill.get('description', 'N/A')}")
            st.markdown(f"**路径**: `{skill.get('path', 'N/A')}`")
            st.markdown(f"**安装时间**: {skill.get('installed_at', 'N/A')}")
            st.markdown(f"**状态**: {'✅ 启用' if skill.get('enabled') else '❌ 禁用'}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("禁用", key=f"disable_{skill['name']}"):
                    st.warning(f"已禁用: {skill['name']}")
            with col2:
                if st.button("卸载", key=f"uninstall_{skill['name']}"):
                    registry.uninstall_skill(skill['name'])
                    st.success(f"已卸载: {skill['name']}")
                    st.rerun()
