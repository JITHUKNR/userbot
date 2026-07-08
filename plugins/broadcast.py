from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

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


# 1. കസ്റ്റം ബട്ടണുകൾ വച്ചുള്ള ബ്രോഡ്കാസ്റ്റ്
@Client.on_message(filters.command("broadcast") & filters.private)
async def custom_button_broadcast(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Please reply to a photo/video/text to broadcast it.")

    # മെസ്സേജിലെ വരികൾ വേർതിരിക്കുന്നു (മുഴുവൻ പാരാഗ്രാഫും വായിക്കുന്നു)
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
    for line in lines[1:]: # രണ്ടാമത്തെ വരി മുതലുള്ളവ ബട്ടണുകൾ ആക്കുന്നു
        if "|" in line:
            btn_name, btn_link = line.split("|", 1)
            # ഒരു വരിയിൽ ഒരു ബട്ടൺ എന്ന രീതിയിൽ സെറ്റ് ചെയ്യുന്നു
            buttons.append([InlineKeyboardButton(btn_name.strip(), url=btn_link.strip())])

    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    
    try:
        await client.copy_message(chat_id=target, from_chat_id=message.chat.id, message_id=message.reply_to_message.id, reply_markup=reply_markup)
        await message.reply_text(f"✅ Broadcasted successfully with {len(buttons)} custom buttons!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


# 2. വൈറൽ ടാസ്ക് ബ്രോഡ്കാസ്റ്റ് (Share 3 times)
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
