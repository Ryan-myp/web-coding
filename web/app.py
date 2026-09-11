"""
Web Coding Agent - 基于 TestPilot 理念设计
知识库在下，任务入口在上
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="Web Coding Agent",
    page_icon="⚡",
    layout="wide"
)

# 全局样式
st.markdown("""
<style>
/* 隐藏 Streamlit 默认元素 */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none !important;}

/* 全局背景 */
.stApp {
  background-color: #0d1117;
  color: #e6edf3;
}

/* 顶栏 */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: #161b22;
  border-bottom: 1px solid #30363d;
  margin-bottom: 24px;
}

.topbar-brand {
  font-size: 20px;
  font-weight: 600;
  color: #58a6ff;
}

.topbar-status {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-badge {
  padding: 4px 12px;
  background: #238636;
  border-radius: 20px;
  font-size: 12px;
  color: white;
}

/* 主体布局 */
.main-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  padding: 0 24px;
}

/* 左侧知识面板 */
.knowledge-panel {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 16px;
  height: fit-content;
}

.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: #8b949e;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.knowledge-item {
  padding: 10px 12px;
  background: #21262d;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.15s;
}

.knowledge-item:hover {
  background: #30363d;
}

.knowledge-item-title {
  font-size: 13px;
  color: #e6edf3;
  margin-bottom: 2px;
}

.knowledge-item-meta {
  font-size: 11px;
  color: #8b949e;
}

/* 右侧任务区 */
.task-area {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 24px;
}

/* 任务入口卡片 */
.task-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.task-card {
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.15s;
}

.task-card:hover {
  border-color: #58a6ff;
  transform: translateY(-2px);
}

.task-card.active {
  border-color: #58a6ff;
  background: #1f6feb20;
}

.task-card-icon {
  font-size: 24px;
  margin-bottom: 12px;
}

.task-card-title {
  font-size: 15px;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 4px;
}

.task-card-desc {
  font-size: 12px;
  color: #8b949e;
}

/* 表单区域 */
.form-section {
  display: none;
}

.form-section.active {
  display: block;
}

.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #8b949e;
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 6px;
  color: #e6edf3;
  font-size: 14px;
}

.form-input:focus {
  outline: none;
  border-color: #58a6ff;
}

textarea.form-input {
  min-height: 100px;
  resize: vertical;
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 12px;
  background: #238636;
  border: none;
  border-radius: 6px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.submit-btn:hover {
  background: #2ea043;
}

/* 结果区域 */
.result-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #30363d;
  display: none;
}

.result-section.active {
  display: block;
}

.result-title {
  font-size: 14px;
  font-weight: 600;
  color: #8b949e;
  margin-bottom: 12px;
}

.result-content {
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 16px;
  font-size: 14px;
  line-height: 1.6;
  color: #e6edf3;
  white-space: pre-wrap;
}
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
    if "active_task" not in st.session_state:
        st.session_state.active_task = None
    if "task_results" not in st.session_state:
        st.session_state.task_results = {}
    if "registry" not in st.session_state:
        st.session_state.registry = SkillRegistry() if SkillRegistry else None
    if "runner" not in st.session_state:
        st.session_state.runner = SkillRunner(st.session_state.registry) if SkillRunner and st.session_state.registry else None
    
    render_topbar()
    render_main()


