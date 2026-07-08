from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

task_settings = {
    "share_link": "https://t.me/WETFLAX", 
    "vip_link": "https://t.me/TRENDA_STORE"
}
group_user_clicks = {}

# ലിങ്കുകൾ സെറ്റ് ചെയ്യാൻ
@Client.on_message(filters.command("setlinks") & filters.private)
async def set_task_links(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply_text("Usage: `/setlinks [Share Link] [VIP Group Link]`")
        return
    
    task_settings["share_link"] = message.command[1]
    task_settings["vip_link"] = message.command[2]
    await message.reply_text(f"✅ Links updated successfully!\n\n**Share:** {task_settings['share_link']}\n**VIP:** {task_settings['vip_link']}")

# സിമ്പിൾ ബ്രോഡ്കാസ്റ്റ് കമാൻഡ്
@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_post(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Please provide the target!\nUsage: `/broadcast @username` or ID or Link.")
    
    target = message.command[1]
    
    # ലിങ്ക് ആണെങ്കിൽ അതിൽ നിന്ന് യൂസർനെയിം വേർതിരിക്കുന്നു
    if "t.me/" in target:
        target = target.split("t.me/")[-1]
        if not target.startswith("+"): 
            target = "@" + target

    # ഐഡി ആണെങ്കിൽ അക്കത്തിലേക്ക് മാറ്റുന്നു
    try:
        target = int(target)
    except ValueError:
        pass

    if not message.reply_to_message:
        return await message.reply_text("Please reply to a photo/video/text to broadcast it.")

    # ബ്രോഡ്കാസ്റ്റ് ചെയ്യുമ്പോൾ കൂടെ വെക്കേണ്ട ബട്ടൺ
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Click Here to Share & Join VIP", callback_data="group_share_task")]
    ])
    
    try:
        # നേരെ മെസ്സേജ് ചാനലിലേക്ക് അയക്കുന്നു
        await client.copy_message(
            chat_id=target,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.id,
            reply_markup=keyboard
        )
        await message.reply_text(f"✅ Successfully broadcasted to {target}!")
    except Exception as e:
        await message.reply_text(f"❌ Failed to broadcast: {e}\n(Make sure the bot is an admin in the target channel/group)")

# ബട്ടണിൽ ക്ലിക്ക് ചെയ്യുമ്പോൾ ഉള്ള ആക്ഷൻ
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
        await callback_query.answer("🎉 Congratulations! Redirecting you to the VIP group...", url=vip_url)
        
    else:
        await callback_query.answer("You have already completed the task! Redirecting to VIP group...", url=vip_url)
