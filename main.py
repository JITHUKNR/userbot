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

# --- Dynamic Settings ---
bot_settings = {
    "share_link": "https://t.me/WETFLAX", 
    "join_link": "https://t.me/TRENDA_STORE",
    "media_id": None,   
    "media_type": None
}

user_shares = {}
# ------------------------

# 1. Set Share Link (Admin)
@app.on_message(filters.command("setshare") & filters.private)
async def set_share_link(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide the share link.\nExample: `/setshare https://t.me/your_channel`")
        return
    bot_settings["share_link"] = message.command[1]
    await message.reply_text(f"✅ Share link updated successfully:\n{bot_settings['share_link']}")

# 2. Set Join Link (Admin)
@app.on_message(filters.command("setjoin") & filters.private)
async def set_join_link(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide the join link.\nExample: `/setjoin https://t.me/your_group`")
        return
    bot_settings["join_link"] = message.command[1]
    await message.reply_text(f"✅ Join link updated successfully:\n{bot_settings['join_link']}")

# 3. Set Photo or Video for Task (Admin)
@app.on_message(filters.command("setmedia") & filters.private)
async def set_media(client, message):
    if not message.reply_to_message or not (message.reply_to_message.photo or message.reply_to_message.video):
        await message.reply_text("Please reply to a Photo or Video with the `/setmedia` command.")
        return
    if message.reply_to_message.photo:
        bot_settings["media_id"] = message.reply_to_message.photo.file_id
        bot_settings["media_type"] = "photo"
    elif message.reply_to_message.video:
        bot_settings["media_id"] = message.reply_to_message.video.file_id
        bot_settings["media_type"] = "video"
    await message.reply_text("✅ Poster/Video updated successfully! It will now be shown in the /task command.")

# 4. Start Command
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("WETFLAX News 🗞️", url="https://t.me/your_wetflax_channel")],
        [InlineKeyboardButton("TRENDA Store 🛒", url="https://t.me/your_trenda_channel")]
    ])
    await message.reply_text("Welcome! I am your official bot. Check out the links below.", reply_markup=buttons)

# 5. Interactive Menu Command (NEW)
@app.on_message(filters.command("menu") & filters.private)
async def menu_command(client, message):
    menu_text = (
        "🤖 **Bot Control Menu**\n\n"
        "Welcome to the main dashboard. Choose a category below to see available commands and features:"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛠 Admin Tools", callback_data="menu_admin"),
         InlineKeyboardButton("👤 User Commands", callback_data="menu_user")],
        [InlineKeyboardButton("⚙️ Bot Features", callback_data="menu_features")],
        [InlineKeyboardButton("Close ❌", callback_data="close_menu")]
    ])
    await message.reply_text(menu_text, reply_markup=buttons)

# 6. Share Task Command (/task)
@app.on_message(filters.command("task") & filters.private)
async def share_task(client, message):
    user_id = message.from_user.id
    user_shares[user_id] = 0 
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Share 0/3 ↪️", callback_data="do_share")]])
    caption_text = "To join this group, you must share our link to **3 groups** by clicking the button below."
    media_id = bot_settings.get("media_id")
    media_type = bot_settings.get("media_type")

    if media_id:
        try:
            if media_type == "photo":
                await message.reply_photo(photo=media_id, caption=caption_text, reply_markup=keyboard)
            elif media_type == "video":
                await message.reply_video(video=media_id, caption=caption_text, reply_markup=keyboard)
            return
        except Exception as e:
            print(f"Error sending media: {e}")
            
    await message.reply_text(caption_text, reply_markup=keyboard)

# 7. Auto-Approve Join Requests
@app.on_chat_join_request()
async def auto_approve(client, message):
    try:
        await client.approve_chat_join_request(message.chat.id, message.from_user.id)
        welcome_text = f"Hello {message.from_user.first_name}, Welcome to {message.chat.title}! 🥳"
        await client.send_message(message.from_user.id, welcome_text)
    except Exception as e:
        print(f"Error auto-approving: {e}")

