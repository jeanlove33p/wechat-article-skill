#!/bin/bash

# WeChat Article Skill - One-Click Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/jeanlove33p/wechat-article-skill/main/install.sh | bash

set -e

echo "🚀 Installing WeChat Article Extractor Skill..."

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    SKILLS_DIR="$HOME/.claude/skills"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SKILLS_DIR="$HOME/.claude/skills"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

# Create skills directory if not exists
mkdir -p "$SKILLS_DIR"

# Download skill file
echo "📥 Downloading skill file..."
curl -L -o "$SKILLS_DIR/wechat-article.skill" \
    https://github.com/jeanlove33p/wechat-article-skill/raw/main/wechat-article.skill

echo "✅ Skill file installed to: $SKILLS_DIR/wechat-article.skill"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 3 not found. Please install Python 3.7+ first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install --break-system-packages playwright 2>/dev/null || pip3 install playwright
    playwright install chromium
else
    echo "⚠️  pip3 not found. Please install manually:"
    echo "   pip3 install playwright"
    echo "   playwright install chromium"
    exit 1
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📖 Usage:"
echo "   Just send a WeChat article URL to Claude:"
echo "   https://mp.weixin.qq.com/s/xxxxx"
echo ""
echo "🔗 Documentation: https://github.com/jeanlove33p/wechat-article-skill"
