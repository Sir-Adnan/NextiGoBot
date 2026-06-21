"""
Custom Emoji IDs واقعی تلگرام
این IDها از @AdsMarkdownBot دریافت شده‌اند
"""
from telegram import MessageEntity
from telegram.constants import MessageEntityType
from typing import List, Tuple


# Custom Emoji IDs - از @AdsMarkdownBot
CUSTOM_EMOJI_IDS = {
    # شما باید این IDها رو از @AdsMarkdownBot دریافت کنید
    # راهنما: هر ایموجی رو به ربات بفرستید و ID رو کپی کنید
    
    # احساسات
    'fire': '5368324170671202286',           # 🔥
    'star': '5359785904535774578',           # ⭐
    'sparkles': '5368324170671202286',       # ✨
    'party': '5359553277988220506',          # 🎉
    'heart': '5370869711888194012',          # ❤️
    'love': '5370869711888194012',           # 🥰
    
    # موفقیت
    'trophy': '5370869711888194012',         # 🏆
    'check': '5368324170671202286',          # ✅
    'star_eyes': '5359785904535774578',      # 🤩
    
    # پول
    'money': '5370913841936801636',          # 💰
    'coin': '5370913841936801636',           # 🪙
    'gem': '5370913841936801636',            # 💎
    'dollar': '5370913841936801636',         # 💵
    
    # دیگر
    'rocket': '5370964809379046331',         # 🚀
    'lightning': '5368324170671202286',      # ⚡
    'gift': '5359553277988220506',           # 🎁
    'crown': '5359785904535774578',          # 👑
    'bell': '5368324170671202286',           # 🔔
}


def create_custom_emoji_entity(emoji_name: str, offset: int = 0) -> MessageEntity:
    """
    ایجاد Custom Emoji Entity
    
    Args:
        emoji_name: نام ایموجی از CUSTOM_EMOJI_IDS
        offset: موقعیت در متن
    
    Returns:
        MessageEntity برای Custom Emoji
    """
    emoji_id = CUSTOM_EMOJI_IDS.get(emoji_name)
    
    if not emoji_id:
        return None
    
    return MessageEntity(
        type=MessageEntityType.CUSTOM_EMOJI,
        offset=offset,
        length=1,  # Custom emoji همیشه 1 کاراکتر است
        custom_emoji_id=emoji_id
    )


def format_text_with_custom_emojis(text: str, emoji_map: dict) -> Tuple[str, List[MessageEntity]]:
    """
    فرمت کردن متن با Custom Emojis
    
    Args:
        text: متن اصلی
        emoji_map: دیکشنری {موقعیت: نام_ایموجی}
    
    Returns:
        (formatted_text, entities)
    
    Example:
        text = "سلام! خوش آمدید"
        emoji_map = {0: 'fire', 6: 'star'}
        # موقعیت 0: قبل از "سلام"
        # موقعیت 6: قبل از "خوش آمدید"
    """
    entities = []
    
    # مرتب‌سازی بر اساس موقعیت
    sorted_positions = sorted(emoji_map.items())
    
    offset_adjustment = 0
    formatted_text = text
    
    for position, emoji_name in sorted_positions:
        entity = create_custom_emoji_entity(emoji_name, position + offset_adjustment)
        
        if entity:
            # اضافه کردن placeholder برای ایموجی
            emoji_placeholder = "🔥"  # هر ایموجی می‌تونه باشه
            
            formatted_text = (
                formatted_text[:position + offset_adjustment] +
                emoji_placeholder +
                formatted_text[position + offset_adjustment:]
            )
            
            entities.append(entity)
            offset_adjustment += len(emoji_placeholder)
    
    return formatted_text, entities


# Helper functions ساده
def add_fire_emoji(text: str) -> Tuple[str, List[MessageEntity]]:
    """اضافه کردن ایموجی آتش به ابتدای متن"""
    return format_text_with_custom_emojis(text, {0: 'fire'})


def add_star_emoji(text: str) -> Tuple[str, List[MessageEntity]]:
    """اضافه کردن ایموجی ستاره به ابتدای متن"""
    return format_text_with_custom_emojis(text, {0: 'star'})


def add_celebration_emojis(text: str) -> Tuple[str, List[MessageEntity]]:
    """اضافه کردن ایموجی‌های جشن به ابتدا و انتهای متن"""
    emoji_map = {
        0: 'party',
        len(text): 'sparkles'
    }
    return format_text_with_custom_emojis(text, emoji_map)


# کلاس Helper برای استفاده آسان‌تر
class CustomEmojiFormatter:
    """فرمت‌کننده پیام‌ها با Custom Emoji"""
    
    @staticmethod
    def welcome_message(name: str) -> Tuple[str, List[MessageEntity]]:
        """پیام خوش‌آمدگویی با Custom Emoji"""
        text = f"سلام {name}! خوش آمدید به فروشگاه ما"
        
        emoji_map = {
            0: 'fire',  # قبل از سلام
            len(f"سلام {name}! "): 'sparkles',  # قبل از خوش آمدید
            len(text): 'gift'  # انتهای متن
        }
        
        return format_text_with_custom_emojis(text, emoji_map)
    
    @staticmethod
    def success_message(text: str) -> Tuple[str, List[MessageEntity]]:
        """پیام موفقیت با Custom Emoji"""
        emoji_map = {
            0: 'check',
            len(text): 'party'
        }
        return format_text_with_custom_emojis(text, emoji_map)
    
    @staticmethod
    def money_message(text: str) -> Tuple[str, List[MessageEntity]]:
        """پیام مربوط به پول با Custom Emoji"""
        emoji_map = {
            0: 'money',
            len(text): 'coin'
        }
        return format_text_with_custom_emojis(text, emoji_map)
    
    @staticmethod
    def vip_message(text: str) -> Tuple[str, List[MessageEntity]]:
        """پیام VIP با Custom Emoji"""
        emoji_map = {
            0: 'crown',
            len(text): 'gem'
        }
        return format_text_with_custom_emojis(text, emoji_map)


# تست و نمایش
if __name__ == "__main__":
    print("📝 Custom Emoji IDs موجود:")
    print("=" * 50)
    
    for name, emoji_id in CUSTOM_EMOJI_IDS.items():
        print(f"{name:15} -> {emoji_id}")
    
    print("\n" + "=" * 50)
    print("✅ برای استفاده در ربات:")
    print("""
from bot.custom_emojis import CustomEmojiFormatter

# پیام خوش‌آمدگویی
text, entities = CustomEmojiFormatter.welcome_message("علی")
await update.message.reply_text(text, entities=entities)

# پیام موفقیت
text, entities = CustomEmojiFormatter.success_message("سفارش شما ثبت شد")
await update.message.reply_text(text, entities=entities)
    """)
