from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

# Links and target settings
task_settings = {
    "share_link": "https://t.me/WETFLAX", 
    "vip_link": "https://t.me/TRENDA_STORE",
    "target_chat": None # The group/channel to post to
}
group_user_clicks = {}

# 1. Set Links (Admin Only - PM)
@Client.on_message(filters.command("setlinks") & filters.private)
async def set_task_links(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply_text("Usage: `/setlinks [Share Link] [VIP Group Link]`")
        return
    
    task_settings["share_link"] = message.command[1]
    task_settings["vip_link"] = message.command[2]
    await message.reply_text(f"✅ Links updated successfully!\n\n**Share:** {task_settings['share_link']}\n**VIP:** {task_settings['vip_link']}")

# 2. Set Target Group (Admin Only - PM)
@Client.on_message(filters.command("settarget") & filters.private)
async def set_target_chat(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide the target group/channel.\nExample: `/settarget @your_group`")
        return
    task_settings["target_chat"] = message.command[1]
    await message.reply_text(f"✅ Target group set to: {task_settings['target_chat']}")

# 3. Create and Send Post from Bot's PM (Admin Only)
@Client.on_message(filters.command("makepost") & filters.private)
async def make_remote_post(client: Client, message: Message):
    target = task_settings.get("target_chat")
    if not target:
        return await message.reply_text("Please set the target group first! Command: `/settarget @your_group`")

    if not message.reply_to_message or not (message.reply_to_message.photo or message.reply_to_message.video):
        return await message.reply_text("Please send me the photo or video first, then reply to it with `/makepost`.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Click Here to Share & Join VIP", callback_data="group_share_task")]
    ])
    
    caption_text = "To join the VIP group, click the button below and share this post to 3 groups! 👇"

    try:
        if message.reply_to_message.photo:
            await client.send_photo(target, photo=message.reply_to_message.photo.file_id, caption=caption_text, reply_markup=keyboard)
        elif message.reply_to_message.video:
            await client.send_video(target, video=message.reply_to_message.video.file_id, caption=caption_text, reply_markup=keyboard)
        
        await message.reply_text(f"✅ Successfully sent the poster to {target}!")
    except Exception as e:
        await message.reply_text(f"❌ Failed to send post: {e}\n(Make sure the bot is an admin in the target group)")

# 4. Handle Button Clicks directly in the Group
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
