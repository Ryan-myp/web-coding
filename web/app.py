"""
web-coding - AI Code Agent Platform
类似 Codex 的 agent 工作台，支持多 Skills 协作完成编码任务
"""
import streamlit as st
import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 页面配置
st.set_page_config(
    page_title="Web Coding - AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 路径设置
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

# 导入核心模块
from skill_registry import SkillRegistry
from skill_runner import SkillRunner


def main():
    # 初始化
    if 'registry' not in st.session_state:
        st.session_state.registry = SkillRegistry()
    if 'runner' not in st.session_state:
        st.session_state.runner = SkillRunner(st.session_state.registry)
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_task' not in st.session_state:
        st.session_state.current_task = None
    
    # 侧边栏
    st.sidebar.title("🤖 Web Coding")
    st.sidebar.markdown("---")
    
    # 已安装 Skills 列表
    skills = st.session_state.registry.list_skills()
    st.sidebar.subheader("📦 已安装 Skills")
    for skill in skills:
        status = "✅" if skill.get("enabled") else "❌"
        st.sidebar.markdown(f"{status} **{skill['name']}**")
    
    st.sidebar.markdown("---")
    
    # 快速操作
    st.sidebar.subheader("⚡ 快速操作")
    if st.sidebar.button("🛡️ 代码分析"):
        st.session_state.current_task = "analyze"
        st.rerun()
    if st.sidebar.button("🔒 安全检查"):
        st.session_state.current_task = "security"
        st.rerun()
    if st.sidebar.button("📋 PRD审查"):
        st.session_state.current_task = "prd_review"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # 清空对话
    if st.sidebar.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.rerun()
    
    # 主内容区
    st.title("🤖 Web Coding Agent")
    st.markdown("输入你的需求，AI 将调用相应的 Skills 完成编码任务")
    
    # 显示对话历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 输入区
    if prompt := st.chat_input("输入你的需求，例如：分析 biz-delivery 代码质量..."):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成 AI 回复
        with st.chat_message("assistant"):
            with st.spinner("正在处理..."):
                response = process_task(prompt, st.session_state.runner, st.session_state.registry)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 显示当前任务详情
    if st.session_state.current_task:
        render_task_detail(st.session_state.current_task)


def process_task(prompt: str, runner: SkillRunner, registry: SkillRegistry) -> str:
    """处理任务"""
    prompt_lower = prompt.lower()
    
    # 检测意图
    if any(kw in prompt_lower for kw in ["代码质量", "分析代码", "检查代码", "code quality", "analyze"]):
        return run_code_analysis(prompt, runner)
    elif any(kw in prompt_lower for kw in ["安全检查", "安全扫描", "security", "owasp"]):
        return run_security_check(prompt, runner)
    elif any(kw in prompt_lower for kw in ["prd", "需求", "review", "审查"]):
        return run_prd_review(prompt)
    elif any(kw in prompt_lower for kw in ["skill", "技能", "安装", "manage"]):
        return run_skill_management(prompt, registry)
    else:
        return generate_general_response(prompt, runner, registry)


def run_code_analysis(prompt: str, runner: SkillRunner) -> str:
    """运行代码分析"""
    # 从 prompt 提取路径
    path = extract_path(prompt)
    if not path:
        path = str(Path.home() / "biz-delivery")
    
    result = runner.analyze_directory(path, "python")
    
    if "error" in result:
        return f"❌ 分析失败: {result['error']}"
    
    score = result.get('score', 0)
    summary = result.get('summary', {})
    findings = result.get('findings', [])
    
    response = f"## 📊 代码质量分析结果\n\n"
    response += f"**目标路径**: `{path}`\n\n"
    response += f"**质量得分**: {score}/100\n\n"
    response += f"**错误数**: {summary.get('errors', 0)} | **警告数**: {summary.get('warnings', 0)}\n\n"
    
    if findings:
        response += "### 🔍 发现的问题\n\n"
        for f in findings[:5]:
            icon = "🔴" if f.get('severity') == 'error' else "🟡"
            response += f"- {icon} **{f.get('message', 'Unknown')}** (Line {f.get('line', '?')})\n"
    else:
        response += "✅ 未发现重大问题!"
    
    return response


def run_security_check(prompt: str, runner: SkillRunner) -> str:
    """运行安全检查"""
    path = extract_path(prompt)
    if not path:
        path = str(Path.home() / "biz-delivery")
    
    result = runner.run_security_check(path)
    
    if "error" in result:
        return f"❌ 检查失败: {result['error']}"
    
    response = f"## 🔒 OWASP 安全检查结果\n\n"
    response += f"**目标路径**: `{path}`\n\n"
    
    for item in result.get('checks', []):
        icon = "✅" if item.get('passed') else "❌"
        response += f"- {icon} **{item.get('name', 'Unknown')}**\n"
        if not item.get('passed'):
            response += f"  - ⚠️ {item.get('detail', '')}\n"
    
    response += f"\n**风险评分**: {result.get('risk_score', 0)}/100"
    return response


def run_prd_review(prompt: str) -> str:
    """运行 PRD 审查"""
    # 尝试从 biz-delivery 运行专家系统
    biz_delivery_path = Path("/Users/yanping.ma/biz-delivery")
    expert_script = biz_delivery_path / "scripts" / "expert_system.py"
    
    if not expert_script.exists():
        return "❌ biz-delivery skill 未找到，请先安装"
    
    # 提取 PRD 内容
    prd_content = extract_prd_content(prompt)
    if not prd_content:
        return "⚠️ 请提供 PRD 内容，例如：\\n\\n```\\n# 项目名称\\n\\n## 背景\\n...\\n\\n## 功能需求\\n...\\n```"
    
    # 运行审查
    try:
        result = subprocess.run(
            ["python3", str(expert_script), "review", prd_content],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return f"## 📋 PRD 审查结果\n\n{result.stdout}"
        else:
            return f"❌ 审查失败: {result.stderr}"
    except Exception as e:
        return f"❌ 审查异常: {str(e)}"


def run_skill_management(prompt: str, registry: SkillRegistry) -> str:
    """运行 Skills 管理"""
    skills = registry.list_skills()
    
    response = "## 📦 已安装的 Skills\n\n"
    for s in skills:
        status = "✅ 启用" if s.get("enabled") else "❌ 禁用"
        response += f"- **{s['name']}** v{s.get('version', '?')} - {status}\n"
        response += f"  - {s.get('description', 'N/A')}\n\n"
    
    response += "---\n\n"
    response += "💡 **提示**: 要安装新 Skill，请提供路径，例如：`安装 skill /path/to/skill`"
    return response


def generate_general_response(prompt: str, runner: SkillRunner, registry: SkillRegistry) -> str:
    """生成通用回复"""
    prompt_lower = prompt.lower()
    
    # 检测是否询问可用技能
    if any(kw in prompt_lower for kw in ["能做什么", "有什么功能", "可用技能", "capabilities"]):
        return """## 🤖 Web Coding Agent 能力

我可以帮你完成以下编码任务：

### 🛡️ 代码质量
- 分析 Python/TypeScript/Go/Java/Rust/C#/PHP 代码
- OWASP Top 10 安全检查
- 识别代码坏味道
- 提供修复建议

### 📋 PRD 审查
- 专家级 PRD 审查
- 技术可行性评估
- 业务价值分析

### 📦 Skills 管理
- 列出已安装 Skills
- 安装/卸载 Skills
- 查看 Skill 详情

### 💬 使用示例
- "分析 /Users/yanping.ma/biz-delivery 的代码质量"
- "检查 /path/to/project 的安全漏洞"
- "审查这个 PRD: ..."
- "列出所有已安装的 Skills""
    
    # 默认回复
        return f"收到你的需求: {prompt}"
我可以帮你：
- 🛡️ **代码质量分析** - 调用 code-quality-guard
- 🔒 **安全检查** - OWASP Top 10 扫描
- 📋 **PRD 审查** - 专家系统审查
- 📦 **Skills 管理** - 查看/安装 Skills

请提供更多细节，或选择具体功能。"""


def extract_path(prompt: str) -> str:
    """从 prompt 提取路径"""
    import re
    # 匹配 Unix 路径
    paths = re.findall(r'(/[^\\s]+)', prompt)
    if paths:
        return paths[0]
    return ""


def extract_prd_content(prompt: str) -> str:
    """从 prompt 提取 PRD 内容"""
    # 查找代码块中的内容
    import re
    code_blocks = re.findall(r'```[\s\S]*?```', prompt)
    if code_blocks:
        return code_blocks[0].replace('```', '').strip()
    
    # 如果没有代码块，返回整个 prompt
    return prompt


def render_task_detail(task_type: str):
    """渲染任务详情"""
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 当前任务: {task_type}")
    
    if task_type == "analyze":
        st.info("🛡️ 代码分析任务已启动")
    elif task_type == "security":
        st.info("🔒 安全检查任务已启动")
    elif task_type == "prd_review":
        st.info("📋 PRD 审查任务已启动")


if __name__ == "__main__":
    main()
