import os
import requests
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_image(url, count):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)

        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print("⚠️ Görsel değil:", url)
            return 0

        os.makedirs("data", exist_ok=True)
        ext = content_type.split("/")[-1]  # image/jpeg → jpeg
        filename = os.path.join("data", f"img_{count}.{ext}")
        with open(filename, "wb") as f:
            f.write(response.content)

        print("✅ Kaydedildi:", filename)
        return 1

    except Exception as e:
        print("❌ Hata:", url, e)
        return 0
