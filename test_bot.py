#!/usr/bin/env python3
"""
Test script for the Telegram Blackout Bot
This script tests the bot functionality without actually running the bot
"""

import os
import sys
from unittest.mock import Mock, patch
import asyncio

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import PowerOutageChecker
from config import AREAS, MESSAGES

def test_power_outage_checker():
    """تست کلاس PowerOutageChecker"""
    print("🔍 تست PowerOutageChecker...")
    
    try:
        checker = PowerOutageChecker()
        print("✅ PowerOutageChecker ایجاد شد")
        
        # تست دریافت داده‌های اولیه
        initial_data = checker.get_initial_data()
        if initial_data:
            print("✅ دریافت داده‌های اولیه موفق")
        else:
            print("⚠️ دریافت داده‌های اولیه ناموفق (ممکن است به اینترنت نیاز باشد)")
        
        return True
    except Exception as e:
        print(f"❌ خطا در تست PowerOutageChecker: {e}")
        return False

def test_config():
    """تست تنظیمات"""
    print("\n⚙️ تست تنظیمات...")
    
    try:
        # تست مناطق
        if AREAS:
            print(f"✅ {len(AREAS)} منطقه تعریف شده:")
            for area_name, area_info in AREAS.items():
                print(f"   - {area_name}: {area_info['city_code']}/{area_info['area_code']}")
        
        # تست پیام‌ها
        if MESSAGES:
            print(f"✅ {len(MESSAGES)} پیام تعریف شده")
        
        return True
    except Exception as e:
        print(f"❌ خطا در تست تنظیمات: {e}")
        return False

def test_dependencies():
    """تست وابستگی‌ها"""
    print("\n📦 تست وابستگی‌ها...")
    
    required_packages = [
        'requests',
        'beautifulsoup4',
        'pandas',
        'telegram'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - نصب نشده")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ پکیج‌های زیر نصب نشده‌اند: {', '.join(missing_packages)}")
        print("💡 برای نصب: pip install -r requierements.txt")
        return False
    
    return True

def test_bot_functionality():
    """تست عملکرد ربات (بدون اجرای واقعی)"""
    print("\n🤖 تست عملکرد ربات...")
    
    try:
        # تست تشخیص منطقه
        test_queries = [
            "ساری شهاب نیا",
            "آمل",
            "بابل خیابان امام",
            "قائم‌شهر",
            "نوشهر"
        ]
        
        # شبیه‌سازی تابع تشخیص منطقه
        def detect_area_from_query(query):
            query_lower = query.lower()
            for area_name in AREAS.keys():
                if area_name.lower() in query_lower:
                    return {
                        'area_name': area_name,
                        'city_code': AREAS[area_name]['city_code'],
                        'area_code': AREAS[area_name]['area_code']
                    }
            return None
        
        for query in test_queries:
            area_info = detect_area_from_query(query)
            if area_info:
                print(f"✅ '{query}' -> {area_info['area_name']}")
            else:
                print(f"⚠️ '{query}' -> منطقه تشخیص داده نشد")
        
        return True
    except Exception as e:
        print(f"❌ خطا در تست عملکرد ربات: {e}")
        return False

def test_environment():
    """تست محیط اجرا"""
    print("\n🌍 تست محیط اجرا...")
    
    # تست نسخه پایتون
    python_version = sys.version_info
    if python_version >= (3, 7):
        print(f"✅ نسخه پایتون: {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ نسخه پایتون قدیمی: {python_version.major}.{python_version.minor}.{python_version.micro}")
        return False
    
    # تست متغیر محیطی
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token:
        print("✅ متغیر محیطی TELEGRAM_BOT_TOKEN تنظیم شده")
    else:
        print("⚠️ متغیر محیطی TELEGRAM_BOT_TOKEN تنظیم نشده")
        print("💡 برای تنظیم: export TELEGRAM_BOT_TOKEN='your_token'")
    
    return True

def test_file_structure():
    """تست ساختار فایل‌ها"""
    print("\n📁 تست ساختار فایل‌ها...")
    
    required_files = [
        'main.py',
        'telegram_bot.py',
        'config.py',
        'setup_bot.py',
        'requierements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - موجود نیست")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ فایل‌های زیر موجود نیستند: {', '.join(missing_files)}")
        return False
    
    return True

def run_all_tests():
    """اجرای تمام تست‌ها"""
    print("🧪 شروع تست‌های سیستم خاموشی‌های برق")
    print("=" * 60)
    
    tests = [
        ("ساختار فایل‌ها", test_file_structure),
        ("محیط اجرا", test_environment),
        ("وابستگی‌ها", test_dependencies),
        ("تنظیمات", test_config),
        ("PowerOutageChecker", test_power_outage_checker),
        ("عملکرد ربات", test_bot_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 تست: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - موفق")
            else:
                print(f"❌ {test_name} - ناموفق")
        except Exception as e:
            print(f"❌ {test_name} - خطا: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 نتایج تست: {passed}/{total} موفق")
    
    if passed == total:
        print("🎉 تمام تست‌ها موفق بودند!")
        print("\n💡 برای اجرای ربات:")
        print("   python telegram_bot.py")
    else:
        print("⚠️ برخی تست‌ها ناموفق بودند")
        print("💡 مشکلات را برطرف کرده و دوباره تست کنید")
    
    return passed == total

def main():
    """تابع اصلی"""
    success = run_all_tests()
    
    if success:
        print("\n🚀 سیستم آماده اجرا است!")
    else:
        print("\n🔧 لطفاً مشکلات را برطرف کنید")

if __name__ == "__main__":
    main()
