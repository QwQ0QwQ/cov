from playwright.sync_api import Playwright, sync_playwright

def get_all_includes(url):
  """
  使用 Playwright 库获取网站中所有的包含方法

  Args:
    url: 要检查的网站URL

  Returns:
    包含方法字典
  """

  # 创建 Playwright 实例
  with sync_playwright() as p:
    # 创建浏览器实例
    browser = p.chromium.launch(headless=False)

    # 创建页面实例
    page = browser.new_page()

    # 导航到目标页面
    page.goto(url, wait_until="networkidle")

    # 初始化包含方法字典
    all_includes = {
      "html": [],
      "js": [],
    }

    
    # 获取所有 HTML 元素
    for element in page.query_selector_all("*"):
      all_includes["html"].append(element)

    # 获取所有 js API
    for script in page.query_selector_all("script"):
      if script.inner_text:
        all_includes["js"].append(script.inner_text)
    # 关闭浏览器
    browser.close()

  return all_includes

def save_to_file(all_includes, filename):
  """
  将包含方法字典保存到文件中

  Args:
    all_includes: 包含方法字典
    filename: 要保存的文件名
  """

  with open(filename, "w", encoding="utf-8") as f:
    for category, includes in all_includes.items():
      f.write(f"### {category}\n")
      for include in includes:
        f.write(f"{include}\n")

# 使用示例
url = "https://baidu.com/"
all_includes = get_all_includes(url)

if all_includes:
  # 将结果保存到文件
  save_to_file(all_includes, "all_includes.txt")
  print("包含方法已保存到文件 all_includes.txt")
else:
  print("未发现包含方法")
