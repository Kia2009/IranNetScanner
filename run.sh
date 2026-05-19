#!/bin/bash

# IranNetScanner - All-in-one Network Scanning Tool
# Author: Gemini Engineer

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "  _____                _   _      _    _____                                 "
    echo " |_   _|              | \ | |    | |  / ____|                                "
    echo "   | |  _ __ __ _ _ __|  \| | ___| |_| (___   ___ __ _ _ __  _ __   ___ _ __ "
    echo "   | | | '__/ _\` | '_ \ . \` |/ _ \ __|\___ \ / __/ _\` | '_ \| '_ \ / _ \ '__|"
    echo "  _| |_| | | (_| | | | | |\  |  __/ |_ ____) | (_| (_| | | | | | | |  __/ |   "
    echo " |_____|_|  \__,_|_| |_|_| \_|\___|\__|_____/ \___\__,_|_| |_|_| |_|\___|_|   "
    echo -e "${NC}"
    echo -e "${YELLOW}      Professional Network Diagnostics for Iran's Internet Environment${NC}"
    echo -e "${BLUE}================================================================================${NC}"
}

# Dependency Check
check_deps() {
    echo -e "${YELLOW}[*] Checking dependencies...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}[!] python3 is not installed. Please install it.${NC}"
        exit 1
    fi

    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}[*] Creating virtual environment...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
}

main_menu() {
    while true; do
        show_banner
        echo -e "${GREEN}1)${NC} 🔍 ISP Information"
        echo -e "${GREEN}2)${NC} 🌐 Domain Reachability"
        echo -e "${GREEN}3)${NC} 📡 DNS Tools (Latency/Hunter)"
        echo -e "${GREEN}4)${NC} ⚡ CDN IP Scanner (CF/Akamai/Google/Amazon/Azure)"
        echo -e "${GREEN}5)${NC} 🛠️  VLESS Config Modifier"
        echo -e "${GREEN}6)${NC} ℹ️  Help & About"
        echo -e "${GREEN}0)${NC} ❌ Exit"
        echo -e ""
        read -p "Select an option: " opt

        case $opt in
            1) python3 scripts/isp_info.py; read -p "Press Enter to return..." ;;
            2) python3 scripts/domain_checker.py; read -p "Press Enter to return..." ;;
            3) dns_menu ;;
            4) cdn_menu ;;
            5) config_modifier ;;
            6) show_help ;;
            0) exit 0 ;;
            *) echo -e "${RED}Invalid option!${NC}"; sleep 1 ;;
        esac
    done
}

dns_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}DNS Tools Menu${NC}"
        echo -e "${GREEN}1)${NC} DNS Latency Test"
        echo -e "${GREEN}2)${NC} DNS Hunter (Check resolution across providers)"
        echo -e "${GREEN}0)${NC} Back to Main Menu"
        echo -e ""
        read -p "Select an option: " opt

        case $opt in
            1) python3 scripts/dns_test.py latency; read -p "Press Enter to return..." ;;
            2)
                read -p "Enter domain to hunt (e.g. google.com): " domain
                python3 scripts/dns_test.py hunter "$domain"
                read -p "Press Enter to return..."
                ;;
            0) return ;;
            *) echo -e "${RED}Invalid option!${NC}"; sleep 1 ;;
        esac
    done
}

cdn_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}CDN IP Scanner Menu${NC}"
        echo -e "${GREEN}1)${NC} Cloudflare"
        echo -e "${GREEN}2)${NC} Akamai"
        echo -e "${GREEN}3)${NC} Google CDN"
        echo -e "${GREEN}4)${NC} Amazon CloudFront"
        echo -e "${GREEN}5)${NC} Microsoft Azure"
        echo -e "${GREEN}0)${NC} Back to Main Menu"
        echo -e ""
        read -p "Select CDN to scan: " opt

        case $opt in
            1) python3 scripts/cdn_scanner.py cloudflare; read -p "Press Enter to return..." ;;
            2) python3 scripts/cdn_scanner.py akamai; read -p "Press Enter to return..." ;;
            3) python3 scripts/cdn_scanner.py google; read -p "Press Enter to return..." ;;
            4) python3 scripts/cdn_scanner.py amazon; read -p "Press Enter to return..." ;;
            5) python3 scripts/cdn_scanner.py azure; read -p "Press Enter to return..." ;;
            0) return ;;
            *) echo -e "${RED}Invalid option!${NC}"; sleep 1 ;;
        esac
    done
}

config_modifier() {
    show_banner
    echo -e "${YELLOW}VLESS Config Modifier${NC}"
    read -p "Paste your VLESS config: " config
    read -p "Enter IP(s) to swap (comma separated): " ips
    python3 scripts/config_modifier.py "$config" "$ips"
    read -p "Press Enter to return..."
}

show_help() {
    show_banner
    echo -e "${CYAN}About IranNetScanner${NC}"
    echo "This tool is designed to help Iranian users bypass network restrictions"
    echo "by finding working CDN edge IPs and testing network health."
    echo ""
    echo "Features merged from:"
    echo "- mirarr-app/network-checker"
    echo "- hossein8360/cdn-ip-finder"
    echo ""
    echo "GitHub: https://github.com/Kia2009/IranNetScanner"
    read -p "Press Enter to return..."
}

# Start
check_deps
main_menu
