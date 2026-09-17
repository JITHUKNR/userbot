from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from database import db

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛡 Group Management", callback_data="menu_group"),
         InlineKeyboardButton("📢 Channel Control", callback_data="menu_channel")],
        [InlineKeyboardButton("📡 Broadcast System", callback_data="menu_broadcast"),
         InlineKeyboardButton("🚀 Viral Share Task", callback_data="menu_viral")],
        [InlineKeyboardButton("Close Dashboard ❌", callback_data="close_menu")]
    ])

def get_group_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔨 Ban", callback_data="help_ban"), 
         InlineKeyboardButton("🔇 Mute", callback_data="help_mute")],
        [InlineKeyboardButton("🗑 Purge", callback_data="help_purge"), 
         InlineKeyboardButton("📌 Pin", callback_data="help_pin")],
        [InlineKeyboardButton("🔒 Lock", callback_data="help_lock"), 
         InlineKeyboardButton("🔓 Unlock", callback_data="help_unlock")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")]
    ])

async def get_channel_list_menu():
    channels = await db.channels.find().to_list(length=100)
    buttons = [[InlineKeyboardButton("➕ Add channel", callback_data="add_channel")]]
    for ch in channels:
        title = ch.get("title", "Channel")
        chat_id = ch.get("chat_id")
        buttons.append([InlineKeyboardButton(f"📢 {title}", callback_data=f"manage_{chat_id}")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)

async def get_channel_panel(chat_id: int):
    ch = await db.channels.find_one({"chat_id": chat_id})
    if not ch:
        return None, None
    
    title = ch.get("title", "Channel")
    app_accept = "Enabled" if ch.get("app_accept", True) else "Disabled"
    auto_approve = "Enabled" if ch.get("auto_approve", False) else "Disabled"
    captcha = "Enabled" if ch.get("captcha", False) else "Disabled"
    lang_filter = "Enabled" if ch.get("lang_filter", False) else "Disabled"
    accept_interact = "Enabled" if ch.get("accept_interact", False) else "Disabled"

    text = (
        f"📢 **{title}**\n"
        f"Application accept: {app_accept}\n"
        f"Auto-approve: {auto_approve}\n"
        f"Use CAPTCHA: {captcha}\n"
        f"Language filter: {lang_filter}\n"
        f"Accept on interact: {accept_interact}"
    )

    buttons = [
        [InlineKeyboardButton("🫂 Applications accept", callback_data=f"toggle_app_{chat_id}")],
        [InlineKeyboardButton("✏️ Set greetings", callback_data=f"set_greet_{chat_id}")],
        [InlineKeyboardButton("✏️ Set farewells", callback_data=f"set_farewell_{chat_id}")],
        [InlineKeyboardButton("🫂 Approve requests", callback_data=f"view_requests_{chat_id}")],
        [InlineKeyboardButton("⚙️ Copy settings to other channels", callback_data=f"copy_settings_{chat_id}")],
        [InlineKeyboardButton("🗑 Remove channel", callback_data=f"remove_ch_{chat_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_channel")]
    ]
    return text, InlineKeyboardMarkup(buttons)

def get_broadcast_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📡 How to use Custom Buttons", callback_data="help_broadcast")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")]
    ])

def get_viral_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Set Viral Links", callback_data="help_setlinks")],
        [InlineKeyboardButton("🖼 How to send Viral Post", callback_data="help_viral")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")]
    ])

@Client.on_message(filters.command(["start", "menu"]) & filters.private)
async def start_menu(client: Client, message: Message):
    text = (
        "👑 **ULTIMATE ADMIN CONTROL PANEL**\n\n"
        "Welcome to your Master Bot.\nSelect a category below:"
    )
    await message.reply_text(text, reply_markup=get_main_menu())

@Client.on_message(filters.forwarded & filters.private)
async def handle_forwarded_channel(client: Client, message: Message):
    if message.forward_from_chat and message.forward_from_chat.type.name in ["CHANNEL", "SUPERGROUP"]:
        chat_id = message.forward_from_chat.id
        title = message.forward_from_chat.title
        
        await db.channels.update_one(
            {"chat_id": chat_id},
            {"$set": {
                "chat_id": chat_id,
                "title": title,
                "app_accept": True,
                "auto_approve": False,
                "captcha": False,
                "lang_filter": False,
                "accept_interact": False
            }},
            upsert=True
        )
        
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Channel Control", callback_data="menu_channel")]])
        await message.reply_text(
            f"✅ **Channel successfully connected!**\n\n**Title:** {title}\n**ID:** `{chat_id}`",
            reply_markup=markup
        )

