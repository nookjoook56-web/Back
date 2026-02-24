import requests

def get_vavoo_signature():
    # Vavoo'nun imza (signature) uç noktası
    url = "https://www.vavoo.tv/api/app/ping"
    payload = {
        "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
        "package": "tv.vavoo.app",
        "version": "3.1.20"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json().get("addonSig")
    except:
        return None

def create_list():
    sig = get_vavoo_signature()
    if not sig:
        print("İmza alınamadı, liste güncellenmedi.")
        return

    channels = ["tr-be-in-sports-1", "tr-be-in-sports-2", "tr-be-in-sports-3"]
    
    with open("vavoo_to_list.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            # Linkin sonuna ?n=1&sig={sig} eklemek zorunludur
            final_link = f"https://vavoo.to/vavoo-iptv/play/{ch}.m3u8?n=1&sig={sig}"
            f.write(f'#EXTINF:-1 group-title="SPOR",{ch.upper()}\n')
            f.write(f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n')
            f.write(f"{final_link}\n")

if __name__ == "__main__":
    create_list()
    
