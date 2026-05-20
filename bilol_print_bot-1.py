#!/usr/bin/env python3
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ============================================================
BOT_TOKEN = "8695094650:AAFTL34CS3PES_mthfOxFcOJTWNp1b5gYjc"
ADMIN_ID   = 8286195257
COMPANY    = "Bilol Print"
PHONE      = "+998 93 005 73 33"
TG         = "@Te_7333"
CITY       = "Toshkent shahri"
# ============================================================

logging.basicConfig(level=logging.INFO)

ORDER_TYPE, ORDER_W, ORDER_H, ORDER_QTY, ORDER_COMMENT, ORDER_PHONE = range(6)
CALC_TYPE, CALC_W, CALC_H, CALC_QTY = range(6, 10)

PRICES = {
    "banner":  {"name": "🖼 Banner (Flex)",   "price": 15000},
    "orakal":  {"name": "🎨 Orakal plyonka",  "price": 25000},
    "tumanka": {"name": "☁️ Tumanka",          "price": 20000},
    "stiker":  {"name": "📋 Stiker",           "price": 30000},
    "litak":   {"name": "📄 Litak",            "price": 500},
}

def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Buyurtma berish",  callback_data="order")],
        [InlineKeyboardButton("💰 Narx kalkulyator", callback_data="calc")],
        [InlineKeyboardButton("🖼 Portfolio",         callback_data="portfolio")],
        [InlineKeyboardButton("📞 Bog'lanish",        callback_data="contact")],
    ])

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Salom! *{COMPANY}* botiga xush kelibsiz!\n\n"
        f"🖨 Banner · Orakal · Tumanka · Stiker\n\nQuyidan tanlang 👇",
        parse_mode="Markdown", reply_markup=main_kb()
    )

async def menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"🖨 *{COMPANY}* — asosiy menyu:",
        parse_mode="Markdown", reply_markup=main_kb()
    )
    return ConversationHandler.END

async def contact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"📞 *Bog'lanish*\n\n📱 Tel: `{PHONE}`\n✈️ Telegram: {TG}\n📍 {CITY}\n⏰ 09:00–20:00",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="menu")]]))

async def portfolio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "🖼 *Bajarilgan ishlar*\n\n"
        "🖼 Katta format banner — 3×6m flex\n"
        "🪟 Vitrina orakal — rang-barang plyonka\n"
        "☁️ Tumanka pechat — A2, yuqori sifat\n"
        "🏷 Stiker to'plami — 100 dona\n"
        "📢 Reklama banneri — 2×1m\n\n"
        f"📸 Ko'proq: {TG}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📦 Buyurtma", callback_data="order")],
            [InlineKeyboardButton("🔙 Orqaga",   callback_data="menu")],
        ]))

# KALKULYATOR
async def calc_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "💰 *Narx Kalkulyator*\n\nQaysi mahsulot?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🖼 Banner",   callback_data="ct_banner")],
            [InlineKeyboardButton("🎨 Orakal",  callback_data="ct_orakal")],
            [InlineKeyboardButton("☁️ Tumanka", callback_data="ct_tumanka")],
            [InlineKeyboardButton("📋 Stiker",  callback_data="ct_stiker")],
            [InlineKeyboardButton("🔙 Orqaga",  callback_data="menu")],
        ]))
    return CALC_TYPE

async def calc_type(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    t = update.callback_query.data.replace("ct_", "")
    ctx.user_data["ct"] = t
    await update.callback_query.edit_message_text(
        f"✅ *{PRICES[t]['name']}*\n\n📐 Eni necha metr? (masalan: 3)",
        parse_mode="Markdown")
    return CALC_W

async def calc_w(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        ctx.user_data["cw"] = float(update.message.text.replace(",", "."))
        await update.message.reply_text("📐 Bo'yi necha metr? (masalan: 2)")
        return CALC_H
    except:
        await update.message.reply_text("⚠️ Faqat raqam yozing!")
        return CALC_W

async def calc_h(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        ctx.user_data["ch"] = float(update.message.text.replace(",", "."))
        await update.message.reply_text("🔢 Necha dona?")
        return CALC_QTY
    except:
        await update.message.reply_text("⚠️ Faqat raqam yozing!")
        return CALC_H

async def calc_qty(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        qty = int(update.message.text)
        w = ctx.user_data["cw"]
        h = ctx.user_data["ch"]
        info = PRICES[ctx.user_data["ct"]]
        total = w * h * info["price"] * qty
        await update.message.reply_text(
            f"💰 *Narx Hisobi*\n\n{info['name']}\n"
            f"📐 {w}m × {h}m = {w*h:.2f} m²\n🔢 {qty} dona\n\n"
            f"━━━━━━━━━━━━━\n💰 *Jami: {total:,.0f} so'm*\n━━━━━━━━━━━━━\n\n📞 {PHONE}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📦 Buyurtma", callback_data="order")],
                [InlineKeyboardButton("🔙 Menyu",    callback_data="menu")],
            ]))
        return ConversationHandler.END
    except:
        await update.message.reply_text("⚠️ Faqat raqam yozing!")
        return CALC_QTY

