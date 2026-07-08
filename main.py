from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from keep_alive import keep_alive

app = Client(
    "my_official_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# 1. നിലവിലുള്ള സ്റ്റാർട്ട് കമാൻഡ്
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("WETFLAX ന്യൂസ് 🗞️", url="https://t.me/your_wetflax_channel")],
        [InlineKeyboardButton("TRENDA സ്റ്റോർ 🛒", url="https://t.me/your_trenda_channel")]
    ])
    
    await message.reply_text(
        "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ പുതിയ ബോട്ട് ആണ്. താഴെയുള്ള ബട്ടണുകൾ ചെക്ക് ചെയ്യുക.", 
        reply_markup=buttons
    )

# 2. നിലവിലുള്ള പെൻഡിങ് റിക്വസ്റ്റുകൾ ഒറ്റയടിക്ക് അക്സെപ്റ്റ് ചെയ്യാൻ
@app.on_message(filters.command("acceptall") & filters.private)
async def accept_all(client, message):
    if len(message.command) < 2:
        await message.reply_text("ദയവായി ചാനലിന്റെ യൂസർനെയിം കൂടെ നൽകുക.\nഉദാഹരണത്തിന്: `/acceptall @your_channel_name`")
        return
    
    chat_id = message.command[1]
    processing_msg = await message.reply_text(f"⏳ {chat_id} -ലെ റിക്വസ്റ്റുകൾ അക്സെപ്റ്റ് ചെയ്തു തുടങ്ങുന്നു...")
    
    try:
        # എല്ലാ റിക്വസ്റ്റുകളും ഒറ്റയടിക്ക് അപ്രൂവ് ചെയ്യാനുള്ള കോഡ്
        await client.approve_all_chat_join_requests(chat_id)
        await processing_msg.edit_text(f"✅ {chat_id} -ലെ എല്ലാ പെൻഡിങ് റിക്വസ്റ്റുകളും വിജയകരമായി അക്സെപ്റ്റ് ചെയ്തു!")
    except Exception as e:
        await processing_msg.edit_text(f"❌ എറർ സംഭവിച്ചു: {e}\n(ബോട്ട് ആ ചാനലിൽ അഡ്മിൻ ആണെന്ന് ഉറപ്പുവരുത്തുക)")

# 3. പുതിയതായി വരുന്ന റിക്വസ്റ്റുകൾ തനിയെ അക്സെപ്റ്റ് ചെയ്യാൻ (Auto-Approve)
@app.on_chat_join_request()
async def auto_approve(client, message):
    try:
        # വരുന്ന റിക്വസ്റ്റ് അപ്പൊത്തന്നെ അക്സെപ്റ്റ് ചെയ്യുന്നു
        await client.approve_chat_join_request(message.chat.id, message.from_user.id)
        
        # അക്സെപ്റ്റ് ചെയ്ത യൂസർക്ക് ഒരു മെസ്സേജ് അയക്കാൻ (വേണ്ടെങ്കിൽ ഈ വരി ഒഴിവാക്കാം)
        welcome_text = f"നമസ്കാരം {message.from_user.first_name}, {message.chat.title} ലേക്ക് സ്വാഗതം! 🥳"
        await client.send_message(message.from_user.id, welcome_text)
    except Exception as e:
        print(f"Error auto-approving: {e}")

print("ബോട്ട് സ്റ്റാർട്ട് ആകുന്നു...")
keep_alive()
app.run()
