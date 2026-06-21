import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from bot.config import BOT_TOKEN
from bot.database_new import db

# Import handlers
from bot.handlers.user import (
    start_command,
    show_products,
    show_product_detail,
    buy_product,
    handle_receipt,
    receipt_sent_callback,
    my_orders
)

from bot.handlers.admin import (
    admin_panel,
    admin_products,
    admin_product_detail,
    start_add_product,
    add_product_name,
    add_product_desc,
    add_product_price,
    toggle_product_status,
    start_add_account,
    add_account_username,
    add_account_password,
    add_account_details,
    admin_pending_orders,
    approve_order,
    reject_order,
    cancel_conversation,
    admin_stats,
    ADD_PRODUCT_NAME,
    ADD_PRODUCT_DESC,
    ADD_PRODUCT_PRICE,
    ADD_ACCOUNT_USERNAME,
    ADD_ACCOUNT_PASSWORD,
    ADD_ACCOUNT_DETAILS
)

# تنظیم لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    """اجرای توابع بعد از راه‌اندازی"""
    # ایجاد دایرکتوری دیتا در صورت عدم وجود
    os.makedirs('data', exist_ok=True)
    
    # ایجاد جداول دیتابیس
    await db.init_db()
    logger.info("✅ دیتابیس آماده شد")


async def error_handler(update: Update, context):
    """مدیریت خطاها"""
    logger.error(f"خطا: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید."
        )


def main():
    """تابع اصلی"""
    # ساخت Application
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # ConversationHandler برای افزودن محصول
    add_product_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_add_product, pattern="^admin_add_product$")],
        states={
            ADD_PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_name)],
            ADD_PRODUCT_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_desc)],
            ADD_PRODUCT_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_price)],
        },
        fallbacks=[
            CallbackQueryHandler(cancel_conversation, pattern="^cancel$"),
            CommandHandler("cancel", cancel_conversation)
        ],
    )
    
    # ConversationHandler برای افزودن اکانت
    add_account_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_add_account, pattern="^admin_add_account_")],
        states={
            ADD_ACCOUNT_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_account_username)],
            ADD_ACCOUNT_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_account_password)],
            ADD_ACCOUNT_DETAILS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_account_details),
                CommandHandler("skip", add_account_details)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(cancel_conversation, pattern="^cancel$"),
            CommandHandler("cancel", cancel_conversation)
        ],
    )
    
    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(add_product_conv)
    application.add_handler(add_account_conv)
    
    # کالبک‌های کاربر
    application.add_handler(CallbackQueryHandler(start_command, pattern="^start$"))
    application.add_handler(CallbackQueryHandler(show_products, pattern="^products$"))
    application.add_handler(CallbackQueryHandler(show_product_detail, pattern="^product_"))
    application.add_handler(CallbackQueryHandler(buy_product, pattern="^buy_"))
    application.add_handler(CallbackQueryHandler(receipt_sent_callback, pattern="^sent_receipt_"))
    application.add_handler(CallbackQueryHandler(my_orders, pattern="^my_orders$"))
    
    # کالبک‌های ادمین
    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
    application.add_handler(CallbackQueryHandler(admin_products, pattern="^admin_products$"))
    application.add_handler(CallbackQueryHandler(admin_product_detail, pattern="^admin_product_"))
    application.add_handler(CallbackQueryHandler(toggle_product_status, pattern="^admin_toggle_"))
    application.add_handler(CallbackQueryHandler(admin_pending_orders, pattern="^admin_pending_orders$"))
    application.add_handler(CallbackQueryHandler(approve_order, pattern="^approve_order_"))
    application.add_handler(CallbackQueryHandler(reject_order, pattern="^reject_order_"))
    application.add_handler(CallbackQueryHandler(admin_stats, pattern="^admin_stats$"))
    
    # هندلر برای دریافت رسید پرداخت
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.Document.ALL,
        handle_receipt
    ))
    
    # هندلر خطا
    application.add_error_handler(error_handler)
    
    # شروع ربات
    logger.info("🤖 ربات شروع به کار کرد...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
