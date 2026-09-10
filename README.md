# web-coding - Skills Integration Platform

基于 Streamlit 的 Skills 集成平台，支持多 Skills 管理、安装、运行。

## 架构

```
web-coding/
├── web/                    # Web UI
│   ├── app.py             # 主应用
│   └── components/        # UI 组件
├── scripts/               # 核心模块
│   ├── skill_registry.py  # Skills 注册表
│   └── skill_runner.py    # Skills 执行器
├── skills/                # 本地 Skills 目录
└── .web-coding/           # 运行时数据
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 Web UI
streamlit run web/app.py

# 安装 Skill
python3 scripts/skill_registry.py install /path/to/skill
```

## 支持的 Skills

- **code-quality-guard**: 代码质量检查 (v7.11)
- **biz-delivery**: 业务交付流程 (PRD → Test Case)
- 更多 Skills 即将支持...

## 扩展新的 Skill

1. 将 Skill 放入 `~/.agents/skills/` 或指定路径
2. 在 Web UI 中点击"安装 Skill"
3. 或通过命令行: `python3 scripts/skill_registry.py install /path/to/skill`
