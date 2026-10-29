import requests
import time

class MilliShieldClientAgent:
    def __init__(self, server_url="http://127.0.0.1:8000"):
        self.server_url = server_url
        self.local_cache = {}  # Yerel hızlı bellek (0.001 ms)
        self.fail_open_mode = False

    def check_server_health(self) -> bool:
        """Sunucu canlılığını ve hat kalitesini 3 ms içinde kontrol eder."""
        try:
            start = time.perf_counter()
            resp = requests.get(f"{self.server_url}/health", timeout=0.1) # 100 ms max timeout
            latency = (time.perf_counter() - start) * 1000
            
            if resp.status_code == 200 and latency < 50: # Sağlıklı hat
                self.fail_open_mode = False
                return True
        except Exception:
            pass

        # Sunucuya ulaşılamazsa veya yavaşsa Fail-Open devreje girer!
        self.fail_open_mode = True
        return False

    def process_network_request(self, domain: str) -> dict:
        """
        Telefonda bir siteye girilirken çalışan hafif karar mekanizması.
        """
        # 1. Cihaz İçi Yerel Bellek (Local Cache) Kontrolü
        if domain in self.local_cache:
            return {
                "action": self.local_cache[domain],
                "source": "LOCAL_CACHE",
                "latency_ms": 0.001
            }

        # 2. Canlılık / Fail-Open Kontrolü
        if not self.check_server_health():
            # Sunucuya ulaşılamıyor, İNTERNETİ KESME! Geçişe izin ver.
            return {
                "action": "PASS",
                "source": "FAIL_OPEN_SAFETY_NET",
                "reason": "Server unreachable -> B Planı devreye girdi, kesintisiz geçiş.",
                "latency_ms": 0.1
            }

        # 3. Sunucu AI Engine Kararı
        try:
            start = time.perf_counter()
            res = requests.post(
                f"{self.server_url}/inspect",
                json={"domain": domain, "client_id": "phone_s24fe"},
                timeout=0.2
            ).json()
            latency = round((time.perf_counter() - start) * 1000, 3)

            # Geçerli kararları cihaza önbelleğe al
            if res["action"] == "PASS":
                self.local_cache[domain] = "PASS"

            return {
                "action": res["action"],
                "source": "HETZNER_AI_SERVER",
                "reason": res["reason"],
                "latency_ms": latency
            }
        except Exception as e:
            return {
                "action": "PASS",
                "source": "FAIL_OPEN_FALLBACK",
                "reason": str(e),
                "latency_ms": 0.1
            }

if __name__ == "__main__":
    client = MilliShieldClientAgent()

    print("\n--- İSTEMCİ (EDGE CLIENT) FAIL-OPEN VE CACHE TESTİ ---")
    test_sites = [
        "mhrs.gov.tr",                     # İlk istek -> Sunucuya gider
        "mhrs.gov.tr",                     # İkinci istek -> Local Cache'den milisaniyede döner
        "mhrs-randevu-al-sistemi-0129.com", # Oltalama -> Sunucu AI engeller
        "github.com"                       # Temiz site -> Geçer
    ]

    for site in test_sites:
        res = client.process_network_request(site)
        status = "✅ [GECIS]" if res["action"] == "PASS" else "❌ [ENGEL]"
        print(f"{status} {site:<35} | Kaynak: {res['source']:<18} | {res['latency_ms']} ms")