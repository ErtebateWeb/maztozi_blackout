#!/usr/bin/env python3
"""
Example usage of the Blackout Checker and Telegram Bot
This script demonstrates how to use the power outage checker and bot functionality
"""

from main import PowerOutageChecker
from config import AREAS, MESSAGES
import os

def example_basic_usage():
    """مثال استفاده پایه از PowerOutageChecker"""
    print("🔌 مثال استفاده پایه از PowerOutageChecker")
    print("=" * 50)
    
    # ایجاد instance
    checker = PowerOutageChecker()
    
    # جستجوی خاموشی‌ها در ساری
    print("🔍 جستجوی خاموشی‌ها در ساری...")
    html_content = checker.search_outages()
    
    if html_content:
        # تجزیه نتایج
        outages = checker.parse_outages(html_content)
        
        if outages:
            print(f"✅ {len(outages)} خاموشی یافت شد:")
            for i, outage in enumerate(outages[:3], 1):  # نمایش 3 مورد اول
                print(f"\n{i}. خاموشی:")
                print(f"   تاریخ: {outage.get('date', 'نامشخص')}")
                print(f"   شروع: {outage.get('start_time', 'نامشخص')}")
                print(f"   پایان: {outage.get('end_time', 'نامشخص')}")
                print(f"   منطقه: {outage.get('region', 'نامشخص')}")
                print(f"   توضیحات: {outage.get('description', 'نامشخص')}")
        else:
            print("❌ هیچ خاموشی‌ای یافت نشد")
    else:
        print("❌ خطا در دریافت اطلاعات")

def example_search_specific():
    """مثال جستجوی خاموشی خاص"""
    print("\n🔍 مثال جستجوی خاموشی خاص")
    print("=" * 50)
    
    checker = PowerOutageChecker()
    
    # جستجوی خاموشی با کلمات کلیدی
    search_terms = ['شهاب نیا', 'خیابان امام']
    
    print(f"🔍 جستجو برای: {', '.join(search_terms)}")
    html_content = checker.search_outages()
    
    if html_content:
        # بررسی وجود خاموشی خاص
        found = checker.check_specific_outage(html_content, search_terms)
        
        if found:
            print("✅ خاموشی مورد نظر یافت شد!")
            
            # تجزیه و فیلتر نتایج
            outages = checker.parse_outages(html_content)
            filtered_outages = []
            
            for outage in outages:
                outage_text = ' '.join(str(v) for v in outage.values()).lower()
                for term in search_terms:
                    if term.lower() in outage_text:
                        filtered_outages.append(outage)
                        break
            
            print(f"📋 {len(filtered_outages)} خاموشی مرتبط:")
            for outage in filtered_outages:
                print(f"   - {outage.get('description', 'نامشخص')}")
        else:
            print("❌ خاموشی مورد نظر یافت نشد")
    else:
        print("❌ خطا در دریافت اطلاعات")

def example_multi_area():
    """مثال جستجو در چندین منطقه"""
    print("\n📍 مثال جستجو در چندین منطقه")
    print("=" * 50)
    
    checker = PowerOutageChecker()
    
    # جستجو در مناطق مختلف
    areas_to_check = ['ساری', 'آمل', 'بابل']
    
    for area_name in areas_to_check:
        if area_name in AREAS:
            area_info = AREAS[area_name]
            print(f"\n🔍 جستجو در {area_name}...")
            
            html_content = checker.search_outages(
                city_code=area_info['city_code'],
                area_code=area_info['area_code']
            )
            
            if html_content:
                outages = checker.parse_outages(html_content)
                if outages:
                    print(f"✅ {len(outages)} خاموشی در {area_name} یافت شد")
                else:
                    print(f"❌ هیچ خاموشی‌ای در {area_name} یافت نشد")
            else:
                print(f"❌ خطا در دریافت اطلاعات {area_name}")

def example_save_data():
    """مثال ذخیره داده‌ها"""
    print("\n💾 مثال ذخیره داده‌ها")
    print("=" * 50)
    
    checker = PowerOutageChecker()
    
    # دریافت و ذخیره داده‌ها
    print("🔍 دریافت خاموشی‌ها...")
    result = checker.run_check(
        search_terms=['شهاب نیا'],
        save_csv=True,
        save_html=True
    )
    
    if result:
        print("✅ داده‌ها با موفقیت ذخیره شدند")
        print("📁 فایل‌های ایجاد شده:")
        print("   - power_outages_YYYYMMDD_HHMMSS.csv")
        print("   - raw_response_YYYYMMDD_HHMMSS.html")
    else:
        print("❌ خطا در ذخیره داده‌ها")

def example_bot_integration():
    """مثال یکپارچه‌سازی با ربات"""
    print("\n🤖 مثال یکپارچه‌سازی با ربات")
    print("=" * 50)
    
    # بررسی وجود توکن ربات
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ متغیر محیطی TELEGRAM_BOT_TOKEN تنظیم نشده است")
        print("💡 برای تست ربات، ابتدا setup_bot.py را اجرا کنید")
        return
    
    print("✅ توکن ربات یافت شد")
    print("🔧 برای اجرای ربات:")
    print("   python telegram_bot.py")
    print("\n📱 دستورات مفید ربات:")
    print("   /start - شروع ربات")
    print("   /search ساری شهاب نیا - جستجوی مستقیم")
    print("   /areas - لیست مناطق")
    print("   /latest - آخرین خاموشی‌ها")

def main():
    """تابع اصلی"""
    print("🔌 مثال‌های استفاده از سیستم خاموشی‌های برق")
    print("=" * 60)
    
    # اجرای مثال‌ها
    example_basic_usage()
    example_search_specific()
    example_multi_area()
    example_save_data()
    example_bot_integration()
    
    print("\n" + "=" * 60)
    print("✅ تمام مثال‌ها اجرا شدند")
    print("\n💡 نکات مهم:")
    print("   - برای اجرای ربات: python telegram_bot.py")
    print("   - برای راه‌اندازی: python setup_bot.py")
    print("   - برای تنظیمات: فایل config.py را ویرایش کنید")

if __name__ == "__main__":
    main()
