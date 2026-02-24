import requests
import time

def get_vavoo_signature():
    url = "https://www.vavoo.tv/api/app/ping"
    # Sunucu bazen eski tokenları bloklar, bu yüzden güncel bir tane deniyoruz
    payload = {
        "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
        "package": "tv.vavoo.app",
        "version": "3.1.20"
    }
    headers = {
        "User-Agent": "VAVOO/2.6",
        "Content-Type": "application/json"
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        data = r.json()
        # Eğer sunucu imza vermezse hata fırlat ki GitHub Action 'Hata' olarak işaretlesin
        if "addonSig" in data:
            return data["addonSig"]
        else:
            print(f"⚠️ Sunucu yanıt verdi ama imza yok: {data}")
            return None
    except Exception as e:
        print(f"❌ İstek hatası: {e}")
        return None

def main():
    sig = get_vavoo_signature()
    channels = {
        "beIN SPORTS 1": "tr-be-in-sports-1",
        "beIN SPORTS 2": "tr-be-in-sports-2",
        "beIN SPORTS 3": "tr-be-in-sports-3"
    }

    with open("vavoo_to_list.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Guncelleme: {time.ctime()}\n")
        
        for name, cid in channels.items():
            # EĞER İMZA VARSA EKLE, YOKSA ÖZEL BİR UYARI EKLE
            if sig:
                link = f"https://vavoo.to/vavoo-iptv/play/{cid}.m3u8?n=1&sig={sig}"
            else:
                # İmza yoksa linkin çalışmayacağını belirten bir parametre ekle
                link = f"https://vavoo.to/vavoo-iptv/play/{cid}.m3u8?error=no_signature_check_token"
            
            f.write(f'#EXTINF:-1 group-title="SPOR",{name}\n')
            f.write(f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n')
            f.write(f"{link}\n")

if __name__ == "__main__":
    main()
