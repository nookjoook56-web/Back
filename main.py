import requests
import time
import os

def get_vavoo_signature():
    """Vavoo sunucusundan anlık imza (signature) alır."""
    url = "https://www.vavoo.tv/api/app/ping"
    
    # 2026 Şubat güncel uygulama payload yapısı
    payload = {
        "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
        "reason": "app focus",
        "package": "tv.vavoo.app",
        "version": "3.1.20",
        "appFocusTime": int(time.time() * 1000)
    }
    
    headers = {
        "User-Agent": "VAVOO/2.6",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            sig = data.get("addonSig")
            if sig:
                print(f"✅ İmza alındı: {sig[:10]}...")
                return sig
            else:
                print("⚠️ Sunucu cevap verdi ancak 'addonSig' bulunamadı.")
        else:
            print(f"❌ Sunucu hatası: {response.status_code}")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
    return None

def create_m3u_list():
    sig = get_vavoo_signature()
    
    # beIN Sports ve Diğer Kanallar
    channels = {
        "beIN SPORTS 1": "tr-be-in-sports-1",
        "beIN SPORTS 2": "tr-be-in-sports-2",
        "beIN SPORTS 3": "tr-be-in-sports-3",
        "beIN SPORTS 4": "tr-be-in-sports-4",
        "beIN SPORTS 5": "tr-be-in-sports-5",
        "beIN SPORTS HABER": "tr-be-in-sports-haber",
        "TRT 1": "tr-trt-1",
        "ATV": "tr-atv",
        "SHOW TV": "tr-show-tv"
    }

    filename = "vavoo_to_list.m3u"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        # GitHub Action'ın değişikliği algılaması için zaman damgası ekliyoruz [cite: 2026-02-07]
        f.write(f"# Son Guncelleme: {time.ctime()} (UTC)\n\n")
        
        for name, cid in channels.items():
            if sig:
                # Sunucunun kabul ettiği tam link formatı
                link = f"https://vavoo.to/vavoo-iptv/play/{cid}.m3u8?n=1&sig={sig}"
            else:
                # İmza alınamazsa hata parametresi ekleyerek m3u'yu bozmadan kaydet
                link = f"https://vavoo.to/vavoo-iptv/play/{cid}.m3u8?error=no_signature_check_token"
            
            f.write(f'#EXTINF:-1 group-title="VAVOO_TR",{name}\n')
            # VLC Player ve IPTV uygulamaları için kritik User-Agent talimatı
            f.write(f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n')
            f.write(f"{link}\n\n")
            
    print(f"🚀 {filename} başarıyla oluşturuldu.")

if __name__ == "__main__":
    create_m3u_list()
    
