"""
ابزارهای استفاده از ایموجی‌های پریمیوم و Custom Emoji تلگرام
"""
from telegram import MessageEntity
from telegram.constants import MessageEntityType
from bot.config import USE_PREMIUM_EMOJIS


class PremiumEmojiHelper:
    """کمک به استفاده از ایموجی‌های پریمیوم"""
    
    # Custom Emoji IDs واقعی تلگرام
    # برای دریافت این IDها می‌تونید از ربات‌هایی مثل @CustomEmojiBot استفاده کنید
    CUSTOM_EMOJIS = {
        'fire': '5368324170671202286',
        'star': '5359785904535774578',
        'heart': '5370869711888194012',
        'money': '5370913841936801636',
        'party': '5359553277988220506',
        'rocket': '5370964809379046331',
        'sparkle': '5359785904535774578',
        'trophy': '5370869711888194012',
        'gem': '5370913841936801636',
    }
    
    @staticmethod
    def create_custom_emoji_text(text: str, emoji_id: str) -> tuple:
        """
        ایجاد متن با Custom Emoji
        
        Returns:
            tuple: (text, entities)
        """
        # Custom Emoji به صورت یک کاراکر خاص نمایش داده می‌شود
        emoji_char = "🔥"  # fallback
        entities = [
            MessageEntity(
                type=MessageEntityType.CUSTOM_EMOJI,
                offset=0,
                length=len(emoji_char),
                custom_emoji_id=emoji_id
            )
        ]
        return emoji_char + " " + text, entities
    
    @staticmethod
    def add_premium_effect(text: str) -> str:
        """
        اضافه کردن افکت‌های پریمیوم به متن
        
        در تلگرام، برای استفاده از افکت‌های پریمیوم:
        1. ربات باید Premium باشد
        2. یا از Custom Emoji Stickers استفاده کنید
        """
        if not USE_PREMIUM_EMOJIS:
            return text
        
        # افزودن فضای بیشتر برای زیباتر شدن
        return f"✨ {text} ✨"
    
    @staticmethod
    def format_message_with_emojis(text: str, emoji_style: str = 'premium') -> str:
        """
        فرمت کردن پیام با ایموجی‌های مناسب
        
        Args:
            text: متن پیام
            emoji_style: 'premium', 'standard', 'none'
        """
        if emoji_style == 'none':
            return text
        
        # نقشه ایموجی‌ها
        emoji_map = {
            # احساسات
            ':fire:': '🔥',
            ':star:': '⭐',
            ':sparkles:': '✨',
            ':party:': '🎉',
            ':heart:': '❤️',
            
            # موفقیت
            ':check:': '✅',
            ':cross:': '❌',
            ':warning:': '⚠️',
            ':trophy:': '🏆',
            
            # پول
            ':money:': '💰',
            ':coin:': '🪙',
            ':card:': '💳',
            ':gem:': '💎',
            
            # محصولات
            ':box:': '📦',
            ':gift:': '🎁',
            ':shopping:': '🛍️',
            ':cart:': '🛒',
            
            # کاربران
            ':user:': '👤',
            ':admin:': '👨‍💼',
            ':crown:': '👑',
            ':key:': '🔑',
            
            # دیگر
            ':rocket:': '🚀',
            ':bell:': '🔔',
            ':clock:': '⏰',
            ':home:': '🏠',
        }
        
        result = text
        for code, emoji in emoji_map.items():
            result = result.replace(code, emoji)
        
        return result


# استفاده در پیام‌ها
def format_premium_message(text: str, add_effects: bool = True) -> str:
    """
    فرمت کردن پیام برای نمایش بهتر
    """
    formatted = PremiumEmojiHelper.format_message_with_emojis(text)
    
    if add_effects and USE_PREMIUM_EMOJIS:
        formatted = PremiumEmojiHelper.add_premium_effect(formatted)
    
    return formatted


# Helper functions برای استفاده آسان
def premium_text(text: str) -> str:
    """متن با افکت پریمیوم"""
    return format_premium_message(text, add_effects=True)


def standard_text(text: str) -> str:
    """متن استاندارد با ایموجی‌ها"""
    return format_premium_message(text, add_effects=False)
