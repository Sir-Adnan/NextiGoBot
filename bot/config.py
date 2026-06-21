import os
from dotenv import load_dotenv

load_dotenv()

# تنظیمات ربات
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

# تنظیمات پرداخت
CARD_NUMBER = os.getenv('CARD_NUMBER', '1234-5678-9012-3456')
CARD_HOLDER_NAME = os.getenv('CARD_HOLDER_NAME', 'نام دارنده کارت')

# تنظیمات دیتابیس PostgreSQL
DB_USER = os.getenv('DB_USER', 'telegram_bot')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme123')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'telegram_shop')

# URL دیتابیس
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# تنظیمات عمومی
ORDER_EXPIRE_TIME = int(os.getenv('ORDER_EXPIRE_TIME', 30))
USE_PREMIUM_EMOJIS = os.getenv('USE_PREMIUM_EMOJIS', 'true').lower() == 'true'

# بررسی تنظیمات ضروری
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN تنظیم نشده است!")

if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID تنظیم نشده است!")
