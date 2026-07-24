from pyrogram import Client, filters

# ഓട്ടോ-അപ്രൂവ് സ്റ്റാറ്റസ് സേവ് ചെയ്യാൻ
auto_approve_state = {}

# 1. ഇതുവരെ വന്ന എല്ലാ റിക്വസ്റ്റുകളും ഒറ്റയടിക്ക് അപ്രൂവ് ചെയ്യാൻ
@Client.on_message(filters.command("approveall") & filters.admin)
async def approve_all_requests(client, message):
    m = await message.reply_text("⏳ അപ്രൂവ് ചെയ്യാൻ തുടങ്ങുന്നു... ദയവായി കാത്തിരിക്കുക.")
    try:
        await client.approve_all_chat_join_requests(message.chat.id)
        await m.edit("✅ എല്ലാ ജോയിൻ റിക്വസ്റ്റുകളും വിജയകരമായി അപ്രൂവ് ചെയ്തു!")
    except Exception as e:
        await m.edit(f"❌ ഒരു എറർ സംഭവിച്ചു. ബോട്ടിന് അഡ്മിൻ പവർ ഉണ്ടോ എന്ന് പരിശോധിക്കുക.\nError: {e}")

# 2. ഓട്ടോ അപ്രൂവ് ON/OFF ചെയ്യാൻ
@Client.on_message(filters.command("autoapprove") & filters.admin)
async def toggle_auto_approve(client, message):
    chat_id = message.chat.id
    if len(message.command) > 1:
        status = message.command[1].lower()
        if status == "on":
            auto_approve_state[chat_id] = True
            await message.reply_text("✅ **ഓട്ടോ-അപ്രൂവ് ON ആക്കി!**\nഇനി ഈ ഗ്രൂപ്പിൽ/ചാനലിൽ വരുന്ന പുതിയ റിക്വസ്റ്റുകൾ ബോട്ട് തനിയെ അപ്രൂവ് ചെയ്യുന്നതാണ്.")
        elif status == "off":
            auto_approve_state[chat_id] = False
            await message.reply_text("❌ **ഓട്ടോ-അപ്രൂവ് OFF ആക്കി!**\nഇനി പുതിയ റിക്വസ്റ്റുകൾ ബോട്ട് തനിയെ അപ്രൂവ് ചെയ്യില്ല. അവ വെയിറ്റിങ്ങിൽ കിടക്കും.")
        else:
            await message.reply_text("⚠️ കൃത്യമായി കൊടുക്കുക: `/autoapprove on` അല്ലെങ്കിൽ `/autoapprove off`")
    else:
        current = "ON ✅" if auto_approve_state.get(chat_id, False) else "OFF ❌"
        await message.reply_text(f"നിലവിൽ ഓട്ടോ-അപ്രൂവ് സ്റ്റാറ്റസ്: **{current}**\n\nമാറ്റാൻ കമാൻഡിനൊപ്പം on അല്ലെങ്കിൽ off എന്ന് കൊടുക്കുക.")

# 3. പുതിയ റിക്വസ്റ്റുകൾ വരുമ്പോൾ (ON ആണെങ്കിൽ മാത്രം) അപ്രൂവ് ചെയ്യാൻ
@Client.on_chat_join_request()
async def auto_approve(client, message):
    chat_id = message.chat.id
    # സ്വിച്ച് ON ആണെങ്കിൽ മാത്രം അപ്രൂവ് ചെയ്യും
    if auto_approve_state.get(chat_id, False):
        try:
            await client.approve_chat_join_request(chat_id, message.from_user.id)
        except:
            pass
