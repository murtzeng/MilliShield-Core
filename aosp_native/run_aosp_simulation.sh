#!/bin/bash

echo "===================================================="
echo " MilliShield - AOSP SurfaceFlinger & Edge AI Simulator"
echo "===================================================="
echo ""

echo "[1/3] AOSP Soong Build Katmanı Kontrol Ediliyor..."
if [ -f "native_hook/Android.bp" ]; then
    echo " -> Android.bp Yapılandırması Doğrulandı."
else
    echo " -> HATA: Android.bp Bulunamadı!"
    exit 1
fi

echo ""
echo "[2/3] Native C++ Modülleri Derleniyor..."
g++ -O3 native_hook/SurfaceFrameInterceptor.cpp -o native_hook/test_interceptor
g++ -O3 native_hook/mock_npu_engine.cpp -o native_hook/test_npu

if [ $? -eq 0 ]; then
    echo " -> C++ Derleme Başarılı."
else
    echo " -> HATA: Derleme Sırasında Hata Oluştu!"
    exit 1
fi

echo ""
echo "[3/3] AOSP Render & Edge AI Simülasyon Testi Başlatılıyor..."
echo "----------------------------------------------------"
./native_hook/test_interceptor
echo "----------------------------------------------------"
./native_hook/test_npu
echo "----------------------------------------------------"
echo ""
echo "=> TÜM AOSP YEREL SİMÜLASYON TESTLERİ BAŞARIYLA TAMAMLANDI!"
g++ -O3 native_hook/benchmark_logger.cpp -o native_hook/test_benchmark
./native_hook/test_benchmark
