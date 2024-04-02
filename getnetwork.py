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
    req=[]
    async def handle_request(request):
        request_data = {
            "method": request.method,
            "url": request.url
        }
        urls.append(request.url)
        requests.append(request_data)
        print(request)
        req.append(request)
    async def handle_response(response):
        response_data = {
            "status": response.status,
            "url": response.url
        }
        urls.append(response.url)
        responses[response.status].append(response_data)

    page.on("dialog", lambda dialog: print(dialog.message))
    await page.get_by_role("button").click()  # Will hang here
    # Double click
    await page.get_by_text("Item").dblclick()
    # Right click
    await page.get_by_text("Item").click(button="right")
    # Shift + click
    await page.get_by_text("Item").click(modifiers=["Shift"])
    # Hover over element
    await page.get_by_text("Item").hover()
    # Hit Enter
    await page.get_by_text("Submit").press("Enter")

    # Dispatch Control+Right
    await page.get_by_role("textbox").press("Control+ArrowRight")

    # Press $ sign on keyboard
    await page.get_by_role("textbox").press("$")
    # Click the top left corner
    await page.get_by_text("Item").click(position={"x": 0, "y": 0})
    await page.locator("#item-to-be-dragged").hover()
    await page.mouse.down()
    await page.locator("#item-to-drop-at").hover()
    await page.mouse.up()
    # 订阅请求和响应事件，并调用相应的处理函数
    page.on("request", handle_request)
    page.on("response", handle_response)
    print("----------requests-----------")
    print(req)
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

