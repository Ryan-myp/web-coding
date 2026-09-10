"""
Skill Dashboard - Skills 仪表盘
"""
import streamlit as st


def render_skill_dashboard(registry):
    """渲染 Skills 仪表盘"""
    st.title("🏠 Skills 仪表盘")
    
    skills = registry.list_skills()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("已安装 Skills", len(skills))
    with col2:
        enabled = len([s for s in skills if s.get('enabled')])
        st.metric("启用中", enabled)
    with col3:
        st.metric("总文件大小", f"{_total_size(skills)} MB")
    
    # 最近使用
    st.markdown("---")
    st.subheader("最近使用的 Skills")
    for skill in skills[:5]:
        st.markdown(f"- 🔧 **{skill['name']}** - {skill.get('description', 'N/A')[:50]}...")


def _total_size(skills):
    total = 0
    for skill in skills:
        path = skill.get('path', '')
        try:
            p = __import__('pathlib').Path(path)
            if p.exists():
                total += sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
        except:
            pass
    return total / (1024 * 1024)
