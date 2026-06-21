#!/usr/bin/env python3
"""
اجرای مستقیم ربات بدون Docker (برای تست و توسعه)
"""

import os
import sys

# بررسی نصب بودن پکیج‌ها
try:
    import telegram
    import dotenv
    import aiosqlite
except ImportError:
    print("❌ پکیج‌های مورد نیاز نصب نیستند!")
    print("\nبرای نصب دستور زیر را اجرا کنید:")
    print("pip install -r requirements.txt")
    sys.exit(1)

# بررسی وجود فایل .env
if not os.path.exists('.env'):
    print("❌ فایل .env یافت نشد!")
    print("\nلطفاً فایل .env.example را به .env کپی کرده و تنظیمات را وارد کنید:")
    print("cp .env.example .env")
    sys.exit(1)

# ایجاد پوشه data
os.makedirs('data', exist_ok=True)

# اجرای ربات
from bot.main import main

if __name__ == '__main__':
    print("🤖 شروع ربات...")
    print("برای توقف ربات Ctrl+C را بزنید")
    print("-" * 50)
    main()