@Client.on_callback_query()
async def handle_all_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    
    if data == "menu_main":
        await callback_query.edit_message_text(
            "👑 **ULTIMATE ADMIN CONTROL PANEL**\n\nSelect a category below:",
            reply_markup=get_main_menu()
        )
    elif data == "menu_group":
        await callback_query.edit_message_text("🛡 **Group Management**\n\nClick a tool below:", reply_markup=get_group_menu())
    
    elif data == "menu_channel":
        markup = await get_channel_list_menu()
        await callback_query.edit_message_text(
            "**Welcome!**\n\n**Your channels:**",
            reply_markup=markup
        )

    elif data == "add_channel":
        text = (
            "**To connect a new channel:**\n\n"
            "1. Add this bot as an **Administrator** in your channel (with invite users permission).\n"
            "2. **Forward any message** from that channel directly to this chat.\n\n"
            "The channel will be automatically detected and registered."
        )
        await callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_channel")]])
        )

    elif data.startswith("manage_"):
        chat_id = int(data.split("_")[1])
        text, markup = await get_channel_panel(chat_id)
        if text and markup:
            await callback_query.edit_message_text(text, reply_markup=markup)
        else:
            await callback_query.answer("Channel not found in database.", show_alert=True)

    elif data.startswith("toggle_app_"):
        chat_id = int(data.split("_")[2])
        ch = await db.channels.find_one({"chat_id": chat_id})
        if ch:
            new_state = not ch.get("app_accept", True)
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"app_accept": new_state}})
            text, markup = await get_channel_panel(chat_id)
            await callback_query.edit_message_text(text, reply_markup=markup)

    elif data.startswith("view_requests_"):
        chat_id = int(data.split("_")[2])
        text = (
            "Please submit the number of applications you wish to accept, or "
            "use the button below to accept all applications."
        )
        buttons = [
            [InlineKeyboardButton("Accept all", callback_data=f"bulk_approve_{chat_id}")],
            [InlineKeyboardButton("🔙 Back", callback_data=f"manage_{chat_id}")]
        ]
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("bulk_approve_"):
        chat_id = int(data.split("_")[2])
        await callback_query.answer("Processing requests...", show_alert=False)
        try:
            await client.approve_all_chat_join_requests(chat_id)
            await callback_query.answer("✅ All join requests accepted successfully!", show_alert=True)
            text, markup = await get_channel_panel(chat_id)
            await callback_query.edit_message_text(text, reply_markup=markup)
        except Exception as e:
            await callback_query.answer(f"❌ Error: {e}", show_alert=True)

    elif data.startswith("set_greet_"):
        await callback_query.answer("Send the welcome message you want to set for this channel.", show_alert=True)

    elif data.startswith("set_farewell_"):
        await callback_query.answer("Send the farewell message you want to set for this channel.", show_alert=True)

    elif data.startswith("copy_settings_"):
        await callback_query.answer("Copy settings feature will be applied to your other channels.", show_alert=True)

    elif data.startswith("remove_ch_"):
        chat_id = int(data.split("_")[2])
        await db.channels.delete_one({"chat_id": chat_id})
        await callback_query.answer("Channel removed from bot.", show_alert=True)
        markup = await get_channel_list_menu()
        await callback_query.edit_message_text("**Welcome!**\n\n**Your channels:**", reply_markup=markup)

    elif data == "menu_broadcast":
        await callback_query.edit_message_text("📡 **Broadcast System**\n\nLearn how to add custom buttons:", reply_markup=get_broadcast_menu())
    elif data == "menu_viral":
        await callback_query.edit_message_text("🚀 **Viral Marketing Task**\n\nThe 'Share 3 Times to Unlock' feature:", reply_markup=get_viral_menu())

    # Help Texts
    elif data == "help_broadcast":
        text = (
            "📡 **Custom Button Broadcast**\n\n"
            "Reply to a post (photo/video/text) with the target and buttons line by line.\n\n"
            "**Format:**\n"
            "`/broadcast @target_channel`\n"
            "`Button 1 Name | https://link1.com`\n"
            "`Button 2 Name | https://link2.com`\n\n"
            "*(You can add as many buttons as you want!)*"
        )
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_broadcast")]]))

    elif data == "help_viral":
        text = (
            "🖼 **Viral Post (Share 3 Times)**\n\n"
            "To send a post with the viral 'Click to Share & Join' button, reply to a post with:\n\n"
            "`/viral @target_channel`\n\n"
            "*(Make sure you have set the links using `/setlinks` first)*"
        )
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_viral")]]))
        
    elif data == "help_setlinks":
        text = "🔗 **Set Task Links**\n\nUsage: `/setlinks [Share-Link] [VIP-Link]`"
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_viral")]]))

    elif data in ["help_ban", "help_mute", "help_purge", "help_pin", "help_lock", "help_unlock"]:
        await callback_query.edit_message_text(f"Command Info for: {data.replace('help_', '/')}\nRun this command in the group.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_group")]]))
        
    elif data in ["help_editpost", "help_timer", "help_info"]:
        await callback_query.edit_message_text("Channel Tools info. Check Dashboard for details.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_channel")]]))

    elif data == "close_menu":
        await callback_query.message.delete()
    elif data == "group_share_task":
        pass
