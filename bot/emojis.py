"""
ایموجی‌های پریمیوم و استیکرهای تلگرام
"""

# ایموجی‌های پریمیوم تلگرام (با افکت انیمیشن)
class PremiumEmojis:
    # احساسات
    FIRE = "🔥"  # آتش با افکت
    STAR = "⭐"  # ستاره با افکت
    SPARKLES = "✨"  # جرقه‌های درخشان
    PARTY = "🎉"  # جشن
    HEART = "❤️"  # قلب قرمز
    LOVE = "🥰"  # عاشقانه
    
    # موفقیت و خطا
    CHECK = "✅"  # تیک سبز
    CROSS = "❌"  # ضربدر قرمز
    WARNING = "⚠️"  # هشدار
    SUCCESS = "🎯"  # موفقیت
    TROPHY = "🏆"  # جایزه
    
    # پول و فروش
    MONEY = "💰"  # کیسه پول
    DOLLAR = "💵"  # دلار
    CARD = "💳"  # کارت
    COIN = "🪙"  # سکه
    CHART_UP = "📈"  # نمودار صعودی
    GIFT = "🎁"  # هدیه
    
    # محصولات
    BOX = "📦"  # بسته
    PACKAGE = "📮"  # پکیج
    SHOPPING = "🛍️"  # خرید
    CART = "🛒"  # سبد خرید
    TAG = "🏷️"  # برچسب
    
    # کاربران
    USER = "👤"  # کاربر
    ADMIN = "👨‍💼"  # ادمین
    CROWN = "👑"  # تاج
    KEY = "🔑"  # کلید
    LOCK = "🔐"  # قفل
    
    # زمان
    CLOCK = "⏰"  # ساعت
    HOURGLASS = "⏳"  # ساعت شنی
    CALENDAR = "📅"  # تقویم
    
    # رسانه
    PICTURE = "🖼️"  # تصویر
    CAMERA = "📸"  # دوربین
    VIDEO = "📹"  # ویدیو
    
    # اسناد
    DOCUMENT = "📄"  # سند
    LIST = "📋"  # لیست
    NOTEBOOK = "📓"  # دفترچه
    RECEIPT = "🧾"  # رسید
    
    # ناوبری
    BACK = "🔙"  # بازگشت
    NEXT = "▶️"  # بعدی
    UP = "⬆️"  # بالا
    DOWN = "⬇️"  # پایین
    HOME = "🏠"  # خانه
    
    # اعمال
    REFRESH = "🔄"  # تازه‌سازی
    SETTINGS = "⚙️"  # تنظیمات
    SEARCH = "🔍"  # جستجو
    ADD = "➕"  # افزودن
    REMOVE = "➖"  # حذف
    EDIT = "✏️"  # ویرایش
    
    # وضعیت
    ONLINE = "🟢"  # آنلاین
    OFFLINE = "🔴"  # آفلاین
    PENDING = "🟡"  # در انتظار
    
    # دیگر
    ROCKET = "🚀"  # موشک
    LIGHTNING = "⚡"  # رعد و برق
    MAGIC = "✨"  # جادویی
    BELL = "🔔"  # زنگ


