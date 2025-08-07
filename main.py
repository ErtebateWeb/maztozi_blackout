import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import time
import logging

# تنظیم logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PowerOutageChecker:
    def __init__(self):
        self.base_url = 'https://khamooshi.maztozi.ir/'
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """تنظیم session با headers مناسب"""
        self.session.headers.update({
            'accept': '*/*',
            'accept-language': 'fa,en-US,en;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-microsoftajax': 'Delta=true',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://khamooshi.maztozi.ir',
            'referer': 'https://khamooshi.maztozi.ir/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
        })

    def get_initial_data(self):
        """دریافت داده‌های اولیه برای استخراج ViewState و سایر فیلدهای ضروری"""
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                viewstate = soup.find('input', {'name': '__VIEWSTATE'})
                viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
                event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})
                
                return {
                    '__VIEWSTATE': viewstate['value'] if viewstate else '',
                    '__VIEWSTATEGENERATOR': viewstate_generator['value'] if viewstate_generator else '',
                    '__EVENTVALIDATION': event_validation['value'] if event_validation else ''
                }
            else:
                logger.error(f"خطا در دریافت صفحه اولیه: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"خطا در دریافت داده‌های اولیه: {e}")
            return None

    def search_outages(self, city_code='990090345', area_code='61'):
        """جستجوی خاموشی‌ها برای شهر و منطقه مشخص"""
        initial_data = self.get_initial_data()
        if not initial_data:
            return None
        
        # داده‌های فرم برای ارسال درخواست
        form_data = {
            'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$upOutage|ctl00$ContentPlaceHolder1$btnSearchOutage',
            'ctl00$ContentPlaceHolder1$txtSubscriberCode': '',
            'ctl00$ContentPlaceHolder1$outage': 'rbIsAddress',
            'ctl00$ContentPlaceHolder1$ddlCity': city_code,
            'ctl00$ContentPlaceHolder1$ddlArea': area_code,
            'ctl00$ContentPlaceHolder1$txtPDateFrom': '',
            'ctl00$ContentPlaceHolder1$txtPDateTo': '',
            'ctl00$ContentPlaceHolder1$txtAddress': '',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': initial_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': initial_data['__VIEWSTATEGENERATOR'],
            '__EVENTVALIDATION': initial_data['__EVENTVALIDATION'],
            '__ASYNCPOST': 'true',
            'ctl00$ContentPlaceHolder1$btnSearchOutage': 'جستجو',
        }
        
        # ارسال درخواست POST
        try:
            response = self.session.post(self.base_url, data=form_data)
            if response.status_code == 200:
                logger.info("درخواست با موفقیت ارسال شد")
                return response.text
            else:
                logger.error(f"خطا در ارسال درخواست: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"خطا در ارسال درخواست: {e}")
            return None

    def parse_outages(self, html_content):
        """تجزیه و تحلیل HTML و استخراج اطلاعات خاموشی‌ها"""
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        outages = []
        
        # جستجوی جدول خاموشی‌ها
        try:
            # پیدا کردن ردیف‌های داده
            rows = soup.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 5:  # حداقل 5 ستون انتظار داریم
                    outage_info = {}
                    
                    # استخراج اطلاعات از هر سلول
                    if len(cells) > 0 and cells[0].get_text(strip=True):
                        outage_info['date'] = cells[0].get_text(strip=True)
                    if len(cells) > 1 and cells[1].get_text(strip=True):
                        outage_info['start_time'] = cells[1].get_text(strip=True)
                    if len(cells) > 2 and cells[2].get_text(strip=True):
                        outage_info['end_time'] = cells[2].get_text(strip=True)
                    if len(cells) > 3 and cells[3].get_text(strip=True):
                        outage_info['region'] = cells[3].get_text(strip=True)
                    if len(cells) > 4 and cells[4].get_text(strip=True):
                        outage_info['description'] = cells[4].get_text(strip=True)
                    
                    if outage_info:  # اگر اطلاعاتی پیدا شد
                        outages.append(outage_info)
            
            return outages
            
        except Exception as e:
            logger.error(f"خطا در تجزیه HTML: {e}")
            return []

    def check_specific_outage(self, html_content, search_terms):
        """بررسی وجود خاموشی خاص بر اساس کلمات کلیدی"""
        if not html_content:
            return False
        
        # تبدیل search_terms به لیست اگر string است
        if isinstance(search_terms, str):
            search_terms = [search_terms]
        
        # بررسی وجود هر یک از کلمات کلیدی
        for term in search_terms:
            if term in html_content:
                logger.info(f"خاموشی '{term}' در لیست پیدا شد!")
                return True
        
        logger.info("خاموشی مورد نظر پیدا نشد.")
        return False

    def save_to_csv(self, outages, filename=None):
        """ذخیره اطلاعات خاموشی‌ها در فایل CSV"""
        if not outages:
            logger.warning("هیچ داده‌ای برای ذخیره وجود ندارد")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"power_outages_{timestamp}.csv"
        
        try:
            df = pd.DataFrame(outages)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logger.info(f"اطلاعات در فایل {filename} ذخیره شد")
        except Exception as e:
            logger.error(f"خطا در ذخیره فایل CSV: {e}")

    def save_raw_html(self, html_content, filename=None):
        """ذخیره HTML خام در فایل"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"raw_response_{timestamp}.html"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"HTML خام در فایل {filename} ذخیره شد")
        except Exception as e:
            logger.error(f"خطا در ذخیره فایل HTML: {e}")

    def run_check(self, search_terms=None, save_csv=True, save_html=False):
        """اجرای کامل فرآیند بررسی خاموشی"""
        logger.info("شروع بررسی خاموشی‌ها...")
        
        # جستجوی خاموشی‌ها
        html_content = self.search_outages()
        
        if html_content:
            # بررسی خاموشی خاص اگر مشخص شده
            if search_terms:
                found = self.check_specific_outage(html_content, search_terms)
                if found:
                    logger.info("خاموشی مورد نظر یافت شد!")
                else:
                    logger.info("خاموشی مورد نظر یافت نشد.")
            
            # ذخیره HTML خام اگر درخواست شده
            if save_html:
                self.save_raw_html(html_content)
            
            # تجزیه و ذخیره در CSV اگر درخواست شده
            if save_csv:
                outages = self.parse_outages(html_content)
                if outages:
                    self.save_to_csv(outages)
                    return outages
                else:
                    logger.warning("هیچ خاموشی پردازش شده‌ای پیدا نشد")
            
            return html_content
        else:
            logger.error("دریافت اطلاعات ناموفق بود")
            return None


# نحوه استفاده
if __name__ == "__main__":
    # ایجاد instance از کلاس
    checker = PowerOutageChecker()
    
    # بررسی خاموشی خاص (مثل خاموشی ۵۳)
    search_terms = ['53- شهاب نیا', '۵۳- شهاب نیا']
    
    # اجرای بررسی
    result = checker.run_check(
        search_terms=search_terms,
        save_csv=True,
        save_html=True
    )
    
    # نمایش نتیجه
    if result:
        print("بررسی با موفقیت انجام شد!")
    else:
        print("خطا در بررسی خاموشی‌ها")
    
    # مثال استفاده مستقل از توابع
    # outages_list = checker.parse_outages(result)
    # checker.save_to_csv(outages_list, "my_outages.csv")