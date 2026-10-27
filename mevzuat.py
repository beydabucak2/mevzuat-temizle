import json
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

URL = os.environ.get("URL")
if not URL:
    sys.exit("HATA: URL ortam değişkeni tanımlı değil")

HEADERS = {"User-Agent": "MevzuatBulteni/1.0 (iletisim: SENIN_MAIL_ADRESIN)"}
CIKTI_DOSYASI = "mevzuat.json"
GORULENLER_DOSYASI = "gorulenler.json"
GORULENLER_LIMIT = 3000
TR_SAAT = ZoneInfo("Europe/Istanbul")

ATLANACAK_KATEGORILER = {"ilan"}
ATLANACAK_ANAHTARLAR = [
    "üniversitesi",
    "atamalar hakkında",
    "acele kamulaştırılması",
    "özelleştirme idaresi",
    "enerji piyasası düzenleme kurulunun",
]


def tr_lower(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()


def temizle(metin):
    return " ".join(metin.split())  


def atlanmali_mi(kategori, baslik):
    if tr_lower(kategori) in ATLANACAK_KATEGORILER:
        return True
    kucuk = tr_lower(baslik)
    return any(anahtar in kucuk for anahtar in ATLANACAK_ANAHTARLAR)


response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
satirlar = soup.find_all("div", class_="mv-satir")
if not satirlar:
    sys.exit("HATA: Sayfada kayıt bulunamadı, sayfa yapısı değişmiş olabilir")

if os.path.exists(GORULENLER_DOSYASI):
    with open(GORULENLER_DOSYASI, encoding="utf-8") as f:
        gorulenler = json.load(f)
else:
    gorulenler = []
gorulen_kumesi = set(gorulenler)

kayitlar = []
for satir in satirlar:
    baslik_el = satir.find(class_="mv-baslik")
    if not baslik_el:
        continue

    link_el = baslik_el.find("a")
    link = link_el["href"] if link_el and link_el.has_attr("href") else ""
    baslik = temizle(baslik_el.get_text())

    tarih_el = satir.find(class_="mv-tarih")
    etiket_el = satir.find(class_="tur-badge")
    tarih = temizle(tarih_el.get_text()) if tarih_el else ""
    kategori = temizle(etiket_el.get_text()) if etiket_el else "genel"

    anahtar = tr_lower(baslik)
    if anahtar in gorulen_kumesi:
        continue  # daha önce görüldü
    gorulenler.append(anahtar)
    gorulen_kumesi.add(anahtar)

    if atlanmali_mi(kategori, baslik):
        continue

    kayitlar.append(
        {"kategori": kategori, "baslik": baslik, "link": link, "tarih": tarih}
    )

simdi = datetime.now(TR_SAAT)
cikti = {
    "bulten_tarihi": simdi.strftime("%d.%m.%Y"),
    "uretim_zamani": simdi.isoformat(timespec="seconds"),
    "taranan_satir_sayisi": len(satirlar),
    "kayit_sayisi": len(kayitlar),
    "kayitlar": kayitlar,
}

with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
    json.dump(cikti, f, ensure_ascii=False, indent=2)

with open(GORULENLER_DOSYASI, "w", encoding="utf-8") as f:
    json.dump(gorulenler[-GORULENLER_LIMIT:], f, ensure_ascii=False)

print(f"Taranan: {len(satirlar)}, bültene giren yeni kayıt: {len(kayitlar)}")
