from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.database_new import db
from bot.keyboards.inline import (
    main_menu_keyboard, products_keyboard, product_detail_keyboard,
    payment_keyboard, back_to_main_keyboard
)
from bot.config import ADMIN_ID, CARD_NUMBER, CARD_HOLDER_NAME
from bot.emojis import PremiumEmojis, EmojiTexts


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور شروع ربات"""
    user = update.effective_user
    is_admin = user.id == ADMIN_ID
    
    if is_admin:
        welcome_text = EmojiTexts.admin_welcome(user.first_name)
    else:
        welcome_text = EmojiTexts.welcome(user.first_name)
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            welcome_text,
            reply_markup=main_menu_keyboard(is_admin)
        )
    else:
        await update.message.reply_text(
            welcome_text,
            reply_markup=main_menu_keyboard(is_admin)
        )


async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش لیست محصولات"""
    query = update.callback_query
    await query.answer()
    
    products = await db.get_products(active_only=True)
    
    if not products:
        await query.edit_message_text(
            f"{PremiumEmojis.CROSS} هیچ محصولی موجود نیست.",
            reply_markup=back_to_main_keyboard()
        )
        return
    
    text = f"{PremiumEmojis.SHOPPING} لیست محصولات:\n\n"
    text += f"محصول مورد نظر خود را انتخاب کنید {PremiumEmojis.DOWN}"
    
    await query.edit_message_text(
        text,
        reply_markup=products_keyboard(products)
    )


async def show_product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش جزئیات محصول"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[1])
    product = await db.get_product(product_id)
    
    if not product:
        await query.edit_message_text(
            f"{PremiumEmojis.CROSS} محصول یافت نشد.",
            reply_markup=back_to_main_keyboard()
        )
        return
    
    accounts_info = await db.get_accounts_count(product_id)
    
    text = f"{PremiumEmojis.BOX} {product['name']}\n\n"
    text += f"{PremiumEmojis.DOCUMENT} توضیحات:\n{product['description']}\n\n"
    text += f"{PremiumEmojis.MONEY} قیمت: {product['price']:,} تومان\n"
    text += f"{PremiumEmojis.CHART_UP} موجودی: {accounts_info['available']} عدد"
    
    await query.edit_message_text(
        text,
        reply_markup=product_detail_keyboard(product_id, accounts_info['available'])
    )


async def buy_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع فرآیند خرید"""
    query = update.callback_query
    await query.answer()
    
    product_id = int(query.data.split('_')[1])
    product = await db.get_product(product_id)
    
    if not product:
        await query.edit_message_text(
            f"{PremiumEmojis.CROSS} محصول یافت نشد.",
            reply_markup=back_to_main_keyboard()
        )
        return
    
    # بررسی موجودی
    account = await db.get_available_account(product_id)
    if not account:
        await query.edit_message_text(
            f"{PremiumEmojis.CROSS} متأسفانه این محصول موجود نیست.",
            reply_markup=back_to_main_keyboard()
        )
        return
    
    # ایجاد سفارش
    user = update.effective_user
    order_id = await db.create_order(
        user_id=user.id,
        username=user.username or user.first_name,
        product_id=product_id,
        amount=product['price'],
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    # نمایش اطلاعات پرداخت
    text = EmojiTexts.payment_info(
        product_name=product['name'],
        price=product['price'],
        card_number=CARD_NUMBER,
        card_holder=CARD_HOLDER_NAME,
        order_id=order_id
    )
    
    context.user_data['waiting_receipt'] = order_id
    
    await query.edit_message_text(
        text,
        parse_mode='HTML',
        reply_markup=payment_keyboard(order_id)
    )


async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت رسید پرداخت از کاربر"""
    if 'waiting_receipt' not in context.user_data:
        return
    
    order_id = context.user_data['waiting_receipt']
    order = await db.get_order(order_id)
    
    if not order or order['status'] != 'pending':
        await update.message.reply_text(
            "❌ سفارش یافت نشد یا قبلاً پردازش شده است.",
            reply_markup=back_to_main_keyboard()
        )
        del context.user_data['waiting_receipt']
        return
    
    # ذخیره رسید پرداخت
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif update.message.document:
        file_id = update.message.document.file_id
    else:
        await update.message.reply_text("❌ لطفاً تصویر یا فایل رسید را ارسال کنید.")
        return
    
    await db.update_order_receipt(order_id, file_id)
    
    # اطلاع به ادمین
    product = await db.get_product(order['product_id'])
    admin_text = EmojiTexts.new_order_admin(
        order_id=order_id,
        username=order['username'],
        product_name=product['name'],
        amount=order['amount']
    )
    
    from bot.keyboards.inline import admin_order_keyboard
    
    if update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=admin_text,
            reply_markup=admin_order_keyboard(order_id)
        )
    else:
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=file_id,
            caption=admin_text,
            reply_markup=admin_order_keyboard(order_id)
        )
    
    # تایید به کاربر
    await update.message.reply_text(
        EmojiTexts.order_received(),
        reply_markup=back_to_main_keyboard()
    )
    
    del context.user_data['waiting_receipt']


async def receipt_sent_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """وقتی کاربر دکمه ارسال رسید را می‌زند"""
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split('_')[2])
    context.user_data['waiting_receipt'] = order_id
    
    await query.edit_message_text(
        "📤 لطفاً تصویر یا فایل رسید پرداخت را ارسال کنید:\n\n"
        "می‌تونید عکس، اسکرین‌شات یا PDF رسید را بفرستید.",
        reply_markup=back_to_main_keyboard()
    )


async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش سفارشات کاربر"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    orders = await db.get_user_orders(user_id)
    
    if not orders:
        await query.edit_message_text(
            "📦 شما هنوز سفارشی ثبت نکرده‌اید.",
            reply_markup=back_to_main_keyboard()
        )
        return
    
    text = "📋 سفارشات شما:\n\n"
    
    for order in orders:
        product = await db.get_product(order['product_id'])
        status_emoji = {
            'pending': '⏳',
            'completed': '✅',
            'rejected': '❌'
        }.get(order['status'], '❓')
        
        status_text = {
            'pending': 'در انتظار تایید',
            'completed': 'تکمیل شده',
            'rejected': 'رد شده'
        }.get(order['status'], 'نامشخص')
        
        text += f"{status_emoji} سفارش #{order['id']}\n"
        text += f"📦 {product['name']}\n"
        text += f"💰 {order['amount']:,} تومان\n"
        text += f"📅 {order['created_at'][:16]}\n"
        text += f"وضعیت: {status_text}\n\n"
    
    await query.edit_message_text(text, reply_markup=back_to_main_keyboard())
