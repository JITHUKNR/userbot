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

# --- ഡൈനാമിക് ലിങ്കുകൾ സേവ് ചെയ്യാനുള്ള സെറ്റപ്പ് ---
bot_settings = {
    "share_link": "https://t.me/WETFLAX", # ഡിഫോൾട്ട് ലിങ്ക് (ഇത് നിങ്ങൾക്ക് കമാൻഡ് വഴി മാറ്റാം)
    "join_link": "https://t.me/TRENDA_STORE"     # ഡിഫോൾട്ട് ലിങ്ക് (ഇത് നിങ്ങൾക്ക് കമാൻഡ് വഴി മാറ്റാം)
}
# യൂസർമാരുടെ ക്ലിക്ക് കൗണ്ട് സേവ് ചെയ്യാൻ
user_shares = {}
# -----------------------------------

# 1. ഷെയർ ചെയ്യേണ്ട ചാനൽ ലിങ്ക് ടെലിഗ്രാമിൽ നിന്ന് സെറ്റ് ചെയ്യാൻ
@app.on_message(filters.command("setshare") & filters.private)
async def set_share_link(client, message):
    if len(message.command) < 2:
        await message.reply_text("ദയവായി ഷെയർ ചെയ്യേണ്ട ലിങ്ക് കൂടെ നൽകുക.\nഉദാഹരണത്തിന്: `/setshare https://t.me/your_channel`")
        return
    
    bot_settings["share_link"] = message.command[1]
    await message.reply_text(f"✅ ഷെയർ ചെയ്യേണ്ട ലിങ്ക് വിജയകരമായി മാറ്റി:\n{bot_settings['share_link']}")

# 2. ജോയിൻ ചെയ്യേണ്ട ഗ്രൂപ്പ് ലിങ്ക് സെറ്റ് ചെയ്യാൻ
@app.on_message(filters.command("setjoin") & filters.private)
async def set_join_link(client, message):
    if len(message.command) < 2:
        await message.reply_text("ദയവായി ജോയിൻ ചെയ്യേണ്ട ലിങ്ക് കൂടെ നൽകുക.\nഉദാഹരണത്തിന്: `/setjoin https://t.me/your_group`")
        return
    
    bot_settings["join_link"] = message.command[1]
    await message.reply_text(f"✅ ജോയിൻ ചെയ്യേണ്ട ലിങ്ക് വിജയകരമായി മാറ്റി:\n{bot_settings['join_link']}")

# 3. സ്റ്റാർട്ട് കമാൻഡ്
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

# 4. ഷെയർ ടാസ്ക് തുടങ്ങാനുള്ള കമാൻഡ് (/task)
@app.on_message(filters.command("task") & filters.private)
async def share_task(client, message):
    user_id = message.from_user.id
    user_shares[user_id] = 0 
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Share 0/3 ↪️", callback_data="do_share")]
    ])
    
    await message.reply_text(
        "നിങ്ങൾ ഈ ഗ്രൂപ്പിൽ ജോയിൻ ചെയ്യാൻ താഴെയുള്ള ബട്ടണിൽ ക്ലിക്ക് ചെയ്ത് **3 ഗ്രൂപ്പുകളിലേക്ക്** ഞങ്ങളുടെ ലിങ്ക് ഷെയർ ചെയ്യണം.",
        reply_markup=keyboard
    )

# 5. ഷെയർ ബട്ടണിൽ ക്ലിക്ക് ചെയ്യുമ്പോൾ സംഭവിക്കേണ്ട കാര്യങ്ങൾ
@app.on_callback_query(filters.regex("do_share"))
async def share_button_click(client, callback_query):
    user_id = callback_query.from_user.id
    current_count = user_shares.get(user_id, 0)
    
    if current_count < 3:
        current_count += 1
        user_shares[user_id] = current_count
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"Share {current_count}/3 ↪️", callback_data="do_share")]
        ])
        
        await callback_query.edit_message_reply_markup(reply_markup=keyboard)
        
        current_share_link = bot_settings["share_link"]
        share_url = f"https://t.me/share/url?url={current_share_link}"
        await callback_query.answer("ലിങ്ക് ഷെയർ ചെയ്യുക!", url=share_url)
        
        if current_count == 3:
            current_join_link = bot_settings["join_link"]
            success_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("ഗ്രൂപ്പിൽ ജോയിൻ ചെയ്യുക ✅", url=current_join_link)]
            ])
            await callback_query.edit_message_text(
                "✅ അഭിനന്ദനങ്ങൾ! നിങ്ങൾ 3 ഗ്രൂപ്പുകളിൽ ഷെയർ ചെയ്തു കഴിഞ്ഞു. താഴെയുള്ള ബട്ടൺ വഴി നിങ്ങൾക്ക് ഗ്രൂപ്പിൽ ജോയിൻ ചെയ്യാം.",
                reply_markup=success_keyboard
            )

# 6. പുതിയതായി വരുന്ന റിക്വസ്റ്റുകൾ തനിയെ അക്സെപ്റ്റ് ചെയ്യാൻ (Auto-Approve)
@app.on_chat_join_request()
async def auto_approve(client, message):
    try:
        await client.approve_chat_join_request(message.chat.id, message.from_user.id)
        welcome_text = f"നമസ്കാരം {message.from_user.first_name}, {message.chat.title} ലേക്ക് സ്വാഗതം! 🥳"
        await client.send_message(message.from_user.id, welcome_text)
    except Exception as e:
        print(f"Error auto-approving: {e}")

# 7. ഓട്ടോ-റിപ്ലൈ ഫിൽറ്ററുകൾ (ഗ്രൂപ്പുകളിൽ മാത്രം വർക്ക് ചെയ്യാൻ)
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

# 8. അഡ്മിൻ പിൻ കമാൻഡ് (Pin)
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
