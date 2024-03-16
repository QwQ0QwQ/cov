from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service


# chromedriver 路径配置
driver_path = Service(r'.\chromedriver\chromedriver.exe')


# ChromeOptions 配置相关
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')


driver = webdriver.Chrome(options=options, service=driver_path)

base_url = "https://www.ximalaya.com/sound/148249100"

driver.get(base_url)

album_info = None
pay_info = None

for request in driver.requests:
    if request.response:
        # print("request.url", request.url)
        if "/bdsp/album/pay" in request.url:
            # print(request.response.body)
            pay_info = gzip.decompress(request.response.body).decode('utf-8')
            try:
                pay_info = json.loads(pay_info)
                logger.info("转json 成功，结果{}".format(pay_info))
            except Exception as e:
                logger.info("转json 失败，结果{}".format(pay_info))
                logger.error("异常信息：", e)

        if "/bdsp/album/info" in request.url:
            # print(request.response.body)
            album_info = gzip.decompress(request.response.body).decode('utf-8')
            try:
                album_info = json.loads(album_info)
                logger.info("转json 成功，结果{}".format(album_info))
            except Exception as e:
                logger.info("转json 失败，结果{}".format(album_info))
                logger.error("异常信息：", e)

logger.info("seleniumwire_network，for 循环完了，结果：专辑信息：{}, 支付信息：{}".format(album_info, pay_info))

driver.quit()
