import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import uuid

BOT_TOKEN = "8784425124:AAHPhkwkd2XpS0-O3CjdU52_vfEOU-od6k0"      # <-- Telegram Bot Token
API_TOKEN = "ca968e2c-60fc-4855-85d9-a7eab46ec4fd"     # <-- ucbot.store API Token
BASE_URL = "http://api.ucbot.store"

async def topup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        if not text.startswith("/r"):
            return  # ignore non /r commands

        parts = text[2:].split(maxsplit=1)  # remove /r and split
        if len(parts) < 2:
            await update.message.reply_text(
                "Usage:\n/rUID UC_CODE\nExample:\n/r2025409039 BDMB-T-S-01760557 1973-7177-2357-5122"
            )
            return

        playerid = parts[0]
        code = parts[1]

        headers = {
            "Authorization": API_TOKEN,
            "Content-Type": "application/json"
        }

        payload = {
            "orderid": str(uuid.uuid4()),
            "playerid": playerid,
            "code": code
        }

        response = requests.post(f"{BASE_URL}/topup-sync", json=payload, headers=headers)
        data = response.json()

        if "batch" in data:
            message = f"🎮 Username: {data.get('username', 'Unknown')}\n"
            message += f"✅ Success: {data.get('success',0)}\n"
            message += f"❌ Failed: {data.get('failed',0)}\n\n"

            for item in data.get("batch", []):
                status_icon = "✅" if item["ok"] else "❌"
                message += f"{status_icon} {item['uc']} - {item['detail']}\n"

            await update.message.reply_text(message)
        else:
            await update.message.reply_text(f"❌ Top-up Failed\nResponse:\n{data}")

    except Exception as e:
        await update.message.reply_text(f"❌ Unexpected Error:\n{e}")
        print("Exception:", e)

app = ApplicationBuilder().token(BOT_TOKEN).build()

# MessageHandler দিয়ে সব /r commands handle হবে
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/r'), topup))

app.run_polling()
