from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Configuração de logs
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# === CONFIGURAÇÕES ===
TOKEN = "8109926247:AAHdLA2Oj4icyWNv-T9EzbXsLTOhXXJ5oG4"
VIP_CHANNEL_LINK = "https://t.me/+lr6ZrCyDtdozNTVh"

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎟 Comprar Acesso VIP", callback_data="buy_vip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            "👋 Olá! Compre acesso VIP exclusivo por 30 dias.",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "👋 Olá! Compre acesso VIP exclusivo por 30 dias.",
            reply_markup=reply_markup
        )

# === Botão "Comprar Acesso VIP" ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_vip":
        await query.edit_message_text("🚧 Integração com pagamento em breve...")

# === Main ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("✅ Bot está rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
