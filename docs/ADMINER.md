# راهنمای Adminer - پنل مدیریت دیتابیس

## دسترسی به پنل

بعد از اجرای Docker Compose، پنل Adminer در آدرس زیر در دسترس است:

```
http://localhost:8080
```

## ورود به پنل

### اطلاعات ورود:

- **System**: PostgreSQL
- **Server**: `postgres`
- **Username**: مقدار `DB_USER` از فایل `.env` (پیش‌فرض: `telegram_bot`)
- **Password**: مقدار `DB_PASSWORD` از فایل `.env` (پیش‌فرض: `changeme123`)
- **Database**: مقدار `DB_NAME` از فایل `.env` (پیش‌فرض: `telegram_shop`)

## قابلیت‌های Adminer

### 🗄️ مشاهده جداول

- **products**: لیست محصولات
- **accounts**: اکانت‌های موجود و فروخته شده
- **orders**: تمام سفارشات
- **settings**: تنظیمات سیستم

### 🔍 جستجو و فیلتر

می‌تونید داده‌ها رو جستجو، فیلتر و مرتب کنید.

### ✏️ ویرایش داده‌ها

می‌تونید داده‌ها رو مستقیماً ویرایش کنید (با احتیاط!)

### 📊 اجرای Query

می‌تونید SQL Query‌های سفارشی اجرا کنید:

```sql
-- مشاهده آمار فروش
SELECT 
    p.name,
    COUNT(o.id) as total_orders,
    SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END) as completed_orders,
    SUM(CASE WHEN o.status = 'completed' THEN o.amount ELSE 0 END) as revenue
FROM products p
LEFT JOIN orders o ON p.id = o.product_id
GROUP BY p.id, p.name;

-- اکانت‌های فروخته نشده
SELECT p.name, a.username, a.password
FROM accounts a
JOIN products p ON a.product_id = p.id
WHERE a.is_sold = FALSE;

-- آخرین سفارشات
SELECT 
    o.id,
    o.username,
    p.name as product,
    o.amount,
    o.status,
    o.created_at
FROM orders o
JOIN products p ON o.product_id = p.id
ORDER BY o.created_at DESC
LIMIT 10;
```

### 📥 Export و Import

- Export: خروجی گرفتن از دیتابیس (SQL, CSV, JSON)
- Import: وارد کردن داده‌ها

### 🔐 مدیریت کاربران

می‌تونید کاربران و دسترسی‌ها رو مدیریت کنید.

## نکات امنیتی

### ⚠️ هشدارهای مهم:

1. **پورت را در Production ببندید**:
   ```yaml
   adminer:
     ports:
       - "127.0.0.1:8080:8080"  # فقط localhost
   ```

2. **از رمز عبور قوی استفاده کنید**

3. **دسترسی مستقیم به Production را محدود کنید**

4. **پشتیبان‌گیری منظم**:
   ```bash
   # Backup دیتابیس
   docker exec telegram-shop-db pg_dump -U telegram_bot telegram_shop > backup.sql
   
   # Restore از backup
   docker exec -i telegram-shop-db psql -U telegram_bot telegram_shop < backup.sql
   ```

## Query‌های مفید

### مشاهده محصولات پرفروش:

```sql
SELECT 
    p.name,
    COUNT(o.id) as sales_count,
    SUM(o.amount) as total_revenue
FROM products p
JOIN orders o ON p.id = o.product_id
WHERE o.status = 'completed'
GROUP BY p.id, p.name
ORDER BY sales_count DESC;
```

### کاربران فعال:

```sql
SELECT 
    username,
    COUNT(*) as order_count,
    SUM(amount) as total_spent
FROM orders
WHERE status = 'completed'
GROUP BY user_id, username
ORDER BY total_spent DESC;
```

### آمار روزانه:

```sql
SELECT 
    DATE(created_at) as date,
    COUNT(*) as orders,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) as revenue
FROM orders
GROUP BY DATE(created_at)
ORDER BY date DESC
LIMIT 30;
```

## دسترسی از راه دور

اگر می‌خواید از راه دور به Adminer دسترسی داشته باشید:

### با Nginx Reverse Proxy:

```nginx
server {
    listen 80;
    server_name db.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### با SSH Tunnel:

```bash
ssh -L 8080:localhost:8080 user@your-server
```

بعدش به `http://localhost:8080` در مرورگر محلی خود بروید.

## عیب‌یابی

### نمی‌توانم وارد شوم:

1. بررسی کنید Docker Compose اجرا شده باشد:
   ```bash
   docker-compose ps
   ```

2. بررسی کنید PostgreSQL سالم است:
   ```bash
   docker-compose logs postgres
   ```

3. رمز عبور را چک کنید در `.env`

### خطای اتصال:

1. بررسی کنید `postgres` container در حال اجرا باشد
2. منتظر بمانید تا PostgreSQL کاملاً آماده شود (حدود 10 ثانیه)

## منابع

- [Adminer Documentation](https://www.adminer.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
