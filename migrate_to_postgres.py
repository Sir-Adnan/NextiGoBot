#!/usr/bin/env python3
"""
اسکریپت انتقال داده‌ها از SQLite به PostgreSQL
"""
import asyncio
import aiosqlite
from bot.database_new import db
from bot.config import DATABASE_URL

OLD_DB_PATH = 'data/bot.db'


async def migrate():
    """انتقال داده‌ها"""
    print("🚀 شروع انتقال داده‌ها...")
    
    # ایجاد جداول جدید
    print("📊 ایجاد جداول PostgreSQL...")
    await db.init_db()
    print("✅ جداول ایجاد شد")
    
    try:
        # اتصال به SQLite قدیمی
        async with aiosqlite.connect(OLD_DB_PATH) as old_db:
            old_db.row_factory = aiosqlite.Row
            
            # انتقال محصولات
            print("\n📦 انتقال محصولات...")
            cursor = await old_db.execute('SELECT * FROM products')
            products = await cursor.fetchall()
            
            product_map = {}  # نگاشت ID قدیم به جدید
            
            for p in products:
                new_id = await db.add_product(
                    name=p['name'],
                    description=p['description'],
                    price=p['price']
                )
                product_map[p['id']] = new_id
                print(f"  ✓ {p['name']} (ID: {p['id']} → {new_id})")
            
            print(f"✅ {len(products)} محصول منتقل شد")
            
            # انتقال اکانت‌ها
            print("\n🎫 انتقال اکانت‌ها...")
            cursor = await old_db.execute('SELECT * FROM accounts')
            accounts = await cursor.fetchall()
            
            account_map = {}
            
            for a in accounts:
                new_product_id = product_map.get(a['product_id'])
                if new_product_id:
                    new_id = await db.add_account(
                        product_id=new_product_id,
                        username=a['username'],
                        password=a['password'],
                        details=a['details']
                    )
                    
                    if a['is_sold']:
                        await db.mark_account_sold(new_id)
                    
                    account_map[a['id']] = new_id
                    status = "فروخته شده" if a['is_sold'] else "موجود"
                    print(f"  ✓ {a['username']} ({status})")
            
            print(f"✅ {len(accounts)} اکانت منتقل شد")
            
            # انتقال سفارشات
            print("\n📋 انتقال سفارشات...")
            cursor = await old_db.execute('SELECT * FROM orders')
            orders = await cursor.fetchall()
            
            for o in orders:
                new_product_id = product_map.get(o['product_id'])
                if new_product_id:
                    new_order_id = await db.create_order(
                        user_id=o['user_id'],
                        username=o['username'],
                        product_id=new_product_id,
                        amount=o['amount']
                    )
                    
                    if o['payment_receipt']:
                        await db.update_order_receipt(new_order_id, o['payment_receipt'])
                    
                    if o['status'] == 'completed' and o['account_id']:
                        new_account_id = account_map.get(o['account_id'])
                        if new_account_id:
                            await db.complete_order(new_order_id, new_account_id)
                    elif o['status'] == 'rejected':
                        await db.reject_order(new_order_id)
                    
                    print(f"  ✓ سفارش #{o['id']} → #{new_order_id} ({o['status']})")
            
            print(f"✅ {len(orders)} سفارش منتقل شد")
    
    except FileNotFoundError:
        print("⚠️  فایل SQLite قدیمی یافت نشد. این احتمالاً نصب جدیدی است.")
    except Exception as e:
        print(f"❌ خطا در انتقال: {e}")
        raise
    
    print("\n" + "="*50)
    print("✅ انتقال داده‌ها با موفقیت انجام شد!")
    print("="*50)
    print(f"\n📊 دیتابیس جدید: {DATABASE_URL}")
    print("🌐 پنل مدیریت: http://localhost:8080")
    print("\nاطلاعات ورود:")
    print(f"  Server: postgres")
    print(f"  Database: {db.async_session.kw['bind'].url.database}")


if __name__ == '__main__':
    asyncio.run(migrate())
