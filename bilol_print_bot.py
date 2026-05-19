#!/usr/bin/env python3
"""
Bilol Print - Professional Telegram Bot
Buyurtma, narx kalkulyator, portfolio
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ============================================================
#  SOZLAMALAR — faqat shu joyni o'zgartiring
# ============================================================
BOT_TOKEN = "8695094650:AAFTL34CS3PES_mthfOxFcOJTWNp1b5gYjc"
ADMIN_ID   = 8286195257   # Sizning Telegram ID

COMPANY = "Bilol Print"
PHONE   = "+998 93 005 73 33"
TG      = "@Te_7333"
CITY    = "Toshkent shahri"
# ============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ConversationHandler states
(
    ORDER_TYPE, ORDER_SIZE_W, ORDER_SIZE_H,
    ORDER_QTY, ORDER_COMMENT, ORDER_PHONE,
    CALC_TYPE, CALC_W, CALC_H, CALC_QTY
) = range(10)

# Narxlar (so'm/m²)
PRICES = {
    "banner": {"name": "🖼 Banner (Flex)", "price": 15000},
    "orakal": {"name": "🎨 Orakal plyonka", "price": 25000},
    "tumanka": {"name": "☁️ Tumanka", "price": 20000},
    "stiker":  {"name": "📋 Stiker", "price": 30000},
    "litak":   {"name": "📄 Litak / Buklet", "price": 500},   # dona
}

PORTFOLIO = [
    {"name": "Katta format banner", "desc": "3x6m flex banner, tashqi reklama", "emoji": "🖼"},
    {"name": "Vitrina orakal",      "desc": "Rang-barang plyonka, oyna bezash",  "emoji": "🪟"},
    {"name": "Tumanka pechat",      "desc": "A2 o'lcham, yuqori aniqlik",         "emoji": "☁️"},
    {"name": "Stiker to'plami",     "desc": "100 dona, logo bilan",               "emoji": "🏷"},
    {"name": "Reklama banneri",     "desc": "2x1m, temirga mahkamlangan",          "emoji": "📢"},
]

# ─────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Buyurtma berish",    callback_data="order")],
        [InlineKeyboardButton("💰 Narx kalkulyator",   callback_data="calc")],
        [InlineKeyboardButton("🖼 Portfolio",           callback_data="portfolio")],
        [InlineKeyboardButton("📞 Biz bilan bog'lanish", callback_data="contact")],
    ])

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "Mijoz"
    text = (
        f"👋 Salom, *{name}*!\n\n"
        f"🖨 *{COMPANY}* botiga xush kelibsiz!\n\n"
        f"Biz qillaydigan xizmatlar:\n"
        f"🖼 Banner · 🎨 Orakal · ☁️ Tumanka · 📋 Stiker · 📄 Litak\n\n"
        f"Quyidagi bo'limlardan birini tanlang 👇"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

async def back_to_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"🖨 *{COMPANY}* — asosiy menyu:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )
    return ConversationHandler.END

# ─────────────────────────────────────────
#  CONTACT
# ─────────────────────────────────────────
async def contact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        f"📞 *Biz bilan bog'lanish*\n\n"
        f"🏢 Kompaniya: *{COMPANY}*\n"
        f"📱 Telefon: `{PHONE}`\n"
        f"✈️ Telegram: {TG}\n"
        f"📍 Manzil: {CITY}\n\n"
        f"⏰ Ish vaqti: Har kuni 09:00 – 20:00\n\n"
        f"Maketingizni Telegramga yuboring — tez javob beramiz! ✅"
    )
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="menu")]])
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ─────────────────────────────────────────
#  PORTFOLIO
# ─────────────────────────────────────────
async def portfolio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = f"🖼 *Portfolio — Bajarilgan ishlar*\n\n"
    for i, item in enumerate(PORTFOLIO, 1):
        text += f"{item['emoji']} *{item['name']}*\n   {item['desc']}\n\n"
    text += "📸 Yangi ishlar uchun Telegramda yozing: " + TG
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Buyurtma berish", callback_data="order")],
        [InlineKeyboardButton("🔙 Orqaga",          callback_data="menu")],
    ])
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ─────────────────────────────────────────
#  NARX KALKULYATOR
# ─────────────────────────────────────────
async def calc_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Banner (Flex)",   callback_data="ctype_banner")],
        [InlineKeyboardButton("🎨 Orakal plyonka", callback_data="ctype_orakal")],
        [InlineKeyboardButton("☁️ Tumanka",         callback_data="ctype_tumanka")],
        [InlineKeyboardButton("📋 Stiker",          callback_data="ctype_stiker")],
        [InlineKeyboardButton("🔙 Orqaga",          callback_data="menu")],
    ])
    await query.edit_message_text(
        "💰 *Narx Kalkulyator*\n\nQaysi mahsulot narxini hisoblash kerak?",
        parse_mode="Markdown", reply_markup=kb
    )
    return CALC_TYPE

async def calc_type(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ptype = query.data.replace("ctype_", "")
    ctx.user_data["calc_type"] = ptype
    info = PRICES[ptype]
    ctx.user_data["calc_info"] = info
    await query.edit_message_text(
        f"✅ Tanlandi: *{info['name']}*\n\n📐 Eni (kenglik) necha metr?\n_(masalan: 3)_",
        parse_mode="Markdown"
    )
    return CALC_W

async def calc_w(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        ctx.user_data["calc_w"] = float(update.message.text.replace(",", "."))
        await update.message.reply_text("📐 Bo'yi (balandlik) necha metr?\n_(masalan: 2)_")
        return CALC_H
    except:
        await update.message.reply_text("⚠️ Faqat raqam yozing. Masalan: 3")
        return CALC_W

async def calc_h(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        ctx.user_data["calc_h"] = float(update.message.text.replace(",", "."))
        await update.message.reply_text("📦 Necha dona kerak?\n_(masalan: 1)_")
        return CALC_QTY
    except:
        await update.message.reply_text("⚠️ Faqat raqam yozing. Masalan: 2")
        return CALC_H

async def calc_qty(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        qty  = int(update.message.text)
        w    = ctx.user_data["calc_w"]
        h    = ctx.user_data["calc_h"]
        info = ctx.user_data["calc_info"]
        area = w * h
        unit_price = info["price"]
        total = area * unit_price * qty

        text = (
            f"💰 *Narx Hisobi*\n\n"
            f"📦 Mahsulot: {info['name']}\n"
            f"📐 O'lcham: {w}m × {h}m = {area:.2f} m²\n"
            f"🔢 Miqdor: {qty} dona\n"
            f"💵 Birlik narxi: {unit_price:,} so'm/m²\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💰 *Jami: {total:,.0f} so'm*\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"_* Aniq narx uchun qo'ng'iroq qiling_\n"
            f"📞 {PHONE}"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📦 Buyurtma berish", callback_data="order")],
            [InlineKeyboardButton("🔄 Qayta hisoblash", callback_data="calc")],
            [InlineKeyboardButton("🔙 Asosiy menyu",    callback_data="menu")],
        ])
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
        return ConversationHandler.END
    except:
        await update.message.reply_text("⚠️ Faqat raqam yozing. Masalan: 2")
        return CALC_QTY

# ─────────────────────────────────────────
#  BUYURTMA
# ─────────────────────────────────────────
async def order_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Banner",   callback_data="otype_banner")],
        [InlineKeyboardButton("🎨 Orakal",  callback_data="otype_orakal")],
        [InlineKeyboardButton("☁️ Tumanka", callback_data="otype_tumanka")],
        [InlineKeyboardButton("📋 Stiker",  callback_data="otype_stiker")],
        [InlineKeyboardButton("📄 Litak",   callback_data="otype_litak")],
        [InlineKeyboardButton("🔙 Orqaga",  callback_data="menu")],
    ])
    await query.edit_message_text(
        "📦 *Buyurtma berish*\n\nQaysi mahsulot kerak?",
        parse_mode="Markdown", reply_markup=kb
    )
    return ORDER_TYPE

async def order_type(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ctx.user_data["order_type"] = query.data.replace("otype_", "")
    await query.edit_message_text(
        "📐 O'lcham: *Eni* (kenglik) necha metr?\n_(masalan: 3)_",
        parse_mode="Markdown"
    )
    return ORDER_SIZE_W

async def order_size_w(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        ctx.user_data["order_w"] = update.message.text.strip()
        await update.message.reply_text("📐 *Bo'yi* (balandlik) necha metr?\n_(masalan: 2)_", parse_mode="Markdown")
        return ORDER_SIZE_H
    except:
        await update.message.reply_text("⚠️ Raqam yozing.")
        return ORDER_SIZE_W

async def order_size_h(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["order_h"] = update.message.text.strip()
    await update.message.reply_text("🔢 Necha dona kerak?\n_(masalan: 1)_", parse_mode="Markdown")
    return ORDER_QTY

async def order_qty(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["order_qty"] = update.message.text.strip()
    await update.message.reply_text(
        "💬 Qo'shimcha izoh yoki talablar bormi?\n_(yo'q bo'lsa 'yo'q' deb yozing)_",
        parse_mode="Markdown"
    )
    return ORDER_COMMENT

async def order_comment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["order_comment"] = update.message.text.strip()
    await update.message.reply_text(
        "📱 *Telefon raqamingiz?*\n_(masalan: +998901234567)_",
        parse_mode="Markdown"
    )
    return ORDER_PHONE

async def order_phone(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    user  = update.effective_user
    d     = ctx.user_data

    ptype = d.get("order_type", "—")
    pname = PRICES.get(ptype, {}).get("name", ptype)

    # Mijozga xabar
    confirm = (
        f"✅ *Buyurtmangiz qabul qilindi!*\n\n"
        f"📦 Mahsulot: {pname}\n"
        f"📐 O'lcham: {d.get('order_w','—')}m × {d.get('order_h','—')}m\n"
        f"🔢 Miqdor: {d.get('order_qty','—')} dona\n"
        f"💬 Izoh: {d.get('order_comment','—')}\n"
        f"📱 Tel: {phone}\n\n"
        f"⏳ Tez orada siz bilan bog'lanamiz!\n"
        f"📞 {PHONE} | {TG}"
    )
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Asosiy menyu", callback_data="menu")]])
    await update.message.reply_text(confirm, parse_mode="Markdown", reply_markup=kb)

    # Adminga xabar
    admin_msg = (
        f"🔔 *YANGI BUYURTMA!*\n\n"
        f"👤 Mijoz: {user.full_name}\n"
        f"🆔 Telegram ID: @{user.username or '—'} ({user.id})\n"
        f"📦 Mahsulot: {pname}\n"
        f"📐 O'lcham: {d.get('order_w','—')}m × {d.get('order_h','—')}m\n"
        f"🔢 Miqdor: {d.get('order_qty','—')} dona\n"
        f"💬 Izoh: {d.get('order_comment','—')}\n"
        f"📱 Tel: {phone}\n"
        f"⏰ Vaqt: hozir"
    )
    try:
        await ctx.bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Admin xabar xatosi: {e}")

    return ConversationHandler.END

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.", reply_markup=main_menu_keyboard())
    return ConversationHandler.END

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Buyurtma handler
    order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(order_start, pattern="^order$")],
        states={
            ORDER_TYPE:   [CallbackQueryHandler(order_type, pattern="^otype_")],
            ORDER_SIZE_W: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_size_w)],
            ORDER_SIZE_H: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_size_h)],
            ORDER_QTY:    [MessageHandler(filters.TEXT & ~filters.COMMAND, order_qty)],
            ORDER_COMMENT:[MessageHandler(filters.TEXT & ~filters.COMMAND, order_comment)],
            ORDER_PHONE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, order_phone)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CallbackQueryHandler(back_to_menu, pattern="^menu$"),
        ],
        allow_reentry=True,
    )

    # Kalkulyator handler
    calc_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(calc_start, pattern="^calc$")],
        states={
            CALC_TYPE: [CallbackQueryHandler(calc_type, pattern="^ctype_")],
            CALC_W:    [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_w)],
            CALC_H:    [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_h)],
            CALC_QTY:  [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_qty)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CallbackQueryHandler(back_to_menu, pattern="^menu$"),
        ],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(order_conv)
    app.add_handler(calc_conv)
    app.add_handler(CallbackQueryHandler(portfolio, pattern="^portfolio$"))
    app.add_handler(CallbackQueryHandler(contact,   pattern="^contact$"))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^menu$"))

    print(f"🚀 {COMPANY} boti ishga tushdi!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
