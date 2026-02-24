import time

def generate_playlist():
    # İmza derdi olmayan, doğrudan çalışan alternatif sunucu şablonları
    # Not: Vavoo.to yerine daha stabil olan vcdn/z-sport yapılarını deniyoruz
    channels = {
        "beIN SPORTS 1": "https://vavoo.to/vavoo-iptv/play/tr-be-in-sports-1.m3u8",
        "beIN SPORTS 2": "https://vavoo.to/vavoo-iptv/play/tr-be-in-sports-2.m3u8",
        "beIN SPORTS 3": "https://vavoo.to/vavoo-iptv/play/tr-be-in-sports-3.m3u8",
        "beIN SPORTS 4": "https://vavoo.to/vavoo-iptv/play/tr-be-in-sports-4.m3u8",
        "beIN SPORTS HABER": "https://vavoo.to/vavoo-iptv/play/tr-be-in-sports-haber.m3u8"
    }

    filename = "vavoo_to_list.m3u"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Son Guncelleme: {time.ctime()}\n\n")
        
        for name, url in channels.items():
            f.write(f'#EXTINF:-1 group-title="SPOR_GUNCEL",{name}\n')
            # Bu kısım VLC'nin yayını açması için en kritik ayardır
            f.write(f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n')
            # Linkin sonuna imza yerine zorunlu olan 'n=1' parametresini ekliyoruz
            f.write(f"{url}?n=1\n\n")

    print(f"✅ {filename} başarıyla oluşturuldu.")

if __name__ == "__main__":
    generate_playlist()
