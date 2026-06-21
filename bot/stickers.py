"""
مدیریت استیکرهای پریمیوم و انیمیشن‌دار
"""
from telegram import Bot, Update
from telegram.ext import ContextTypes
import random


class StickerManager:
    """مدیریت استیکرهای ربات"""
    
    # Sticker Set IDs - می‌تونید استیکر پک‌های خودتون رو اضافه کنید
    # این استیکرها رایگان و عمومی هستند
    
    # استیکرهای موفقیت
    SUCCESS_STICKERS = [
        'CAACAgQAAxkBAAIBaGZvYxK4AAFqJlxfVvXKBw5teLBIAAJNEAAC5c4hUqB5gv2J4VanNQQ',  # ✅ Success
        'CAACAgQAAxkBAAIBamZvYzB-pHdAAcPqS1NeGrTw0MQwAAJOEAAC5c4hUpXB8gxfKiQaNQQ',  # 🎉 Party
    ]
    
    # استیکرهای خطا
    ERROR_STICKERS = [
        'CAACAgQAAxkBAAIBbGZvY0k5Yh_WTDxo7AABLfvN8WQBmwACTxAAC5c4hUhNfGKAAQxTZgzUE',  # ❌ Error
    ]
    
    # استیکرهای انتظار
    WAITING_STICKERS = [
        'CAACAgQAAxkBAAIBbmZvY2J4iAABY_hqLKHU2gk-7f0SWAACUBAAAvXOIVJNZm2gABUShTUE',  # ⏳ Waiting
    ]
    
    # استیکرهای خوش‌آمدگویی
    WELCOME_STICKERS = [
        'CAACAgQAAxkBAAIBcGZvY3rjl0QVE8g9wAABuAABvPl2P6oAAVEQAAL1ziFSdWJtoAABCQkdNQQ',  # 👋 Hello
    ]
    
    # استیکرهای فروش
    SHOPPING_STICKERS = [
        'CAACAgQAAxkBAAIBcmZvY5LNkNH8AAHqQoABTxsHQkCdAABSEAAC9c4hUnYAAbmGBQHGNQQ',  # 🛍️ Shopping
        'CAACAgQAAxkBAAIBdGZvY6rLZGBcnBUAAZ9hIVL0AATYagACUxAAAvXOIVJ7xAABNn4plDU0',  # 💰 Money
    ]
    
    # استیکرهای ادمین
    ADMIN_STICKERS = [
        'CAACAgQAAxkBAAIBdmZvY8KZl0c7egABAAHqBxLJP2n3gAJUEAAC9c4hUvh1uJIAAbOQNQQ',  # 👑 Crown
    ]
    
    @staticmethod
    async def send_random_sticker(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        sticker_category: str = 'success'
    ):
        """
        ارسال استیکر تصادفی از یک دسته
        
        Args:
            update: Update object
            context: Context object
            sticker_category: نوع استیکر (success, error, waiting, welcome, shopping, admin)
        """
        sticker_lists = {
            'success': StickerManager.SUCCESS_STICKERS,
            'error': StickerManager.ERROR_STICKERS,
            'waiting': StickerManager.WAITING_STICKERS,
            'welcome': StickerManager.WELCOME_STICKERS,
            'shopping': StickerManager.SHOPPING_STICKERS,
            'admin': StickerManager.ADMIN_STICKERS,
        }
        
        stickers = sticker_lists.get(sticker_category, StickerManager.SUCCESS_STICKERS)
        
        if stickers:
            sticker = random.choice(stickers)
            if update.message:
                await update.message.reply_sticker(sticker)
            elif update.callback_query:
                await context.bot.send_sticker(
                    chat_id=update.effective_chat.id,
                    sticker=sticker
                )
    
    @staticmethod
    async def send_success_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ارسال استیکر موفقیت"""
        await StickerManager.send_random_sticker(update, context, 'success')
    
    @staticmethod
    async def send_welcome_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ارسال استیکر خوش‌آمدگویی"""
        await StickerManager.send_random_sticker(update, context, 'welcome')
    
    @staticmethod
    async def send_shopping_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ارسال استیکر خرید"""
        await StickerManager.send_random_sticker(update, context, 'shopping')


# استیکرهای انیمیشن‌دار (Premium)
class AnimatedStickers:
    """استیکرهای انیمیشن‌دار پریمیوم"""
    
    # برای استفاده از استیکرهای انیمیشن‌دار:
    # 1. استیکر پک انیمیشن‌دار بسازید
    # 2. با @Stickers ربات آپلود کنید
    # 3. File ID رو اینجا اضافه کنید
    
    PREMIUM_SUCCESS = None  # File ID استیکر انیمیشن‌دار موفقیت
    PREMIUM_FIRE = None  # File ID استیکر آتش انیمیشن‌دار
    PREMIUM_MONEY = None  # File ID استیکر پول انیمیشن‌دار
    
    @staticmethod
    async def send_premium_sticker(
        bot: Bot,
        chat_id: int,
        sticker_type: str = 'success'
    ):
        """ارسال استیکر پریمیوم"""
        sticker_map = {
            'success': AnimatedStickers.PREMIUM_SUCCESS,
            'fire': AnimatedStickers.PREMIUM_FIRE,
            'money': AnimatedStickers.PREMIUM_MONEY,
        }
        
        sticker_id = sticker_map.get(sticker_type)
        
        if sticker_id:
            await bot.send_sticker(chat_id=chat_id, sticker=sticker_id)


# راهنمای دریافت File ID استیکرها
"""
برای دریافت File ID استیکرها:

1. استیکر رو به ربات خودتون بفرستید
2. از این کد استفاده کنید:

```python
async def get_sticker_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.sticker:
        sticker_id = update.message.sticker.file_id
        await update.message.reply_text(f"Sticker ID: `{sticker_id}`", parse_mode='Markdown')

# اضافه کردن handler
application.add_handler(MessageHandler(filters.Sticker.ALL, get_sticker_id))
```

3. File ID رو در این فایل ذخیره کنید
4. از اون استیکر در پیام‌های مختلف استفاده کنید
"""


# Helper function برای استفاده آسان
async def send_celebration_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال استیکر جشن برای موفقیت"""
    await StickerManager.send_success_sticker(update, context)


async def send_shop_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال استیکر خرید"""
    await StickerManager.send_shopping_sticker(update, context)
