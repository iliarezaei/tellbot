#!/usr/bin/env python3
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN      = os.environ.get("BOT_TOKEN", "")
OWNER_ID       = int(os.environ.get("OWNER_ID", "5851560671"))
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "MrRezaa69")
WEBAPP_URL     = os.environ.get("WEBAPP_URL", "https://telbot-54b3.onrender.com")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

WELCOME = (
    "👋 سلام! من دستیار هوشمند *ایلیا رضایی* هستم.\n\n"
    "• 🛠 متخصص شبکه — MikroTik، Cisco\n"
    "• 🐧 لینوکس و ویندوز سرور\n"
    "• 📷 نصب CCTV\n"
    "• 📡 کابل‌کشی ساختارمند\n\n"
    "برای مشاهده خدمات و تماس، روی دکمه زیر بزن 👇"
)

FAQS = {
    "services":"🛠 *خدمات:*\n• شبکه اداری (MikroTik/Cisco)\n• CCTV\n• سرور لینوکس\n• ویندوز سرور\n• کابل‌کشی\n• پشتیبانی",
    "experience":"📋 *مهارت‌ها:*\n• Linux, Windows Server\n• MikroTik RouterOS, Cisco IOS\n• شبکه پسیو Cat5e/Cat6\n• CCTV — IP و آنالوگ\n• ۱.۵+ سال تجربه",
    "location":"📍 *موقعیت:*\n• حضوری: یزد و اطراف\n• از راه دور: سراسر ایران",
    "availability":"🟢 ایلیا در حال حاضر برای پروژه‌های جدید آماده است!",
}

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 باز کردن Mini App", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton("🛠 خدمات", callback_data="services"),
            InlineKeyboardButton("📋 مهارت‌ها", callback_data="experience"),
        ],
        [
            InlineKeyboardButton("📍 موقعیت", callback_data="location"),
            InlineKeyboardButton("🟢 همکاری", callback_data="availability"),
        ],
        [InlineKeyboardButton("💬 تماس مستقیم ↗", url=f"https://t.me/{OWNER_USERNAME}")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Mini App", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("💬 تماس مستقیم ↗", url=f"https://t.me/{OWNER_USERNAME}")],
        [InlineKeyboardButton("🏠 منوی اصلی", callback_data="home")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(WELCOME, parse_mode="Markdown", reply_markup=main_keyboard())
    if user.id != OWNER_ID:
        await context.bot.send_message(OWNER_ID,
            f"👤 *کاربر جدید:*\nنام: {user.full_name}\n@{user.username or 'ندارد'} | `{user.id}`",
            parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id == OWNER_ID:
        return
    text = update.message.text
    await update.message.reply_text(
        "✅ پیامت دریافت شد!\n\nایلیا در اولین فرصت جواب می‌ده.\nبرای پاسخ سریع‌تر از Mini App استفاده کن 👇",
        reply_markup=back_keyboard()
    )
    await context.bot.send_message(OWNER_ID,
        f"📩 *پیام جدید:*\n👤 {user.full_name} | @{user.username or 'ندارد'} | `{user.id}`\n\n💬 {text}",
        parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "home":
        await query.edit_message_text(WELCOME, parse_mode="Markdown", reply_markup=main_keyboard())
    elif query.data in FAQS:
        await query.edit_message_text(FAQS[query.data], parse_mode="Markdown", reply_markup=back_keyboard())

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 /start — منوی اصلی\nیا فقط پیامت رو بنویس!", reply_markup=main_keyboard())

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ ربات ایلیا رضایی با Mini App در حال اجراست...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
