#!/usr/bin/env python3
"""
Setup script for Telegram Blackout Bot
This script helps you configure and run the Telegram bot
"""

import os
import sys
import subprocess
import getpass

def print_banner():
    """نمایش بنر شروع"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    ربات تلگرام خاموشی‌های برق                    ║
║                    Telegram Blackout Bot                     ║
║                                                              ║
║  این ربات اطلاعات خاموشی‌های برق مازندران را از سایت رسمی      ║
║  دریافت کرده و در اختیار کاربران قرار می‌دهد                   ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """بررسی نسخه پایتون"""
    if sys.version_info < (3, 7):
        print("❌ خطا: این ربات نیاز به Python 3.7 یا بالاتر دارد!")
        print(f"نسخه فعلی: {sys.version}")
        return False
    print(f"✅ نسخه پایتون: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """نصب وابستگی‌ها"""
    print("\n📦 نصب وابستگی‌ها...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requierements.txt"])
        print("✅ وابستگی‌ها با موفقیت نصب شدند")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطا در نصب وابستگی‌ها: {e}")
        return False

def get_bot_token():
    """دریافت توکن ربات"""
    print("\n🤖 تنظیم توکن ربات تلگرام:")
    print("1. به @BotFather در تلگرام پیام دهید")
    print("2. دستور /newbot را ارسال کنید")
    print("3. نام ربات و username را وارد کنید")
    print("4. توکن دریافتی را در اینجا وارد کنید")
    
    while True:
        token = getpass.getpass("🔑 توکن ربات را وارد کنید: ").strip()
        if token and len(token) > 50:
            return token
        else:
            print("❌ توکن نامعتبر است. لطفاً دوباره تلاش کنید.")

def create_env_file(token):
    """ایجاد فایل .env"""
    env_content = f"""# تنظیمات ربات تلگرام خاموشی‌های برق
TELEGRAM_BOT_TOKEN={token}

# تنظیمات اختیاری
# LOG_LEVEL=INFO
# DEFAULT_AREA=ساری
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ فایل .env ایجاد شد")
        return True
    except Exception as e:
        print(f"❌ خطا در ایجاد فایل .env: {e}")
        return False

def test_bot_connection(token):
    """تست اتصال ربات"""
    print("\n🔍 تست اتصال ربات...")
    try:
        import requests
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                print(f"✅ اتصال موفق! ربات: @{bot_info['result']['username']}")
                return True
            else:
                print("❌ خطا در اطلاعات ربات")
                return False
        else:
            print(f"❌ خطا در اتصال: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطا در تست اتصال: {e}")
        return False

def create_run_script():
    """ایجاد اسکریپت اجرا"""
    if os.name == 'nt':  # Windows
        script_content = """@echo off
echo Starting Telegram Blackout Bot...
python telegram_bot.py
pause
"""
        script_name = "run_bot.bat"
    else:  # Unix/Linux/Mac
        script_content = """#!/bin/bash
echo "Starting Telegram Blackout Bot..."
python3 telegram_bot.py
"""
        script_name = "run_bot.sh"
        # Make executable
        os.chmod(script_name, 0o755)
    
    try:
        with open(script_name, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"✅ اسکریپت اجرا ایجاد شد: {script_name}")
        return True
    except Exception as e:
        print(f"❌ خطا در ایجاد اسکریپت اجرا: {e}")
        return False

def show_usage_instructions():
    """نمایش دستورالعمل‌های استفاده"""
    instructions = """
🎉 **راه‌اندازی کامل شد!**

📋 **نحوه اجرای ربات:**

🔹 **روش 1 - مستقیم:**
   python telegram_bot.py

🔹 **روش 2 - با اسکریپت:**
   ./run_bot.sh (Linux/Mac)
   run_bot.bat (Windows)

🔹 **روش 3 - در پس‌زمینه:**
   nohup python telegram_bot.py > bot.log 2>&1 &

📱 **نحوه استفاده از ربات:**
1. ربات را در تلگرام پیدا کنید
2. دستور /start را ارسال کنید
3. از منوها برای جستجوی خاموشی‌ها استفاده کنید

💡 **دستورات مفید:**
- /start - شروع ربات
- /help - راهنما
- /search - جستجوی خاموشی
- /areas - لیست مناطق
- /latest - آخرین خاموشی‌ها

🔧 **تنظیمات بیشتر:**
- فایل config.py را برای تغییر مناطق ویرایش کنید
- فایل .env را برای تغییر تنظیمات ویرایش کنید

📞 **پشتیبانی:**
در صورت بروز مشکل، لاگ‌ها را بررسی کنید.
    """
    print(instructions)

def main():
    """تابع اصلی"""
    print_banner()
    
    # بررسی نسخه پایتون
    if not check_python_version():
        return
    
    # نصب وابستگی‌ها
    if not install_dependencies():
        print("❌ نصب وابستگی‌ها ناموفق بود!")
        return
    
    # دریافت توکن
    token = get_bot_token()
    
    # تست اتصال
    if not test_bot_connection(token):
        print("❌ تست اتصال ناموفق بود!")
        return
    
    # ایجاد فایل .env
    if not create_env_file(token):
        print("❌ ایجاد فایل .env ناموفق بود!")
        return
    
    # ایجاد اسکریپت اجرا
    create_run_script()
    
    # نمایش دستورالعمل‌ها
    show_usage_instructions()

if __name__ == "__main__":
    main()
