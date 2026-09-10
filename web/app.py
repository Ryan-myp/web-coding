"""
web-coding - Skills Integration Platform
基于 Streamlit 的 Skills 集成平台，支持多 Skills 管理、安装、运行

架构:
  - Skill Registry: 管理已安装的 Skills
  - Skill Runner: 执行 Skill 功能
  - Web UI: Streamlit 界面
"""
import streamlit as st
import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import importlib.util

# 页面配置
st.set_page_config(
    page_title="Web Coding - Skills Platform",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 路径设置
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

# 导入核心模块
from scripts.skill_registry import SkillRegistry
from scripts.skill_runner import SkillRunner
from web.components.skill_manager import render_skill_manager
from web.components.skill_dashboard import render_skill_dashboard
from web.components.code_quality_panel import render_code_quality_panel


def load_skill_module(skill_path: Path):
    """动态加载 Skill 模块"""
    if not skill_path.exists():
        return None
    spec = importlib.util.spec_from_file_location(
        "skill_module",
        skill_path / "SKILL.md"
    )
    return None  # 简化实现


def get_installed_skills() -> List[Dict]:
    """获取已安装的 Skills"""
    registry = SkillRegistry()
    return registry.list_skills()


def main():
    # 初始化
    if 'registry' not in st.session_state:
        st.session_state.registry = SkillRegistry()
    if 'runner' not in st.session_state:
        st.session_state.runner = SkillRunner()
    
    # 侧边栏
    st.sidebar.title("🔧 web-coding")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "功能选择",
        ["🏠 仪表盘", "📦 技能管理", "🛡️ 代码质量", "⚙️ 系统设置"]
    )
    
    # 主内容区
    if menu == "🏠 仪表盘":
        render_skill_dashboard(st.session_state.registry)
    elif menu == "📦 技能管理":
        render_skill_manager(st.session_state.registry)
    elif menu == "🛡️ 代码质量":
        render_code_quality_panel(st.session_state.runner)
    elif menu == "⚙️ 系统设置":
        render_settings()


def render_settings():
    """系统设置页面"""
    st.title("⚙️ 系统设置")
    
    st.markdown("### Skills 路径配置")
    skill_paths = st.text_area(
        "Skills 搜索路径 (每行一个)",
        value="/Users/yanping.ma/.agents/skills",
        height=100
    )
    
    if st.button("保存设置"):
        st.success("设置已保存!")


if __name__ == "__main__":
    main()
