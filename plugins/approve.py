from pyrogram import Client, filters

# 1. ഇതുവരെ വന്ന എല്ലാ റിക്വസ്റ്റുകളും ഒറ്റയടിക്ക് അപ്രൂവ് ചെയ്യാൻ
@Client.on_message(filters.command("approveall") & filters.admin)
async def approve_all_requests(client, message):
    m = await message.reply_text("⏳ അപ്രൂവ് ചെയ്യാൻ തുടങ്ങുന്നു... ദയവായി കുറച്ചു സമയം കാത്തിരിക്കുക.")
    try:
        await client.approve_all_chat_join_requests(message.chat.id)
        await m.edit("✅ എല്ലാ ജോയിൻ റിക്വസ്റ്റുകളും വിജയകരമായി അപ്രൂവ് ചെയ്തു!")
    except Exception as e:
        await m.edit(f"❌ ഒരു എറർ സംഭവിച്ചു. ബോട്ടിന് അഡ്മിൻ പവർ ഉണ്ടോ എന്ന് ഉറപ്പുവരുത്തുക.\n\nError: {e}")

# 2. ഇനി വരുന്ന റിക്വസ്റ്റുകൾ തനിയെ അപ്രൂവ് ചെയ്യാൻ (Auto-Approve)
@Client.on_chat_join_request()
async def auto_approve(client, message):
    try:
        await client.approve_chat_join_request(message.chat.id, message.from_user.id)
    except:
        pass
