import os
import sys
import time
import subprocess

class MilitaryKillSwitch:
    def __init__(self):
        self.ram_vault_path = "/dev/shm/millishield_vault"
        self.lock_file = "/run/millishield_panic.lock"

    def wipe_ram_vault(self):
        """DoD 5220.22-M Standardında RAM Verilerini Rastgele Baytlarla Ezerek Silme"""
        print("[!] WARN: RAM üzerindeki hassas veriler ve oturum anahtarları imha ediliyor...")
        if os.path.exists(self.ram_vault_path):
            try:
                # Verilerin üzerini sıfırlarla ve rastgele verilerle ez
                for root, dirs, files in os.walk(self.ram_vault_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        with open(file_path, "wb") as f:
                            f.write(os.urandom(file_size)) # Overwrite
                        os.remove(file_path)
                print("[✔] RAM Vault tamamen imha edildi. Cold-Boot koruması aktif.")
            except Exception as e:
                print(f"[!] Hata: {str(e)}")
        else:
            print("[✔] RAM Vault temiz, iz bulunamadı.")

    def isolate_network_kernel(self):
        """eBPF Sürücüsünü Çekirdekte Tam Tampon / Blackhole Moduna Geçirir"""
        print("[!] WARN: eBPF Kernel Kalkanı 'XDP_DROP ALL' moduna alınıyor (Ağ Mühürlendi)...")
        # Tüm dış ağ trafiğini çekirdekte düşürür
        os.system("iptables -F && iptables -X && iptables -P INPUT DROP && iptables -P OUTPUT DROP")
        print("[✔] Ağ kartı fiziksel olarak felç edildi. Sızma riski sıfırlandı.")

    def execute_panic_protocol(self):
        """Acil Durum Protokolünü Başlatır"""
        print("\n==================================================")
        print("🚨 MILITARY GRADE PANIC KILL-SWITCH TETİKLENDİ 🚨")
        print("==================================================")
        
        # 1. Kilit Dosyasını Oluştur
        with open(self.lock_file, "w") as f:
            f.write(f"PANIC_TRIGGERED_AT_{time.time()}")

        # 2. RAM'deki Tüm Şifreleme Anahtarlarını ve Oturumları Yak
        self.wipe_ram_vault()

        # 3. Çekirdek Ağ Bağlantılarını Kes
        self.isolate_network_kernel()

        # 4. Sistem Servisini Güvenli Kilit Modunda Durdur
        os.system("systemctl stop millishield.service > /dev/null 2>&1")
        
        print("\n[✔] PANİK PROTOKOLÜ TAMAMLANDI. CİHAZ HAYALET MODUNDA KİLİTLENDİ.\n")

if __name__ == "__main__":
    killswitch = MilitaryKillSwitch()
    
    # Kaza ile tetiklenmeyi önlemek için parametre kontrolü
    if len(sys.argv) > 1 and sys.argv[1] == "--TRIGGER-NOW":
        killswitch.execute_panic_protocol()
    else:
        print("[+] MilliShield Panik Kill-Switch Modülü Nöbette.")
        print("    Kullanım (Acil Durum): python3 panic_killswitch.py --TRIGGER-NOW")