# متن‌های با ایموجی برای پیام‌ها
class EmojiTexts:
    @staticmethod
    def welcome(name: str) -> str:
        return (
            f"{PremiumEmojis.SPARKLES} سلام {name}! {PremiumEmojis.FIRE}\n\n"
            f"{PremiumEmojis.SHOPPING} به فروشگاه ما خوش آمدید {PremiumEmojis.GIFT}\n"
            f"از منوی زیر می‌تونید محصولات رو مشاهده و خرید کنید {PremiumEmojis.ROCKET}"
        )
    
    @staticmethod
    def admin_welcome(name: str) -> str:
        return (
            f"{PremiumEmojis.CROWN} سلام {name}! {PremiumEmojis.ADMIN}\n\n"
            f"{PremiumEmojis.SHOPPING} به فروشگاه ما خوش آمدید {PremiumEmojis.GIFT}\n\n"
            f"{PremiumEmojis.KEY} شما به عنوان ادمین وارد شدید {PremiumEmojis.STAR}\n"
            f"دسترسی به پنل مدیریت دارید {PremiumEmojis.SETTINGS}"
        )
    
    @staticmethod
    def product_added(name: str, price: int) -> str:
        return (
            f"{PremiumEmojis.CHECK} محصول با موفقیت اضافه شد! {PremiumEmojis.PARTY}\n\n"
            f"{PremiumEmojis.BOX} نام: {name}\n"
            f"{PremiumEmojis.MONEY} قیمت: {price:,} تومان"
        )
    
    @staticmethod
    def account_added(product_name: str) -> str:
        return (
            f"{PremiumEmojis.CHECK} اکانت با موفقیت اضافه شد! {PremiumEmojis.SPARKLES}\n\n"
            f"{PremiumEmojis.BOX} محصول: {product_name}"
        )
    
    @staticmethod
    def order_received() -> str:
        return (
            f"{PremiumEmojis.CHECK} رسید پرداخت شما دریافت شد {PremiumEmojis.RECEIPT}\n\n"
            f"{PremiumEmojis.HOURGLASS} لطفاً منتظر تایید ادمین باشید\n"
            f"{PremiumEmojis.BELL} پس از تایید، اطلاعات اکانت برای شما ارسال می‌شود"
        )
    
    @staticmethod
    def order_approved(product_name: str, username: str, password: str) -> str:
        return (
            f"{PremiumEmojis.TROPHY} سفارش شما تایید شد! {PremiumEmojis.PARTY}\n\n"
            f"{PremiumEmojis.BOX} محصول: {product_name}\n\n"
            f"{PremiumEmojis.LOCK} اطلاعات اکانت:\n"
            f"{PremiumEmojis.USER} نام کاربری: <code>{username}</code>\n"
            f"{PremiumEmojis.KEY} رمز عبور: <code>{password}</code>\n\n"
            f"{PremiumEmojis.WARNING} لطفاً اطلاعات را ذخیره کنید {PremiumEmojis.HEART}"
        )
    
    @staticmethod
    def payment_info(product_name: str, price: int, card_number: str, card_holder: str, order_id: int) -> str:
        return (
            f"{PremiumEmojis.CARD} اطلاعات پرداخت {PremiumEmojis.MONEY}\n\n"
            f"{PremiumEmojis.BOX} محصول: {product_name}\n"
            f"{PremiumEmojis.COIN} مبلغ قابل پرداخت: {price:,} تومان\n\n"
            f"{PremiumEmojis.CARD} شماره کارت:\n<code>{card_number}</code>\n"
            f"{PremiumEmojis.USER} به نام: {card_holder}\n\n"
            f"{PremiumEmojis.DOCUMENT} شماره سفارش: #{order_id}\n\n"
            f"{PremiumEmojis.CAMERA} پس از واریز مبلغ، عکس رسید یا اسکرین‌شات را ارسال کنید\n"
            f"{PremiumEmojis.CHECK} بعد از تایید ادمین، اطلاعات اکانت برای شما ارسال می‌شود {PremiumEmojis.ROCKET}"
        )
    
    @staticmethod
    def new_order_admin(order_id: int, username: str, product_name: str, amount: int) -> str:
        return (
            f"{PremiumEmojis.BELL} سفارش جدید ثبت شد! {PremiumEmojis.SPARKLES}\n\n"
            f"{PremiumEmojis.DOCUMENT} شماره سفارش: #{order_id}\n"
            f"{PremiumEmojis.USER} کاربر: {username}\n"
            f"{PremiumEmojis.BOX} محصول: {product_name}\n"
            f"{PremiumEmojis.MONEY} مبلغ: {amount:,} تومان\n\n"
            f"{PremiumEmojis.DOWN} رسید پرداخت:"
        )


# Custom Emoji IDs برای ایموجی‌های پریمیوم تلگرام
# این IDها رو می‌تونید از ربات‌های Premium Emoji استخراج کنید
class CustomEmojiIds:
    FIRE_ANIMATED = "5368324170671202286"
    STAR_ANIMATED = "5359785904535774578"
    HEART_ANIMATED = "5370869711888194012"
    MONEY_ANIMATED = "5370913841936801636"
    PARTY_ANIMATED = "5359553277988220506"
    ROCKET_ANIMATED = "5370964809379046331"
    
    @staticmethod
    def get_custom_emoji(emoji_id: str, fallback: str = "✨") -> str:
        """
        تولید ایموجی سفارشی با ID
        اگر کاربر پریمیوم نداشت، fallback نمایش داده می‌شود
        """
        try:
            return f"<tg-emoji emoji-id='{emoji_id}'>{fallback}</tg-emoji>"
        except:
            return fallback
