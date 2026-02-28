import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import uuid  # Unique orderid

BOT_TOKEN = "8784425124:AAHPhkwkd2XpS0-O3CjdU52_vfEOU-od6k0"
API_TOKEN = "ca968e2c-60fc-4855-85d9-a7eab46ec4fd"

BASE_URL = "http://api.ucbot.store"

async def topup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Input: /topup UID CODE1,CODE2
        playerid = context.args[0]
        codes = context.args[1]

        headers = {
            "Authorization": API_TOKEN,
            "Content-Type": "application/json"
        }

        payload = {
            "orderid": str(uuid.uuid4()),  # unique order id
            "playerid": playerid,
            "code": codes
        }

        response = requests.post(
            f"{BASE_URL}/topup-sync",
            json=payload,
            headers=headers
        )

        data = response.json()
        await update.message.reply_text(f"API Response:\n{data}")

    except IndexError:
        await update.message.reply_text("Usage:\n/topup UID CODE1,CODE2")
    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{e}")
        print("Exception:", e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("topup", topup))
app.run_polling()
