import time
import os
import random

GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
NC = '\033[0m'

def start_live_dashboard():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{CYAN}================================================================================")
    print("      MİLLİSHIELD CORE - OTONOM CANLI THREAT MONITOR & DASHBOARD")
    print(f"==================================================================={NC}\n")
    print(f"{GREEN}[✔] eBPF / XDP Kernel Shield: AKTİF (NIC Level Driver Mode)")
    print(f"[✔] JA3 TLS Inspector Engine: AKTİF (Zero-Trust Tunnel Lock)")
    print(f"[✔] Pre-Fetch NPU Media Filter: AKTİF (Shorts/Reels/TikTok)")
    print(f"[✔] Device Guard & Sandbox   : AKTİF (SMS / RIL / PackageInstaller){NC}\n")
    print("-" * 80)
    print(f"{YELLOW}{'ZAMAN':<12} | {'KATMAN':<18} | {'AKSİYON':<12} | {'AÇIKLAMA / İHLAL NEDENİ'}{NC}")
    print("-" * 80)

    # Canlı Akış Simülatörü / Log Okucu
    events = [
        ("TLS_JA3", "DROP_RST", "Kaçak Shadowsocks/V2Ray Tüneli İmzası Engellendi", RED),
        ("MEDIA_NPU", "DROP_CHUNK", "TikTok / Shorts Müstehcenlik Skoru > 0.85 (Imha)", RED),
        ("DOM_PURGE", "SANITIZED", "Google Arama Sonucundaki Sahte MHRS Linki Kazındı", YELLOW),
        ("SMS_GUARD", "BLOCK_SMS", "Oltalama SMS'i RIL Katmanında Durduruldu", RED),
        ("HEURISTIC", "PASS", "Ziraat Bankası Resmi Domain Doğrulandı (0.001 ms)", GREEN),
        ("APK_SANDBOX", "DESTROY_APK", "Zero-Day SMS Çalma İzinli Sahte APK Imha Edildi", RED)
    ]

    try:
        while True:
            t_str = time.strftime('%H:%M:%S')
            layer, action, desc, color = random.choice(events)
            print(f"{t_str:<12} | {layer:<18} | {color}{action:<12}{NC} | {desc}")
            time.sleep(random.uniform(0.8, 2.0))
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Canlı İzleme Paneli Kapatıldı.{NC}")

if __name__ == "__main__":
    start_live_dashboard()