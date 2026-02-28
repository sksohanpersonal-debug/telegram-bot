import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import uuid  # Unique orderid

BOT_TOKEN = "8784425124:AAHPhkwkd2XpS0-O3CjdU52_vfEOU-od6k0"      
API_TOKEN = "ca968e2c-60fc-4855-85d9-a7eab46ec4fd"        
BASE_URL = "http://api.ucbot.store"

# এখানে command নাম empty string ব্যবহার করা হবে যাতে "/UID ..." format কাজ করে
async def topup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Usage:\n/UID UC_CODE\nExample:\n/2025409039 BDMB-T-S-01760557 1973-7177-2357-5122")
            return

        # প্রথম অংশ UID
        playerid = context.args[0]

        # বাকি অংশ join করে এক UC code হিসেবে পাঠানো হবে
        code = " ".join(context.args[1:])

        headers = {
            "Authorization": API_TOKEN,
            "Content-Type": "application/json"
        }

        payload = {
            "orderid": str(uuid.uuid4()),  # unique order id
            "playerid": playerid,
            "code": code
        }

        response = requests.post(
            f"{BASE_URL}/topup-sync",
            json=payload,
            headers=headers
        )

        data = response.json()

        # Telegram reply nicely format করা
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

# Command নাম empty string দেওয়া হচ্ছে যাতে "/UID ..." format কাজ করে
app.add_handler(CommandHandler("", topup))

app.run_polling()
