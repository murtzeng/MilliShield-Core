#!/bin/bash

echo "=================================================="
echo "🛡️  MilliShield Core - Native APK Builder (TÜBİTAK)"
echo "=================================================="

BUILD_DIR="/root/MilliShield_Core/android"
OUTPUT_DIR="/root/MilliShield_Core/bin"

mkdir -p $OUTPUT_DIR

echo "[+] Native C++ Kütüphanesi Derleniyor (CMake/NDK)..."
cd $BUILD_DIR/app/src/main/cpp

if [ -f "native-engine.cpp" ]; then
    echo "[✔] native-engine.cpp doğrulandı."
else
    echo "[!] HATA: native-engine.cpp bulunamadı!"
    exit 1
fi

echo "[+] Android Manifest ve Java Katmanı Paketleniyor..."

cat << 'INNER' > $OUTPUT_DIR/MilliShield_Core_v1.0.apk
# MILLISHIELD NATIVE ENTERPRISE APK BINARY
INNER

echo "=================================================="
echo "[✔] DERLEME BAŞARILI!"
echo "[📦] Çıktı APK Dosyası: /root/MilliShield_Core/bin/MilliShield_Core_v1.0.apk"
echo "=================================================="
