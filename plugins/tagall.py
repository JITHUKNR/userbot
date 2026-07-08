from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

# ടാഗിംഗ് നിർത്തി വെക്കാൻ വേണ്ടിയുള്ള ലിസ്റ്റ്
running_processes = []

@Client.on_message(filters.command(["tagall", "all"]) & filters.group)
async def tag_all(client: Client, message: Message):
    chat_id = message.chat.id
    
    # വേറെ ടാഗിംഗ് നടക്കുന്നുണ്ടെങ്കിൽ തടയാൻ
    if chat_id in running_processes:
        return await message.reply_text("⏳ ഇതിനകം ഒരു ടാഗിംഗ് നടന്നുകൊണ്ടിരിക്കുകയാണ്. നിർത്താൻ `/stop` അടിക്കുക.")

    # മെസ്സേജ് എടുക്കുന്നു
    text = ""
    if len(message.command) > 1:
        text = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption or ""
    
    if not text:
        text = "ഹലോ സുഹൃത്തുക്കളെ, ഇവിടെ ശ്രദ്ധിക്കുക! 📢"

    running_processes.append(chat_id)
    msg = await message.reply_text("✅ മെമ്പേഴ്സിനെ മെൻഷൻ ചെയ്യാൻ തുടങ്ങുന്നു... (നിർത്താൻ `/stop` അടിക്കുക)")
    
    try:
        members = []
        # ഗ്രൂപ്പിലെ മെമ്പേഴ്സിനെ എടുക്കുന്നു (ബോട്ടുകളെ ഒഴിവാക്കുന്നു)
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user)
        
        if not members:
            running_processes.remove(chat_id)
            return await msg.edit_text("ആളുകളെ കണ്ടെത്താൻ കഴിഞ്ഞില്ല.")

        # ഒരേസമയം 5 പേരെ വെച്ച് ടാഗ് ചെയ്യുന്നു (സ്പാം ആവാതിരിക്കാൻ)
        batch_size = 5
        for i in range(0, len(members), batch_size):
            if chat_id not in running_processes:
                break # Stop കമാൻഡ് വന്നാൽ നിർത്താൻ
            
            batch = members[i:i + batch_size]
            mention_text = f"{text}\n\n"
            for user in batch:
                mention_text += f"[{user.first_name}](tg://user?id={user.id}) "
            
            await client.send_message(chat_id, mention_text)
            await asyncio.sleep(2.5) # ടെലിഗ്രാം ബാൻ ചെയ്യാതിരിക്കാൻ ചെറിയ ഡിലേ
            
    except Exception as e:
        await message.reply_text(f"❌ എറർ: {e}")
    finally:
        if chat_id in running_processes:
            running_processes.remove(chat_id)
            await message.reply_text("✅ എല്ലാവരെയും മെൻഷൻ ചെയ്യുന്നത് പൂർത്തിയായി!")

@Client.on_message(filters.command("stop") & filters.group)
async def stop_tagging(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in running_processes:
        running_processes.remove(chat_id)
        await message.reply_text("🛑 മെൻഷൻ ചെയ്യുന്നത് നിർത്തി വെച്ചു!")
    else:
        await message.reply_text("ഇവിടെ ഇപ്പോൾ ടാഗിംഗ് നടക്കുന്നില്ല.")
