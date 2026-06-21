import aiosqlite
from datetime import datetime
from typing import List, Optional, Dict
from bot.config import DB_PATH


class Database:
    def __init__(self):
        self.db_path = DB_PATH
    
    async def init_db(self):
        """ایجاد جداول دیتابیس"""
        async with aiosqlite.connect(self.db_path) as db:
            # جدول محصولات
            await db.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price INTEGER NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول اکانت‌ها
            await db.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    details TEXT,
                    is_sold INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            # جدول سفارشات
            await db.execute('''
                CREATE TABLE IF NOT EXISTS orders (
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
            ''')
            
            await db.commit()
    
    # ============= محصولات =============
    
    async def add_product(self, name: str, description: str, price: int) -> int:
        """افزودن محصول جدید"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'INSERT INTO products (name, description, price) VALUES (?, ?, ?)',
                (name, description, price)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_products(self, active_only: bool = True) -> List[Dict]:
        """دریافت لیست محصولات"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if active_only:
                cursor = await db.execute(
                    'SELECT * FROM products WHERE is_active = 1 ORDER BY id DESC'
                )
            else:
                cursor = await db.execute('SELECT * FROM products ORDER BY id DESC')
            
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_product(self, product_id: int) -> Optional[Dict]:
        """دریافت اطلاعات یک محصول"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def update_product_status(self, product_id: int, is_active: bool):
        """تغییر وضعیت فعال/غیرفعال محصول"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'UPDATE products SET is_active = ? WHERE id = ?',
                (1 if is_active else 0, product_id)
            )
            await db.commit()
    
    # ============= اکانت‌ها =============
    
    async def add_account(self, product_id: int, username: str, password: str, details: str = None) -> int:
        """افزودن اکانت جدید"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'INSERT INTO accounts (product_id, username, password, details) VALUES (?, ?, ?, ?)',
                (product_id, username, password, details)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_available_account(self, product_id: int) -> Optional[Dict]:
        """دریافت یک اکانت فروخته نشده"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                'SELECT * FROM accounts WHERE product_id = ? AND is_sold = 0 LIMIT 1',
                (product_id,)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def get_accounts_count(self, product_id: int) -> Dict[str, int]:
        """دریافت تعداد اکانت‌های موجود و فروخته شده"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'SELECT COUNT(*) as total, SUM(is_sold) as sold FROM accounts WHERE product_id = ?',
                (product_id,)
            )
            row = await cursor.fetchone()
            total = row[0] or 0
            sold = row[1] or 0
            return {'total': total, 'available': total - sold, 'sold': sold}
    
    async def mark_account_sold(self, account_id: int):
        """علامت‌گذاری اکانت به عنوان فروخته شده"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'UPDATE accounts SET is_sold = 1 WHERE id = ?',
                (account_id,)
            )
            await db.commit()
    
    # ============= سفارشات =============
    
    async def create_order(self, user_id: int, username: str, product_id: int, amount: int) -> int:
        """ایجاد سفارش جدید"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'INSERT INTO orders (user_id, username, product_id, amount, status) VALUES (?, ?, ?, ?, ?)',
                (user_id, username, product_id, amount, 'pending')
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_order(self, order_id: int) -> Optional[Dict]:
        """دریافت اطلاعات سفارش"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def update_order_receipt(self, order_id: int, receipt_file_id: str):
        """ذخیره رسید پرداخت"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'UPDATE orders SET payment_receipt = ? WHERE id = ?',
                (receipt_file_id, order_id)
            )
            await db.commit()
    
    async def complete_order(self, order_id: int, account_id: int):
        """تکمیل سفارش و تخصیص اکانت"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'UPDATE orders SET status = ?, account_id = ?, completed_at = ? WHERE id = ?',
                ('completed', account_id, datetime.now(), order_id)
            )
            await db.commit()
    
    async def reject_order(self, order_id: int):
        """رد کردن سفارش"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'UPDATE orders SET status = ? WHERE id = ?',
                ('rejected', order_id)
            )
            await db.commit()
    
    async def get_pending_orders(self) -> List[Dict]:
        """دریافت سفارشات در انتظار تایید"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                'SELECT * FROM orders WHERE status = "pending" ORDER BY created_at DESC'
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_user_orders(self, user_id: int) -> List[Dict]:
        """دریافت سفارشات یک کاربر"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
                (user_id,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_account(self, account_id: int) -> Optional[Dict]:
        """دریافت اطلاعات اکانت"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None


# نمونه سراسری دیتابیس
db = Database()
