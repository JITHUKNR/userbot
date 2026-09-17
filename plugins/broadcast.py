import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from database import db

task_settings = {
    "share_link": "https://t.me/WETFLAX", 
    "vip_link": "https://t.me/TRENDA_STORE"
}
group_user_clicks = {}

@Client.on_message(filters.command("setlinks") & filters.private)
async def set_task_links(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text("Usage: `/setlinks [Share Link] [VIP Group Link]`")
    task_settings["share_link"] = message.command[1]
    task_settings["vip_link"] = message.command[2]
    await message.reply_text(f"✅ Links updated!\n**Share:** {task_settings['share_link']}\n**VIP:** {task_settings['vip_link']}")


# 1. കസ്റ്റം ബട്ടണുകൾ വച്ചുള്ള ബ്രോഡ്കാസ്റ്റ് (ഡിലീറ്റ് ചെയ്യാവുന്ന ഫീച്ചറോട് കൂടി)
@Client.on_message(filters.command("broadcast") & filters.private)
async def custom_button_broadcast(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Please reply to a photo/video/text to broadcast it.")

    # മെസ്സേജിലെ വരികൾ വേർതിരിക്കുന്നു
    lines = message.text.split("\n")
    first_line = lines[0].split(" ")
    
    if len(first_line) < 2:
        return await message.reply_text("Please provide target!\nExample:\n`/broadcast @WETFLAX\nButton | https://link.com`")
        
    target = first_line[1]
    
    # ലിങ്കോ ഐഡിയോ ക്ലീൻ ചെയ്യുന്നു
    if "t.me/" in target:
        target = target.split("t.me/")[-1]
        if not target.startswith("+"): target = "@" + target
    try: target = int(target)
    except ValueError: pass

    # ബട്ടണുകൾ ഉണ്ടാക്കുന്നു
    buttons = []
    for line in lines[1:]: 
        if "|" in line:
            btn_name, btn_link = line.split("|", 1)
            buttons.append([InlineKeyboardButton(btn_name.strip(), url=btn_link.strip())])

    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    
    # ഒരു ചാനലിലേക്കാണ് അയക്കുന്നതെങ്കിൽ (Target ഒരു ചാനൽ/ഗ്രൂപ്പ് ആണെങ്കിൽ)
    if isinstance(target, (int, str)):
        try:
            sent_msg = await client.copy_message(chat_id=target, from_chat_id=message.chat.id, message_id=message.reply_to_message.id, reply_markup=reply_markup)
            await message.reply_text(f"✅ Broadcasted successfully with {len(buttons)} custom buttons!")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    else:
        pass

    # ബോട്ട് വഴി രജിസ്റ്റർ ചെയ്ത എല്ലാ യൂസർമാർക്കും ബ്രോഡ്കാസ്റ്റ് അയക്കണമെങ്കിൽ താഴെ കൊടുത്തിരിക്കുന്ന ലോജിക് ഉപയോഗിക്കാം:
    # (ഉദാഹരണത്തിന് എല്ലാ യൂസർമാർക്കും അയക്കുമ്പോൾ ഡിലീറ്റ് ചെയ്യാൻ സേവ് ചെയ്യേണ്ടത് ഇങ്ങനെയാണ്):
    status_msg = await message.reply_text("📡 Broadcasting to all users in database...")
    sent_messages = []
    success = 0
    
    async for user in db.channels.database["users"].find():
        try:
            sent_msg = await client.copy_message(
                chat_id=user["user_id"], 
                from_chat_id=message.chat.id, 
                message_id=message.reply_to_message.id, 
                reply_markup=reply_markup
            )
            sent_messages.append({"chat_id": user["user_id"], "message_id": sent_msg.id})
            success += 1
            await asyncio.sleep(0.03)
        except Exception:
            pass

    # ഡിലീറ്റ് ചെയ്യാൻ വേണ്ടി മെസ്സേജ് ഐഡികൾ ഡാറ്റാബേസിൽ സേവ് ചെയ്യുന്നു
    if sent_messages:
        await db.channels.database["broadcast_logs"].update_one(
    {"_id": "latest_broadcast"},
    {"$set": {"messages": sent_messages}},
    upsert=True
)

    await status_msg.edit_text(f"✅ **Broadcast Completed!**\nSent to `{success}` users.\n\n*(You can delete this broadcast anytime using `/delete_broadcast`)*")


# 2. ബ്രോഡ്കാസ്റ്റ് ചെയ്ത എല്ലാ മെസ്സേജുകളും ഡിലീറ്റ് ചെയ്യാനുള്ള കമാൻഡ്
@Client.on_message(filters.command("delete_broadcast") & filters.private)
async def delete_all_broadcast(client: Client, message: Message):
    log = await db.channels.database["broadcast_logs"].find_one({"_id": "latest_broadcast"})
    if not log or not log.get("messages"):
        return await message.reply_text("❌ No recent broadcast found to delete!")
    
    status_msg = await message.reply_text("⏳ Deleting broadcast from all users...")
    
    deleted_count = 0
    for item in log["messages"]:
        try:
            await client.delete_messages(chat_id=item["chat_id"], message_ids=item["message_id"])
            deleted_count += 1
            await asyncio.sleep(0.04) # Telegram FloodWait ഒഴിവാക്കാൻ
        except Exception:
            pass
            
    # ഡിലീറ്റ് ചെയ്തു കഴിഞ്ഞാൽ ഡാറ്റാബേസ് ക്ലിയർ ചെയ്യാം
    await db.channels.database["broadcast_logs"].delete_one({"_id": "latest_broadcast"})
    
    await status_msg.edit_text(f"✅ **Broadcast successfully deleted!**\nRemoved from `{deleted_count}` chats.")


# 3. വൈറൽ ടാസ്ക് ബ്രോഡ്കാസ്റ്റ് (Share 3 times)
@Client.on_message(filters.command("viral") & filters.private)
async def viral_broadcast(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/viral @target_channel` (Reply to a post)")
    
    target = message.command[1]
    if "t.me/" in target:
        target = target.split("t.me/")[-1]
        if not target.startswith("+"): target = "@" + target
    try: target = int(target)
    except ValueError: pass

    if not message.reply_to_message:
        return await message.reply_text("Please reply to a message to send the viral post.")

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎁 Click Here to Share & Join VIP", callback_data="group_share_task")]])
    
    try:
        await client.copy_message(chat_id=target, from_chat_id=message.chat.id, message_id=message.reply_to_message.id, reply_markup=keyboard)
        await message.reply_text(f"✅ Viral Post successfully sent to {target}!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


# വൈറൽ ബട്ടൺ ക്ലിക്ക് ലോജിക്
@Client.on_callback_query(filters.regex("group_share_task"))
async def handle_group_task(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    current_count = group_user_clicks.get(user_id, 0)
    
    share_url = f"https://t.me/share/url?url={task_settings['share_link']}"
    vip_url = task_settings['vip_link']
    
    if current_count == 0:
        group_user_clicks[user_id] = 1
        await callback_query.answer("✅ 1/3 Completed! Click the button again to share.", url=share_url)
    elif current_count == 1:
        group_user_clicks[user_id] = 2
        await callback_query.answer("✅ 2/3 Completed! Share one last time.", url=share_url)
    elif current_count == 2:
        group_user_clicks[user_id] = 3
        await callback_query.answer("🎉 Congratulations! Redirecting to VIP...", url=vip_url)
    else:
        await callback_query.answer("You have already completed the task! Redirecting to VIP...", url=vip_url)
    else:
