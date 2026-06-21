from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.database_new import db
from bot.emojis import PremiumEmojis, EmojiTexts
from bot.keyboards.inline import (
    admin_panel_keyboard, admin_products_keyboard,
    admin_product_detail_keyboard, back_to_main_keyboard, cancel_keyboard
)
from bot.config import ADMIN_ID


# States برای ConversationHandler
ADD_PRODUCT_NAME, ADD_PRODUCT_DESC, ADD_PRODUCT_PRICE = range(3)
ADD_ACCOUNT_USERNAME, ADD_ACCOUNT_PASSWORD, ADD_ACCOUNT_DETAILS = range(3, 6)


def is_admin(user_id: int) -> bool:
    """بررسی ادمین بودن کاربر"""
    return user_id == ADMIN_ID


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش پنل ادمین"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text(f"{PremiumEmojis.CROSS} شما دسترسی به پنل ادمین ندارید.")
        return
    
    text = f"{PremiumEmojis.CROWN} پنل مدیریت {PremiumEmojis.SPARKLES}\n\n"
    text += "یکی از گزینه‌ها را انتخاب کنید:"
    
    await query.edit_message_text(
        text,
        reply_markup=admin_panel_keyboard()
    )


async def admin_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش لیست محصولات برای ادمین"""
    query = update.callback_query
    await query.answer()
    
    products = await db.get_products(active_only=False)
    
    if not products:
        await query.edit_message_text(
            "❌ هیچ محصولی وجود ندارد.",
            reply_markup=back_to_main_keyboard()
        )
        return
    
    await query.edit_message_text(
        "📦 مدیریت محصولات:\n\nمحصول مورد نظر را انتخاب کنید:",
        reply_markup=admin_products_keyboard(products)
    )


async def admin_product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش جزئیات محصول برای ادمین"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[2])
    product = await db.get_product(product_id)
    
    if not product:
        await query.edit_message_text("❌ محصول یافت نشد.")
        return
    
    accounts_info = await db.get_accounts_count(product_id)
    
    text = f"📦 {product['name']}\n\n"
    text += f"📝 {product['description']}\n\n"
    text += f"💰 قیمت: {product['price']:,} تومان\n"
    text += f"📊 موجودی: {accounts_info['available']} عدد\n"
    text += f"✅ فروخته شده: {accounts_info['sold']} عدد\n"
    text += f"📈 کل: {accounts_info['total']} عدد\n"
    text += f"\nوضعیت: {'✅ فعال' if product['is_active'] else '❌ غیرفعال'}"
    
    await query.edit_message_text(
        text,
        reply_markup=admin_product_detail_keyboard(product_id)
    )


async def start_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع افزودن محصول جدید"""
    query = update.callback_query
    await query.answer()
    
    text = f"{PremiumEmojis.ADD} افزودن محصول جدید {PremiumEmojis.BOX}\n\n"
    text += "نام محصول را وارد کنید:"
    
    await query.edit_message_text(
        text,
        reply_markup=cancel_keyboard()
    )
    
    return ADD_PRODUCT_NAME


async def add_product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت نام محصول"""
    context.user_data['product_name'] = update.message.text
    
    await update.message.reply_text(
        "✅ نام محصول ثبت شد.\n\nحالا توضیحات محصول را وارد کنید:",
        reply_markup=cancel_keyboard()
    )
    
    return ADD_PRODUCT_DESC


async def add_product_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت توضیحات محصول"""
    context.user_data['product_desc'] = update.message.text
    
    await update.message.reply_text(
        "✅ توضیحات ثبت شد.\n\nحالا قیمت محصول را به تومان وارد کنید:",
        reply_markup=cancel_keyboard()
    )
    
    return ADD_PRODUCT_PRICE



async def add_product_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت قیمت محصول و ثبت در دیتابیس"""
    try:
        price = int(update.message.text.replace(',', ''))
        
        if price <= 0:
            raise ValueError
        
        product_id = await db.add_product(
            name=context.user_data['product_name'],
            description=context.user_data['product_desc'],
            price=price
        )
        
        text = EmojiTexts.product_added(
            name=context.user_data['product_name'],
            price=price
        )
        text += f"\n\n{PremiumEmojis.DOCUMENT} شناسه محصول: #{product_id}"
        
        await update.message.reply_text(
            text,
            reply_markup=admin_panel_keyboard()
        )
        
        # پاک کردن داده‌های موقت
        context.user_data.clear()
        
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            f"{PremiumEmojis.CROSS} قیمت نامعتبر است. لطفاً یک عدد صحیح وارد کنید:",
            reply_markup=cancel_keyboard()
        )
        return ADD_PRODUCT_PRICE


async def toggle_product_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تغییر وضعیت فعال/غیرفعال محصول"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[2])
    product = await db.get_product(product_id)
    
    new_status = not product['is_active']
    await db.update_product_status(product_id, new_status)
    
    status_text = "فعال" if new_status else "غیرفعال"
    await query.answer(f"✅ محصول {status_text} شد.")
    
    # نمایش دوباره جزئیات محصول
    await admin_product_detail(update, context)


async def start_add_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع افزودن اکانت جدید"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[3])
    context.user_data['account_product_id'] = product_id
    
    await query.edit_message_text(
        "➕ افزودن اکانت جدید\n\nنام کاربری (username) را وارد کنید:",
        reply_markup=cancel_keyboard()
    )
    
    return ADD_ACCOUNT_USERNAME



async def add_account_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت نام کاربری اکانت"""
    context.user_data['account_username'] = update.message.text
    
    await update.message.reply_text(
        "✅ نام کاربری ثبت شد.\n\nحالا رمز عبور (password) را وارد کنید:",
        reply_markup=cancel_keyboard()
    )
    
    return ADD_ACCOUNT_PASSWORD


async def add_account_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت رمز عبور اکانت"""
    context.user_data['account_password'] = update.message.text
    
    await update.message.reply_text(
        "✅ رمز عبور ثبت شد.\n\n"
        "اطلاعات اضافی (اختیاری) را وارد کنید یا /skip را بزنید:",
        reply_markup=cancel_keyboard()
    )
    
    return ADD_ACCOUNT_DETAILS


async def add_account_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت جزئیات اضافی و ثبت اکانت"""
    details = update.message.text if update.message.text != '/skip' else None
    
    account_id = await db.add_account(
        product_id=context.user_data['account_product_id'],
        username=context.user_data['account_username'],
        password=context.user_data['account_password'],
        details=details
    )
    
    product = await db.get_product(context.user_data['account_product_id'])
    
    text = EmojiTexts.account_added(product['name'])
    text += f"\n{PremiumEmojis.USER} نام کاربری: {context.user_data['account_username']}\n"
    text += f"{PremiumEmojis.KEY} شناسه اکانت: #{account_id}"
    
    await update.message.reply_text(
        text,
        reply_markup=admin_panel_keyboard()
    )
    
    context.user_data.clear()
    return ConversationHandler.END


async def admin_pending_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش سفارشات در انتظار تایید"""
    query = update.callback_query
    await query.answer()
    
    orders = await db.get_pending_orders()
    
    if not orders:
        await query.edit_message_text(
            "✅ هیچ سفارشی در انتظار تایید نیست.",
            reply_markup=admin_panel_keyboard()
        )
        return
    
    text = f"📋 سفارشات در انتظار تایید ({len(orders)} سفارش):\n\n"
    
    for order in orders:
        product = await db.get_product(order['product_id'])
        text += f"📝 سفارش #{order['id']}\n"
        text += f"👤 {order['username']}\n"
        text += f"📦 {product['name']}\n"
        text += f"💰 {order['amount']:,} تومان\n"
        text += f"📅 {order['created_at'][:16]}\n\n"
    
    await query.edit_message_text(text, reply_markup=admin_panel_keyboard())



async def approve_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تایید سفارش و ارسال اکانت به مشتری"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    order = await db.get_order(order_id)
    
    if not order or order['status'] != 'pending':
        await query.edit_message_text("❌ سفارش یافت نشد یا قبلاً پردازش شده است.")
        return
    
    # یافتن اکانت موجود
    account = await db.get_available_account(order['product_id'])
    
    if not account:
        await query.answer("❌ اکانتی برای این محصول موجود نیست!", show_alert=True)
        return
    
    # تکمیل سفارش
    await db.complete_order(order_id, account['id'])
    await db.mark_account_sold(account['id'])
    
    # ارسال اطلاعات اکانت به مشتری
    product = await db.get_product(order['product_id'])
    
    customer_text = EmojiTexts.order_approved(
        product_name=product['name'],
        username=account['username'],
        password=account['password']
    )
    
    if account['details']:
        customer_text += f"\n\n{PremiumEmojis.DOCUMENT} توضیحات:\n{account['details']}"
    
    customer_text += f"\n\n{PremiumEmojis.DOCUMENT} شماره سفارش: #{order_id}"
    
    await context.bot.send_message(
        chat_id=order['user_id'],
        text=customer_text,
        parse_mode='HTML'
    )
    
    # تایید به ادمین
    await query.edit_message_caption(
        caption=query.message.caption + f"\n\n{PremiumEmojis.CHECK} تایید شد و به مشتری ارسال شد."
    )


async def reject_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رد کردن سفارش"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    order = await db.get_order(order_id)
    
    if not order or order['status'] != 'pending':
        await query.edit_message_text("❌ سفارش یافت نشد یا قبلاً پردازش شده است.")
        return
    
    await db.reject_order(order_id)
    
    # اطلاع به مشتری
    await context.bot.send_message(
        chat_id=order['user_id'],
        text=f"{PremiumEmojis.CROSS} متأسفانه سفارش شما رد شد.\n\n"
             f"{PremiumEmojis.DOCUMENT} شماره سفارش: #{order_id}\n"
             f"لطفاً با پشتیبانی تماس بگیرید."
    )
    
    # تایید به ادمین
    await query.edit_message_caption(
        caption=query.message.caption + f"\n\n{PremiumEmojis.CROSS} رد شد."
    )


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لغو مکالمه"""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "❌ عملیات لغو شد.",
            reply_markup=admin_panel_keyboard()
        )
    else:
        await update.message.reply_text(
            "❌ عملیات لغو شد.",
            reply_markup=admin_panel_keyboard()
        )
    
    context.user_data.clear()
    return ConversationHandler.END



async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش آمار فروش"""
    query = update.callback_query
    await query.answer()
    
    # دریافت آمار
    stats = await db.get_orders_stats()
    
    text = f"{PremiumEmojis.CHART_UP} آمار فروش {PremiumEmojis.TROPHY}\n\n"
    text += f"{PremiumEmojis.LIST} کل سفارشات: {stats['total']}\n"
    text += f"{PremiumEmojis.CHECK} تکمیل شده: {stats['completed']}\n"
    text += f"{PremiumEmojis.HOURGLASS} در انتظار: {stats['pending']}\n"
    text += f"{PremiumEmojis.MONEY} درآمد کل: {stats['revenue']:,} تومان\n\n"
    text += f"{PremiumEmojis.SPARKLES} عملکرد عالی!"
    
    await query.edit_message_text(
        text,
        reply_markup=admin_panel_keyboard()
    )



async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش آمار فروش"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ شما دسترسی ندارید.")
        return
    
    # دریافت آمار
    stats = await db.get_orders_stats()
    
    text = f"{PremiumEmojis.CHART_UP} آمار فروش {PremiumEmojis.TROPHY}\n\n"
    text += f"{PremiumEmojis.LIST} کل سفارشات: {stats['total']}\n"
    text += f"{PremiumEmojis.CHECK} تکمیل شده: {stats['completed']}\n"
    text += f"{PremiumEmojis.HOURGLASS} در انتظار: {stats['pending']}\n"
    text += f"{PremiumEmojis.MONEY} مجموع فروش: {stats['revenue']:,} تومان\n\n"
    
    # آمار محصولات
    products = await db.get_products(active_only=False)
    text += f"{PremiumEmojis.BOX} تعداد محصولات: {len(products)}\n"
    
    # آمار اکانت‌ها
    total_accounts = 0
    total_sold = 0
    for product in products:
        counts = await db.get_accounts_count(product['id'])
        total_accounts += counts['total']
        total_sold += counts['sold']
    
    text += f"{PremiumEmojis.KEY} کل اکانت‌ها: {total_accounts}\n"
    text += f"{PremiumEmojis.GIFT} موجودی: {total_accounts - total_sold}\n"
    text += f"{PremiumEmojis.FIRE} فروخته شده: {total_sold}"
    
    await query.edit_message_text(text, reply_markup=admin_panel_keyboard())
