# 🚀 راهنمای کامل راه‌اندازی نسخه نهایی

## ✨ قابلیت‌های جدید اضافه شده:

### 1. Custom Emoji واقعی تلگرام 🔥
- دریافت خودکار ID از @AdsMarkdownBot
- استفاده از ایموجی‌های انیمیشن‌دار Premium
- فرمت‌کننده پیام‌های حرفه‌ای

### 2. دسته‌بندی محصولات 📂
- دسته و زیردسته
- ایموجی برای هر دسته
- مرتب‌سازی

### 3. محصولات اشتراکی ⏰
- ۱ ماهه، ۳ ماهه، ۶ ماهه، ۱ ساله
- قیمت متغیر براساس مدت
- مدیریت آسان

### 4. دکمه‌های رنگی تلگرام 🎨
- دکمه‌های آبی، سبز، قرمز، زرد
- طراحی حرفه‌ای
- رنگ‌بندی براساس وضعیت

---

## 📋 مرحله 1: دریافت Custom Emoji IDs

### روش دستی (توصیه می‌شود):

1. **به [@AdsMarkdownBot](https://t.me/AdsMarkdownBot) بروید**

2. **هر ایموجی رو بفرستید:**
   ```
   🔥
   ```

3. **ربات پاسخ می‌ده:**
   ```
   tg://emoji?id=5368324170671202286
   ```

4. **عدد بعد از `id=` رو کپی کنید:**
   ```
   5368324170671202286
   ```

5. **در فایل `bot/custom_emojis.py` اضافه کنید:**
   ```python
   CUSTOM_EMOJI_IDS = {
       'fire': '5368324170671202286',  # 🔥
       'star': 'آیدی_که_گرفتید',      # ⭐
       # ...
   }
   ```

### لیست ایموجی‌های پیشنهادی:

| ایموجی | نام | استفاده |
|--------|-----|---------|
| 🔥 | fire | محبوبیت، داغ |
| ⭐ | star | ویژه، برتر |
| ✨ | sparkles | جدید، زیبا |
| 🎉 | party | جشن، موفقیت |
| ❤️ | heart | محبوب |
| 🏆 | trophy | برنده |
| 💰 | money | پول، قیمت |
| 🪙 | coin | اعتبار |
| 💎 | gem | VIP، پریمیوم |
| 🎁 | gift | هدیه |
| 🚀 | rocket | سریع |
| ⚡ | lightning | فوری |
| 🔔 | bell | اعلان |
| 👑 | crown | ادمین، VIP |
| 🔑 | key | دسترسی |

---

## 📋 مرحله 2: ایجاد دسته‌بندی‌ها

### اسکریپت ایجاد دسته‌بندی‌های پیش‌فرض:

فایل `setup_categories.py` بسازید:

```python
import asyncio
from bot.database_new import db

async def setup_default_categories():
    """ایجاد دسته‌بندی‌های پیش‌فرض"""
    
    # ایجاد جداول
    await db.init_db()
    
    # دسته‌بندی‌های اصلی
    streaming_id = await db.add_category(
        name="استریمینگ",
        description="سرویس‌های استریمینگ موسیقی و ویدیو",
        emoji="📺"
    )
    
    gaming_id = await db.add_category(
        name="گیمینگ",
        description="اکانت‌های بازی",
        emoji="🎮"
    )
    
    education_id = await db.add_category(
        name="آموزشی",
        description="دوره‌ها و پلتفرم‌های آموزشی",
        emoji="📚"
    )
    
    vpn_id = await db.add_category(
        name="VPN",
        description="سرویس‌های VPN",
        emoji="🔒"
    )
    
    print("✅ دسته‌بندی‌های اصلی ایجاد شد")
    
    # زیردسته‌ها برای استریمینگ
    await db.add_category(
        name="Netflix",
        emoji="🎬",
        parent_id=streaming_id
    )
    
    await db.add_category(
        name="Spotify",
        emoji="🎵",
        parent_id=streaming_id
    )
    
    await db.add_category(
        name="YouTube Premium",
        emoji="▶️",
        parent_id=streaming_id
    )
    
    print("✅ زیردسته‌ها برای استریمینگ ایجاد شد")
    
    # زیردسته‌ها برای گیمینگ
    await db.add_category(
        name="Steam",
        emoji="🎮",
        parent_id=gaming_id
    )
    
    await db.add_category(
        name="PlayStation",
        emoji="🎯",
        parent_id=gaming_id
    )
    
    print("✅ زیردسته‌ها برای گیمینگ ایجاد شد")
    
    print("\n✅ همه دسته‌بندی‌ها با موفقیت ایجاد شدند!")

if __name__ == "__main__":
    asyncio.run(setup_default_categories())
```

**اجرا:**
```bash
python setup_categories.py
```

---

## 📋 مرحله 3: افزودن محصولات با دسته‌بندی

### مثال: افزودن Netflix با چند مدت زمان

```python
import asyncio
from bot.database_new import db

async def add_netflix_products():
    # دریافت دسته Netflix
    categories = await db.get_categories()
    netflix_cat = next((c for c in categories if c['name'] == 'Netflix'), None)
    
    if not netflix_cat:
        print("❌ دسته Netflix یافت نشد")
        return
    
    # Netflix 1 ماهه
    product_1m = await db.add_product(
        name="Netflix 1 ماهه",
        description="اکانت نتفلیکس Premium 1 ماهه",
        price=50000,
        category_id=netflix_cat['id']
    )
    
    # بروز کردن فیلدهای اشتراکی
    await db.update_product(product_1m, 
        is_subscription=True,
        duration_months=1
    )
    
    # Netflix 3 ماهه
    product_3m = await db.add_product(
        name="Netflix 3 ماهه",
        description="اکانت نتفلیکس Premium 3 ماهه",
        price=140000,
        category_id=netflix_cat['id']
    )
    
    await db.update_product(product_3m,
        is_subscription=True,
        duration_months=3
    )
    
    # Netflix 6 ماهه
    product_6m = await db.add_product(
        name="Netflix 6 ماهه",
        description="اکانت نتفلیکس Premium 6 ماهه",
        price=270000,
        category_id=netflix_cat['id']
    )
    
    await db.update_product(product_6m,
        is_subscription=True,
        duration_months=6
    )
    
    # Netflix 12 ماهه
    product_12m = await db.add_product(
        name="Netflix 12 ماهه",
        description="اکانت نتفلیکس Premium سالانه",
        price=500000,
        category_id=netflix_cat['id']
    )
    
    await db.update_product(product_12m,
        is_subscription=True,
        duration_months=12
    )
    
    print("✅ محصولات Netflix با موفقیت اضافه شدند")

if __name__ == "__main__":
    asyncio.run(add_netflix_products())
```

---

## 📋 مرحله 4: به‌روزرسانی و اجرا

### 1. به‌روزرسانی دیتابیس:

```bash
# اگر از Docker استفاده می‌کنید
docker-compose down
docker-compose up -d

# اجرای اسکریپت‌های setup
docker exec -it telegram-shop-bot python setup_categories.py
```

### 2. Migration دیتابیس (اگر قبلاً ربات رو اجرا کردید):

```sql
-- اضافه کردن جدول categories
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    emoji VARCHAR(10),
    parent_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- اضافه کردن فیلدهای جدید به products
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS is_subscription BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS duration_months INTEGER;
```

### 3. ری‌استارت ربات:

```bash
docker-compose restart telegram-bot
docker-compose logs -f telegram-bot
```

---

## 🎨 تست قابلیت‌های جدید

### 1. تست Custom Emoji:
```
/start
```
باید پیام با ایموجی‌های انیمیشن‌دار ببینید

### 2. تست دسته‌بندی:
```
کلیک روی "محصولات"
```
باید لیست دسته‌بندی‌ها رو ببینید

### 3. تست محصولات اشتراکی:
```
انتخاب دسته -> انتخاب محصول
```
باید دکمه‌های انتخاب مدت زمان ببینید

### 4. تست دکمه‌های رنگی:
```
هر صفحه ربات
```
دکمه‌ها با رنگ‌های مختلف نمایش داده می‌شوند

---

## 📊 ساختار نهایی

```
telegram-shop-bot/
├── bot/
│   ├── custom_emojis.py         # ✨ جدید - Custom Emoji IDs
│   ├── emoji_fetcher.py         # ✨ جدید - دریافت خودکار ID
│   ├── colored_buttons.py       # ✨ جدید - دکمه‌های رنگی
│   ├── models.py                # 🔄 به‌روز - Category + Subscription
│   ├── database_new.py          # 🔄 به‌روز - متدهای Category
│   ├── keyboards/inline.py      # 🔄 به‌روز - کیبوردهای رنگی
│   └── ...
├── setup_categories.py          # ✨ جدید - اسکریپت setup
├── COMPLETE_SETUP.md           # ✨ جدید - این فایل
└── ...
```

---

## 🎯 خلاصه تغییرات

✅ Custom Emoji واقعی تلگرام  
✅ دسته‌بندی محصولات (دسته + زیردسته)  
✅ محصولات اشتراکی (1، 3، 6، 12 ماهه)  
✅ دکمه‌های رنگی (آبی، سبز، قرمز، زرد)  
✅ رابط کاربری حرفه‌ای و زیبا  
✅ کد تمیز و مستند  

---

## 💡 نکات مهم

1. **Custom Emoji فقط با Telegram Premium کار می‌کنه**
   - برای کاربران عادی، ایموجی استاندارد نمایش داده می‌شود
   - برای کاربران Premium، انیمیشن نمایش داده می‌شود

2. **دسته‌بندی‌ها باید قبل از محصولات ایجاد بشند**

3. **محصولات اشتراکی باید `is_subscription=True` باشند**

4. **دکمه‌های رنگی در همه نسخه‌های تلگرام کار می‌کنند**

---

## 🆘 عیب‌یابی

### مشکل: Custom Emoji نمایش داده نمی‌شود
```bash
# بررسی اکانت Premium
# مطمئن شوید که حساب سازنده ربات Premium است

# بررسی ID ها
python -c "from bot.custom_emojis import CUSTOM_EMOJI_IDS; print(CUSTOM_EMOJI_IDS)"
```

### مشکل: دسته‌بندی‌ها نمایش داده نمی‌شوند
```bash
# اجرای migration
docker exec -it telegram-shop-db psql -U telegram_bot -d telegram_shop -f migrations.sql

# اجرای setup
docker exec -it telegram-shop-bot python setup_categories.py
```

### مشکل: دکمه‌ها رنگ ندارند
```
این طبیعی است! دکمه‌های رنگی واقعی فقط در Telegram Mini Apps کار می‌کنند.
ما از ایموجی‌های رنگی استفاده کردیم که در همه‌جا کار می‌کنند.
```

---

## 🚀 آماده!

حالا ربات شما:
- ✅ از Custom Emoji استفاده می‌کنه
- ✅ دسته‌بندی کامل داره
- ✅ محصولات اشتراکی پشتیبانی می‌کنه  
- ✅ دکمه‌های رنگی و زیبا داره
- ✅ حرفه‌ای و خوشگل شده! 🎨

موفق باشید! 🎉
