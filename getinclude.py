from playwright.sync_api import Playwright, sync_playwright


def get_all_includes(url):
    """
  使用 Playwright 库获取网站中所有的包含方法以及标签种类和数量

  Args:
    url: 要检查的网站URL

  Returns:
    包含方法字典和标签统计字典
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

        # tag_counts = {}
        # for element in page.query_selector_all("*"):
        #     tag_name = element.tag_name.lower()  # 区分大小写
        #     tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
        # 初始化标签统计字典
        tag_counts = {}
        for element in page.query_selector_all("*"):
            # tag_name = element.tag_name
            tag_name = element.get_attribute("tagName")
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1

        # 获取所有 HTML 元素
        for element in page.query_selector_all("*"):
            all_includes["html"].append(element)

        # 获取所有 js API
        for script in page.query_selector_all("script"):
            if script.inner_text:
                all_includes["js"].append(script.inner_text)

        # 关闭浏览器
        browser.close()
        print(all_includes)
    return all_includes, tag_counts


def save_to_file(all_includes, tag_counts, filename):
    """
  将包含方法字典和标签统计字典保存到文件中

  Args:
    all_includes: 包含方法字典
    tag_counts: 标签统计字典
    filename: 要保存的文件名
  """

    with open(filename, "w", encoding="utf-8") as f:
        for category, includes in all_includes.items():
            f.write(f"### {category}###\n")
            for include in includes:
                f.write(f"{include}\n")

        f.write("\n### 标签统计 ###\n")
        for tag_name, count in tag_counts.items():
            f.write(f"{tag_name}: {count}\n")
            f.write(f"{tag_name}: {count}\n")


# 使用示例
url = "https://baidu.com/"
all_includes, tag_counts = get_all_includes(url)

if all_includes or tag_counts:
    # 将结果保存到文件
    save_to_file(all_includes, tag_counts, "all_includes.txt")
    print("包含方法和标签统计已保存到文件 all_includes.txt")
else:
    print("未发现包含方法或标签")
