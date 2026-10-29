import re
import sys
import datetime

class SmartScheduler:
    def __init__(self):
        # Hafta İçi Odak Saatleri (Örn: Gece 23:00 - 07:00 ve Ders Saatleri 09:00-12:00, 13:00-17:00)
        self.weekday_block_hours = [(23, 7), (9, 12), (13, 17)]
        # Hafta Sonu Kısıtlama Saatleri (Daha Esnek: Sadece Gece Uykusu 00:00 - 07:00)
        self.weekend_block_hours = [(0, 7)]
        
        # Geçici Mola (Grace Period) Bitiş Zamanı
        self.mola_bitis = None

    def mola_ver(self, dakika: int):
        """Kısıtlamayı belirtilen dakika kadar erteler."""
        self.mola_bitis = datetime.datetime.now() + datetime.timedelta(minutes=dakika)
        print(f"\n[!] {dakika} dakikalık mola başlatıldı! Kalkan geçici olarak serbest.")

    def is_block_time(self) -> bool:
        simdi = datetime.datetime.now()
        
        # 1. Manuel Mola Kontrolü: Aktif bir mola varsa kısıtlama UYGULAMA
        if self.mola_bitis and simdi < self.mola_bitis:
            return False
            
        gun = simdi.weekday() # 0-4 Hafta içi, 5-6 Hafta sonu
        saat = simdi.hour
        
        saatler = self.weekday_block_hours if gun < 5 else self.weekend_block_hours
        
        for baslangic, bitis in saatler:
            if baslangic > bitis: # Gece yarısını geçen saatler (Örn: 23:00 - 07:00)
                if saat >= baslangic or saat < bitis:
                    return True
            else:
                if baslangic <= saat < bitis:
                    return True
                    
        return False


class PrecisionBlocker:
    def __init__(self):
        self.scheduler = SmartScheduler()

        # 1. TAM MUAF LİSTE (Her Zaman Açık: Müzik, Ders, DM)
        self.whitelist_patterns = [
            r"music\.youtube\.com",                 # YouTube Music
            r".*youtube\.com/watch\?v=",            # Normal YouTube Ders/Uzun Videoları
            r".*instagram\.com/api/v1/direct_v2",   # Instagram Mesajlaşma (DM)
            r".*whatsapp\.com",                      # WhatsApp Trafiği
            r".*spotify\.com",                      # Spotify Stream
        ]

        # 2. ENGEL LİSTESİ (Shorts, Reels, TikTok, Reklam/Kumar)
        self.blacklist_patterns = [
            # Sonsuz Kaydırma Akışları
            r".*youtube\.com/youtubei/v1/reel",
            r".*youtube\.com/shorts/",
            r".*instagram\.com/api/v1/clips",
            r".*instagram\.com/api/v1/discover/explore",
            
            # TikTok (Tam Süzgeç)
            r".*tiktokcdn\.com",
            r".*byteoversea\.com",
            r".*tiktok\.com",

            # Zararlı Reklamlı Oyunlar & Kumar Sunucuları (7/24 Engelli)
            r".*unityads\.unity3d\.com",
            r".*applovin\.com",
            r".*admob\.com",
            r".*casino.*",
            r".*betting.*"
        ]

    def inspect_traffic(self, url: str) -> dict:
        # Önce Güvenli Muafiyet Kontrolü
        for white in self.whitelist_patterns:
            if re.search(white, url, re.IGNORECASE):
                return {"action": "ALLOW", "reason": "Güvenli Hizmet (Müzik/Ders/DM)"}

        # Zamanlayıcı Kontrolü (Sadece kısıtlama saatlerinde engelle)
        if not self.scheduler.is_block_time():
            return {"action": "ALLOW", "reason": "Serbest Zaman / Mola Süresi"}

        # Kısıtlama Saatindeysek Süzgeci Çalıştır
        for black in self.blacklist_patterns:
            if re.search(black, url, re.IGNORECASE):
                return {"action": "DROP", "reason": "Shorts/Reels/TikTok/Reklam Engellendi"}

        return {"action": "ALLOW", "reason": "Genel Web Trafiği"}


if __name__ == "__main__":
    blocker = PrecisionBlocker()
    
    # Terminalden mola parametresi verilmiş mi kontrol et (Örn: python3 scroll_nsfw_blocker.py --mola 15)
    if len(sys.argv) > 2 and sys.argv[1] == "--mola":
        try:
            mola_dk = int(sys.argv[2])
            blocker.scheduler.mola_ver(mola_dk)
        except ValueError:
            print("[!] Geçersiz mola süresi. Örnek kullanım: --mola 15")

    print("[+] Cerrahi Süzgeç & Akıllı Zamanlayıcı Hazır. Testler Koşuluyor...\n")

    test_urls = [
        "https://music.youtube.com/watch?v=sarki123",            # YT Music
        "https://www.youtube.com/watch?v=fizik_dersi_1",          # YT Ders
        "https://www.youtube.com/shorts/abc1234",                 # YT Shorts
        "https://www.instagram.com/api/v1/direct_v2/threads/",   # IG DM (Sohbet)
        "https://www.instagram.com/api/v1/clips/home/",           # IG Reels
        "https://v16m.tiktokcdn.com/video/m/",                    # TikTok Video
        "https://ads.unityads.unity3d.com/v2/sdk"                 # Oyun İçi Reklam
    ]

    for url in test_urls:
        res = blocker.inspect_traffic(url)
        print(f"URL: {url}\n  -> Karar: {res['action']} | Nedeni: {res['reason']}\n")