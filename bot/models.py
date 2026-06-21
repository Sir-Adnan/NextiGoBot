"""
مدل‌های دیتابیس با SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    """مدل دسته‌بندی محصولات"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    emoji = Column(String(10), nullable=True)  # ایموجی برای دسته
    parent_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)  # ترتیب نمایش
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # روابط
    products = relationship("Product", back_populates="category")
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'emoji': self.emoji,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Product(Base):
    """مدل محصولات"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # اضافه کردن فیلدهای دوره‌ای
    is_subscription = Column(Boolean, default=False)  # آیا محصول اشتراکی است؟
    duration_months = Column(Integer, nullable=True)  # مدت زمان (ماه)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # روابط
    category = relationship("Category", back_populates="products")
    accounts = relationship("Account", back_populates="product", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'is_subscription': self.is_subscription,
            'duration_months': self.duration_months,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def get_duration_text(self) -> str:
        """دریافت متن مدت زمان"""
        if not self.is_subscription or not self.duration_months:
            return ""
        
        if self.duration_months == 1:
            return "۱ ماهه"
        elif self.duration_months == 3:
            return "۳ ماهه"
        elif self.duration_months == 6:
            return "۶ ماهه"
        elif self.duration_months == 12:
            return "۱ ساله"
        else:
            return f"{self.duration_months} ماهه"


class Account(Base):
    """مدل اکانت‌ها"""
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    is_sold = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sold_at = Column(DateTime, nullable=True)
    
    # روابط
    product = relationship("Product", back_populates="accounts")
    orders = relationship("Order", back_populates="account")
    
    def __repr__(self):
        return f"<Account(id={self.id}, username='{self.username}', is_sold={self.is_sold})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'username': self.username,
            'password': self.password,
            'details': self.details,
            'is_sold': self.is_sold,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sold_at': self.sold_at.isoformat() if self.sold_at else None,
        }


class Order(Base):
    """مدل سفارشات"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id', ondelete='SET NULL'), nullable=True)
    amount = Column(Integer, nullable=False)
    status = Column(String(50), default='pending')  # pending, completed, rejected, cancelled
    payment_receipt = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # روابط
    product = relationship("Product", back_populates="orders")
    account = relationship("Account", back_populates="orders")
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status='{self.status}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'product_id': self.product_id,
            'account_id': self.account_id,
            'amount': self.amount,
            'status': self.status,
            'payment_receipt': self.payment_receipt,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }


class Setting(Base):
    """مدل تنظیمات"""
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Setting(key='{self.key}', value='{self.value}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
