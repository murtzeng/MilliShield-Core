#!/bin/bash

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=======================================================${NC}"
echo -e "${CYAN}   MİLLİSHIELD CORE - RADİKAL SİSTEM DAĞITIM SİHRBAZI  ${NC}"
echo -e "${CYAN}=======================================================${NC}\n"

# 1. C/C++ Çekirdek Modüllerini Derleme
echo -e "${GREEN}[1/3] C/C++ Çekirdek ve Watchdog Modülleri Derleniyor...${NC}"
gcc -O2 kernel/shield_watchdog.c -o kernel/shield_watchdog
g++ -O3 client/native_guard.cpp -o client/native_guard
echo -e "${GREEN}[✔] C/C++ Derlemeleri Tamamlandı.${NC}\n"

# 2. Servis İzinleri ve Dizin Yapısı
echo -e "${GREEN}[2/3] Çalıştırma İzinleri Düzenleniyor...${NC}"
chmod +x shield_service.sh
mkdir -p logs engine/quantized_models
echo -e "${GREEN}[✔] İzinler Yapılandırıldı.${NC}\n"

# 3. Ana Servisi Başlatma
echo -e "${GREEN}[3/3] MilliShield Core Servisleri Başlatılıyor...${NC}"
./shield_service.sh start

echo -e "\n${CYAN}=======================================================${NC}"
echo -e "${GREEN}[✔] MİLLİSHIELD CORE BAŞARIYLA CANLIYA ALINDI!${NC}"
echo -e "${CYAN}=======================================================${NC}"