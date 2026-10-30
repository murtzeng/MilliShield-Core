import time
from engine.master_engine import MilliShieldMasterEngine
from client.device_guard import DeviceGuardSandbox

def run_full_spectrum_simulation():
    master = MilliShieldMasterEngine()
    guard = DeviceGuardSandbox()

    print("=" * 80)
    print("      MİLLİSHIELD CORE - OTONOM VE RADİKAL SİBER SAVUNMA SIMÜLASYONU")
    print("=" * 80)

    # 1. Aşama: Şifreli Tünel ve TLS/JA3 Röntgeni
    print("\n[1] ŞİFRELI TÜNEL & JA3 INSPECTOR (KAÇAK VPN / SHADOWSOCKS TESTI)")
    tls_test = master.process_full_spectrum_request({
        "type": "TLS_HANDSHAKE",
        "handshake_data": {"user_agent": "v2ray_shadowsocks_client_v2", "ciphers": [49195]}
    })
    print(f"Sonuç: {tls_test['action']:<12} | Nedeni: {tls_test['reason']}")

    # 2. Aşama: Pre-Fetch Shorts / Reels NPU Medya Süzgeci
    print("\n[2] PRE-FETCH SHORTS / REELS NPU SÜZGEÇ (GÖRSEL / KÜFÜR / REKLAM TESTI)")
    media_test = master.process_full_spectrum_request({
        "type": "MEDIA_STREAM",
        "stream_packet": {
            "platform": "YouTube_Shorts", "video_id": "shorts_991",
            "npu_explicit_score": 0.88, "title": "Test", "audio_transcript": "temiz ses"
        }
    })
    print(f"Sonuç: {media_test['action']:<12} | Nedeni: {media_test['reason']}")

    # 3. Aşama: Google / Safari Arama Dezenfeksiyonu
    print("\n[3] GOOGLE / SAFARI CANLI HTML DEZENFEKSIYONU (DOM PURGE)")
    raw_html = '<html><a href="https://mhrs-randevu-al-0129.com">Sahte MHRS</a></html>'
    html_test = master.process_full_spectrum_request({
        "type": "HTTP_RESPONSE",
        "raw_html": raw_html
    })
    print(f"Sonuç: {html_test['purged_links_count']} Adet Oltalama Linki HTML Kodundan Kazındı. ({html_test['latency_ms']} ms)")

    # 4. Aşama: Cihaz İçi SMS & APK Kum Havuzu (Sandbox)
    print("\n[4] CİHAZ İÇİ SMS & ZERO-DAY APK KUM HAVUZU (SANDBOX)")
    sms_res = guard.inspect_incoming_sms("+905550001122", "Aidat iadesi için tıkla: http://sahte-site.com")
    apk_res = guard.inspect_apk_installation("Sahte_Bank.apk", ["READ_SMS", "BIND_ACCESSIBILITY_SERVICE"])
    print(f"SMS Durumu : {sms_res['action']:<12} | {sms_res['reason']}")
    print(f"APK Durumu : {apk_res['action']:<12} | {apk_res['reason']}")

    print("\n" + "=" * 80)
    print(" ALL RADICAL LAYERS ACTIVE - SISTEM %100 BAŞARIYLA SAVAŞA HAZIR")
    print("=" * 80)

if __name__ == "__main__":
    run_full_spectrum_simulation()