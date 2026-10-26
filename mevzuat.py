import requests
from bs4 import BeautifulSoup
import json
import os

url = os.environ.get("URL")
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
satirlar = soup.find_all("div", class_="mv-satir")

mevzuatlar = []

for satir in satirlar:
    baslik_el = satir.find(class_="mv-baslik")
    tarih_el = satir.find(class_="mv-tarih")
    etiket_el = satir.find(class_="tur-badge")
    
    if baslik_el:
        mevzuatlar.append({
            "kategori": etiket_el.text.strip() if etiket_el else "Genel",
            "baslik": baslik_el.text.strip(),
            "link": baslik_el.find("a")["href"] if baslik_el.find("a") else "",
            "tarih": tarih_el.text.strip() if tarih_el else ""
        })

with open("mevzuat.json", "w", encoding="utf-8") as f:
    json.dump(mevzuatlar, f, ensure_ascii=False, indent=2)