# BUYURTMA
async def order_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "📦 *Buyurtma*\n\nQaysi mahsulot?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🖼 Banner",   callback_data="ot_banner")],
            [InlineKeyboardButton("🎨 Orakal",  callback_data="ot_orakal")],
            [InlineKeyboardButton("☁️ Tumanka", callback_data="ot_tumanka")],
            [InlineKeyboardButton("📋 Stiker",  callback_data="ot_stiker")],
            [InlineKeyboardButton("📄 Litak",   callback_data="ot_litak")],
            [InlineKeyboardButton("🔙 Orqaga",  callback_data="menu")],
        ]))
    return ORDER_TYPE

async def order_type(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    ctx.user_data["ot"] = update.callback_query.data.replace("ot_", "")
    await update.callback_query.edit_message_text("📐 Eni necha metr? (masalan: 3)")
    return ORDER_W

async def order_w(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["ow"] = update.message.text.strip()
    await update.message.reply_text("📐 Bo'yi necha metr? (masalan: 2)")
    return ORDER_H

async def order_h(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["oh"] = update.message.text.strip()
    await update.message.reply_text("🔢 Necha dona?")
    return ORDER_QTY

async def order_qty(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["oq"] = update.message.text.strip()
    await update.message.reply_text("💬 Qo'shimcha izoh? (yo'q bo'lsa: yo'q)")
    return ORDER_COMMENT

async def order_comment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["oc"] = update.message.text.strip()
    await update.message.reply_text("📱 Telefon raqamingiz?")
    return ORDER_PHONE

async def order_phone(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    user = update.effective_user
    d = ctx.user_data
    pname = PRICES.get(d.get("ot",""), {}).get("name", d.get("ot",""))
    await update.message.reply_text(
        f"✅ *Buyurtma qabul qilindi!*\n\n{pname}\n"
        f"📐 {d.get('ow','—')}m × {d.get('oh','—')}m | {d.get('oq','—')} dona\n"
        f"💬 {d.get('oc','—')}\n📱 {phone}\n\n⏳ Tez orada bog'lanamiz!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menyu", callback_data="menu")]]))
    try:
        await ctx.bot.send_message(
            ADMIN_ID,
            f"🔔 *YANGI BUYURTMA!*\n\n👤 {user.full_name} | @{user.username or '—'}\n"
            f"{pname}\n📐 {d.get('ow','—')}m × {d.get('oh','—')}m\n"
            f"🔢 {d.get('oq','—')} dona\n💬 {d.get('oc','—')}\n📱 {phone}",
            parse_mode="Markdown")
    except Exception as e:
        logging.error(e)
    return ConversationHandler.END

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.", reply_markup=main_kb())
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    calc_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(calc_start, pattern="^calc$")],
        states={
            CALC_TYPE: [CallbackQueryHandler(calc_type, pattern="^ct_")],
            CALC_W:    [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_w)],
            CALC_H:    [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_h)],
            CALC_QTY:  [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_qty)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CallbackQueryHandler(menu, pattern="^menu$")],
        allow_reentry=True,
    )

    order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(order_start, pattern="^order$")],
        states={
            ORDER_TYPE:    [CallbackQueryHandler(order_type, pattern="^ot_")],
            ORDER_W:       [MessageHandler(filters.TEXT & ~filters.COMMAND, order_w)],
            ORDER_H:       [MessageHandler(filters.TEXT & ~filters.COMMAND, order_h)],
            ORDER_QTY:     [MessageHandler(filters.TEXT & ~filters.COMMAND, order_qty)],
            ORDER_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_comment)],
            ORDER_PHONE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, order_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CallbackQueryHandler(menu, pattern="^menu$")],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(calc_conv)
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(portfolio, pattern="^portfolio$"))
    app.add_handler(CallbackQueryHandler(contact,   pattern="^contact$"))
    app.add_handler(CallbackQueryHandler(menu,      pattern="^menu$"))

    print(f"🚀 {COMPANY} boti ishga tushdi!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
