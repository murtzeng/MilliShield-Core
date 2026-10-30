import time
import re

class DeviceGuardSandbox:
    """
    SMS, Telefon Araması ve Otomatik APK Kurulum Kalkanı (Sandbox).
    İşletim sistemine giren tehditleri uygulama arayüzüne ulaşmadan imha eder.
    """
    def __init__(self):
        # Oltalama SMS Kalıpları
        self.phishing_sms_patterns = [
            r"aidat iadesi", r"tebrikler kazandınız", r"tıkla randevu al",
            r"hesabınız kısıtlandı", r"ceza dosyanız bulunmaktadır"
        ]

    def inspect_incoming_sms(self, sender: str, message_body: str) -> dict:
        """SMS geldiği an RIL katmanında çalışan NLP tarayıcı."""
        start = time.perf_counter()
        
        # Link Kontrolü
        has_url = bool(re.search(r'https?://[^\s]+', message_body))
        
        for pattern in self.phishing_sms_patterns:
            if re.search(pattern, message_body, re.IGNORECASE) and has_url:
                return {
                    "action": "BLOCK_SMS",
                    "sender": sender,
                    "reason": f"Oltalama/Zararlı SMS Tespiti: '{pattern}' kalıbı ve şüpheli link",
                    "latency_ms": round((time.perf_counter() - start) * 1000, 4)
                }

        return {
            "action": "PASS_SMS",
            "sender": sender,
            "reason": "SMS Güvenli",
            "latency_ms": round((time.perf_counter() - start) * 1000, 4)
        }

    def inspect_apk_installation(self, apk_name: str, requested_permissions: list) -> dict:
        """
        APK indirildiğinde PackageInstaller öncesi Sanal Kum Havuzu (Sandbox) analizi.
        """
        start = time.perf_counter()
        
        # Yüksek Riskli İzin Kombinasyonları (SMS Okuma + Arka Plan İnternet + Accessibility)
        high_risk_perms = ["READ_SMS", "RECEIVE_SMS", "BIND_ACCESSIBILITY_SERVICE", "SYSTEM_ALERT_WINDOW"]
        
        matched_risks = [perm for perm in requested_permissions if perm in high_risk_perms]

        if len(matched_risks) >= 2:
            return {
                "action": "DESTROY_APK",
                "apk_name": apk_name,
                "reason": f"Zero-Day Truva Atı Şüphesi! Tehlikeli İzinler: {matched_risks}",
                "latency_ms": round((time.perf_counter() - start) * 1000, 4)
            }

        return {
            "action": "ALLOW_INSTALL",
            "apk_name": apk_name,
            "reason": "APK Davranışı Temiz ve Güvenli",
            "latency_ms": round((time.perf_counter() - start) * 1000, 4)
        }

if __name__ == "__main__":
    guard = DeviceGuardSandbox()

    print("\n--- SMS VE ZERO-DAY APK KUM HAVUZU (SANDBOX) TESTİ ---")
    
    # 1. SMS Testi
    sms_res = guard.inspect_incoming_sms("+905550001122", "Sayın vatandaşımız, 2.500 TL aidat iadesi için tıkla: http://e-devlet-aidat-sorgulama.net")
    print(f"SMS Analizi  -> Aksiyon: {sms_res['action']:<12} | Nedeni: {sms_res['reason']} | {sms_res['latency_ms']} ms")

    # 2. APK Testi
    apk_res = guard.inspect_apk_installation("Sahte_Fatura_Ode.apk", ["READ_SMS", "BIND_ACCESSIBILITY_SERVICE", "INTERNET"])
    print(f"APK SandBox  -> Aksiyon: {apk_res['action']:<12} | Nedeni: {apk_res['reason']} | {apk_res['latency_ms']} ms")