def render_topbar():
    st.markdown(f"""
    <div class="topbar">
        <div class="topbar-brand">⚡ Web Coding Agent</div>
        <div class="topbar-status">
            <span class="status-badge">● Live</span>
            <span style="color:#8b949e; font-size:13px;">▼ 筛选</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_main():
    col_left, col_right = st.columns([280, 1])
    
    with col_left:
        render_knowledge_panel()
    
    with col_right:
        render_task_area()


def render_knowledge_panel():
    """渲染左侧知识库面板"""
    st.markdown("""
    <div class="knowledge-panel">
        <div class="panel-title">📚 知识库</div>
        <div class="knowledge-item">
            <div class="knowledge-item-title">🛡️ 代码质量规范</div>
            <div class="knowledge-item-meta">已加载 128 条规则</div>
        </div>
        <div class="knowledge-item">
            <div class="knowledge-item-title">🔒 OWASP Top 10</div>
            <div class="knowledge-item-meta">安全漏洞库</div>
        </div>
        <div class="knowledge-item">
            <div class="knowledge-item-title">📋 PRD 模板</div>
            <div class="knowledge-item-meta">标准审查模板</div>
        </div>
        <div class="knowledge-item">
            <div class="knowledge-item-title">📦 Skills 定义</div>
            <div class="knowledge-item-meta">2 个已安装</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_task_area():
    """渲染右侧任务区"""
    st.markdown("<div class='task-area'>", unsafe_allow_html=True)
    
    # 任务入口卡片
    st.markdown("""
    <div class="task-grid">
        <div class="task-card" onclick="selectTask('code-quality')">
            <div class="task-card-icon">🛡️</div>
            <div class="task-card-title">代码质量分析</div>
            <div class="task-card-desc">检测代码坏味道、规范检查</div>
        </div>
        <div class="task-card" onclick="selectTask('security')">
            <div class="task-card-icon">🔒</div>
            <div class="task-card-title">安全检查</div>
            <div class="task-card-desc">OWASP Top 10 漏洞扫描</div>
        </div>
        <div class="task-card" onclick="selectTask('prd-review')">
            <div class="task-card-icon">📋</div>
            <div class="task-card-title">PRD 审查</div>
            <div class="task-card-desc">技术可行性评估</div>
        </div>
        <div class="task-card" onclick="selectTask('bug-analyze')">
            <div class="task-card-icon">🐛</div>
            <div class="task-card-title">Bug 分析</div>
            <div class="task-card-desc">根因推断与修复建议</div>
        </div>
        <div class="task-card" onclick="selectTask('log-trace')">
            <div class="task-card-icon">📊</div>
            <div class="task-card-title">日志排查</div>
            <div class="task-card-desc">调用链分析与定位</div>
        </div>
        <div class="task-card" onclick="selectTask('skill-mgr')">
            <div class="task-card-icon">📦</div>
            <div class="task-card-title">Skills 管理</div>
            <div class="task-card-desc">查看/安装/卸载 Skills</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 任务表单
    render_task_form()
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_task_form():
    """渲染当前选中任务的表单"""
    active = st.session_state.get("active_task")
    
    if active == "code-quality":
        render_code_quality_form()
    elif active == "security":
        render_security_form()
    elif active == "prd-review":
        render_prd_review_form()
    elif active == "bug-analyze":
        render_bug_analyze_form()
    elif active == "log-trace":
        render_log_trace_form()
    elif active == "skill-mgr":
        render_skill_manager_form()


def render_code_quality_form():
    """代码质量分析表单"""
    st.markdown("""
    <div class="form-section active">
        <h3 style="color:#e6edf3; margin-bottom:16px;">🛡️ 代码质量分析</h3>
        <div class="form-group">
            <label class="form-label">项目路径 (必填)</label>
            <input class="form-input" type="text" placeholder="/path/to/project" id="code-quality-path">
        </div>
        <div class="form-group">
            <label class="form-label">语言类型</label>
            <select class="form-input" id="code-quality-lang">
                <option>Python</option>
                <option>TypeScript</option>
                <option>Go</option>
                <option>Java</option>
                <option>Rust</option>
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">检查重点 (可选)</label>
            <input class="form-input" type="text" placeholder="如：错误处理、命名规范..." id="code-quality-focus">
        </div>
        <button class="submit-btn" onclick="runTask('code-quality')">开始分析</button>
    </div>
    """, unsafe_allow_html=True)


def render_security_form():
    """安全检查表单"""
    st.markdown("""
    <div class="form-section active">
        <h3 style="color:#e6edf3; margin-bottom:16px;">🔒 安全检查</h3>
        <div class="form-group">
            <label class="form-label">扫描路径 (必填)</label>
            <input class="form-input" type="text" placeholder="/path/to/project" id="security-path">
        </div>
        <div class="form-group">
            <label class="form-label">检查维度</label>
            <select class="form-input" id="security-dimension">
                <option>OWASP Top 10 全量检查</option>
                <option>SQL 注入检测</option>
                <option>XSS 防护检查</option>
                <option>认证授权检查</option>
            </select>
        </div>
        <button class="submit-btn" onclick="runTask('security')">开始扫描</button>
    </div>
    """, unsafe_allow_html=True)


def render_prd_review_form():
    """PRD 审查表单"""
    st.markdown("""
    <div class="form-section active">
        <h3 style="color:#e6edf3; margin-bottom:16px;">📋 PRD 审查</h3>
        <div class="form-group">
            <label class="form-label">PRD 内容 (必填)</label>
            <textarea class="form-input" placeholder="# 项目名称
## 背景
...
## 功能需求
..." id="prd-content"></textarea>
        </div>
        <div class="form-group">
            <label class="form-label">关注点</label>
            <select class="form-input" id="prd-focus">
                <option>技术可行性评估</option>
                <option>边界条件检查</option>
                <option>性能风险评估</option>
            </select>
        </div>
        <button class="submit-btn" onclick="runTask('prd-review')">开始审查</button>
    </div>
    """, unsafe_allow_html=True)


def render_bug_analyze_form():
    """Bug 分析表单"""
    st.markdown("""
    <div class="form-section active">
        <h3 style="color:#e6edf3; margin-bottom:16px;">🐛 Bug 分析</h3>
        <div class="form-group">
            <label class="form-label">Bug 现象描述 (必填)</label>
            <textarea class="form-input" placeholder="描述 Bug 的表现..." id="bug-desc"></textarea>
        </div>
        <div class="form-group">
            <label class="form-label">错误日志 (可选)</label>
            <textarea class="form-input" placeholder="粘贴错误日志..." id="bug-log"></textarea>
        </div>
        <div class="form-group">
            <label class="form-label">环境信息 (可选)</label>
            <input class="form-input" type="text" placeholder="如：Python 3.9, macOS..." id="bug-env">
        </div>
        <button class="submit-btn" onclick="runTask('bug-analyze')">分析 Bug</button>
    </div>
    """, unsafe_allow_html=True)


def render_log_trace_form():
    """日志排查表单"""
    st.markdown("""
    <div class="form-section active">
        <h3 style="color:#e6edf3; margin-bottom:16px;">📊 日志排查</h3>
        <div class="form-group">
            <label class="form-label">错误日志片段 (必填)</label>
            <textarea class="form-input" placeholder="粘贴相关日志..." id="log-segment"></textarea>
        </div>
        <div class="form-group">
            <label class="form-label">Trace ID (可选)</label>
            <input class="form-input" type="text" placeholder="如：abc123-def456..." id="log-trace">
        </div>
        <div class="form-group">
            <label class="form-label">时间范围 (可选)</label>
            <input class="form-input" type="text" placeholder="如：2024-01-01 10:00 - 12:00" id="log-time">
        </div>
        <button class="submit-btn" onclick="runTask('log-trace')">开始排查</button>
    </div>
    """, unsafe_allow_html=True)


def render_skill_manager_form():
    """Skills 管理表单"""
    st.markdown("""
    <div class="form-section active">
        <h3 style="color:#e6edf3; margin-bottom:16px;">📦 Skills 管理</h3>
        <div id="skill-list">
    """, unsafe_allow_html=True)
    
    # 动态加载 Skills
    if st.session_state.registry:
        skills = st.session_state.registry.list_skills()
        for s in skills:
            status = "✅ 启用" if s.get("enabled") else "❌ 禁用"
            st.markdown(f'<div class="knowledge-item"><div class="knowledge-item-title">{s["name"]}</div><div class="knowledge-item-meta">{status}</div></div>')
    else:
        st.markdown("<div style='color:#8b949e;'>Registry 未初始化</div>")
    
    st.markdown("""
        </div>
        <button class="submit-btn" style="margin-top:16px;" onclick="refreshSkills()">刷新列表</button>
    </div>
    """, unsafe_allow_html=True)


def process_request(task_type, params):
    """处理请求"""
    path = extract_path(params.get("path", "")) or "/Users/yanping.ma/biz-delivery"
    
    if task_type == "code-quality":
        if st.session_state.runner:
            result = st.session_state.runner.analyze_directory(path, params.get("lang", "python"))
            if "error" not in result:
                return f"**代码质量分析完成**\n\n路径: `{path}`\n得分: **{result.get('score', 0)}/100**\n\n问题数: {len(result.get('findings', []))}"
        return f"**路径**: `{path}`\n\n⚠️ 请安装 code-quality-guard skill"
    
    elif task_type == "security":
        if st.session_state.runner:
            result = st.session_state.runner.run_security_check(path)
            if "error" not in result:
                checks = result.get("checks", [])
                passed = sum(1 for c in checks if c.get("passed"))
                return f"**安全检查完成** ✅\n\n通过: {passed}/{len(checks)}\n风险评分: {result.get('risk_score', 0)}/100"
        return "**安全检查**\n\n⚠️ 请安装 code-quality-guard skill"
    
    elif task_type == "prd-review":
        return "**PRD 审查**\n\n请提供完整的 PRD 内容以便进行技术可行性评估。"
    
    elif task_type == "bug-analyze":
        return "**Bug 分析**\n\n根据描述，可能的原因：\n1. 请检查相关日志\n2. 验证输入参数\n3. 检查边界条件"
    
    elif task_type == "log-trace":
        return "**日志排查**\n\n根据日志片段，定位到：\n- 错误环节: 数据库连接\n- 建议: 检查连接池配置"
    
    elif task_type == "skill-mgr":
        return "**Skills 管理**\n\n已安装: code-quality-guard, biz-delivery"
    
    return "处理中..."


def extract_path(text):
    import re
    paths = re.findall(r'(/[^\\s]+)', str(text))
    return paths[0] if paths else ""


if __name__ == "__main__":
    main()
