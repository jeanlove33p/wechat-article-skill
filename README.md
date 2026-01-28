# WeChat Article Extractor Skill

A Claude Code skill for extracting and converting WeChat public platform articles to Markdown format.

## Overview

This skill enables Claude to automatically extract content from WeChat articles (mp.weixin.qq.com) that are often blocked by verification pages or access restrictions. It uses browser automation to handle anti-scraping mechanisms and converts articles to clean, readable Markdown.

## Features

- 🚀 **Automatic Extraction**: Uses Playwright to automate browser interaction
- 🔓 **Handles Verification**: Detects and waits for manual verification when needed
- 📝 **Markdown Output**: Converts articles to well-formatted Markdown
- 📊 **Complete Metadata**: Extracts title, author, publish time, and full content
- 🎯 **Zero Configuration**: Works out of the box with minimal setup

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Install Dependencies

```bash
# Install Playwright
pip install playwright

# Install browser binaries
playwright install chromium
```

### Install the Skill

1. Download the `wechat-article.skill` file
2. Place it in your Claude Code skills directory:
   - macOS/Linux: `~/.claude/skills/`
   - Windows: `%USERPROFILE%\.claude\skills\`

Or install from source:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/wechat-article-skill.git

# Copy to skills directory
cp -r wechat-article-skill ~/.claude/skills/wechat-article
```

## Usage

### With Claude Code

Simply provide a WeChat article URL to Claude:

```
User: Please read this WeChat article: https://mp.weixin.qq.com/s/xxxxx
```

Claude will automatically:
1. Recognize the WeChat URL
2. Run the extraction script
3. Save the article as Markdown
4. Read and analyze the content
5. Answer your questions about the article

### Standalone Script

You can also use the extraction script directly:

```bash
python3 scripts/extract_article.py <wechat_url> [output.md]
```

**Example:**

```bash
python3 scripts/extract_article.py https://mp.weixin.qq.com/s/U-429WfyRV6nLzStzTsQbg article.md
```

## How It Works

### 1. Browser Automation

The script uses Playwright to:
- Launch a Chromium browser with realistic user agent
- Navigate to the WeChat article URL
- Detect verification pages ("环境异常")
- Wait for manual verification if needed (up to 2 minutes)

### 2. Content Extraction

Once the page loads:
- Extracts article metadata (title, author, publish time)
- Captures the main content from `#js_content` element
- Converts HTML to plain text

### 3. Markdown Conversion

Generates clean Markdown with:
- Article title as H1 heading
- Author and publish time metadata
- Original URL reference
- Full article content

### Output Format

```markdown
# Article Title

**作者**: Author Name

**发布时间**: 2026-01-28

**原文链接**: https://mp.weixin.qq.com/s/xxxxx

---

Article content here...
```

## Handling Verification

WeChat often shows verification pages to prevent scraping. When this happens:

1. The script opens a **visible browser window**
2. You'll see a message: "⚠️ Verification required"
3. Complete the verification challenge in the browser
4. The script automatically continues after verification
5. The browser closes and content is extracted

**Timeout**: 2 minutes for verification (configurable in script)

## Examples

### Example 1: Extract and Save

```bash
python3 scripts/extract_article.py \
  https://mp.weixin.qq.com/s/U-429WfyRV6nLzStzTsQbg \
  output.md
```

**Output:**
```
Loading URL: https://mp.weixin.qq.com/s/U-429WfyRV6nLzStzTsQbg
✅ Article saved to: output.md

============================================================
Title: 刚刚，"港股零食量贩第一股"诞生...
Author: 食品内参
Published: 2026年1月28日 10:08
============================================================
```

### Example 2: Extract Without Saving

```bash
python3 scripts/extract_article.py https://mp.weixin.qq.com/s/xxxxx
```

Prints article metadata and content preview to console.

## Troubleshooting

### Verification Timeout

**Problem**: Script times out waiting for verification

**Solutions**:
- Increase timeout in script (default: 2 minutes)
- Complete verification faster
- Try accessing article in WeChat app first

### Content Not Extracted

**Problem**: Script fails to extract article content

**Solutions**:
- Verify the URL is a valid WeChat article
- Check if article has been deleted
- Try opening URL in regular browser first

### Browser Launch Fails

**Problem**: Playwright cannot launch browser

**Solutions**:
```bash
# Reinstall browser binaries
playwright install chromium

# Check system compatibility
playwright install --help
```

## Limitations

- Requires manual verification for first-time access
- Cannot bypass WeChat's access restrictions completely
- May not work for deleted or private articles
- Requires graphical environment for verification (headed mode)

## Technical Details

### Dependencies

- **playwright**: Browser automation framework
- **Python 3.7+**: Runtime environment

### Script Parameters

```python
extract_wechat_article(
    url: str,              # WeChat article URL
    output_file: str,      # Optional output path
    timeout: int = 30000   # Page load timeout (ms)
)
```

### Return Value

```python
{
    'title': str,           # Article title
    'author': str,          # Author/公众号 name
    'publish_time': str,    # Publication time
    'content_html': str,    # Raw HTML content
    'content_text': str,    # Plain text content
    'markdown': str,        # Formatted Markdown
    'url': str             # Original URL
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/wechat-article-skill.git
cd wechat-article-skill

# Install dependencies
pip install playwright
playwright install chromium

# Run tests
python3 scripts/extract_article.py https://mp.weixin.qq.com/s/test-url
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for [Claude Code](https://github.com/anthropics/claude-code)
- Uses [Playwright](https://playwright.dev/) for browser automation
- Inspired by the need to access WeChat articles programmatically

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Open an [Issue](https://github.com/YOUR_USERNAME/wechat-article-skill/issues)
3. Contribute improvements via Pull Requests

## Changelog

### v1.0.0 (2026-01-28)

- Initial release
- Basic article extraction functionality
- Verification page handling
- Markdown conversion
- Standalone script support

---

**Made with ❤️ for the Claude Code community**
