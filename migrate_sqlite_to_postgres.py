#!/usr/bin/env python3
"""
اسکریپت مهاجرت داده از SQLite به PostgreSQL
"""

import asyncio
import aiosqlite
import os
from dotenv import load_dotenv
from bot.database_new import db as new_db

load_dotenv()

SQLITE_PATH = os.getenv('OLD_DB_PATH', 'data/bot.db')


async def migrate():
    """مهاجرت داده‌ها"""
    print("🚀 شروع مهاجرت داده‌ها...")
    print("-" * 50)
    
    # بررسی وجود فایل SQLite
    if not os.path.exists(SQLITE_PATH):
        print(f"❌ فایل SQLite یافت نشد: {SQLITE_PATH}")
        return
    
    # ایجاد جداول جدید
    print("📦 ایجاد جداول PostgreSQL...")
    await new_db.init_db()
    print("✅ جداول ایجاد شد")
    
    # اتصال به SQLite
    async with aiosqlite.connect(SQLITE_PATH) as sqlite_db:
        sqlite_db.row_factory = aiosqlite.Row
        
        # مهاجرت محصولات
        print("\n📦 مهاجرت محصولات...")
        cursor = await sqlite_db.execute('SELECT * FROM products')
        products = await cursor.fetchall()
        
        product_map = {}  # نقشه ID قدیم به جدید
        for product in products:
            new_id = await new_db.add_product(
                name=product['name'],
                description=product['description'],
                price=product['price']
            )
            product_map[product['id']] = new_id
            print(f"  ✓ {product['name']} (ID: {product['id']} -> {new_id})")
        
        print(f"✅ {len(products)} محصول منتقل شد")
        
        # مهاجرت اکانت‌ها
        print("\n🔐 مهاجرت اکانت‌ها...")
        cursor = await sqlite_db.execute('SELECT * FROM accounts')
        accounts = await cursor.fetchall()
        
        account_map = {}
        for account in accounts:
            new_product_id = product_map.get(account['product_id'])
            if new_product_id:
                new_id = await new_db.add_account(
                    product_id=new_product_id,
                    username=account['username'],
                    password=account['password'],
                    details=account.get('details')
                )
                account_map[account['id']] = new_id
                
                # اگر فروخته شده
                if account['is_sold']:
                    await new_db.mark_account_sold(new_id)
                
                status = "فروخته شده" if account['is_sold'] else "موجود"
                print(f"  ✓ {account['username']} ({status}) (ID: {account['id']} -> {new_id})")
        
        print(f"✅ {len(accounts)} اکانت منتقل شد")
        
        # مهاجرت سفارشات
        print("\n📋 مهاجرت سفارشات...")
        cursor = await sqlite_db.execute('SELECT * FROM orders')
        orders = await cursor.fetchall()
        
        for order in orders:
            new_product_id = product_map.get(order['product_id'])
            new_account_id = account_map.get(order['account_id']) if order.get('account_id') else None
            
            if new_product_id:
                new_id = await new_db.create_order(
                    user_id=order['user_id'],
                    username=order.get('username', 'Unknown'),
                    product_id=new_product_id,
                    amount=order['amount']
                )
                
                # به‌روزرسانی وضعیت
                if order.get('payment_receipt'):
                    await new_db.update_order_receipt(new_id, order['payment_receipt'])
                
                if order['status'] == 'completed' and new_account_id:
                    await new_db.complete_order(new_id, new_account_id)
                elif order['status'] == 'rejected':
                    await new_db.reject_order(new_id)
                
                print(f"  ✓ سفارش #{order['id']} ({order['status']}) -> #{new_id}")
        
        print(f"✅ {len(orders)} سفارش منتقل شد")
    
    # خلاصه
    print("\n" + "=" * 50)
    print("✅ مهاجرت با موفقیت انجام شد!")
    print(f"📦 محصولات: {len(products)}")
    print(f"🔐 اکانت‌ها: {len(accounts)}")
    print(f"📋 سفارشات: {len(orders)}")
    print("=" * 50)
    
    # راهنمای بعدی
    print("\n📝 گام‌های بعدی:")
    print("1. فایل SQLite قدیمی را بکاپ بگیرید:")
    print(f"   mv {SQLITE_PATH} {SQLITE_PATH}.backup")
    print("\n2. ربات را ری‌استارت کنید:")
    print("   docker-compose restart telegram-bot")
    print("\n3. دسترسی به Adminer:")
    print("   http://localhost:8080")


if __name__ == '__main__':
    try:
        asyncio.run(migrate())
    except KeyboardInterrupt:
        print("\n\n❌ مهاجرت لغو شد توسط کاربر")
    except Exception as e:
        print(f"\n\n❌ خطا در مهاجرت: {e}")
        import traceback
        traceback.print_exc()
