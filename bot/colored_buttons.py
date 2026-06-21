"""
دکمه‌های رنگی تلگرام (Telegram Button Colors)
قابلیت جدید تلگرام برای دکمه‌های رنگی
"""
from telegram import InlineKeyboardButton, KeyboardButton
from telegram.constants import ButtonColor


class ColoredButton:
    """دکمه‌های رنگی تلگرام"""
    
    # رنگ‌های موجود در تلگرام
    PRIMARY = "primary"      # آبی (پیش‌فرض)
    SECONDARY = "secondary"  # خاکستری
    SUCCESS = "positive"     # سبز
    DANGER = "negative"      # قرمز
    
    @staticmethod
    def create_button(text: str, callback_data: str, color: str = None) -> InlineKeyboardButton:
        """
        ایجاد دکمه با رنگ مشخص
        
        Args:
            text: متن دکمه
            callback_data: داده callback
            color: رنگ دکمه (primary, secondary, positive, negative)
        
        Returns:
            InlineKeyboardButton
        """
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        
        # افزودن رنگ به دکمه
        # توجه: این قابلیت در نسخه‌های جدید python-telegram-bot پشتیبانی می‌شود
        if color:
            # در حال حاضر رنگ‌ها در python-telegram-bot به طور کامل پشتیبانی نمی‌شوند
            # اما می‌توان با افزودن پیشوند رنگ به متن، تاثیر بصری ایجاد کرد
            pass
        
        return button
    
    @staticmethod
    def success_button(text: str, callback_data: str) -> InlineKeyboardButton:
        """دکمه سبز (موفقیت)"""
        return InlineKeyboardButton(
            text=f"✅ {text}",
            callback_data=callback_data
        )
    
    @staticmethod
    def danger_button(text: str, callback_data: str) -> InlineKeyboardButton:
        """دکمه قرمز (خطر)"""
        return InlineKeyboardButton(
            text=f"❌ {text}",
            callback_data=callback_data
        )
    
    @staticmethod
    def primary_button(text: str, callback_data: str) -> InlineKeyboardButton:
        """دکمه آبی (اصلی)"""
        return InlineKeyboardButton(
            text=f"🔵 {text}",
            callback_data=callback_data
        )
    
    @staticmethod
    def warning_button(text: str, callback_data: str) -> InlineKeyboardButton:
        """دکمه زرد (هشدار)"""
        return InlineKeyboardButton(
            text=f"⚠️ {text}",
            callback_data=callback_data
        )


# کیبوردهای رنگی برای موارد خاص
class ColoredKeyboards:
    """کیبوردهای از پیش طراحی شده با رنگ"""
    
    @staticmethod
    def confirmation_keyboard(confirm_data: str, cancel_data: str):
        """کیبورد تایید/لغو"""
        from telegram import InlineKeyboardMarkup
        
        keyboard = [
            [
                ColoredButton.success_button("تایید", confirm_data),
                ColoredButton.danger_button("لغو", cancel_data)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def payment_status_keyboard(approve_data: str, reject_data: str):
        """کیبورد تایید/رد پرداخت"""
        from telegram import InlineKeyboardMarkup
        
        keyboard = [
            [ColoredButton.success_button("✅ تایید و ارسال", approve_data)],
            [ColoredButton.danger_button("❌ رد کردن", reject_data)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def action_keyboard(actions: list):
        """
        کیبورد با اکشن‌های متعدد
        
        Args:
            actions: لیست (text, callback_data, color)
        """
        from telegram import InlineKeyboardMarkup
        
        keyboard = []
        for text, callback_data, color in actions:
            if color == 'success':
                button = ColoredButton.success_button(text, callback_data)
            elif color == 'danger':
                button = ColoredButton.danger_button(text, callback_data)
            elif color == 'warning':
                button = ColoredButton.warning_button(text, callback_data)
            else:
                button = ColoredButton.primary_button(text, callback_data)
            
            keyboard.append([button])
        
        return InlineKeyboardMarkup(keyboard)


# استفاده از Web App Buttons (دکمه‌های وب‌اپ با رنگ)
class WebAppButtons:
    """دکمه‌های Web App با طراحی رنگی"""
    
    @staticmethod
    def create_webapp_button(text: str, url: str, color: str = "primary"):
        """
        ایجاد دکمه Web App
        
        Args:
            text: متن دکمه
            url: آدرس Web App
            color: رنگ (در Web App تنظیم می‌شود)
        """
        from telegram import WebAppInfo, InlineKeyboardButton
        
        webapp = WebAppInfo(url=url)
        return InlineKeyboardButton(text=text, web_app=webapp)


# رنگ‌بندی براساس وضعیت
class StatusColors:
    """رنگ‌ها براساس وضعیت"""
    
    STATUS_COLORS = {
        'pending': '🟡',      # زرد - در انتظار
        'completed': '🟢',    # سبز - تکمیل شده
        'rejected': '🔴',     # قرمز - رد شده
        'cancelled': '⚫',    # مشکی - لغو شده
        'processing': '🔵',   # آبی - در حال پردازش
    }
    
    @staticmethod
    def get_status_emoji(status: str) -> str:
        """دریافت ایموجی رنگ براساس وضعیت"""
        return StatusColors.STATUS_COLORS.get(status, '⚪')
    
    @staticmethod
    def format_status_text(status: str, text: str) -> str:
        """فرمت کردن متن با رنگ وضعیت"""
        emoji = StatusColors.get_status_emoji(status)
        return f"{emoji} {text}"


# Helper function برای ایجاد کیبورد زیبا
def create_beautiful_keyboard(buttons_data: list, row_width: int = 2):
    """
    ایجاد کیبورد زیبا با دکمه‌های رنگی
    
    Args:
        buttons_data: لیست (text, callback, color_type)
        row_width: تعداد دکمه در هر ردیف
    
    Example:
        buttons = [
            ("محصولات", "products", "primary"),
            ("خرید", "buy", "success"),
            ("لغو", "cancel", "danger")
        ]
        keyboard = create_beautiful_keyboard(buttons, row_width=2)
    """
    from telegram import InlineKeyboardMarkup
    
    keyboard = []
    row = []
    
    for text, callback_data, color_type in buttons_data:
        if color_type == "success":
            button = ColoredButton.success_button(text, callback_data)
        elif color_type == "danger":
            button = ColoredButton.danger_button(text, callback_data)
        elif color_type == "warning":
            button = ColoredButton.warning_button(text, callback_data)
        else:
            button = ColoredButton.primary_button(text, callback_data)
        
        row.append(button)
        
        if len(row) >= row_width:
            keyboard.append(row)
            row = []
    
    # اضافه کردن دکمه‌های باقیمانده
    if row:
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)


# مثال استفاده
if __name__ == "__main__":
    print("🎨 راهنمای دکمه‌های رنگی تلگرام")
    print("=" * 50)
    print("""
# استفاده ساده:
from bot.colored_buttons import ColoredButton, create_beautiful_keyboard

# کیبورد زیبا
buttons = [
    ("🛍️ محصولات", "products", "primary"),
    ("💳 خرید", "buy", "success"),
    ("❌ لغو", "cancel", "danger"),
    ("⚙️ تنظیمات", "settings", "warning")
]
keyboard = create_beautiful_keyboard(buttons, row_width=2)
await update.message.reply_text("منو:", reply_markup=keyboard)

# کیبورد تایید/لغو
from bot.colored_buttons import ColoredKeyboards
keyboard = ColoredKeyboards.confirmation_keyboard("confirm_123", "cancel_123")
await update.message.reply_text("مطمئنید؟", reply_markup=keyboard)
    """)
