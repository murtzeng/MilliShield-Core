import re
import time
from engine.ai_core_engine import DynamicHeuristicEngine

class HTTPResponseSanitizer:
    """
    Arama Motorları ve Web Yanıtı Canlı Dezenfeksiyon Motoru.
    Gelen HTML/JSON içeriğindeki zararlı ve oltalama bağlantılarını
    ekrana yansımadan DOM seviyesinde temizler.
    """
    def __init__(self):
        self.ai_engine = DynamicHeuristicEngine()
        self.url_pattern = re.compile(r'href=["\'](https?://[^"\']+)["\']|url\(["\']?(https?://[^"\']+)["\']?', re.IGNORECASE)

    def sanitize_html_response(self, raw_html: str) -> dict:
        """Gelen HTML gövdesini tarar, sezgisel AI ile şüpheli linkleri siler."""
        start = time.perf_counter()
        purged_count = 0
        cleaned_html = raw_html

        found_urls = set()
        for match in self.url_pattern.finditer(raw_html):
            url = match.group(1) or match.group(2)
            if url:
                found_urls.add(url)

        for url in found_urls:
            domain_match = re.search(r'https?://([^/]+)', url)
            if domain_match:
                domain = domain_match.group(1)
                analysis = self.ai_engine.analyze_domain(domain)
                
                if analysis["action"] == "DROP":
                    cleaned_html = cleaned_html.replace(url, "#BLOCKED_BY_MILLISHIELD#")
                    purged_count += 1

        process_time = round((time.perf_counter() - start) * 1000, 4)

        return {
            "original_length": len(raw_html),
            "sanitized_length": len(cleaned_html),
            "purged_links_count": purged_count,
            "sanitized_html": cleaned_html,
            "latency_ms": process_time
        }

if __name__ == "__main__":
    sanitizer = HTTPResponseSanitizer()
    sample_google_search_html = """
    <html>
        <body>
            <a href="https://mhrs.gov.tr/randevu">MHRS Resmi Site</a>
            <a href="https://mhrs-randevu-al-sistemi-0129.com/login">MHRS Oltalama</a>
        </body>
    </html>
    """
    res = sanitizer.sanitize_html_response(sample_google_search_html)
    print(f"Silinen Sahte Linkler: {res['purged_links_count']} Adet | {res['latency_ms']} ms")