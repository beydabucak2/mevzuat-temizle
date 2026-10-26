import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

url = os.environ.get("URL")
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
satirlar = soup.find_all("div", class_="mv-satir")

bugun = datetime.now().strftime("%d.%m.%Y")
bulten_metni = f"Tarih: {bugun}\n\n"
kayit_sayisi = 0

for satir in satirlar:
    baslik_el = satir.find(class_="mv-baslik")
    tarih_el = satir.find(class_="mv-tarih")
    etiket_el = satir.find(class_="tur-badge")
    
    if baslik_el:
        ilan_tarihi = tarih_el.text.strip() if tarih_el else ""
        
        if ilan_tarihi == bugun:
            kategori = etiket_el.text.strip() if etiket_el else "Genel"
            baslik = baslik_el.text.strip()
            link = baslik_el.find("a")["href"] if baslik_el.find("a") else ""
            
            bulten_metni += f"Kategori: {kategori}\nBaşlık: {baslik}\nLink: {link}\n\n"
            kayit_sayisi += 1

if kayit_sayisi == 0:
    bulten_metni += "Bugüne ait yeni mevzuat bulunamadı."

with open("mevzuat.txt", "w", encoding="utf-8") as f:
    f.write(bulten_metni)
