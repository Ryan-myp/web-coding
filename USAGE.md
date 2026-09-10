# web-coding 使用指南

## 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 Web UI
streamlit run web/app.py
```

## 使用方式

### 方式一: Web UI

1. 打开 http://localhost:8501
2. 点击左侧菜单:
   - **🏠 仪表盘**: 查看已安装的 Skills
   - **📦 技能管理**: 安装/卸载 Skills
   - **🛡️ 代码质量**: 代码分析 (code-quality-guard)
   - **⚙️ 系统设置**: 配置路径

### 方式二: 命令行

```bash
# 安装 Skill
python3 scripts/skill_registry.py install /path/to/skill

# 列出已安装的 Skills
python3 scripts/skill_registry.py list

# 搜索 Skills
python3 scripts/skill_registry.py search "quality"
```

## 支持的 Skills

| Skill | 功能 | 说明 |
|-------|------|------|
| **code-quality-guard** | 代码质量检查 | OWASP 安全 + 多语言 AST 分析 |
| **biz-delivery** | 业务交付 | PRD → Test Case 全流程 |

## 扩展新 Skill

1. 在 `~/.agents/skills/` 创建 Skill 目录
2. 添加 `SKILL.md` 文件
3. 在 Web UI 中点击"安装 Skill"并填入路径

## 示例: 安装 code-quality-guard

```bash
# 从 GitHub 克隆
git clone https://github.com/Ryan-myp/coding.git ~/.agents/skills/code-quality-guard

# 在 Web UI 中安装
python3 scripts/skill_registry.py install ~/.agents/skills/code-quality-guard
```
