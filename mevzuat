import os
import requests
from bs4 import BeautifulSoup

def mevzuat_cek_ve_gonder():
    print("Mevzuat verileri çekiliyor...")
    
    url = os.environ.get("URL")
    if not url:
        print("Hata: Hedef URL bulunamadı!")
        return
        
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        cevap = requests.get(url, headers=headers)
        cevap.raise_for_status()
    except Exception as e:
        print(f"Sayfaya erişilemedi: {e}")
        return

    soup = BeautifulSoup(cevap.text, 'html.parser')
    satirlar = soup.find_all('div', class_='mv-satir')
    
    sonuclar = []
    for satir in satirlar:
        kategori_badge = satir.find('span', class_='tur-badge')
        kategori = kategori_badge.text.strip() if kategori_badge else "Bilinmiyor"
        
        baslik_div = satir.find('div', class_='mv-baslik')
        if baslik_div and baslik_div.find('a'):
            baslik = baslik_div.find('a').text.strip()
            link = baslik_div.find('a')['href']
            if not link.startswith("http"):
                link = "https://mevzuatlar.com.tr/" + link.lstrip("/")
        else:
            baslik = "Başlık Yok"
            link = ""
            
        tarih_div = satir.find('div', class_='mv-tarih')
        tarih = tarih_div.text.strip() if tarih_div else "Tarih Yok"
        
        sonuclar.append({
            "kategori": kategori,
            "baslik": baslik,
            "link": link,
            "tarih": tarih
        })
        
    print(f"Toplam {len(sonuclar)} adet kayıt bulundu.")
    
    webhook_url = os.environ.get("WEBHOOK_URL")
    if not webhook_url:
        print("Hata: Webhook URL bulunamadı!")
        return
    
    payload = {
        "gunluk_kayit_sayisi": len(sonuclar),
        "mevzuatlar": sonuclar
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        print(f"Webhook tetiklendi. Durum kodu: {response.status_code}")
    except Exception as e:
        print(f"Webhook gönderim hatası: {e}")

if __name__ == "__main__":
    mevzuat_cek_ve_gonder()
