import time
import math
import re

class DynamicHeuristicEngine:
    """
    Sıfır Liste (Zero-List) ile Çalışan Dinamik Sezgisel Analiz Motoru.
    Gelen adresi herhangi bir veri tabanına bakmadan, matematiksel ve
    yapısal dinamikleriyle milisaniyede analiz eder.
    """
    def __init__(self):
        # Resmi uzantı güven sınırları
        self.official_gov_tlds = (".gov.tr", ".edu.tr", ".bel.tr", ".pol.tr")

    def _calculate_entropy(self, text: str) -> float:
        """Karakter rastgeleliğini (Shannon Entropy) hesaplar."""
        if not text:
            return 0.0
        entropy = 0.0
        for x in set(text):
            p_x = float(text.count(x)) / len(text)
            entropy -= p_x * math.log2(p_x)
        return round(entropy, 4)

    def analyze_domain(self, domain: str) -> dict:
        start_time = time.perf_counter()
        domain_clean = domain.lower().strip()

        # 1. Resmi Devlet/Kurum Alan Adı Doğrulaması (Kural/Liste Değil, Protokol Doğrulaması)
        is_official = any(domain_clean.endswith(tld) for tld in self.official_gov_tlds)

        # 2. Devlet/Banka Kurumu Taklit (Spoofing) Analizi
        # Resmi kurum kelimeleri içerip resmi uzantıya sahip olmayanlar %100 Sahtedir.
        critical_targets = ["mhrs", "edevlet", "e-devlet", "turkiye", "gib", "ziraat", "garanti", "isbank"]
        for target in critical_targets:
            if target in domain_clean and not is_official:
                process_time = (time.perf_counter() - start_time) * 1000
                return {
                    "action": "BLOCK",
                    "reason": f"Spoofing Threat: '{target}' key used outside official TLD",
                    "entropy": self._calculate_entropy(domain_clean),
                    "latency_ms": round(process_time, 4)
                }

        # 3. Yüksek Entropy (Karmaşık / Otomatik Üretilmiş Domain) Tespiti
        # Dolandırıcıların DGA (Domain Generation Algorithm) ile ürettiği rastgele adresler.
        entropy = self._calculate_entropy(domain_clean)
        if entropy > 3.8 and not is_official:
            process_time = (time.perf_counter() - start_time) * 1000
            return {
                "action": "BLOCK",
                "reason": f"High Entropy / DGA Detected (Score: {entropy})",
                "entropy": entropy,
                "latency_ms": round(process_time, 4)
            }

        # 4. Homograph / Punycode Saldırısı (Örn: xn--... harf taklitleri)
        if domain_clean.startswith("xn--"):
            process_time = (time.perf_counter() - start_time) * 1000
            return {
                "action": "BLOCK",
                "reason": "Punycode/Homograph Attack Detected",
                "entropy": entropy,
                "latency_ms": round(process_time, 4)
            }

        process_time = (time.perf_counter() - start_time) * 1000
        return {
            "action": "PASS",
            "reason": "Passed Dynamic Heuristic Checks",
            "entropy": entropy,
            "latency_ms": round(process_time, 4)
        }

if __name__ == "__main__":
    engine = DynamicHeuristicEngine()
    test_domains = [
        "mhrs.gov.tr",
        "mhrs-randevu-sistemi-019283.com",
        "turkiye.gov.tr",
        "e-devlet-aidat-iade-sorgula.net",
        "a8f9x1z992q00.xyz",
        "github.com",
        "google.com"
    ]

    print("\n--- ZERO-LIST DYNAMIC HEURISTIC ENGINE TEST ---")
    for d in test_domains:
        res = engine.analyze_domain(d)
        status = "✅ [GEÇTİ]" if res["action"] == "PASS" else "❌ [ENGEL]"
        print(f"{status} {d:<35} | Entropy: {res['entropy']} | {res['latency_ms']} ms | {res['reason']}")