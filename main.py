from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from keep_alive import keep_alive

# ഇവിടെ bot_token ആണ് നൽകുന്നത്
app = Client(
    "my_official_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

@app.on_message(filters.command("start"))
def start_command(client, message):
    # ട്രെൻഡ സ്റ്റോറിനും വെറ്റ്ഫ്ലാക്സിനുമുള്ള ബട്ടണുകൾ ഇവിടെ സെറ്റ് ചെയ്യാം
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("WETFLAX ന്യൂസ് 🗞️", url="https://t.me/your_wetflax_channel")],
        [InlineKeyboardButton("TRENDA സ്റ്റോർ 🛒", url="https://t.me/your_trenda_channel")]
    ])
    
    message.reply_text(
        "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ പുതിയ ബോട്ട് ആണ്. താഴെയുള്ള ബട്ടണുകൾ ചെക്ക് ചെയ്യുക.", 
        reply_markup=buttons
    )

print("ബോട്ട് സ്റ്റാർട്ട് ആകുന്നു...")
keep_alive()
app.run()
