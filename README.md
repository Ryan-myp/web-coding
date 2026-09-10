# web-coding - Skills Integration Platform

基于 Streamlit 的 Skills 集成平台，支持多 Skills 管理、安装、运行。

## 📦 已集成的 Skills

| Skill | 功能 | 说明 |
|-------|------|------|
| **code-quality-guard** | 代码质量检查 | OWASP 安全 + 多语言 AST 分析 |
| **biz-delivery** | 业务交付 | PRD → Test Case 全流程 |

## 🚀 快速开始

### 方式一: 一键安装

```bash
# 安装所有默认 Skills
./install_skills.sh

# 启动 Web UI
cd /tmp/web-coding
streamlit run web/app.py
```

### 方式二: 手动安装

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 Web UI
streamlit run web/app.py

# 在 Web UI 中点击"技能管理"安装 Skills
```

## 📁 项目结构

```
web-coding/
├── web/                    # Web UI
│   ├── app.py             # 主应用
│   └── components/        # UI 组件
│       ├── skill_manager.py      # Skills 管理
│       ├── skill_dashboard.py    # Skills 仪表盘
│       └── code_quality_panel.py # 代码质量面板
├── scripts/               # 核心模块
│   ├── skill_registry.py  # Skills 注册表
│   ├── skill_runner.py    # Skills 执行器
│   └── auto_install.py    # 自动安装
├── skills/                # 本地 Skills 目录
└── install_skills.sh      # 一键安装脚本
```

## 🔧 使用方式

### Web UI

1. 启动: `streamlit run web/app.py`
2. 访问: http://localhost:8501
3. 功能:
   - 🏠 仪表盘: 查看已安装的 Skills
   - 📦 技能管理: 安装/卸载 Skills
   - 🛡️ 代码质量: 代码分析 (code-quality-guard)
   - ⚙️ 系统设置: 配置路径

### 命令行

```bash
# 列出已安装的 Skills
python3 scripts/skill_registry.py list

# 安装 Skill
python3 scripts/skill_registry.py install /path/to/skill

# 自动安装默认 Skills
python3 scripts/auto_install.py default
```

## 📚 文档

- [USAGE.md](USAGE.md) - 详细使用指南
- [GitHub](https://github.com/Ryan-myp/web-coding)

## 🔗 相关项目

- [coding](https://github.com/Ryan-myp/coding) - code-quality-guard & biz-delivery 源码
- [biz-delivery](https://github.com/Ryan-myp/biz-delivery) - 独立部署版本
