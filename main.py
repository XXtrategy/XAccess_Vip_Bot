import logging
import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === CONFIGURAÇÕES ===
TOKEN = "8109926247:AAHdLA2Oj4icyWNv-T9EzbXsLTOhXXJ5oG4"
ASAAS_API_KEY = "sua_api_key_aqui"
VIP_CHANNEL_LINK = "https://t.me/+lr6ZrCyDtdozNTVh"

# === LOGS ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === FUNÇÕES SYNC PARA EXECUÇÃO EXTERNA ===
def criar_pagamento_sync(user_id: int, headers: dict):
    try:
        cliente_payload = {
            "name": f"Cliente {user_id}",
            "cpfCnpj": "12345678909",
            "email": f"{user_id}@fakeemail.com",
            "phone": "+5547999999999"
        }

        cliente_res = requests.post("https://www.asaas.com/api/v3/customers", json=cliente_payload, headers=headers)
        if cliente_res.status_code != 200:
            return None

        customer_id = cliente_res.json()["id"]

        pagamento_payload = {
            "customer": customer_id,
            "billingType": "PIX",
            "value": 28.00,
            "description": "Acesso VIP por 30 dias",
            "dueDate": "2025-05-01"
        }

        pagamento_res = requests.post("https://www.asaas.com/api/v3/payments", json=pagamento_payload, headers=headers)
        if pagamento_res.status_code != 200:
            return None

        return pagamento_res.json()["invoiceUrl"]

    except Exception as e:
        logging.error(f"Erro ao criar pagamento: {e}")
        return None

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎟 Comprar Acesso VIP", callback_data='buy_vip')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Olá! Compre acesso VIP exclusivo por 30 dias.", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_vip":
        headers = {
            "Content-Type": "application/json",
            "access_token": ASAAS_API_KEY
        }

        user_id = query.from_user.id
        loop = asyncio.get_event_loop()
        invoice_url = await loop.run_in_executor(None, criar_pagamento_sync, user_id, headers)

        if invoice_url:
            await query.edit_message_text(
                f"✅ Pagamento gerado!\n\n🔗 Pague seu Pix aqui:\n{invoice_url}\n\n"
                f"Após o pagamento, você será adicionado automaticamente ao canal VIP."
            )
        else:
            await query.edit_message_text("❌ Erro ao gerar o pagamento. Tente novamente mais tarde.")

# === MAIN ===
def main():
    app = ApplicationBuilder().token(TOKEN).get_updates_request_timeout(60).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
