import requests
import time

# Yeni paylaştığın domain bilgileri
DOMAINS = {
    "vavoo": "vavoo.to",
    "vixsrc": "vixsrc.to",
    "animesaturn": "animesaturn.cx",
    "animeunity": "animeunity.so"
}

def get_vavoo_to_signature():
    # Vavoo.to üzerindeki imza (signature) mekanizması
    url = f"https://www.vavoo.tv/api/app/ping"
    
    payload = {
        "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
        "package": "tv.vavoo.app",
        "version": "3.1.20"
    }
    
    headers = {
        "User-Agent": "okhttp/4.11.0",
        "X-Vavoo-Client": "tv.vavoo.app"
    }

    try:
        print(f"📡 {DOMAINS['vavoo']} üzerinden imza alınıyor...")
        r = requests.post(url, json=payload, headers=headers)
        if r.status_code == 200:
            return r.json().get("addonSig")
    except:
        return None

def generate_sports_list():
    sig = get_vavoo_to_signature()
    
    # beIN Sports kanalları için güncel liste
    channels = {
        "beIN SPORTS 1": "tr-be-in-sports-1",
        "beIN SPORTS 2": "tr-be-in-sports-2",
        "beIN SPORTS 3": "tr-be-in-sports-3"
    }
    
    with open("vavoo_to_list.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for name, cid in channels.items():
            # Vavoo.to üzerinden doğrudan oynatma linki
            link = f"https://{DOMAINS['vavoo']}/vavoo-iptv/play/{cid}.m3u8"
            f.write(f'#EXTINF:-1 group-title="SPOR",{name}\n')
            f.write(f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n')
            f.write(f"{link}\n")
            
    print(f"✅ Liste {DOMAINS['vavoo']} için güncellendi: vavoo_to_list.m3u")

if __name__ == "__main__":
    generate_sports_list()
  
