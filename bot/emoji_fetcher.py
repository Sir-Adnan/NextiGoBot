"""
ابزار خودکار برای دریافت Custom Emoji ID از @AdsMarkdownBot
"""
import asyncio
import re
from telegram import Bot
from telegram.error import TelegramError


class CustomEmojiIDFetcher:
    """دریافت خودکار Custom Emoji ID"""
    
    # ربات برای دریافت ID
    MARKDOWN_BOT = "@AdsMarkdownBot"
    
    # لیست ایموجی‌های مورد نظر
    EMOJIS_TO_FETCH = {
        'fire': '🔥',
        'star': '⭐',
        'sparkles': '✨',
        'party': '🎉',
        'heart': '❤️',
        'trophy': '🏆',
        'money': '💰',
        'coin': '🪙',
        'gem': '💎',
        'gift': '🎁',
        'rocket': '🚀',
        'lightning': '⚡',
        'bell': '🔔',
        'crown': '👑',
        'key': '🔑',
        'lock': '🔐',
        'shopping': '🛍️',
        'cart': '🛒',
        'box': '📦',
        'check': '✅',
        'cross': '❌',
        'warning': '⚠️',
    }
    
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
    
    async def send_emoji_to_bot(self, emoji: str) -> str:
        """
        ارسال ایموجی به @AdsMarkdownBot و دریافت ID
        
        توجه: این فانکشن نیاز به تعامل دستی با ربات دارد
        """
        try:
            # ارسال ایموجی به ربات Markdown
            message = await self.bot.send_message(
                chat_id="@AdsMarkdownBot",
                text=emoji
            )
            
            # منتظر پاسخ می‌مانیم
            await asyncio.sleep(2)
            
            # دریافت پاسخ
            # توجه: این قسمت نیاز به webhook یا polling دارد
            return None
            
        except TelegramError as e:
            print(f"خطا در ارسال ایموجی {emoji}: {e}")
            return None
    
    @staticmethod
    def extract_emoji_id(text: str) -> str:
        """استخراج Emoji ID از متن پاسخ"""
        # پترن برای پیدا کردن ID
        pattern = r'tg://emoji\?id=(\d+)'
        match = re.search(pattern, text)
        
        if match:
            return match.group(1)
        
        # پترن جایگزین
        pattern2 = r'custom_emoji_id["\s:]+(\d+)'
        match2 = re.search(pattern2, text)
        
        if match2:
            return match2.group(1)
        
        return None
    
    @staticmethod
    def generate_emoji_config() -> str:
        """تولید کد Python برای تنظیمات"""
        config = """
# Custom Emoji IDs - دریافت شده از @AdsMarkdownBot
CUSTOM_EMOJI_IDS = {
"""
        
        # این IDها رو باید دستی وارد کنید
        sample_ids = {
            'fire': '5368324170671202286',
            'star': '5359785904535774578',
            'sparkles': '5368324170671202286',
            'party': '5359553277988220506',
            'heart': '5370869711888194012',
            'trophy': '5370869711888194012',
            'money': '5370913841936801636',
            'rocket': '5370964809379046331',
        }
        
        for name, emoji_id in sample_ids.items():
            config += f"    '{name}': '{emoji_id}',\n"
        
        config += "}\n"
        
        return config


# راهنمای استفاده دستی
MANUAL_GUIDE = """
📝 راهنمای دریافت Custom Emoji ID:

1. به ربات @AdsMarkdownBot بروید
2. هر ایموجی رو بفرستید (مثلاً 🔥)
3. ربات یک پیام با markdown می‌فرسته
4. در پیام، کد شبیه این رو پیدا کنید:
   tg://emoji?id=5368324170671202286
   
5. عدد بعد از id= همان Custom Emoji ID است
6. این ID رو در فایل bot/custom_emojis.py ذخیره کنید

مثال:
ایموجی: 🔥
پاسخ ربات: tg://emoji?id=5368324170671202286
Custom Emoji ID: 5368324170671202286
"""


async def fetch_all_emoji_ids(bot_token: str):
    """دریافت خودکار همه IDها (نیاز به webhook)"""
    print(MANUAL_GUIDE)
    print("\n" + "="*50)
    print("⚠️ توجه: دریافت خودکار نیاز به راه‌اندازی webhook دارد")
    print("لطفاً به صورت دستی از @AdsMarkdownBot استفاده کنید")
    print("="*50 + "\n")
    
    # تولید کد کانفیگ
    config_code = CustomEmojiIDFetcher.generate_emoji_config()
    print("کد Python برای استفاده:")
    print(config_code)


if __name__ == "__main__":
    print(MANUAL_GUIDE)
    print("\nبرای دریافت خودکار (نیاز به webhook):")
    print("python bot/emoji_fetcher.py YOUR_BOT_TOKEN")
