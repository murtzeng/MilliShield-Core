#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}[-] MilliShield Core Yumuşak Kaldırma İşlemi Başlatılıyor...${NC}"

# 1. Bekçi ve Servis Süreçlerini Durdur
pkill -9 -f shield_watchdog 2>/dev/null
pkill -9 -f uvicorn 2>/dev/null
killall -9 python3 2>/dev/null
fuser -k 8000/tcp 2>/dev/null

# 2. PID ve Geçici Dosyaları Temizle
rm -f .shield_server.pid
rm -f logs/*.log

echo -e "${GREEN}[✔] MilliShield Core servisleri tamamen durduruldu ve sistem temizlendi.${NC}"
echo -e "${GREEN}[✔] Cihazınız varsayılan orijinal haline döndü.${NC}"