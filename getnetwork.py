import asyncio
from playwright.async_api import async_playwright, Playwright
import re
import os
from collections import OrderedDict, defaultdict

requests = []
responses = defaultdict(list)

def extract_url(text_array):
  """
  从文本数组中提取 URL。

  Args:
    text_array: 文本数组。

  Returns:
    URL 列表。
  """
  urls = []
  for text in text_array:
    urls.extend(re.findall(r"(?<![\w])((http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)", text))
  return urls

async def run(playwright: Playwright, url: str):
    chromium = playwright.chromium
    browser = await chromium.launch()
    page = await browser.new_page()
    urls=[]
    requests = []
    responses = defaultdict(list)
    async def handle_request(request):
        request_data = {
            "method": request.method,
            "url": request.url
        }
        urls.append(request.url)
        requests.append(request_data)
    async def handle_response(response):
        response_data = {
            "status": response.status,
            "url": response.url
        }
        urls.append(response.url)
        responses[response.status].append(response_data)

    # 订阅请求和响应事件，并调用相应的处理函数
    page.on("request", handle_request)
    page.on("response", handle_response)

    await page.goto(url)  # Use the url parameter here
    await browser.close()
    results=extract_url(urls)
    # print(results)
    domain=set()
    file=set()
    pattern = r".*\..*"
    # 使用 OrderedDict 保证写入文件时顺序不变
    file_dict = OrderedDict()
    for url in results:
        domain.add(url[2]) # Modify index if URL is at a different position
        if bool(re.match(pattern,url[0])):
            file.add(url[0])
    domain = list(domain)
    file = list(file)
    print(domain)
    print(file)

async def main():
    async with async_playwright() as playwright:
        target_url = "https://baidu.com"  # Replace with your desired URL
        await run(playwright, target_url)

asyncio.run(main())

