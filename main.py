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

# --- ഷെയർ ട്രിക്കിനുള്ള സെറ്റിംഗ്സ് ---
# യൂസർമാരുടെ ക്ലിക്ക് കൗണ്ട് താൽക്കാലികമായി സേവ് ചെയ്യാൻ
user_shares = {}
# ഇവിടെ നിങ്ങളുടെ ചാനലിന്റെ ലിങ്ക് കൊടുക്കുക (ഇതാണ് ആളുകൾ ഷെയർ ചെയ്യേണ്ടത്)
SHARE_TEXT = "https://t.me/your_channel_link_here" 
# 3 തവണ ഷെയർ ചെയ്താൽ അവർക്ക് ജോയിൻ ചെയ്യാൻ കിട്ടേണ്ട പ്രൈവറ്റ് ഗ്രൂപ്പ്/ചാനൽ ലിങ്ക് കൊടുക്കുക
JOIN_LINK = "https://t.me/+YourPrivateGroupLinkHere" 
# -----------------------------------

# 1. സ്റ്റാർട്ട് കമാൻഡ്
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

# 2. ഷെയർ ടാസ്ക് തുടങ്ങാനുള്ള കമാൻഡ് (/task)
@app.on_message(filters.command("task") & filters.private)
async def share_task(client, message):
    user_id = message.from_user.id
    user_shares[user_id] = 0 # കൗണ്ട് 0 ആക്കി വെക്കുന്നു
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Share 0/3 ↪️", callback_data="do_share")]
    ])
    
    await message.reply_text(
        "നിങ്ങൾ ഈ ഗ്രൂപ്പിൽ ജോയിൻ ചെയ്യാൻ താഴെയുള്ള ബട്ടണിൽ ക്ലിക്ക് ചെയ്ത് **3 ഗ്രൂപ്പുകളിലേക്ക്** ഞങ്ങളുടെ ചാനൽ ഷെയർ ചെയ്യണം.",
        reply_markup=keyboard
    )

# 3. ഷെയർ ബട്ടണിൽ ക്ലിക്ക് ചെയ്യുമ്പോൾ സംഭവിക്കേണ്ട കാര്യങ്ങൾ
@app.on_callback_query(filters.regex("do_share"))
async def share_button_click(client, callback_query):
    user_id = callback_query.from_user.id
    current_count = user_shares.get(user_id, 0)
    
    if current_count < 3:
        # കൗണ്ട് 1 കൂട്ടുന്നു
        current_count += 1
        user_shares[user_id] = current_count
        
        # അടുത്ത ബട്ടൺ സെറ്റ് ചെയ്യുന്നു (ഉദാ: Share 1/3)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"Share {current_count}/3 ↪️", callback_data="do_share")]
        ])
        
        # മെസ്സേജ് അപ്ഡേറ്റ് ചെയ്യുന്നു
        await callback_query.edit_message_reply_markup(reply_markup=keyboard)
        
        # ഷെയർ ചെയ്യാനുള്ള വിൻഡോ ഓപ്പൺ ആക്കി കൊടുക്കുന്നു
        share_url = f"https://t.me/share/url?url={SHARE_TEXT}"
        await callback_query.answer("ലിങ്ക് ഷെയർ ചെയ്യുക!", url=share_url)
        
        # 3 തവണ തികഞ്ഞാൽ
        if current_count == 3:
            success_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("ഗ്രൂപ്പിൽ ജോയിൻ ചെയ്യുക ✅", url=JOIN_LINK)]
            ])
            await callback_query.edit_message_text(
                "✅ അഭിനന്ദനങ്ങൾ! നിങ്ങൾ 3 ഗ്രൂപ്പുകളിൽ ഷെയർ ചെയ്തു കഴിഞ്ഞു. താഴെയുള്ള ബട്ടൺ വഴി നിങ്ങൾക്ക് ഗ്രൂപ്പിൽ ജോയിൻ ചെയ്യാം.",
                reply_markup=success_keyboard
            )

# 4. പുതിയതായി വരുന്ന റിക്വസ്റ്റുകൾ തനിയെ അക്സെപ്റ്റ് ചെയ്യാൻ (Auto-Approve)
@app.on_chat_join_request()
async def auto_approve(client, message):
    try:
        await client.approve_chat_join_request(message.chat.id, message.from_user.id)
        welcome_text = f"നമസ്കാരം {message.from_user.first_name}, {message.chat.title} ലേക്ക് സ്വാഗതം! 🥳"
        await client.send_message(message.from_user.id, welcome_text)
    except Exception as e:
        print(f"Error auto-approving: {e}")

# 5. ഓട്ടോ-റിപ്ലൈ ഫിൽറ്ററുകൾ (ഗ്രൂപ്പുകളിൽ മാത്രം വർക്ക് ചെയ്യാൻ)
@app.on_message(filters.text & filters.group)
async def auto_filters(client, message):
    text = message.text.lower()
    
    if "news" in text or "വാർത്ത" in text:
        await message.reply_text("ഏറ്റവും പുതിയ ബ്രേക്കിംഗ് വാർത്തകൾക്കും അപ്‌ഡേറ്റുകൾക്കും **WETFLAX** ചാനൽ സന്ദർശിക്കുക! 🗞️")
        
    elif "link" in text or "offer" in text:
        await message.reply_text("ഇന്നത്തെ കിടിലൻ ഡീലുകളും ഓഫറുകളും **TRENDA സ്റ്റോറിൽ** ലഭ്യമാണ്! 🛒 വേഗമാകട്ടെ!")
        
    elif message.text.startswith("/rules"):
        rules_text = "നമ്മുടെ ഗ്രൂപ്പിലെ നിയമങ്ങൾ:\n1. സ്പാം മെസ്സേജുകൾ അയക്കരുത്.\n2. പരസ്പരം ബഹുമാനിക്കുക."
        await message.reply_text(rules_text)

# 6. അഡ്മിൻ പിൻ കമാൻഡ് (Pin)
@app.on_message(filters.command("pin") & filters.reply)
async def pin_message(client, message):
    try:
        await message.reply_to_message.pin()
        await message.reply_text("📌 മെസ്സേജ് വിജയകരമായി പിൻ ചെയ്തു!")
    except Exception as e:
        await message.reply_text("❌ എനിക്ക് ഈ മെസ്സേജ് പിൻ ചെയ്യാനുള്ള പെർമിഷൻ ഇല്ല.")

print("ബോട്ട് സ്റ്റാർട്ട് ആകുന്നു...")
keep_alive()
app.run()
