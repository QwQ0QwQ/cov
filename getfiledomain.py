import re
import os
from collections import OrderedDict

def extract_url(file_path):
  """
  从文件中提取 URL。

  Args:
    file_path: 文件路径。

  Returns:
    URL 列表。
  """
  with open(file_path, "r") as f:
    text = f.read()
  return re.findall(r"(?<![\w])((http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)", text)

def save_url(url_list, file_path):
  """
  将 URL 列表保存到文件。

  Args:
    url_list: URL 列表。
    file_path: 文件路径。

  Returns:
    None。
  """
  with open(file_path, "w") as f:
    for url in url_list:
      f.write(url + "\n")

def main():
  """
  主函数。
  """
  # 读取文件路径
  file_path = input("请输入文件路径：")

  # 提取 URL
  url_list = extract_url(file_path)

  # 分类保存 URL
  file_name, ext = os.path.splitext(file_path)
  # 使用 OrderedDict 保证写入文件时顺序不变
  file_dict = OrderedDict()
  for url in url_list:
    # Extract URL string from the tuple (assuming it's the first element)
    url_str = url[2]  # Modify index if URL is at a different position
    if not "." in url_str:
      continue
    file_dict.setdefault(url_str, []).append(url[3])

  with open(f"{file_name}_files.txt", "w") as f:
    for url, paths in file_dict.items():
      f.write(f"{url}\n")
      for path in paths:
        f.write(f"\t{path}\n")

if __name__ == "__main__":
  main()
