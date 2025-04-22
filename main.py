import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import os

TOKEN = "8109926247:AAHdLA2Oj4icyWNv-T9EzbXsLTOhXXJ5oG4"
ASAAS_API_KEY = "$aact_prod_000MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OjNmYjM2OTM3LTc1ZWYtNDFkZi05NjY5LThhMDdiZjIyYjU4MDo6JGFhY2hfODI5YWZjZDQtOGU4Ni00OGY3LThhMWEtOTkyOGNjOGMxOTJi"
VIP_CHANNEL_LINK = "https://t.me/+lr6ZrCyDtdozNTVh"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎟 Comprar Acesso VIP", callback_data='buy_vip')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Olá! Compre acesso VIP exclusivo por 30 dias.\n\nClique no botão abaixo para gerar seu Pix:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_vip":
        headers = {
            "Content-Type": "application/json",
            "access_token": ASAAS_API_KEY
        }

        # 1. Criar cliente fictício
        cliente_payload = {
            "name": f"Cliente {query.from_user.id}",
            "cpfCnpj": "12345678909",
            "email": f"{query.from_user.id}@fakeemail.com",
            "phone": "+5547958339457"
        }

        cliente_res = requests.post("https://www.asaas.com/api/v3/customers", json=cliente_payload, headers=headers)

        if cliente_res.status_code == 200:
            customer_id = cliente_res.json()["id"]

            # 2. Criar pagamento
            pagamento_payload = {
                "customer": customer_id,
                "billingType": "PIX",
                "value": 28.00,
                "description": "Acesso VIP por 30 dias",
                "dueDate": "2025-05-01"
            }

            pagamento_res = requests.post("https://www.asaas.com/api/v3/payments", json=pagamento_payload, headers=headers)

            if pagamento_res.status_code == 200:
                pagamento = pagamento_res.json()
                invoice_url = pagamento["invoiceUrl"]

                await query.edit_message_text(
                    f"✅ Pagamento gerado!\n\n🔗 Pague seu Pix aqui:\n{invoice_url}\n\n"
                    f"Após o pagamento, você será adicionado automaticamente ao canal VIP."
                )
            else:
                await query.edit_message_text("❌ Erro ao gerar pagamento. Tente novamente.")
        else:
            await query.edit_message_text("❌ Erro ao criar cliente no Asaas. Tente novamente.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
