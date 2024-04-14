import requests
from bs4 import BeautifulSoup


def scrape_tags(url):
    """Fetches the HTML content from the given URL, parses it with BeautifulSoup,
    and counts the occurrences of all HTML tags."""

    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    tags = soup.find_all()

    tag_counts = {}
    for tag in tags:
        tag_name = tag.name
        tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1

    for tag_name, count in tag_counts.items():
        print(tag_name, count)


# Example usage
target_url = 'https://www.example.com'  # Replace with the actual URL
scrape_tags(target_url)
