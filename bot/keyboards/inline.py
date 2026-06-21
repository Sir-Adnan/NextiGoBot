from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.emojis import PremiumEmojis
from bot.colored_buttons import ColoredButton, StatusColors


def main_menu_keyboard(is_admin: bool = False):
    """منوی اصلی با دکمه‌های رنگی"""
    keyboard = [
        [ColoredButton.primary_button(f"{PremiumEmojis.SHOPPING} محصولات", "products")],
        [ColoredButton.primary_button(f"{PremiumEmojis.LIST} سفارشات من", "my_orders")]
    ]
    
    if is_admin:
        keyboard.append([ColoredButton.success_button(f"{PremiumEmojis.SETTINGS} پنل ادمین", "admin_panel")])
    
    return InlineKeyboardMarkup(keyboard)


def admin_panel_keyboard():
    """کیبورد پنل ادمین"""
    keyboard = [
        [InlineKeyboardButton(f"{PremiumEmojis.ADD} افزودن محصول", callback_data="admin_add_product")],
        [InlineKeyboardButton(f"{PremiumEmojis.BOX} مدیریت محصولات", callback_data="admin_products")],
        [InlineKeyboardButton(f"{PremiumEmojis.LIST} سفارشات در انتظار", callback_data="admin_pending_orders")],
        [InlineKeyboardButton(f"{PremiumEmojis.CHART_UP} آمار فروش", callback_data="admin_stats")],
        [InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data="start")]
    ]
    return InlineKeyboardMarkup(keyboard)


def products_keyboard(products):
    """لیست محصولات"""
    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                f"{PremiumEmojis.BOX} {product['name']} - {product['price']:,} تومان",
                callback_data=f"product_{product['id']}"
            )
        ])
    keyboard.append([InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data="start")])
    return InlineKeyboardMarkup(keyboard)


def product_detail_keyboard(product_id: int, accounts_available: int):
    """جزئیات محصول"""
    keyboard = []
    
    if accounts_available > 0:
        keyboard.append([InlineKeyboardButton(f"{PremiumEmojis.CARD} خرید", callback_data=f"buy_{product_id}")])
    else:
        keyboard.append([InlineKeyboardButton(f"{PremiumEmojis.CROSS} موجود نیست", callback_data="unavailable")])
    
    keyboard.append([InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data="products")])
    return InlineKeyboardMarkup(keyboard)


def payment_keyboard(order_id: int):
    """کیبورد پرداخت"""
    keyboard = [
        [InlineKeyboardButton(f"{PremiumEmojis.CHECK} رسید پرداخت را ارسال کردم", callback_data=f"sent_receipt_{order_id}")],
        [InlineKeyboardButton(f"{PremiumEmojis.CROSS} لغو سفارش", callback_data=f"cancel_order_{order_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def admin_products_keyboard(products):
    """لیست محصولات برای ادمین"""
    keyboard = []
    for product in products:
        status = f"{PremiumEmojis.ONLINE}" if product['is_active'] else f"{PremiumEmojis.OFFLINE}"
        keyboard.append([
            InlineKeyboardButton(
                f"{status} {product['name']}",
                callback_data=f"admin_product_{product['id']}"
            )
        ])
    keyboard.append([InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data="admin_panel")])
    return InlineKeyboardMarkup(keyboard)


def admin_product_detail_keyboard(product_id: int):
    """جزئیات محصول برای ادمین"""
    keyboard = [
        [InlineKeyboardButton(f"{PremiumEmojis.ADD} افزودن اکانت", callback_data=f"admin_add_account_{product_id}")],
        [InlineKeyboardButton(f"{PremiumEmojis.REFRESH} تغییر وضعیت", callback_data=f"admin_toggle_{product_id}")],
        [InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data="admin_products")]
    ]
    return InlineKeyboardMarkup(keyboard)


def admin_order_keyboard(order_id: int):
    """کیبورد تایید سفارش برای ادمین"""
    keyboard = [
        [InlineKeyboardButton(f"{PremiumEmojis.CHECK} تایید و ارسال", callback_data=f"approve_order_{order_id}")],
        [InlineKeyboardButton(f"{PremiumEmojis.CROSS} رد کردن", callback_data=f"reject_order_{order_id}")],
        [InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data="admin_pending_orders")]
    ]
    return InlineKeyboardMarkup(keyboard)


def back_to_main_keyboard():
    """دکمه بازگشت به منوی اصلی"""
    keyboard = [[InlineKeyboardButton(f"{PremiumEmojis.HOME} منوی اصلی", callback_data="start")]]
    return InlineKeyboardMarkup(keyboard)


def cancel_keyboard():
    """دکمه لغو"""
    keyboard = [[InlineKeyboardButton(f"{PremiumEmojis.CROSS} لغو", callback_data="cancel")]]
    return InlineKeyboardMarkup(keyboard)



def categories_keyboard(categories):
    """لیست دسته‌بندی‌ها با دکمه‌های رنگی"""
    keyboard = []
    for category in categories:
        emoji = category.get('emoji', '📂')
        keyboard.append([
            ColoredButton.primary_button(
                f"{emoji} {category['name']}",
                f"category_{category['id']}"
            )
        ])
    keyboard.append([InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data="start")])
    return InlineKeyboardMarkup(keyboard)


def subscription_durations_keyboard(product_id: int):
    """دکمه‌های انتخاب مدت زمان اشتراک"""
    keyboard = [
        [
            ColoredButton.primary_button("۱ ماهه", f"duration_{product_id}_1"),
            ColoredButton.primary_button("۳ ماهه", f"duration_{product_id}_3")
        ],
        [
            ColoredButton.success_button("۶ ماهه", f"duration_{product_id}_6"),
            ColoredButton.success_button("۱ ساله", f"duration_{product_id}_12")
        ],
        [InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data=f"product_{product_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def product_detail_keyboard_with_duration(product_id: int, accounts_available: int, has_durations: bool = False):
    """جزئیات محصول با گزینه انتخاب مدت زمان"""
    keyboard = []
    
    if accounts_available > 0:
        if has_durations:
            keyboard.append([ColoredButton.success_button(
                f"{PremiumEmojis.CARD} انتخاب مدت زمان",
                f"choose_duration_{product_id}"
            )])
        else:
            keyboard.append([ColoredButton.success_button(
                f"{PremiumEmojis.CARD} خرید",
                f"buy_{product_id}"
            )])
    else:
        keyboard.append([ColoredButton.danger_button(
            f"{PremiumEmojis.CROSS} موجود نیست",
            "unavailable"
        )])
    
    keyboard.append([InlineKeyboardButton(f"{PremiumEmojis.BACK} بازگشت", callback_data="products")])
    return InlineKeyboardMarkup(keyboard)
