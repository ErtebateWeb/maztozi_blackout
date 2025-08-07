import os
import logging
from datetime import datetime
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from main import PowerOutageChecker
import pandas as pd

# تنظیم logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BlackoutTelegramBot:
    def __init__(self, token):
        self.token = token
        self.checker = PowerOutageChecker()
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
        
        # مناطق پیش‌فرض
        self.default_areas = {
            'ساری': {'city_code': '990090345', 'area_code': '61'},
            'آمل': {'city_code': '990090346', 'area_code': '62'},
            'بابل': {'city_code': '990090347', 'area_code': '63'},
            'قائم‌شهر': {'city_code': '990090348', 'area_code': '64'},
            'نوشهر': {'city_code': '990090349', 'area_code': '65'},
        }
    
    def setup_handlers(self):
        """تنظیم handlers برای bot"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("search", self.search_command))
        self.application.add_handler(CommandHandler("areas", self.areas_command))
        self.application.add_handler(CommandHandler("latest", self.latest_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور شروع"""
        welcome_message = """
🔌 **خوش آمدید به ربات اطلاع‌رسانی خاموشی‌های برق مازندران**

برای دریافت اطلاعات خاموشی‌ها از دستورات زیر استفاده کنید:

📋 **دستورات موجود:**
/start - نمایش این پیام
/help - راهنمای کامل
/search - جستجوی خاموشی
/areas - لیست مناطق
/latest - آخرین خاموشی‌ها

💡 **نحوه استفاده:**
- برای جستجو: `/search منطقه کلمه_کلیدی`
- مثال: `/search ساری شهاب نیا`
- یا فقط `/search` برای جستجوی تعاملی

🔍 **جستجوی سریع:**
فقط نام منطقه یا کلمه کلیدی را تایپ کنید
مثال: "ساری" یا "شهاب نیا"
        """
        
        keyboard = [
            [InlineKeyboardButton("🔍 جستجوی خاموشی", callback_data="search_menu")],
            [InlineKeyboardButton("📋 آخرین خاموشی‌ها", callback_data="latest_outages")],
            [InlineKeyboardButton("📍 مناطق موجود", callback_data="areas_list")],
            [InlineKeyboardButton("❓ راهنما", callback_data="help_info")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور راهنما"""
        help_text = """
📚 **راهنمای کامل ربات خاموشی‌های برق**

🔍 **جستجوی خاموشی:**
- `/search منطقه کلمه_کلیدی` - جستجوی مستقیم
- `/search` - جستجوی تعاملی
- مثال: `/search ساری شهاب نیا`

📍 **مناطق موجود:**
- ساری، آمل، بابل، قائم‌شهر، نوشهر
- `/areas` - نمایش لیست کامل

📋 **آخرین خاموشی‌ها:**
- `/latest` - نمایش آخرین خاموشی‌های ثبت شده

💡 **جستجوی سریع:**
- فقط نام منطقه را تایپ کنید: "ساری"
- یا کلمه کلیدی: "شهاب نیا"
- یا ترکیبی: "ساری شهاب"

⚙️ **نکات مهم:**
- از کلمات فارسی استفاده کنید
- برای جستجوی دقیق‌تر، نام منطقه + کلمه کلیدی را ترکیب کنید
- نتایج شامل تاریخ، زمان شروع/پایان، منطقه و توضیحات است
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور جستجو"""
        if context.args:
            # جستجوی مستقیم
            query = ' '.join(context.args)
            await self.perform_search(update, context, query)
        else:
            # جستجوی تعاملی
            await self.show_search_menu(update, context)
    
    async def areas_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش مناطق موجود"""
        areas_text = "📍 **مناطق موجود برای جستجو:**\n\n"
        
        for area_name in self.default_areas.keys():
            areas_text += f"• {area_name}\n"
        
        areas_text += "\n💡 برای جستجو در منطقه خاص، نام منطقه را تایپ کنید یا از /search استفاده کنید"
        
        keyboard = [
            [InlineKeyboardButton(f"🔍 جستجو در {area}", callback_data=f"search_area_{area}") 
             for area in list(self.default_areas.keys())[:2]],
            [InlineKeyboardButton(f"🔍 جستجو در {area}", callback_data=f"search_area_{area}") 
             for area in list(self.default_areas.keys())[2:4]],
            [InlineKeyboardButton("🔍 جستجو در نوشهر", callback_data="search_area_نوشهر")],
            [InlineKeyboardButton("🔍 جستجوی تعاملی", callback_data="search_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(areas_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def latest_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش آخرین خاموشی‌ها"""
        await update.message.reply_text("🔍 در حال دریافت آخرین خاموشی‌ها...")
        
        try:
            # دریافت خاموشی‌ها از ساری (پیش‌فرض)
            html_content = self.checker.search_outages()
            if html_content:
                outages = self.checker.parse_outages(html_content)
                if outages:
                    await self.send_outages_result(update, context, outages, "آخرین خاموشی‌های ساری")
                else:
                    await update.message.reply_text("❌ هیچ خاموشی‌ای در حال حاضر یافت نشد.")
            else:
                await update.message.reply_text("❌ خطا در دریافت اطلاعات خاموشی‌ها")
        except Exception as e:
            logger.error(f"خطا در دریافت آخرین خاموشی‌ها: {e}")
            await update.message.reply_text("❌ خطا در دریافت اطلاعات")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش پیام‌های متنی"""
        text = update.message.text.strip()
        
        if text:
            await self.perform_search(update, context, text)
    
    async def show_search_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش منوی جستجو"""
        keyboard = [
            [InlineKeyboardButton(f"🔍 {area}", callback_data=f"search_area_{area}") 
             for area in list(self.default_areas.keys())[:3]],
            [InlineKeyboardButton(f"🔍 {area}", callback_data=f"search_area_{area}") 
             for area in list(self.default_areas.keys())[3:]],
            [InlineKeyboardButton("🔍 جستجوی آزاد", callback_data="free_search")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🔍 **انتخاب منطقه برای جستجو:**\n\n"
            "یکی از مناطق زیر را انتخاب کنید یا برای جستجوی آزاد کلیک کنید:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش کلیک دکمه‌ها"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "search_menu":
            await self.show_search_menu(update, context)
        elif data == "latest_outages":
            await self.latest_command(update, context)
        elif data == "areas_list":
            await self.areas_command(update, context)
        elif data == "help_info":
            await self.help_command(update, context)
        elif data.startswith("search_area_"):
            area = data.replace("search_area_", "")
            await self.perform_search(update, context, area)
        elif data == "free_search":
            await query.edit_message_text(
                "🔍 **جستجوی آزاد:**\n\n"
                "لطفاً کلمه کلیدی مورد نظر خود را تایپ کنید:\n"
                "مثال: شهاب نیا، خیابان امام، و غیره"
            )
    
    async def perform_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE, query):
        """انجام جستجو"""
        await update.message.reply_text(f"🔍 در حال جستجو برای: **{query}**")
        
        try:
            # تشخیص منطقه از query
            area_info = self.detect_area_from_query(query)
            
            if area_info:
                # جستجو در منطقه خاص
                html_content = self.checker.search_outages(
                    city_code=area_info['city_code'],
                    area_code=area_info['area_code']
                )
                area_name = area_info['area_name']
            else:
                # جستجو در ساری (پیش‌فرض)
                html_content = self.checker.search_outages()
                area_name = "ساری"
            
            if html_content:
                # جستجوی کلمات کلیدی در نتایج
                search_terms = self.extract_search_terms(query)
                if search_terms:
                    # بررسی وجود کلمات کلیدی
                    found = self.checker.check_specific_outage(html_content, search_terms)
                    if not found:
                        await update.message.reply_text(
                            f"❌ هیچ خاموشی‌ای با کلمات کلیدی '{', '.join(search_terms)}' در {area_name} یافت نشد."
                        )
                        return
                
                # تجزیه نتایج
                outages = self.checker.parse_outages(html_content)
                
                if outages:
                    # فیلتر کردن نتایج بر اساس کلمات کلیدی
                    if search_terms:
                        filtered_outages = self.filter_outages_by_terms(outages, search_terms)
                        if filtered_outages:
                            await self.send_outages_result(update, context, filtered_outages, f"نتایج جستجو در {area_name}")
                        else:
                            await update.message.reply_text(
                                f"❌ هیچ خاموشی‌ای با کلمات کلیدی '{', '.join(search_terms)}' در {area_name} یافت نشد."
                            )
                    else:
                        await self.send_outages_result(update, context, outages, f"تمام خاموشی‌های {area_name}")
                else:
                    await update.message.reply_text(f"❌ هیچ خاموشی‌ای در {area_name} یافت نشد.")
            else:
                await update.message.reply_text("❌ خطا در دریافت اطلاعات خاموشی‌ها")
                
        except Exception as e:
            logger.error(f"خطا در جستجو: {e}")
            await update.message.reply_text("❌ خطا در انجام جستجو")
    
    def detect_area_from_query(self, query):
        """تشخیص منطقه از query"""
        query_lower = query.lower()
        
        for area_name, area_info in self.default_areas.items():
            if area_name.lower() in query_lower:
                return {
                    'area_name': area_name,
                    'city_code': area_info['city_code'],
                    'area_code': area_info['area_code']
                }
        
        return None
    
    def extract_search_terms(self, query):
        """استخراج کلمات کلیدی از query"""
        # حذف نام مناطق از query
        query_clean = query
        for area_name in self.default_areas.keys():
            query_clean = query_clean.replace(area_name, '').strip()
        
        # تقسیم به کلمات کلیدی
        terms = [term.strip() for term in query_clean.split() if term.strip()]
        return terms if terms else None
    
    def filter_outages_by_terms(self, outages, search_terms):
        """فیلتر کردن خاموشی‌ها بر اساس کلمات کلیدی"""
        filtered = []
        
        for outage in outages:
            outage_text = ' '.join(str(v) for v in outage.values()).lower()
            for term in search_terms:
                if term.lower() in outage_text:
                    filtered.append(outage)
                    break
        
        return filtered
    
    async def send_outages_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE, outages, title):
        """ارسال نتایج خاموشی‌ها"""
        if not outages:
            await update.message.reply_text("❌ هیچ نتیجه‌ای یافت نشد.")
            return
        
        # محدود کردن تعداد نتایج
        max_results = 10
        if len(outages) > max_results:
            outages = outages[:max_results]
            title += f" (نمایش {max_results} نتیجه اول)"
        
        result_text = f"🔌 **{title}**\n\n"
        
        for i, outage in enumerate(outages, 1):
            result_text += f"**{i}. خاموشی:**\n"
            result_text += f"📅 تاریخ: {outage.get('date', 'نامشخص')}\n"
            result_text += f"⏰ شروع: {outage.get('start_time', 'نامشخص')}\n"
            result_text += f"⏰ پایان: {outage.get('end_time', 'نامشخص')}\n"
            result_text += f"📍 منطقه: {outage.get('region', 'نامشخص')}\n"
            result_text += f"📝 توضیحات: {outage.get('description', 'نامشخص')}\n"
            result_text += "─" * 30 + "\n\n"
        
        if len(outages) == max_results:
            result_text += f"⚠️ فقط {max_results} نتیجه اول نمایش داده شد."
        
        # تقسیم پیام اگر خیلی طولانی است
        if len(result_text) > 4096:
            chunks = [result_text[i:i+4096] for i in range(0, len(result_text), 4096)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode='Markdown')
        else:
            await update.message.reply_text(result_text, parse_mode='Markdown')
    
    def run(self):
        """اجرای bot"""
        logger.info("شروع ربات خاموشی‌های برق...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """تابع اصلی"""
    # دریافت token از متغیر محیطی
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ متغیر محیطی TELEGRAM_BOT_TOKEN تنظیم نشده است!")
        print("لطفاً token ربات خود را در متغیر محیطی TELEGRAM_BOT_TOKEN تنظیم کنید.")
        return
    
    # ایجاد و اجرای bot
    bot = BlackoutTelegramBot(token)
    bot.run()

if __name__ == "__main__":
    main()
