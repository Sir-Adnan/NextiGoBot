# 🚀 راهنمای ارتقا به نسخه جدید

## تغییرات مهم نسخه 2.0

### ✨ قابلیت‌های جدید

1. **ایموجی‌های پریمیوم تلگرام** 🔥
   - استفاده از ایموجی‌های انیمیشن‌دار
   - رابط کاربری زیباتر و جذاب‌تر
   - پشتیبانی از Custom Emoji IDs

2. **دیتابیس PostgreSQL** 🗄️
   - جایگزینی SQLite با PostgreSQL
   - عملکرد بهتر و سریع‌تر
   - پشتیبانی از transaction‌های پیچیده
   - امکان scale کردن

3. **پنل مدیریت Adminer** 🎛️
   - دسترسی گرافیکی به دیتابیس
   - مدیریت آسان داده‌ها
   - اجرای Query‌های SQL
   - Export و Import داده‌ها

4. **آمار فروش** 📊
   - نمایش آمار کامل فروش
   - تعداد سفارشات و درآمد
   - وضعیت موجودی اکانت‌ها

## مهاجرت از نسخه قدیم

### گام 1: پشتیبان‌گیری

اگر نسخه قبلی رو دارید، اول از دیتابیس SQLite بکاپ بگیرید:

```bash
cp data/bot.db data/bot.db.backup
```

### گام 2: به‌روزرسانی فایل‌ها

```bash
# Pull کردن آخرین تغییرات
git pull origin main

# نصب پکیج‌های جدید
pip install -r requirements.txt
```

### گام 3: تنظیم محیط جدید

فایل `.env` قدیمی را به‌روز کنید:

```env
# تنظیمات قدیمی (حذف کنید)
# DB_PATH=/app/data/bot.db

# تنظیمات جدید (اضافه کنید)
POSTGRES_DB=telegram_shop
POSTGRES_USER=telegram_bot
POSTGRES_PASSWORD=changeme123
DB_HOST=postgres
DB_PORT=5432
USE_PREMIUM_EMOJIS=true
```

### گام 4: مهاجرت داده‌ها (اختیاری)

اگر می‌خواید داده‌های قدیمی رو منتقل کنید، از اسکریپت مهاجرت استفاده کنید:

```bash
python migrate_sqlite_to_postgres.py
```

### گام 5: اجرای سیستم جدید

```bash
# حذف کانتینرهای قدیمی
docker-compose down

# اجرای سیستم جدید
docker-compose up -d

# مشاهده لاگ‌ها
docker-compose logs -f telegram-bot
```

## دسترسی به Adminer

بعد از اجرا، به آدرس زیر بروید:

```
http://localhost:8080
```

اطلاعات ورود:
- **System**: PostgreSQL
- **Server**: postgres
- **Username**: telegram_bot
- **Password**: changeme123
- **Database**: telegram_shop

## بررسی عملکرد

### 1. تست ربات

```bash
# ارسال /start به ربات
# بررسی نمایش ایموجی‌ها
# تست خرید محصول
```

### 2. تست دیتابیس

```bash
# اتصال به PostgreSQL
docker exec -it telegram-shop-db psql -U telegram_bot -d telegram_shop

# مشاهده جداول
\dt

# خروج
\q
```

### 3. مشاهده لاگ‌ها

```bash
docker-compose logs -f
```

## مشکلات رایج و راه‌حل

### ربات استارت نمی‌شود

```bash
# بررسی وضعیت
docker-compose ps

# مشاهده لاگ خطا
docker-compose logs telegram-bot
```

### PostgreSQL متصل نمی‌شود

```bash
# ری‌استارت دیتابیس
docker-compose restart postgres

# منتظر بمانید تا healthy شود
docker-compose ps
```

### Adminer باز نمی‌شود

```bash
# بررسی پورت
netstat -an | grep 8080

# ری‌استارت Adminer
docker-compose restart adminer
```

### خطای Migration

اگر مهاجرت داده‌ها با خطا مواجه شد:

```bash
# ریست کامل دیتابیس
docker-compose down -v
docker-compose up -d

# دوباره Migration را امتحان کنید
```

## بازگشت به نسخه قدیم

اگر مشکلی پیش آمد و می‌خواید به نسخه قدیم برگردید:

```bash
# توقف سیستم جدید
docker-compose down

# برگشت به commit قبلی
git checkout <previous-commit-hash>

# اجرای نسخه قدیم
docker-compose up -d
```

## پشتیبانی

برای کمک بیشتر:

- [مستندات کامل](docs/)
- [گزارش مشکل](https://github.com/yourusername/telegram-shop-bot/issues)
- [راهنمای Adminer](docs/ADMINER.md)

## نکات عملکردی

### 1. Backup خودکار

اضافه کردن Cron Job برای بکاپ روزانه:

```bash
# افزودن به crontab
0 2 * * * docker exec telegram-shop-db pg_dump -U telegram_bot telegram_shop > /backup/db_$(date +\%Y\%m\%d).sql
```

### 2. Monitoring

نصب ابزارهای مانیتورینگ:

```bash
# pgAdmin برای مدیریت پیشرفته
# Grafana برای نمایش آمار
# Prometheus برای جمع‌آوری متریک‌ها
```

### 3. Security

تنظیمات امنیتی اضافی:

```yaml
# در docker-compose.yml
adminer:
  ports:
    - "127.0.0.1:8080:8080"  # فقط localhost
```

## Performance Tips

1. **Connection Pooling**: تنظیم شده در `database_new.py`
2. **Index‌ها**: برای Query‌های پرتکرار Index بسازید
3. **Cache**: Redis برای کش کردن داده‌ها

## بهترین روش‌ها

- همیشه قبل از آپدیت، بکاپ بگیرید
- محیط توسعه جدا از پروداکشن داشته باشید
- از Git برای version control استفاده کنید
- لاگ‌ها را منظم بررسی کنید
- از Adminer فقط در محیط امن استفاده کنید
