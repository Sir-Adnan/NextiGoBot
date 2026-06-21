# 🤖 ربات تلگرام فروش محصولات و اکانت‌ها

ربات تلگرام حرفه‌ای برای مدیریت و فروش محصولات و اکانت‌ها با قابلیت پرداخت کارت به کارت

<div dir="rtl">

## ✨ قابلیت‌ها

- 🔐 سیستم احراز هویت ادمین
- 📦 مدیریت کامل محصولات (افزودن، فعال/غیرفعال کردن)
- 💳 پرداخت کارت به کارت با آپلود رسید
- 🎫 مدیریت اکانت‌ها و تخصیص خودکار
- 📊 پنل ادمین کامل و قدرتمند
- 🛒 سیستم خرید آسان برای مشتریان
- 📝 تاریخچه کامل سفارشات
- 🔄 تایید/رد سفارشات توسط ادمین
- 📱 رابط کاربری ساده و کاربرپسند
- 🐳 آماده اجرا با Docker
- 💾 دیتابیس SQLite یکپارچه

## 🚀 نصب سریع

### روش ۱: استفاده از Docker (توصیه می‌شود)

```bash
# کلون کردن پروژه
git clone https://github.com/yourusername/telegram-shop-bot.git
cd telegram-shop-bot

# کپی فایل تنظیمات
cp .env.example .env

# ویرایش .env و وارد کردن اطلاعات
nano .env

# اجرای ربات
docker-compose up -d
```

### روش ۲: اجرای مستقیم (برای توسعه)

```bash
# نصب پایتون ۳.۱۱+
# نصب پکیج‌ها
pip install -r requirements.txt

# کپی فایل تنظیمات
cp .env.example .env

# ویرایش .env
nano .env

# اجرای ربات
python run_local.py
```

## ⚙️ تنظیمات

فایل `.env` را ویرایش کنید:

```env
# توکن ربات از @BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# آیدی عددی ادمین از @userinfobot
ADMIN_ID=123456789

# اطلاعات کارت بانکی
CARD_NUMBER=1234-5678-9012-3456
CARD_HOLDER_NAME=علی احمدی

# مسیر دیتابیس
DB_PATH=/app/data/bot.db

# زمان انقضای سفارش (دقیقه)
ORDER_EXPIRE_TIME=30
```

## 📖 راهنمای استفاده

### برای ادمین:

1. **ورود به پنل**: `/start` → ⚙️ پنل ادمین
2. **افزودن محصول**: پنل ادمین → ➕ افزودن محصول
3. **افزودن اکانت**: مدیریت محصولات → انتخاب محصول → ➕ افزودن اکانت
4. **بررسی سفارشات**: پنل ادمین → 📋 سفارشات در انتظار
5. **تایید سفارش**: مشاهده رسید → ✅ تایید و ارسال

### برای مشتری:

1. **مشاهده محصولات**: `/start` → 🛍 محصولات
2. **خرید**: انتخاب محصول → 💳 خرید
3. **پرداخت**: واریز به کارت → ارسال رسید
4. **دریافت اکانت**: بعد از تایید ادمین، اطلاعات اکانت ارسال می‌شود

## 📁 ساختار پروژه

```
telegram-shop-bot/
├── bot/                      # پکیج اصلی ربات
│   ├── __init__.py
│   ├── main.py              # فایل اصلی
│   ├── config.py            # تنظیمات
│   ├── database.py          # دیتابیس
│   ├── handlers/            # هندلرهای ربات
│   │   ├── __init__.py
│   │   ├── admin.py        # هندلرهای ادمین
│   │   └── user.py         # هندلرهای کاربر
│   └── keyboards/           # کیبوردهای اینلاین
│       ├── __init__.py
│       └── inline.py
├── data/                    # دیتابیس (خودکار ایجاد می‌شود)
├── .env.example            # نمونه فایل تنظیمات
├── .gitignore
├── docker-compose.yml      # تنظیمات Docker
├── Dockerfile
├── requirements.txt        # پکیج‌های پایتون
├── run_local.py           # اجرای مستقیم
├── run.sh                 # اسکریپت اجرا
├── SETUP_FA.md           # راهنمای کامل نصب
└── README.md
```

## 🔧 دستورات مفید

```bash
# مشاهده لاگ‌ها
docker-compose logs -f

# مشاهده لاگ ربات
docker-compose logs -f telegram-bot

# مشاهده لاگ دیتابیس
docker-compose logs -f postgres

# توقف ربات
docker-compose down

# ری‌استارت
docker-compose restart

# ری‌بیلد (بعد از تغییر کد)
docker-compose up -d --build

# پاک کردن دیتابیس (خطرناک!)
docker-compose down -v

# Backup دیتابیس
docker exec telegram-shop-db pg_dump -U telegram_bot telegram_shop > backup.sql

# Restore از backup
docker exec -i telegram-shop-db psql -U telegram_bot telegram_shop < backup.sql

# دسترسی به shell PostgreSQL
docker exec -it telegram-shop-db psql -U telegram_bot -d telegram_shop
```

## 🛠 توسعه

برای توسعه و اضافه کردن قابلیت‌های جدید:

1. کد را کلون کنید
2. از `run_local.py` برای تست استفاده کنید
3. تغییرات را اعمال کنید
4. PR بفرستید!

## 🐛 عیب‌یابی

مشکلات رایج و راه‌حل:

**ربات استارت نمی‌شود:**
- توکن را چک کنید
- Docker را چک کنید

**پیام نمی‌دهد:**
- `/start` را بزنید
- ADMIN_ID را چک کنید

**خطای دیتابیس:**
```bash
docker-compose down -v
docker-compose up -d
```

## 📄 لایسنس

MIT License - استفاده آزاد

## 🤝 مشارکت

مشارکت‌ها خوش‌آمدید! لطفاً یک Issue یا PR باز کنید.

## 📞 پشتیبانی

- 📧 ایمیل: support@example.com
- 💬 تلگرام: @yourusername
- 🐛 گزارش باگ: [GitHub Issues](https://github.com/yourusername/telegram-shop-bot/issues)

</div>

---

<div align="center">

ساخته شده با ❤️ برای جامعه ایرانی

[راهنمای کامل فارسی](SETUP_FA.md) | [مستندات](docs/) | [دمو](https://t.me/yourbot)

</div>
