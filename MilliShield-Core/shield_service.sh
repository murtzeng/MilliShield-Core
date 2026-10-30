#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

PYTHON_BIN="/root/MilliShield_Core/.venv/bin/python3"
PORT=8000

case "$1" in
    start)
        echo -e "${GREEN}[+] MilliShield Core Radikal Kalkan Başlatılıyor...${NC}"
        
        # --- KALICI PORT KORUMASI (PORT GUARD) ---
        # 8000 portunu tutan eski veya yetim süreç varsa acımasızca temizle
        if fuser $PORT/tcp >/dev/null 2>&1; then
            echo -e "${RED}[!] 8000 portunda çakışma tespit edildi, otomatik temizleniyor...${NC}"
            fuser -k -9 $PORT/tcp >/dev/null 2>&1
            sleep 1
        fi

        # FastAPI / Uvicorn Sunucusunu Başlat
        nohup $PYTHON_BIN -m uvicorn engine.api_server:app --host 0.0.0.0 --port $PORT > logs/server.log 2>&1 &
        echo $! > .shield_server.pid
        sleep 1.5

        if kill -0 $(cat .shield_server.pid) 2>/dev/null; then
            echo -e "${GREEN}[✔] Sunucu ve AI Motoru Aktif (PID: $(cat .shield_server.pid))${NC}"
        else
            echo -e "${RED}[!] Başlatma Hatası! Hata logu:${NC}"
            cat logs/server.log
        fi
        ;;
    stop)
        echo -e "${RED}[-] MilliShield Core Durduruluyor...${NC}"
        if [ -f .shield_server.pid ]; then
            kill -9 $(cat .shield_server.pid) 2>/dev/null
            rm -f .shield_server.pid
        fi
        fuser -k -9 $PORT/tcp >/dev/null 2>&1
        echo -e "${RED}[✔] Kalkan Devre Dışı Bırakıldı ve Port Temizlendi.${NC}"
        ;;
    status)
        if [ -f .shield_server.pid ] && kill -0 $(cat .shield_server.pid) 2>/dev/null; then
            echo -e "${GREEN}[✔] MilliShield Core AKTİF - (PID: $(cat .shield_server.pid)).${NC}"
        else
            echo -e "${RED}[!] Servis PASİF.${NC}"
        fi
        ;;
    test)
        echo -e "${GREEN}[*] Canlı Simülasyon Çalıştırılıyor...${NC}"
        $PYTHON_BIN test_simulation.py
        ;;
    *)
        echo "Kullanım: $0 {start|stop|status|test}"
        exit 1
esac