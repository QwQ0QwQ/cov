from playwright.sync_api import Playwright, sync_playwright

def get_all_includes(url):
  """
  使用 Playwright 库获取网站中所有的包含方法

  Args:
    url: 要检查的网站URL

  Returns:
    包含方法列表
  """

  # 创建 Playwright 实例
  with sync_playwright() as p:
    # 创建浏览器实例
    browser = p.chromium.launch(headless=False)

    # 创建页面实例
    page = browser.new_page()

    # 导航到目标页面
    page.goto(url, wait_until="networkidle")

    # 获取所有 HTML 元素
    all_includes = []
    for element in page.query_selector_all("*"):
      all_includes.append(element)

    # 获取所有 js API
    for script in page.query_selector_all("script"):
      if script.inner_text:
        all_includes.append(script.inner_text)

    # 关闭浏览器
    browser.close()

  return all_includes

# 使用示例
url = "https://baidu.com/"
all_includes = get_all_includes(url)

if all_includes:
  # 输出结果
  for include in all_includes:
    print(include)
else:
  print("未发现包含方法")
