# scraper.py

import os  # Dosya işlemleri için (klasör oluşturma, dosya kaydetme)
import requests  # Web'den veri çekmek için
from bs4 import BeautifulSoup  # HTML içeriğini parse (inceleme) etmek için
from urllib.parse import urljoin  # Göreli URL'leri tam URL'ye çevirmek için kullanılır

# 💡 Bu fonksiyon, bir URL'den belirli bir veri tipini (görsel, başlık, link) kazımak için kullanılır
def start_scraping(url, data_type):
    response = requests.get(url)  # Web sayfasını indirir
    soup = BeautifulSoup(response.text, "html.parser")  # HTML'yi analiz edilebilir hale getirir

    os.makedirs("data", exist_ok=True)  # 💡 Bu klasör yoksa oluşturur, varsa hata vermez (sık kullanılan güvenli yöntemdir)

    # Kullanıcının seçtiği veri türüne göre işlem yapılır
    if data_type == "images":
        count = 0

        # Tüm <img> taglerini bulur
        images = soup.find_all("img")

        # Ayrıca CSS içinde background-image geçen tagleri de bulur
        bg_tags = soup.find_all(style=lambda s: s and 'background-image' in s)

        # --- 1. Gerçek <img> tag'lerinden gelen görseller
        for img in images:
            # Bazı sitelerde 'src' yerine 'data-src' kullanılır (lazy loading)
            src = img.get("src") or img.get("data-src")
            if not src:
                continue
            full_url = urljoin(url, src)  # 💡 Göreli URL'yi tam URL'ye dönüştürür
            count += download_image(full_url, count)

        # --- 2. CSS içindeki background-image: url(...) şeklinde gelen görseller
        for tag in bg_tags:
            style = tag.get("style")
            start = style.find("url(")
            end = style.find(")", start)
            if start != -1 and end != -1:
                bg_url = style[start + 4:end].strip('\'"')  # Parantez ve tırnaklardan arındır
                full_url = urljoin(url, bg_url)
                count += download_image(full_url, count)

        return count

    elif data_type == "titles":
        # <h1>, <h2>, <h3> gibi başlık tag'lerini seçer
        titles = [tag.text.strip() for tag in soup.find_all(["h1", "h2", "h3"])]
        with open("data/titles.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(titles))  # Tüm başlıkları tek dosyaya yaz
        return len(titles)

    elif data_type == "links":
        # Tüm <a href="..."> linklerini bul
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        with open("data/links.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(links))  # Linkleri dosyaya yaz
        return len(links)

    else:
        raise ValueError("Bilinmeyen veri türü")  # 💡 Güvenlik için: Tanımsız veri türü verilirse hata fırlatır

# 💡 Bu fonksiyon tek bir görseli indirip 'data/' klasörüne kaydeder
def download_image(url, count):
    try:
        img_data = requests.get(url).content
        filename = os.path.join("data", f"img_{count}.jpg")
        with open(filename, "wb") as f:
            f.write(img_data)
        return 1  # Başarılı indirme
    except:
        return 0  # Hata olursa pas geç
