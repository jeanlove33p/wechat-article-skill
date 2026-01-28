#!/usr/bin/env python3
"""
Extract WeChat article content using Playwright.
Handles verification pages and extracts article title, author, and content.
"""

import sys
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

def extract_wechat_article(url, output_file=None, timeout=30000):
    """
    Extract article content from WeChat public platform URL.

    Args:
        url: WeChat article URL (mp.weixin.qq.com)
        output_file: Optional path to save markdown output
        timeout: Page load timeout in milliseconds

    Returns:
        dict with keys: title, author, content, publish_time
    """
    with sync_playwright() as p:
        # Launch browser with realistic settings
        browser = p.chromium.launch(
            headless=False,  # Use headed mode to handle verification
            args=['--disable-blink-features=AutomationControlled']
        )

        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        page = context.new_page()

        try:
            print(f"Loading URL: {url}")
            page.goto(url, wait_until='networkidle', timeout=timeout)

            # Check for verification page
            if page.locator('text=环境异常').count() > 0 or page.locator('text=去验证').count() > 0:
                print("\n⚠️  Verification required. Please complete the verification in the browser window.")
                print("Waiting for verification to complete...")

                # Wait for article content to appear (max 2 minutes)
                page.wait_for_selector('#js_content', timeout=120000)
                print("✅ Verification completed!")

            # Extract article metadata
            title = page.locator('#activity-name').inner_text() if page.locator('#activity-name').count() > 0 else "Untitled"
            author = page.locator('#js_name').inner_text() if page.locator('#js_name').count() > 0 else "Unknown"

            # Try to get publish time
            publish_time = ""
            if page.locator('#publish_time').count() > 0:
                publish_time = page.locator('#publish_time').inner_text()

            # Extract main content
            content_element = page.locator('#js_content')
            if content_element.count() == 0:
                raise Exception("Article content not found. The page might not be loaded correctly.")

            # Get HTML content
            content_html = content_element.inner_html()

            # Get plain text as fallback
            content_text = content_element.inner_text()

            result = {
                'title': title.strip(),
                'author': author.strip(),
                'publish_time': publish_time.strip(),
                'content_html': content_html,
                'content_text': content_text,
                'url': url
            }

            # Convert to markdown format
            markdown = f"# {result['title']}\n\n"
            markdown += f"**作者**: {result['author']}\n\n"
            if result['publish_time']:
                markdown += f"**发布时间**: {result['publish_time']}\n\n"
            markdown += f"**原文链接**: {result['url']}\n\n"
            markdown += "---\n\n"
            markdown += result['content_text']

            result['markdown'] = markdown

            # Save to file if specified
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                print(f"\n✅ Article saved to: {output_file}")

            return result

        except PlaywrightTimeout:
            print("\n❌ Timeout: Page took too long to load or verification was not completed.")
            return None
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None
        finally:
            browser.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_article.py <wechat_url> [output_file.md]")
        print("\nExample:")
        print("  python3 extract_article.py https://mp.weixin.qq.com/s/xxxxx article.md")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not url.startswith('https://mp.weixin.qq.com/'):
        print("❌ Error: URL must be a WeChat article (mp.weixin.qq.com)")
        sys.exit(1)

    result = extract_wechat_article(url, output_file)

    if result:
        print("\n" + "="*60)
        print(f"Title: {result['title']}")
        print(f"Author: {result['author']}")
        if result['publish_time']:
            print(f"Published: {result['publish_time']}")
        print("="*60)

        if not output_file:
            print("\nContent preview:")
            print(result['content_text'][:500] + "..." if len(result['content_text']) > 500 else result['content_text'])
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
