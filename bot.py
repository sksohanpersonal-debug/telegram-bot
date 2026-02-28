import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8784425124:AAHPhkwkd2XpS0-O3CjdU52_vfEOU-od6k0"       
API_TOKEN = "ca968e2c-60fc-4855-85d9-a7eab46ec4fd"   

BASE_URL = "http://api.ucbot.store"

async def topup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        uid = context.args[0]
        uc_codes = context.args[1].split(",")

        headers = {
            "Authorization": API_TOKEN
        }

        payload = {
            "uid": uid,
            "uc": uc_codes
        }

        # Debug: print payload and headers
        print("Payload:", payload)
        print("Headers:", headers)

        response = requests.post(
            f"{BASE_URL}/topup",
            json=payload,
            headers=headers
        )

        # Debug: print full response
        print("Response:", response.text)

        data = response.json()

        if data.get("status") == "success":
            username = data.get("username")
            success = data.get("success")
            failed = data.get("failed")

            message = f"🎮 Username: {username}\n"
            message += f"✅ Success: {success}\n"
            message += f"❌ Failed: {failed}\n\n"

            for item in data.get("batch", []):
                status_icon = "✅" if item["ok"] else "❌"
                message += f"{status_icon} {item['uc']} - {item['detail']}\n"

            await update.message.reply_text(message)
        else:
            # Show full API response in Telegram
            await update.message.reply_text(f"❌ Top-up Failed (API Error)\nResponse:\n{response.text}")

    except IndexError:
        await update.message.reply_text("Usage:\n/topup UID UC1,UC2,UC3")
    except Exception as e:
        await update.message.reply_text(f"❌ Unexpected error:\n{e}")
        print("Exception:", e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("topup", topup))

app.run_polling()
