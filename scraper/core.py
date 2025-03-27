from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from scraper.helpers import download_image

def start_scraping(url, data_type):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    count = 0

    if data_type == "images":
        images = soup.find_all("img")
        bg_tags = soup.find_all(style=lambda s: s and 'background-image' in s)

        for img in images:
            src = img.get("src") or img.get("data-src")
            if not src:
                continue
            full_url = urljoin(url, src)
            count += download_image(full_url, count)

        for tag in bg_tags:
            style = tag.get("style")
            start = style.find("url(")
            end = style.find(")", start)
            if start != -1 and end != -1:
                bg_url = style[start + 4:end].strip('\'"')
                full_url = urljoin(url, bg_url)
                count += download_image(full_url, count)

        return count

    elif data_type == "titles":
        titles = [tag.text.strip() for tag in soup.find_all(["h1", "h2", "h3"])]
        with open("data/titles.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(titles))
        return len(titles)

    elif data_type == "links":
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        with open("data/links.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(links))
        return len(links)

    else:
        raise ValueError("Bilinmeyen veri türü")
