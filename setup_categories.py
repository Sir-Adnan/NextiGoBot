#!/usr/bin/env python3
"""
اسکریپت راه‌اندازی دسته‌بندی‌های پیش‌فرض
"""
import asyncio
import sys
from bot.database_new import db


async def setup_default_categories():
    """ایجاد دسته‌بندی‌های پیش‌فرض"""
    
    print("🚀 شروع راه‌اندازی دسته‌بندی‌ها...")
    print("-" * 50)
    
    try:
        # ایجاد جداول
        print("📦 ایجاد جداول دیتابیس...")
        await db.init_db()
        print("✅ جداول ایجاد شد")
        
        # دسته‌بندی‌های اصلی
        print("\n📂 ایجاد دسته‌بندی‌های اصلی...")
        
        streaming_id = await db.add_category(
            name="استریمینگ",
            description="سرویس‌های استریمینگ موسیقی و ویدیو",
            emoji="📺"
        )
        print(f"  ✓ استریمینگ (ID: {streaming_id})")
        
        gaming_id = await db.add_category(
            name="گیمینگ",
            description="اکانت‌های بازی و پلتفرم‌های گیمینگ",
            emoji="🎮"
        )
        print(f"  ✓ گیمینگ (ID: {gaming_id})")
        
        education_id = await db.add_category(
            name="آموزشی",
            description="دوره‌ها و پلتفرم‌های آموزشی",
            emoji="📚"
        )
        print(f"  ✓ آموزشی (ID: {education_id})")
        
        vpn_id = await db.add_category(
            name="VPN و امنیت",
            description="سرویس‌های VPN و امنیتی",
            emoji="🔒"
        )
        print(f"  ✓ VPN و امنیت (ID: {vpn_id})")
        
        software_id = await db.add_category(
            name="نرم‌افزار",
            description="لایسنس نرم‌افزارها",
            emoji="💿"
        )
        print(f"  ✓ نرم‌افزار (ID: {software_id})")
        
        # زیردسته‌ها برای استریمینگ
        print("\n🎬 ایجاد زیردسته‌های استریمینگ...")
        
        await db.add_category(
            name="Netflix",
            description="اکانت‌های نتفلیکس",
            emoji="🎬",
            parent_id=streaming_id
        )
        print("  ✓ Netflix")
        
        await db.add_category(
            name="Spotify",
            description="اکانت‌های اسپاتیفای",
            emoji="🎵",
            parent_id=streaming_id
        )
        print("  ✓ Spotify")
        
        await db.add_category(
            name="YouTube Premium",
            description="یوتیوب پریمیوم",
            emoji="▶️",
            parent_id=streaming_id
        )
        print("  ✓ YouTube Premium")
        
        await db.add_category(
            name="Apple Music",
            description="اپل موزیک",
            emoji="🍎",
            parent_id=streaming_id
        )
        print("  ✓ Apple Music")
        
        # زیردسته‌ها برای گیمینگ
        print("\n🎮 ایجاد زیردسته‌های گیمینگ...")
        
        await db.add_category(
            name="Steam",
            description="اکانت‌های استیم",
            emoji="💨",
            parent_id=gaming_id
        )
        print("  ✓ Steam")
        
        await db.add_category(
            name="PlayStation",
            description="PlayStation Plus",
            emoji="🎯",
            parent_id=gaming_id
        )
        print("  ✓ PlayStation")
        
        await db.add_category(
            name="Xbox",
            description="Xbox Game Pass",
            emoji="🎮",
            parent_id=gaming_id
        )
        print("  ✓ Xbox")
        
        # زیردسته‌ها برای آموزشی
        print("\n📚 ایجاد زیردسته‌های آموزشی...")
        
        await db.add_category(
            name="Udemy",
            description="دوره‌های یودمی",
            emoji="🎓",
            parent_id=education_id
        )
        print("  ✓ Udemy")
        
        await db.add_category(
            name="Coursera",
            description="دوره‌های کورسرا",
            emoji="📖",
            parent_id=education_id
        )
        print("  ✓ Coursera")
        
        await db.add_category(
            name="LinkedIn Learning",
            description="لینکدین لرنینگ",
            emoji="💼",
            parent_id=education_id
        )
        print("  ✓ LinkedIn Learning")
        
        # زیردسته‌ها برای VPN
        print("\n🔒 ایجاد زیردسته‌های VPN...")
        
        await db.add_category(
            name="NordVPN",
            description="نورد وی‌پی‌ان",
            emoji="🛡️",
            parent_id=vpn_id
        )
        print("  ✓ NordVPN")
        
        await db.add_category(
            name="ExpressVPN",
            description="اکسپرس وی‌پی‌ان",
            emoji="⚡",
            parent_id=vpn_id
        )
        print("  ✓ ExpressVPN")
        
        # زیردسته‌ها برای نرم‌افزار
        print("\n💿 ایجاد زیردسته‌های نرم‌افزار...")
        
        await db.add_category(
            name="Microsoft Office",
            description="آفیس مایکروسافت",
            emoji="📊",
            parent_id=software_id
        )
        print("  ✓ Microsoft Office")
        
        await db.add_category(
            name="Adobe Creative Cloud",
            description="ادوبی کریتیو کلود",
            emoji="🎨",
            parent_id=software_id
        )
        print("  ✓ Adobe Creative Cloud")
        
        print("\n" + "=" * 50)
        print("✅ همه دسته‌بندی‌ها با موفقیت ایجاد شدند!")
        print("=" * 50)
        
        # نمایش خلاصه
        categories = await db.get_categories(active_only=False)
        print(f"\n📊 خلاصه: {len(categories)} دسته‌بندی ایجاد شد")
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
        return False


async def show_categories():
    """نمایش لیست دسته‌بندی‌ها"""
    print("\n📋 لیست دسته‌بندی‌های موجود:")
    print("-" * 50)
    
    categories = await db.get_categories(parent_id=None)
    
    for cat in categories:
        emoji = cat.get('emoji', '📂')
        print(f"\n{emoji} {cat['name']} (ID: {cat['id']})")
        
        # نمایش زیردسته‌ها
        subcategories = await db.get_categories(parent_id=cat['id'])
        for subcat in subcategories:
            sub_emoji = subcat.get('emoji', '  📄')
            print(f"  └─ {sub_emoji} {subcat['name']} (ID: {subcat['id']})")


async def main():
    """تابع اصلی"""
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        await show_categories()
    else:
        success = await setup_default_categories()
        if success:
            print("\n💡 برای مشاهده لیست دسته‌بندی‌ها:")
            print("   python setup_categories.py show")
            print("\n🚀 حالا می‌تونید ربات رو ری‌استارت کنید:")
            print("   docker-compose restart telegram-bot")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ لغو شد توسط کاربر")
    except Exception as e:
        print(f"\n\n❌ خطای غیرمنتظره: {e}")
        sys.exit(1)
