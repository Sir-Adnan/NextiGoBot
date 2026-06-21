# مستندات دیتابیس

## ساختار دیتابیس

### جدول Products (محصولات)

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**فیلدها:**
- `id`: شناسه یکتا
- `name`: نام محصول
- `description`: توضیحات محصول
- `price`: قیمت به تومان
- `is_active`: وضعیت فعال/غیرفعال (1/0)
- `created_at`: تاریخ ایجاد

### جدول Accounts (اکانت‌ها)

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    details TEXT,
    is_sold INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
```

**فیلدها:**
- `id`: شناسه یکتا
- `product_id`: شناسه محصول مرتبط
- `username`: نام کاربری اکانت
- `password`: رمز عبور اکانت
- `details`: اطلاعات اضافی (اختیاری)
- `is_sold`: وضعیت فروخته شده (1/0)
- `created_at`: تاریخ ایجاد

### جدول Orders (سفارشات)

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    product_id INTEGER NOT NULL,
    account_id INTEGER,
    amount INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    payment_receipt TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (account_id) REFERENCES accounts (id)
)
```

**فیلدها:**
- `id`: شناسه یکتا
- `user_id`: شناسه کاربر تلگرام
- `username`: نام کاربری تلگرام
- `product_id`: شناسه محصول
- `account_id`: شناسه اکانت تخصیص داده شده
- `amount`: مبلغ پرداختی
- `status`: وضعیت سفارش (pending/completed/rejected)
- `payment_receipt`: شناسه فایل رسید
- `created_at`: تاریخ ایجاد
- `completed_at`: تاریخ تکمیل

## API دیتابیس

### متدهای محصول

#### `add_product(name, description, price)`
افزودن محصول جدید
```python
product_id = await db.add_product(
    name="اکانت نتفلیکس",
    description="اکانت پریمیوم 1 ماهه",
    price=50000
)
```

#### `get_products(active_only=True)`
دریافت لیست محصولات
```python
products = await db.get_products(active_only=True)
```

#### `get_product(product_id)`
دریافت یک محصول
```python
product = await db.get_product(1)
```

#### `update_product_status(product_id, is_active)`
تغییر وضعیت محصول
```python
await db.update_product_status(1, False)
```

### متدهای اکانت

#### `add_account(product_id, username, password, details=None)`
افزودن اکانت جدید
```python
account_id = await db.add_account(
    product_id=1,
    username="user@example.com",
    password="pass123",
    details="اطلاعات اضافی"
)
```

#### `get_available_account(product_id)`
دریافت اولین اکانت موجود
```python
account = await db.get_available_account(1)
```

#### `get_accounts_count(product_id)`
دریافت تعداد اکانت‌ها
```python
counts = await db.get_accounts_count(1)
# {'total': 10, 'available': 7, 'sold': 3}
```

#### `mark_account_sold(account_id)`
علامت‌گذاری اکانت به عنوان فروخته شده
```python
await db.mark_account_sold(1)
```

### متدهای سفارش

#### `create_order(user_id, username, product_id, amount)`
ایجاد سفارش جدید
```python
order_id = await db.create_order(
    user_id=123456789,
    username="user123",
    product_id=1,
    amount=50000
)
```

#### `get_order(order_id)`
دریافت اطلاعات سفارش
```python
order = await db.get_order(1)
```

#### `update_order_receipt(order_id, receipt_file_id)`
ذخیره رسید پرداخت
```python
await db.update_order_receipt(1, "AgACAgQAAxkBAAI...")
```

#### `complete_order(order_id, account_id)`
تکمیل سفارش
```python
await db.complete_order(1, 5)
```

#### `reject_order(order_id)`
رد کردن سفارش
```python
await db.reject_order(1)
```

#### `get_pending_orders()`
دریافت سفارشات در انتظار
```python
orders = await db.get_pending_orders()
```

#### `get_user_orders(user_id)`
دریافت سفارشات یک کاربر
```python
orders = await db.get_user_orders(123456789)
```

## نمونه استفاده

```python
from bot.database import db

# مقداردهی اولیه
await db.init_db()

# افزودن محصول
product_id = await db.add_product(
    name="اکانت Spotify",
    description="پریمیوم 3 ماهه",
    price=100000
)

# افزودن اکانت‌ها
for i in range(5):
    await db.add_account(
        product_id=product_id,
        username=f"user{i}@spotify.com",
        password=f"pass{i}123"
    )

# بررسی موجودی
counts = await db.get_accounts_count(product_id)
print(f"موجودی: {counts['available']}")

# ایجاد سفارش
order_id = await db.create_order(
    user_id=123456789,
    username="customer1",
    product_id=product_id,
    amount=100000
)

# تخصیص اکانت
account = await db.get_available_account(product_id)
await db.complete_order(order_id, account['id'])
await db.mark_account_sold(account['id'])
```
