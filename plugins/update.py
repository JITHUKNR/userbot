import os
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus

# അഡ്മിൻ ആണോ എന്ന് ചെക്ക് ചെയ്യാനുള്ള ഫിൽറ്റർ
async def check_admin(_, client, message):
    if not message.from_user: return False
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        return user.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

is_admin = filters.create(check_admin)

@Client.on_message(filters.command("update") & is_admin)
async def update_bot(client, message):
    m = await message.reply_text("🔄 **GitHub-ൽ നിന്നും പുതിയ കോഡ് എടുക്കുന്നു (Git Pull)...**")
    
    try:
        # git pull കമാൻഡ് റൺ ചെയ്യാൻ
        stream = os.popen('git pull')
        output = stream.read()
        
        if "Already up to date" in output:
            await m.edit("✅ **ബോട്ട് നിലവിൽ ലേറ്റസ്റ്റ് അപ്‌ഡേറ്റിലാണ്!** പുതിയ കോഡുകൾ ലഭ്യമല്ല.")
        else:
            await m.edit(f"✅ **പുതിയ കോഡ് വിജയകരമായി എടുത്തു!**\n\n`{output}`\n\n🚀 **ബോട്ട് റീസ്റ്റാർട്ട് ചെയ്യുകയാണ്... കുറച്ചു സെക്കൻഡുകൾക്കുള്ളിൽ ബോട്ട് വീണ്ടും ആക്ടീവ് ആകും!**")
            # PM2 ഉപയോഗിച്ച് ബോട്ട് റീസ്റ്റാർട്ട് ചെയ്യാൻ
            os.system("pm2 restart userbot")
    except Exception as e:
        await m.edit(f"❌ **ഒരു എറർ സംഭവിച്ചു:**\n`{e}`")
