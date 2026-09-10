#!/bin/bash
# web-coding Skills 安装脚本

set -e

echo "🔧 web-coding Skills 安装器"
echo "=========================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python3"
    exit 1
fi

# 创建配置目录
CONFIG_DIR="$HOME/.web-coding"
mkdir -p "$CONFIG_DIR"
mkdir -p "$HOME/.agents/skills"

echo "📦 正在安装默认 Skills..."
echo ""

# 克隆 coding repo (包含 code-quality-guard)
CODING_REPO="$CONFIG_DIR/repos/coding"
if [ ! -d "$CODING_REPO/.git" ]; then
    echo "📥 克隆 coding repo..."
    git clone https://github.com/Ryan-myp/coding.git "$CODING_REPO" 2>/dev/null || {
        echo "⚠️ 克隆失败，请检查网络连接"
        exit 1
    }
else
    echo "✅ coding repo 已存在"
fi

# 复制 code-quality-guard
CODE_QUALITY_PATH="$HOME/.agents/skills/code-quality-guard"
if [ ! -d "$CODE_QUALITY_PATH" ]; then
    echo "📦 安装 code-quality-guard..."
    cp -r "$CODING_REPO/.agents/skills/code-quality-guard" "$CODE_QUALITY_PATH"
    echo "✅ code-quality-guard 已安装"
else
    echo "✅ code-quality-guard 已存在"
fi

# 复制 biz-delivery
BIZ_DELIVERY_PATH="$HOME/.agents/skills/biz-delivery"
if [ ! -d "$BIZ_DELIVERY_PATH" ]; then
    echo "📦 安装 biz-delivery..."
    cp -r "$CODING_REPO" "$BIZ_DELIVERY_PATH"
    echo "✅ biz-delivery 已安装"
else
    echo "✅ biz-delivery 已存在"
fi

echo ""
echo "✅ Skills 安装完成!"
echo ""
echo "📁 已安装 Skills:"
echo "   - code-quality-guard ($CODE_QUALITY_PATH)"
echo "   - biz-delivery ($BIZ_DELIVERY_PATH)"
echo ""
echo "🚀 启动 web-coding:"
echo "   cd /tmp/web-coding"
echo "   streamlit run web/app.py"
