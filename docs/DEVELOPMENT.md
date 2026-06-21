# راهنمای توسعه

## نصب محیط توسعه

### ۱. کلون کردن پروژه

```bash
git clone https://github.com/yourusername/telegram-shop-bot.git
cd telegram-shop-bot
```

### ۲. ایجاد محیط مجازی پایتون

```bash
python -m venv venv

# فعال‌سازی در لینوکس/مک
source venv/bin/activate

# فعال‌سازی در ویندوز
venv\Scripts\activate
```

### ۳. نصب پکیج‌ها

```bash
pip install -r requirements.txt
```

### ۴. تنظیم محیط

```bash
cp .env.example .env
# ویرایش .env و وارد کردن اطلاعات
```

### ۵. اجرای ربات

```bash
python run_local.py
```

## ساختار کد

### bot/main.py
فایل اصلی که ربات را راه‌اندازی می‌کند و هندلرها را ثبت می‌کند.

### bot/config.py
مدیریت تنظیمات و متغیرهای محیطی.

### bot/database.py
کلاس Database که تمام عملیات دیتابیس را مدیریت می‌کند.

### bot/handlers/
- `user.py`: هندلرهای مربوط به کاربران عادی
- `admin.py`: هندلرهای پنل ادمین

### bot/keyboards/
- `inline.py`: کیبوردهای اینلاین تلگرام

## افزودن قابلیت جدید

### ۱. افزودن هندلر جدید

```python
# در bot/handlers/user.py یا admin.py

async def my_new_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """توضیحات هندلر"""
    query = update.callback_query
    await query.answer()
    
    # کد شما
    
    await query.edit_message_text("پیام جدید")
```

### ۲. ثبت هندلر در main.py

```python
from bot.handlers.user import my_new_handler

# در تابع main()
application.add_handler(
    CallbackQueryHandler(my_new_handler, pattern="^my_pattern$")
)
```

### ۳. افزودن دکمه جدید

```python
# در bot/keyboards/inline.py

def my_new_keyboard():
    keyboard = [
        [InlineKeyboardButton("دکمه من", callback_data="my_pattern")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="start")]
    ]
    return InlineKeyboardMarkup(keyboard)
```

## افزودن جدول جدید به دیتابیس

```python
# در bot/database.py -> init_db()

await db.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field1 TEXT NOT NULL,
        field2 INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
```

## تست

### تست دستی

```bash
python run_local.py
```

### تست تنظیمات

```bash
python test_setup.py
```

## دیباگ

### فعال کردن لاگ‌های بیشتر

```python
# در bot/main.py
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # تغییر به DEBUG
)
```

### مشاهده لاگ‌های Docker

```bash
docker-compose logs -f
```

## بهترین روش‌ها

### ۱. همیشه از async/await استفاده کنید

```python
# ✅ درست
async def my_handler(update, context):
    result = await db.get_products()
    
# ❌ غلط
def my_handler(update, context):
    result = db.get_products()
```

### ۲. مدیریت خطا

```python
async def my_handler(update, context):
    try:
        # کد شما
        pass
    except Exception as e:
        logger.error(f"خطا: {e}")
        await update.effective_message.reply_text("خطایی رخ داد")
```

### ۳. بستن اتصالات دیتابیس

```python
# استفاده از context manager
async with aiosqlite.connect(self.db_path) as db:
    # عملیات دیتابیس
    pass
# اتصال خودکار بسته می‌شود
```

### ۴. اعتبارسنجی ورودی

```python
try:
    price = int(user_input.replace(',', ''))
    if price <= 0:
        raise ValueError
except ValueError:
    await update.message.reply_text("قیمت نامعتبر است")
    return
```

## مشارکت

### ۱. Fork کردن پروژه

### ۲. ایجاد برنچ جدید

```bash
git checkout -b feature/my-new-feature
```

### ۳. Commit کردن تغییرات

```bash
git commit -am 'Add some feature'
```

### ۴. Push کردن برنچ

```bash
git push origin feature/my-new-feature
```

### ۵. ایجاد Pull Request

## منابع مفید

- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [aiosqlite Documentation](https://aiosqlite.omnilib.dev/)
- [Docker Documentation](https://docs.docker.com/)

## سوالات متداول

**Q: چطور چند ادمین داشته باشم؟**

A: در `bot/config.py`:
```python
ADMIN_IDS = [int(id) for id in os.getenv('ADMIN_IDS', '').split(',')]

def is_admin(user_id):
    return user_id in ADMIN_IDS
```

**Q: چطور تصاویر محصول اضافه کنم؟**

A: یک فیلد `image_file_id` به جدول products اضافه کنید و از `send_photo` استفاده کنید.

**Q: چطور پرداخت آنلاین اضافه کنم؟**

A: از [Telegram Payments API](https://core.telegram.org/bots/payments) استفاده کنید یا یک درگاه پرداخت ایرانی مثل زرین‌پال متصل کنید.
