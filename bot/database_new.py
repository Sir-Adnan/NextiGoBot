"""
دیتابیس با SQLAlchemy و PostgreSQL
"""
import os
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from bot.models import Base, Product, Account, Order, Setting


class Database:
    def __init__(self, database_url: str = None):
        if database_url is None:
            # ساخت URL از متغیرهای محیطی
            db_user = os.getenv('DB_USER', 'telegram_bot')
            db_password = os.getenv('DB_PASSWORD', 'changeme123')
            db_host = os.getenv('DB_HOST', 'localhost')
            db_port = os.getenv('DB_PORT', '5432')
            db_name = os.getenv('DB_NAME', 'telegram_shop')
            
            database_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        self.engine = create_async_engine(
            database_url,
            echo=False,  # برای دیباگ True کنید
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def init_db(self):
        """ایجاد جداول دیتابیس"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_all(self):
        """حذف تمام جداول (فقط برای توسعه)"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    # ============= محصولات =============
    
    async def add_product(self, name: str, description: str, price: int, image_url: str = None) -> int:
        """افزودن محصول جدید"""
        async with self.async_session() as session:
            product = Product(
                name=name,
                description=description,
                price=price,
                image_url=image_url
            )
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product.id
    
    async def get_products(self, active_only: bool = True) -> List[Dict]:
        """دریافت لیست محصولات"""
        async with self.async_session() as session:
            query = select(Product)
            if active_only:
                query = query.where(Product.is_active == True)
            query = query.order_by(Product.id.desc())
            
            result = await session.execute(query)
            products = result.scalars().all()
            return [p.to_dict() for p in products]
    
    async def get_product(self, product_id: int) -> Optional[Dict]:
        """دریافت اطلاعات یک محصول"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            product = result.scalar_one_or_none()
            return product.to_dict() if product else None
    
    async def update_product_status(self, product_id: int, is_active: bool):
        """تغییر وضعیت فعال/غیرفعال محصول"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            product = result.scalar_one_or_none()
            if product:
                product.is_active = is_active
                product.updated_at = datetime.utcnow()
                await session.commit()
    
    async def update_product(self, product_id: int, **kwargs):
        """به‌روزرسانی محصول"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            product = result.scalar_one_or_none()
            if product:
                for key, value in kwargs.items():
                    if hasattr(product, key):
                        setattr(product, key, value)
                product.updated_at = datetime.utcnow()
                await session.commit()
    
    # ============= اکانت‌ها =============
    
    async def add_account(self, product_id: int, username: str, password: str, details: str = None) -> int:
        """افزودن اکانت جدید"""
        async with self.async_session() as session:
            account = Account(
                product_id=product_id,
                username=username,
                password=password,
                details=details
            )
            session.add(account)
            await session.commit()
            await session.refresh(account)
            return account.id
    
    async def get_available_account(self, product_id: int) -> Optional[Dict]:
        """دریافت یک اکانت فروخته نشده"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Account)
                .where(and_(Account.product_id == product_id, Account.is_sold == False))
                .limit(1)
            )
            account = result.scalar_one_or_none()
            return account.to_dict() if account else None
    
    async def get_accounts_count(self, product_id: int) -> Dict[str, int]:
        """دریافت تعداد اکانت‌های موجود و فروخته شده"""
        async with self.async_session() as session:
            # تعداد کل
            total_result = await session.execute(
                select(func.count(Account.id)).where(Account.product_id == product_id)
            )
            total = total_result.scalar()
            
            # تعداد فروخته شده
            sold_result = await session.execute(
                select(func.count(Account.id))
                .where(and_(Account.product_id == product_id, Account.is_sold == True))
            )
            sold = sold_result.scalar()
            
            return {
                'total': total or 0,
                'available': (total or 0) - (sold or 0),
                'sold': sold or 0
            }
    
    async def mark_account_sold(self, account_id: int):
        """علامت‌گذاری اکانت به عنوان فروخته شده"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Account).where(Account.id == account_id)
            )
            account = result.scalar_one_or_none()
            if account:
                account.is_sold = True
                account.sold_at = datetime.utcnow()
                await session.commit()
    
    async def get_account(self, account_id: int) -> Optional[Dict]:
        """دریافت اطلاعات اکانت"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Account).where(Account.id == account_id)
            )
            account = result.scalar_one_or_none()
            return account.to_dict() if account else None
    
    # ============= سفارشات =============
    
    async def create_order(self, user_id: int, username: str, product_id: int, 
                          amount: int, first_name: str = None, last_name: str = None) -> int:
        """ایجاد سفارش جدید"""
        async with self.async_session() as session:
            order = Order(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                product_id=product_id,
                amount=amount,
                status='pending'
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order.id
    
    async def get_order(self, order_id: int) -> Optional[Dict]:
        """دریافت اطلاعات سفارش"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Order)
                .options(selectinload(Order.product), selectinload(Order.account))
                .where(Order.id == order_id)
            )
            order = result.scalar_one_or_none()
            return order.to_dict() if order else None
    
    async def update_order_receipt(self, order_id: int, receipt_file_id: str):
        """ذخیره رسید پرداخت"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Order).where(Order.id == order_id)
            )
            order = result.scalar_one_or_none()
            if order:
                order.payment_receipt = receipt_file_id
                await session.commit()
    
    async def complete_order(self, order_id: int, account_id: int):
        """تکمیل سفارش و تخصیص اکانت"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Order).where(Order.id == order_id)
            )
            order = result.scalar_one_or_none()
            if order:
                order.status = 'completed'
                order.account_id = account_id
                order.completed_at = datetime.utcnow()
                await session.commit()
    
    async def reject_order(self, order_id: int):
        """رد کردن سفارش"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Order).where(Order.id == order_id)
            )
            order = result.scalar_one_or_none()
            if order:
                order.status = 'rejected'
                await session.commit()
    
    async def cancel_order(self, order_id: int):
        """لغو سفارش"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Order).where(Order.id == order_id)
            )
            order = result.scalar_one_or_none()
            if order:
                order.status = 'cancelled'
                await session.commit()
    
    async def get_pending_orders(self) -> List[Dict]:
        """دریافت سفارشات در انتظار تایید"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Order)
                .options(selectinload(Order.product))
                .where(Order.status == 'pending')
                .order_by(Order.created_at.desc())
            )
            orders = result.scalars().all()
            return [o.to_dict() for o in orders]
    
    async def get_user_orders(self, user_id: int) -> List[Dict]:
        """دریافت سفارشات یک کاربر"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Order)
                .options(selectinload(Order.product))
                .where(Order.user_id == user_id)
                .order_by(Order.created_at.desc())
            )
            orders = result.scalars().all()
            return [o.to_dict() for o in orders]
    
    async def get_orders_stats(self) -> Dict:
        """دریافت آمار سفارشات"""
        async with self.async_session() as session:
            # تعداد کل سفارشات
            total_result = await session.execute(select(func.count(Order.id)))
            total = total_result.scalar()
            
            # سفارشات تکمیل شده
            completed_result = await session.execute(
                select(func.count(Order.id)).where(Order.status == 'completed')
            )
            completed = completed_result.scalar()
            
            # سفارشات در انتظار
            pending_result = await session.execute(
                select(func.count(Order.id)).where(Order.status == 'pending')
            )
            pending = pending_result.scalar()
            
            # مجموع فروش
            revenue_result = await session.execute(
                select(func.sum(Order.amount)).where(Order.status == 'completed')
            )
            revenue = revenue_result.scalar() or 0
            
            return {
                'total': total or 0,
                'completed': completed or 0,
                'pending': pending or 0,
                'revenue': revenue
            }
    
    # ============= تنظیمات =============
    
    async def get_setting(self, key: str) -> Optional[str]:
        """دریافت یک تنظیم"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Setting).where(Setting.key == key)
            )
            setting = result.scalar_one_or_none()
            return setting.value if setting else None
    
    async def set_setting(self, key: str, value: str, description: str = None):
        """ذخیره یک تنظیم"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Setting).where(Setting.key == key)
            )
            setting = result.scalar_one_or_none()
            
            if setting:
                setting.value = value
                if description:
                    setting.description = description
                setting.updated_at = datetime.utcnow()
            else:
                setting = Setting(key=key, value=value, description=description)
                session.add(setting)
            
            await session.commit()


# نمونه سراسری دیتابیس
db = Database()
