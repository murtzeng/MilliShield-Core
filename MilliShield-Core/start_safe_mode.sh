#!/bin/bash

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}[+] MilliShield Core Güvenli Modda (Yumuşak Mod) Başlatılıyor...${NC}"

# İzinleri Ver
chmod +x shield_service.sh
chmod +x uninstall_shield.sh

# Servisi Çalıştır
./shield_service.sh start

echo -e "${GREEN}[✔] Kalkan aktif! İstediğin an './uninstall_shield.sh' çalıştırarak tamamen kaldırabilirsin.${NC}"