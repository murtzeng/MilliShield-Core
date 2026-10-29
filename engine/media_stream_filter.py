import time
import re

class AdvancedMediaStreamFilter:
    """
    YouTube Shorts, Instagram Reels ve TikTok İçin Ön-Yükleme (Pre-Fetch)
    ve Çok Katmanlı (Ses/Görsel/Reklam) Medya Denetim Motoru.
    
    Çalışma Mantığı:
    1. Pre-Buffer Intercept: Video henüz ekrana düşmeden medya parçalarını (chunk) yakalar.
    2. Multi-Modal Analysis: Metin, Ses (Transkript), NPU Kare/Görsel Analizi ve Reklam/Sömürgeci Süzgeci.
    3. Instant Drop: 1 karede dahi ihlal varsa video akıştan kazınır (DROP_CHUNK).
    """
    def __init__(self):
        # 1. Sözcük & Transkript İhlal Listeleri (Yasal/Etik Denetim)
        self.profanity_list = ["küfür1", "amk", "aq", "sik", "piç", "yarrak", "orospu"]
        self.prohibited_keywords = [
            "bet", "casino", "gambling", "kumar", "bonus kazan", "yatırımsız kazanç",
            "crypto_scam", "yasa dışı", "şiddet", "kan", "dehşet"
        ]

        # 2. Reklam & İzleyici (Tracker) Ağ Yapıları
        self.ad_tracker_domains = [
            "adservice.google.com", "analytics.tiktok.com", "graph.instagram.com/ads",
            "doubleclick.net", "ad.doubleclick.net"
        ]

    def _inspect_text_and_audio(self, transcript: str, title: str) -> tuple[bool, str]:
        """Ses transkriptinde ve başlıkta küfür, şiddet, kumar arar."""
        combined_text = f"{title} {transcript}".lower()

        # Küfür Denetimi
        for word in self.profanity_list:
            if re.search(r'\b' + re.escape(word) + r'\b', combined_text):
                return True, f"İhlal Tespiti (Küfür/Argo): '{word}'"

        # Şiddet / Kumar / Dolandırıcılık Denetimi
        for kw in self.prohibited_keywords:
            if kw in combined_text:
                return True, f"İhlal Tespiti (Yasaklı Kategori/Sözcük): '{kw}'"

        return False, ""

    def inspect_prefetched_stream(self, stream_packet: dict) -> dict:
        """
        Video henüz ekrana gelmeden ön yükleme (buffering) aşamasında çalışan ana denetim.
        """
        start = time.perf_counter()

        platform = stream_packet.get("platform", "Unknown")
        video_id = stream_packet.get("video_id", "0x00")
        chunk_index = stream_packet.get("chunk_index", 0)
        
        # Meta Veriler & NPU Skorları
        title = stream_packet.get("title", "")
        transcript = stream_packet.get("audio_transcript", "")
        npu_explicit_score = stream_packet.get("npu_explicit_score", 0.0) # Müstehcenlik/Görsel Şiddet (0.0 - 1.0)
        is_ad_chunk = stream_packet.get("is_ad_chunk", False)
        source_domain = stream_packet.get("source_domain", "")

        # Katman 1: Reklam ve Sömürgeci Ağı Mühürleme
        if is_ad_chunk or any(ad_dom in source_domain for ad_dom in self.ad_tracker_domains):
            return {
                "action": "DROP_CHUNK",
                "platform": platform,
                "video_id": video_id,
                "reason": "Reklam/Sömürgeci Veri Parçacığı İmha Edildi",
                "latency_ms": round((time.perf_counter() - start) * 1000, 4)
            }

        # Katman 2: NPU/Edge Görsel & Müstehcenlik/Şiddet Analizi
        # (NPU kareleri tarar; 0.65 üstü risk kesin engellener)
        if npu_explicit_score > 0.65:
            return {
                "action": "DROP_CHUNK",
                "platform": platform,
                "video_id": video_id,
                "reason": f"NPU Görsel İhlal Tespiti (Müstehcenlik/Şiddet Skoru: {npu_explicit_score})",
                "latency_ms": round((time.perf_counter() - start) * 1000, 4)
            }

        # Katman 3: Ses Transkripti & Küfür/Metin Denetimi
        has_violation, reason_msg = self._inspect_text_and_audio(transcript, title)
        if has_violation:
            return {
                "action": "DROP_CHUNK",
                "platform": platform,
                "video_id": video_id,
                "reason": reason_msg,
                "latency_ms": round((time.perf_counter() - start) * 1000, 4)
            }

        # Katman 4: Temiz İçerik Geçiş İzni
        return {
            "action": "PASS_CHUNK",
            "platform": platform,
            "video_id": video_id,
            "reason": "İçerik Temiz - Ön Yüklemeye ve Gösterime İzin Verildi",
            "latency_ms": round((time.perf_counter() - start) * 1000, 4)
        }

if __name__ == "__main__":
    filter_engine = AdvancedMediaStreamFilter()

    # CANLI PRE-FETCH TEST SENARYOLARI
    test_streams = [
        {
            "platform": "YouTube_Shorts",
            "video_id": "shorts_9912",
            "chunk_index": 1,
            "title": "Python Dersleri - Bölüm 1",
            "audio_transcript": "Merhaba arkadaşlar bugün yazılım öğreniyoruz.",
            "npu_explicit_score": 0.02,
            "is_ad_chunk": False,
            "source_domain": "googlevideo.com"
        },
        {
            "platform": "Instagram_Reels",
            "video_id": "reels_4410",
            "chunk_index": 1,
            "title": "Çok Komik Anlar",
            "audio_transcript": "Lan oğlum böyle amk işi mi olur kaç oradan!", # KÜFÜR İÇERİYOR
            "npu_explicit_score": 0.10,
            "is_ad_chunk": False,
            "source_domain": "cdn.instagram.com"
        },
        {
            "platform": "TikTok",
            "video_id": "tiktok_8812",
            "chunk_index": 1,
            "title": "Gece Kulübü Canlı Yayın",
            "audio_transcript": "Eğlence devam ediyor...",
            "npu_explicit_score": 0.89, # MÜSTEHCENLİK / GÖRSEL İHLAL
            "is_ad_chunk": False,
            "source_domain": "tiktokcdn.com"
        },
        {
            "platform": "YouTube_Shorts",
            "video_id": "shorts_ad_001",
            "chunk_index": 1,
            "title": "Bahis Bonusu Kazan!",
            "audio_transcript": "Tıkla anında bakiye kazan.",
            "npu_explicit_score": 0.20,
            "is_ad_chunk": True, # REKLAM PARÇASI
            "source_domain": "doubleclick.net"
        }
    ]

    print("\n" + "="*75)
    print("      MİLLİSHIELD PRE-FETCH MEDYA SÜZME ENGINE (SHORTS / REELS)")
    print("="*75)

    for stream in test_streams:
        res = filter_engine.inspect_prefetched_stream(stream)
        status = "✅ [GEÇTİ]" if res["action"] == "PASS_CHUNK" else "❌ [IMHA]"
        print(f"{status} {res['platform']:<16} | Video ID: {res['video_id']} | {res['latency_ms']} ms")
        print(f"   └─ Aksiyon: {res['action']:<12} | Nedeni: {res['reason']}\n")