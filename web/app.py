"""
Web Coding Agent - 类似 Codex 的简洁界面
"""
import streamlit as st
import sys
from pathlib import Path

# 页面配置
st.set_page_config(page_title="Web Coding", page_icon="⚡", layout="wide")

# 添加基础样式
st.markdown("""
<style>
.stApp { background-color: #0d1117; }
[data-testid="stSidebar"] { display: none !important; }
header { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# 路径设置
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
    # 初始化 session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "registry" not in st.session_state:
        st.session_state.registry = SkillRegistry() if SkillRegistry else None
    if "runner" not in st.session_state:
        st.session_state.runner = SkillRunner(st.session_state.registry) if SkillRunner and st.session_state.registry else None

    # 主界面
    col_left, col_main = st.columns([280, 1])

    with col_left:
        render_sidebar()

    with col_main:
        render_main()


def render_sidebar():
    """渲染侧边栏"""
    st.markdown("### ⚡ Web Coding")
    st.markdown("---")
    
    if st.button("＋ 新对话"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**🛠️ Skills**")
    st.markdown("- 🛡️ 代码质量分析")
    st.markdown("- 🔒 安全检查")
    st.markdown("- 📋 PRD 审查")
    st.markdown("- 📦 Skills 管理")
    
    st.markdown("---")
    st.markdown("**📜 最近对话**")
    st.markdown("- 分析 biz-delivery 代码")
    st.markdown("  *今天 09:56*")
    st.markdown("- 检查安全漏洞")
    st.markdown("  *昨天 14:30*")


def render_main():
    """渲染主内容区"""
    st.title("Web Coding Agent")
    st.caption("AI 编码助手 - 输入需求，自动完成编码任务")
    st.markdown("---")

    # 显示消息
    if st.session_state.messages:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown("**你好，我是 Web Coding Agent**")
            st.markdown("我可以帮你：")
            st.markdown("- 🛡️ 分析 Python/TypeScript/Go/Java 代码质量")
            st.markdown("- 🔒 检查 OWASP Top 10 安全漏洞")
            st.markdown("- 📋 审查 PRD 技术可行性")
            st.markdown("- 📦 管理已安装的 Skills")
        
        # 快速操作按钮
        st.markdown("**快速开始：**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🛡️ 代码质量"):
                handle_action("代码质量分析")
        with col2:
            if st.button("🔒 安全检查"):
                handle_action("安全检查")
        with col3:
            if st.button("📋 PRD 审查"):
                handle_action("PRD 审查")
        with col4:
            if st.button("📦 Skills"):
                handle_action("列出 Skills")

    # 输入框
    prompt = st.chat_input("描述你的需求...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        
        response = process_request(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})


def handle_action(action):
    """处理快速操作"""
    if action == "代码质量分析":
        prompt = "分析代码质量"
    elif action == "安全检查":
        prompt = "检查安全漏洞"
    elif action == "PRD 审查":
        prompt = "审查 PRD"
    elif action == "列出 Skills":
        prompt = "列出所有 Skills"
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = process_request(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})


def process_request(prompt):
    """处理请求"""
    p = prompt.lower()
    
    if "代码质量" in p or "analyze" in p:
        path = extract_path(prompt) or "/Users/yanping.ma/biz-delivery"
        if st.session_state.runner:
            try:
                result = st.session_state.runner.analyze_directory(path, "python")
                if "error" not in result:
                    score = result.get("score", 0)
                    return f"**代码质量分析**\n\n路径: `{path}`\n得分: **{score}/100**"
            except Exception as e:
                return f"❌ 分析失败: {str(e)}"
        return f"**代码质量分析**\n\n路径: `{path}`\n\n⚠️ 请安装 code-quality-guard skill"
    
    elif "安全检查" in p or "security" in p or "owasp" in p:
        path = extract_path(prompt) or "/Users/yanping.ma/biz-delivery"
        if st.session_state.runner:
            try:
                result = st.session_state.runner.run_security_check(path)
                if "error" not in result:
                    checks = result.get("checks", [])
                    passed = sum(1 for c in checks if c.get("passed"))
                    return f"**安全检查完成** ✅\n\n通过: {passed}/{len(checks)}"
            except Exception as e:
                return f"❌ 检查失败: {str(e)}"
        return "**安全检查**\n\n⚠️ 请安装 code-quality-guard skill"
    
    elif "prd" in p or "审查" in p:
        return "**PRD 审查**\n\n请提供 PRD 内容，例如：\n```\n# 项目名称\n## 背景\n...\n```"
    
    elif "skill" in p or "技能" in p:
        if st.session_state.registry:
            skills = st.session_state.registry.list_skills()
            lines = ["**已安装 Skills:**\n"]
            for s in skills:
                status = "✅" if s.get("enabled") else "❌"
                lines.append(f"- {status} **{s['name']}** v{s.get('version', '?')}")
            return "\n".join(lines)
        return "**Skills 管理**\n\n⚠️ Registry 未初始化"
    
    return f"收到: {prompt}\n\n我可以帮你：\n• 🛡️ 代码质量分析\n• 🔒 安全检查\n• 📋 PRD 审查\n• 📦 Skills 管理"


def extract_path(prompt):
    """从 prompt 提取路径"""
    import re
    paths = re.findall(r'(/[^\\s]+)', prompt)
    return paths[0] if paths else ""


if __name__ == "__main__":
    main()