# 8. Auto-reply Filters (Group Only)
@app.on_message(filters.text & filters.group)
async def auto_filters(client, message):
    text = message.text.lower()
    if "news" in text:
        await message.reply_text("For the latest breaking news and updates, visit the **WETFLAX** channel! 🗞️")
    elif "link" in text or "offer" in text:
        await message.reply_text("Today's best deals and offers are available at **TRENDA STORE**! 🛒 Hurry up!")
    elif message.text.startswith("/rules"):
        rules_text = "Our Group Rules:\n1. No spam messages.\n2. Respect each other."
        await message.reply_text(rules_text)

# 9. Admin Pin Command
@app.on_message(filters.command("pin") & filters.reply)
async def pin_message(client, message):
    try:
        await message.reply_to_message.pin()
        await message.reply_text("📌 Message pinned successfully!")
    except Exception as e:
        await message.reply_text("❌ I don't have permission to pin messages.")

# 10. Callback Queries for Menu and Share Buttons
@app.on_callback_query()
async def handle_callbacks(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    # Menu Logic
    if data == "menu_admin":
        text = (
            "🛠 **Admin Tools**\n\n"
            "`/setshare [link]` - Set the viral share link.\n"
            "`/setjoin [link]` - Set the private group join link.\n"
            "`/setmedia` - Reply to a photo/video to set it for the task.\n"
            "`/pin` - Reply to a message to pin it in a group."
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=buttons)
        
    elif data == "menu_user":
        text = (
            "👤 **User Commands**\n\n"
            "`/start` - Check bot status.\n"
            "`/task` - Start the 3-share group join task.\n"
            "`/menu` - Open this main menu."
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=buttons)
        
    elif data == "menu_features":
        text = (
            "⚙️ **Bot Features**\n\n"
            "✅ **Auto-Approve:** Automatically accepts pending join requests in channels/groups.\n"
            "✅ **Auto-Filters:** Triggers automatic replies for keywords like 'news', 'link', 'offer' in groups."
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=buttons)
        
    elif data == "menu_main":
        menu_text = (
            "🤖 **Bot Control Menu**\n\n"
            "Welcome to the main dashboard. Choose a category below to see available commands and features:"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛠 Admin Tools", callback_data="menu_admin"),
             InlineKeyboardButton("👤 User Commands", callback_data="menu_user")],
            [InlineKeyboardButton("⚙️ Bot Features", callback_data="menu_features")],
            [InlineKeyboardButton("Close ❌", callback_data="close_menu")]
        ])
        await callback_query.edit_message_text(menu_text, reply_markup=buttons)
        
    elif data == "close_menu":
        await callback_query.message.delete()
        
    # Share Task Logic
    elif data == "do_share":
        current_count = user_shares.get(user_id, 0)
        
        if current_count < 3:
            current_count += 1
            user_shares[user_id] = current_count
            
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f"Share {current_count}/3 ↪️", callback_data="do_share")]])
            await callback_query.edit_message_reply_markup(reply_markup=keyboard)
            
            current_share_link = bot_settings["share_link"]
            share_url = f"https://t.me/share/url?url={current_share_link}"
            await callback_query.answer("Please share the link!", url=share_url)
            
            if current_count == 3:
                current_join_link = bot_settings["join_link"]
                success_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Join Group ✅", url=current_join_link)]])
                success_msg = "✅ Congratulations! You have successfully shared to 3 groups. Click the button below to join."
                
                if callback_query.message.photo or callback_query.message.video:
                    await callback_query.edit_message_caption(caption=success_msg, reply_markup=success_keyboard)
                else:
                    await callback_query.edit_message_text(text=success_msg, reply_markup=success_keyboard)

print("Bot is starting...")
keep_alive()
app.run()
