import re
import time

class PreFetchSanitizer:
    """
    Sömürgeci Script & Tracker Temizleyici ve Ön Analiz Motoru.
    Gelen isteklerin arka plan bağımlılıklarını süzerek veri boyutunu küçültür
    ve bağlantı hızını artırır.
    """
    def __init__(self):
        # Arka planda telefonu ve interneti yavaşlatan sömürgeci desenler (Pattern-based)
        self.tracker_patterns = [
            r".*analytics.*", r".*telemetry.*", r".*tracker.*",
            r".*pixel.*", r".*adservice.*", r".*doubleclick.*",
            r".*coinhive.*", r".*miner.*"
        ]
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.tracker_patterns]

    def sanitize_page_requests(self, resource_urls: list) -> dict:
        """
        Sayfanın çekmeye çalıştığı arka plan URL'lerini analiz eder.
        Sömürgeci script'leri 'DROP' eder, temiz olanları 'ALLOW' verir.
        """
        start_time = time.perf_counter()
        clean_urls = []
        dropped_urls = []

        for url in resource_urls:
            is_tracker = any(pattern.match(url) for pattern in self.compiled_patterns)
            if is_tracker:
                dropped_urls.append(url)
            else:
                clean_urls.append(url)

        process_time = (time.perf_counter() - start_time) * 1000

        return {
            "total_requests": len(resource_urls),
            "allowed_count": len(clean_urls),
            "dropped_count": len(dropped_urls),
            "dropped_urls": dropped_urls,
            "saved_bandwidth_ratio": f"%{round((len(dropped_urls) / max(len(resource_urls), 1)) * 100, 1)}",
            "latency_ms": round(process_time, 4)
        }

if __name__ == "__main__":
    sanitizer = PreFetchSanitizer()
    sample_page_resources = [
        "https://mhrs.gov.tr/assets/main.js",
        "https://mhrs.gov.tr/assets/style.css",
        "https://google-analytics.com/analytics.js",
        "https://adservice.google.com/adsid/google/ui",
        "https://tracker.badsite.com/pixel.gif",
        "https://mhrs.gov.tr/api/v1/randevu"
    ]

    print("\n--- PRE-FETCH & TRACKER SANITIZER TEST ---")
    # Fonksiyon adını sanitize_page_requests olarak güncelledik
    res = sanitizer.sanitize_page_requests(sample_page_resources)
    print(f"Toplam İstek      : {res['total_requests']}")
    print(f"İzin Verilen      : {res['allowed_count']}")
    print(f"İmha Edilen Çöp  : {res['dropped_count']} (Tasarruf: {res['saved_bandwidth_ratio']})")
    print(f"İşlem Süresi      : {res['latency_ms']} ms")
    print("\nEngellenen Arka Plan Sömürgeleri:")
    for url in res["dropped_urls"]:
        print(f" ❌ DROP -> {url}")