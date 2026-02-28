import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import uuid

BOT_TOKEN = "8784425124:AAHPhkwkd2XpS0-O3CjdU52_vfEOU-od6k0"
API_TOKEN = "ca968e2c-60fc-4855-85d9-a7eab46ec4fd"
BASE_URL = "http://api.ucbot.store"

async def topup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        if not text.startswith("/"):
            return  # ignore non-command messages

        parts = text[1:].split(maxsplit=1)  # remove "/" and split
        if len(parts) < 2:
            await update.message.reply_text(
                "Usage:\n/UID UC_CODE\nExample:\n/2025409039 BDMB-T-S-01760557 1973-7177-2357-5122"
            )
            return

        playerid = parts[0]
        code = parts[1]  # rest of the text (space included)

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

# MessageHandler দিয়ে সব "/" command handle হবে
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/'), topup))

app.run_polling()
