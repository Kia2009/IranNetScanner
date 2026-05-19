# 🇮🇷 IranNetScanner

**All-in-one Terminal Network Scanning & Diagnostic Tool for Iran's Internet.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Bash](https://img.shields.io/badge/Shell-Bash-green.svg)](https://www.gnu.org/software/bash/)

IranNetScanner is a professional, high-performance TUI application designed to help users and developers in Iran diagnose network issues, find reachable CDN edge IPs (Cloudflare, Akamai, Google, Amazon, Azure), and optimize their connection settings.

It merges the best features from [network-checker](https://github.com/mirarr-app/network-checker) and [cdn-ip-finder](https://github.com/hossein8360/cdn-ip-finder) into a single, easy-to-use terminal interface.

---

## 🚀 Installation (One-Liner)

```bash
git clone https://github.com/Kia2009/IranNetScanner.git && cd IranNetScanner && chmod +x run.sh && ./run.sh
```

---

## ✨ Features

- 🔍 **ISP Detection:** Automatically identify your operator (MCI, Irancell, etc.) and ASN info.
- 🌐 **Domain Checker:** Test reachability of major global domains.
- 📡 **DNS Tools:**
  - **Latency Test:** Compare speeds of global and local (IR) DNS providers.
  - **DNS Hunter:** See how different DNS providers resolve specific domains in Iran.
- ⚡ **CDN Edge Scanner:** Scan thousands of IPs from Cloudflare, Akamai, Google, Amazon, and Azure to find the ones with the lowest latency on your specific ISP.
- 🛠️ **VLESS Modifier:** Quickly swap IPs in your VLESS configurations.
- 📊 **Polished TUI:** Beautiful ANSI colors, progress bars, and formatted tables for a professional experience.

---

## 🇮🇷 راهنمای فارسی

**ایران‌نت‌اسکنر (IranNetScanner)** یک ابزار حرفه‌ای تحت ترمینال برای عیب‌یابی شبکه و پیدا کردن آی‌پی‌های تمیز CDN در ایران است.

### امکانات کلیدی:
- 🔍 **شناسایی اپراتور:** تشخیص خودکار همراه اول، ایرانسل و غیره.
- 🌐 **بررسی وضعیت دامنه‌ها:** تست دسترسی‌پذیری سایت‌های مهم.
- 📡 **ابزارهای دی‌ان‌اس:** تست تاخیر و بررسی نحوه رزولوشین دامنه‌ها.
- ⚡ **اسکنر آی‌پی CDN:** اسکن گسترده رنج‌های کلودفلر، آکامای، گوگل، آمازون و آزور.
- 🛠️ **ویرایشگر کانفیگ:** اصلاح سریع آی‌پی در لینک‌های VLESS.

### نحوه اجرا:
فقط دستور زیر را در ترمینال کپی کنید:
```bash
git clone https://github.com/Kia2009/IranNetScanner.git && cd IranNetScanner && chmod +x run.sh && ./run.sh
```

---

## 🛠️ Tech Stack

- **Frontend:** Bash (Shell Script) with ANSI escape codes.
- **Backend:** Python 3 (Concurrent scanning, DNS resolution, HTTP testing).
- **Libraries:** `rich`, `requests`, `dnspython`, `ipaddress`, `tqdm`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Credits

Inspired by and based on:
- [mirarr-app/network-checker](https://github.com/mirarr-app/network-checker)
- [hossein8360/cdn-ip-finder](https://github.com/hossein8360/cdn-ip-finder)
- [Morteza Bashsiz's Scanner](https://github.com/MortezaBashsiz)
