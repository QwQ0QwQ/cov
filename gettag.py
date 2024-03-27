import requests as requests
from bs4 import BeautifulSoup

url = 'https://baidu.com/'
response = requests.get(url)
html_doc = response.text
# print(html_doc)

soup = BeautifulSoup(html_doc, 'html.parser')
tags = soup.find_all()



tag_counts = {}
for tag in tags:
    print(tag)
    tag_name = tag.name
    tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1

for tag_name, count in tag_counts.items():
    print(tag_name, count)
