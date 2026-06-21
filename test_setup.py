#!/usr/bin/env python3
"""
اسکریپت تست تنظیمات ربات
"""

import os
import sys

def check_file(filepath, description):
    """بررسی وجود فایل"""
    if os.path.exists(filepath):
        print(f"✅ {description}: موجود است")
        return True
    else:
        print(f"❌ {description}: یافت نشد - {filepath}")
        return False

def check_env_var(var_name):
    """بررسی متغیر محیطی"""
    from dotenv import load_dotenv
    load_dotenv()
    
    value = os.getenv(var_name)
    if value and value != f"your_{var_name.lower()}_here":
        print(f"✅ {var_name}: تنظیم شده")
        return True
    else:
        print(f"❌ {var_name}: تنظیم نشده")
        return False

def main():
    """تست اصلی"""
    print("🧪 تست تنظیمات ربات...")
    print("-" * 50)
    
    all_ok = True
    
    # بررسی فایل‌های ضروری
    print("\n📁 بررسی فایل‌ها:")
    all_ok &= check_file("bot/main.py", "فایل اصلی ربات")
    all_ok &= check_file("bot/config.py", "فایل تنظیمات")
    all_ok &= check_file("bot/database.py", "فایل دیتابیس")
    all_ok &= check_file("requirements.txt", "فایل پکیج‌ها")
    all_ok &= check_file("Dockerfile", "Dockerfile")
    all_ok &= check_file("docker-compose.yml", "Docker Compose")
    
    # بررسی .env
    print("\n🔐 بررسی تنظیمات محیطی:")
    if check_file(".env", "فایل .env"):
        all_ok &= check_env_var("BOT_TOKEN")
        all_ok &= check_env_var("ADMIN_ID")
        all_ok &= check_env_var("CARD_NUMBER")
    else:
        print("\n⚠️  فایل .env یافت نشد!")
        print("لطفاً دستور زیر را اجرا کنید:")
        print("cp .env.example .env")
        all_ok = False
    
    # بررسی پکیج‌ها
    print("\n📦 بررسی پکیج‌های پایتون:")
    try:
        import telegram
        print("✅ python-telegram-bot: نصب شده")
    except ImportError:
        print("❌ python-telegram-bot: نصب نشده")
        all_ok = False
    
    try:
        import aiosqlite
        print("✅ aiosqlite: نصب شده")
    except ImportError:
        print("❌ aiosqlite: نصب نشده")
        all_ok = False
    
    try:
        import dotenv
        print("✅ python-dotenv: نصب شده")
    except ImportError:
        print("❌ python-dotenv: نصب نشده")
        all_ok = False
    
    # نتیجه نهایی
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ همه چیز آماده است! می‌توانید ربات را اجرا کنید.")
        print("\nبرای اجرا:")
        print("  با Docker: docker-compose up -d")
        print("  مستقیم: python run_local.py")
    else:
        print("❌ برخی تنظیمات کامل نیست. لطفاً موارد بالا را بررسی کنید.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
