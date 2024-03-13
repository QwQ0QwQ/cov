from selenium import webdriver

def get_all_includes(url):
  """
  使用Selenium库获取网站中所有的包含方法

  Args:
    url: 要检查的网站URL

  Returns:
    包含方法列表
  """

  driver = webdriver.Chrome()
  driver.get(url)

  # 获取所有HTML元素
  all_includes = []
  for element in driver.find_elements_by_xpath("//*"):
    all_includes.append(element)

  # 获取所有js API
  for script in driver.find_elements_by_tag_name("script"):
    if script.text:
      all_includes.append(script.text)

  driver.quit()

  return all_includes

def classify_results(results):
  """
  将结果分类

  Args:
    results: 要分类的结果

  Returns:
    分类后的结果
  """

  classified_results = {}

  # 按类型分类
  for result in results:
    if result.type in classified_results:
      classified_results[result.type].append(result)
    else:
      classified_results[result.type] = [result]

  # 按风险级别分类
  for result_type, results in classified_results.items():
    for result in results:
      if result.risk_level in classified_results:
        classified_results[result.risk_level].append(result)
      else:
        classified_results[result.risk_level] = [result]

  # 按影响范围分类
  for result_type, results in classified_results.items():
    for result in results:
      if result.impact_scope in classified_results:
        classified_results[result.impact_scope].append(result)
      else:
        classified_results[result.impact_scope] = [result]

  return classified_results

# 使用示例
url = "https://baidu.com/"
all_includes = get_all_includes(url)

if all_includes:
  # 将结果分类
  classified_results = classify_results(all_includes)

  # 输出结果
  for result_type, results in classified_results.items():
    print(f"{result_type}:")
    for result in results:
      print(f"  {result}")
else:
  print("未发现包含方法")

