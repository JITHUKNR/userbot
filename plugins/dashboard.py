import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from database import db

USER_STATE = {}

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

async def get_channel_panel(client: Client, chat_id: int):
    ch = await db.channels.find_one({"chat_id": chat_id})
    if not ch:
        return None, None
    
    title = ch.get("title", "Channel")
    
    # പെൻഡിങ് റിക്വസ്റ്റുകളുടെ എണ്ണം തത്സമയം കണക്കാക്കുന്നു
    pending_count = 0
    try:
        async for _ in client.get_chat_join_requests(chat_id):
            pending_count += 1
    except Exception:
        pending_count = 0

    app_accept = "Enabled" if ch.get("app_accept", True) else "Disabled"
    auto_approve = "Enabled" if ch.get("auto_approve", False) else "Disabled"
    captcha = "Enabled" if ch.get("captcha", False) else "Disabled"
    lang_filter = "Enabled" if ch.get("lang_filter", False) else "Disabled"
    accept_interact = "Enabled" if ch.get("captcha", False) else "Disabled"

    text = (
        f"📢 **{title}**\n"
        f"Application accept: {app_accept}\n"
        f"Auto-approve: {auto_approve}\n"
        f"Use CAPTCHA: {captcha}\n"
        f"Language filter: {lang_filter}\n"
        f"Accept on interact: {accept_interact}\n\n"
        f"⏳ **Pending Requests:** `{pending_count}`"
    )

    buttons = [
        [InlineKeyboardButton("🫂 Applications accept", callback_data=f"sub_app_{chat_id}")],
        [InlineKeyboardButton("✏️ Set greetings", callback_data=f"sub_greet_{chat_id}")],
        [InlineKeyboardButton("✏️ Set farewells", callback_data=f"sub_farewell_{chat_id}")],
        [InlineKeyboardButton(f"🫂 Approve requests ({pending_count})", callback_data=f"view_requests_{chat_id}")],
        [InlineKeyboardButton("⚙️ Copy settings to other channels", callback_data=f"copy_settings_{chat_id}")],
        [InlineKeyboardButton("🗑 Remove channel", callback_data=f"remove_ch_{chat_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_channel")]
    ]
    return text, InlineKeyboardMarkup(buttons)

async def get_app_settings_panel(chat_id: int):
    ch = await db.channels.find_one({"chat_id": chat_id})
    auto_status = "🟢 Enabled" if ch.get("auto_approve", False) else "🔴 Disabled"
    captcha_status = "🟢 Enabled" if ch.get("captcha", False) else "🔴 Disabled"
    captcha_text = ch.get("captcha_text", "Are you interested in this channel? Please verify below.")
    captcha_btn = ch.get("captcha_button", "✅ Yes, I want to join")

    text = (
        f"⚙️ **Application & Verification Settings**\n\n"
        f"• **Direct Auto-Approve:** {auto_status}\n"
        f"• **CAPTCHA Verification:** {captcha_status}\n\n"
        f"📝 **Current CAPTCHA Message:**\n`{captcha_text}`\n\n"
        f"🔘 **Button Label:** `{captcha_btn}`\n\n"
        f"*(When CAPTCHA is enabled, users will receive this button in private chat to verify)*"
    )
    buttons = [
        [InlineKeyboardButton(f"Auto-Approve: {auto_status}", callback_data=f"toggle_auto_{chat_id}")],
        [InlineKeyboardButton(f"CAPTCHA: {captcha_status}", callback_data=f"toggle_captcha_{chat_id}")],
        [InlineKeyboardButton("✍️ Edit CAPTCHA Text", callback_data=f"edit_captchatxt_{chat_id}")],
        [InlineKeyboardButton("🔘 Edit Button Name", callback_data=f"edit_captchabtn_{chat_id}")],
        [InlineKeyboardButton("🔙 Back to Channel", callback_data=f"manage_{chat_id}")]
    ]
    return text, InlineKeyboardMarkup(buttons)

async def get_greet_panel(chat_id: int):
    ch = await db.channels.find_one({"chat_id": chat_id})
    status = "🟢 Enabled" if ch.get("greetings_enabled", False) else "🔴 Disabled"
    current_text = ch.get("greetings_text", "Welcome to our channel! 🎉")
    text = (
        f"✏️ **Greeting Message Settings**\n\n"
        f"• **Status:** {status}\n\n"
        f"📝 **Current Greeting Text:**\n`{current_text}`"
    )
    buttons = [
        [InlineKeyboardButton(f"Status: {status}", callback_data=f"toggle_greet_{chat_id}")],
        [InlineKeyboardButton("✍️ Change Greeting Text", callback_data=f"edit_greet_{chat_id}")],
        [InlineKeyboardButton("🔙 Back to Channel", callback_data=f"manage_{chat_id}")]
    ]
    return text, InlineKeyboardMarkup(buttons)

async def get_farewell_panel(chat_id: int):
    ch = await db.channels.find_one({"chat_id": chat_id})
    status = "🟢 Enabled" if ch.get("farewells_enabled", False) else "🔴 Disabled"
    current_text = ch.get("farewells_text", "Goodbye! Thanks for being with us.")
    text = (
        f"✏️ **Farewell Message Settings**\n\n"
        f"• **Status:** {status}\n\n"
        f"📝 **Current Farewell Text:**\n`{current_text}`"
    )
    buttons = [
        [InlineKeyboardButton(f"Status: {status}", callback_data=f"toggle_farewell_{chat_id}")],
        [InlineKeyboardButton("✍️ Change Farewell Text", callback_data=f"edit_farewell_{chat_id}")],
        [InlineKeyboardButton("🔙 Back to Channel", callback_data=f"manage_{chat_id}")]
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
                "greetings_enabled": False,
                "farewells_enabled": False
            }},
            upsert=True
        )
        
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Channel Control", callback_data="menu_channel")]])
        await message.reply_text(
            f"✅ **Channel successfully connected!**\n\n**Title:** {title}\n**ID:** `{chat_id}`",
            reply_markup=markup
        )

@Client.on_message(filters.text & filters.private & ~filters.forwarded & ~filters.command(["start", "menu", "update"]))
async def handle_text_inputs(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in USER_STATE:
        state_data = USER_STATE[user_id]
        action = state_data.get("action")
        chat_id = state_data.get("chat_id")
        text_received = message.text

        if action == "edit_captchatxt":
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"captcha_text": text_received}})
            del USER_STATE[user_id]
            txt, markup = await get_app_settings_panel(chat_id)
            await message.reply_text("✅ **CAPTCHA text updated successfully!**", reply_markup=markup)

        elif action == "edit_captchabtn":
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"captcha_button": text_received}})
            del USER_STATE[user_id]
            txt, markup = await get_app_settings_panel(chat_id)
            await message.reply_text("✅ **CAPTCHA button name updated successfully!**", reply_markup=markup)

        elif action == "edit_greet":
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"greetings_text": text_received}})
            del USER_STATE[user_id]
            txt, markup = await get_greet_panel(chat_id)
            await message.reply_text("✅ **Greeting message updated successfully!**", reply_markup=markup)

        elif action == "edit_farewell":
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"farewells_text": text_received}})
            del USER_STATE[user_id]
            txt, markup = await get_farewell_panel(chat_id)
            await message.reply_text("✅ **Farewell message updated successfully!**", reply_markup=markup)

@Client.on_chat_join_request()
async def handle_incoming_join_request(client: Client, request):
    chat_id = request.chat.id
    user_id = request.from_user.id
    
    ch = await db.channels.find_one({"chat_id": chat_id})
    if not ch or not ch.get("app_accept", True):
        return

    if ch.get("captcha", False):
        captcha_text = ch.get("captcha_text", f"Are you interested in joining **{ch.get('title')}**? Please verify below.")
        button_name = ch.get("captcha_button", "✅ Yes, I want to join")
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(button_name, callback_data=f"verify_join_{chat_id}")]])
        try:
            await client.send_message(user_id, captcha_text, reply_markup=markup)
        except Exception:
            pass
    elif ch.get("auto_approve", False):
        try:
            await client.approve_chat_join_request(chat_id, user_id)
            if ch.get("greetings_enabled", False):
                greet_text = ch.get("greetings_text", f"Welcome to **{ch.get('title')}**! 🎉")
                try:
                    await client.send_message(user_id, greet_text)
                except Exception:
                    pass
        except Exception:
            pass

@Client.on_callback_query()
async def handle_all_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if user_id in USER_STATE and data.startswith("cancel_state_"):
        del USER_STATE[user_id]
        chat_id = int(data.split("cancel_state_")[1])
        text, markup = await get_channel_panel(client, chat_id)
        await callback_query.edit_message_text(text, reply_markup=markup)
        return

    if data.startswith("verify_join_"):
        chat_id = int(data.split("verify_join_")[1])
        try:
            await client.approve_chat_join_request(chat_id, user_id)
            await callback_query.edit_message_text("✅ **Verification successful! You have been accepted to the channel.**")
            ch = await db.channels.find_one({"chat_id": chat_id})
            if ch and ch.get("greetings_enabled", False):
                greet_text = ch.get("greetings_text", f"Welcome to **{ch.get('title')}**! 🎉")
                try:
                    await client.send_message(user_id, greet_text)
                except Exception:
                    pass
        except Exception as e:
            await callback_query.answer(f"Error: {e}", show_alert=True)
        return

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
        chat_id = int(data.split("manage_")[1])
        text, markup = await get_channel_panel(client, chat_id)
        if text and markup:
            await callback_query.edit_message_text(text, reply_markup=markup)
        else:
            await callback_query.answer("Channel not found in database.", show_alert=True)

    elif data.startswith("sub_app_"):
        chat_id = int(data.split("sub_app_")[1])
        text, markup = await get_app_settings_panel(chat_id)
        await callback_query.edit_message_text(text, reply_markup=markup)

    elif data.startswith("toggle_auto_"):
        chat_id = int(data.split("toggle_auto_")[1])
        ch = await db.channels.find_one({"chat_id": chat_id})
        if ch:
            new_state = not ch.get("auto_approve", False)
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"auto_approve": new_state}})
            text, markup = await get_app_settings_panel(chat_id)
            await callback_query.edit_message_text(text, reply_markup=markup)

    elif data.startswith("toggle_captcha_"):
        chat_id = int(data.split("toggle_captcha_")[1])
        ch = await db.channels.find_one({"chat_id": chat_id})
        if ch:
            new_state = not ch.get("captcha", False)
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"captcha": new_state}})
            text, markup = await get_app_settings_panel(chat_id)
            await callback_query.edit_message_text(text, reply_markup=markup)

    elif data.startswith("edit_captchatxt_"):
        chat_id = int(data.split("edit_captchatxt_")[1])
        USER_STATE[user_id] = {"action": "edit_captchatxt", "chat_id": chat_id}
        await callback_query.edit_message_text(
            "📝 **Send the new CAPTCHA verification message in your next text:**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_state_{chat_id}")]])
        )

    elif data.startswith("edit_captchabtn_"):
        chat_id = int(data.split("edit_captchabtn_")[1])
        USER_STATE[user_id] = {"action": "edit_captchabtn", "chat_id": chat_id}
        await callback_query.edit_message_text(
            "🔘 **Send the new name for the Verification Button:**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_state_{chat_id}")]])
        )

    elif data.startswith("sub_greet_"):
        chat_id = int(data.split("sub_greet_")[1])
        text, markup = await get_greet_panel(chat_id)
        await callback_query.edit_message_text(text, reply_markup=markup)

    elif data.startswith("toggle_greet_"):
        chat_id = int(data.split("toggle_greet_")[1])
        ch = await db.channels.find_one({"chat_id": chat_id})
        if ch:
            new_state = not ch.get("greetings_enabled", False)
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"greetings_enabled": new_state}})
            text, markup = await get_greet_panel(chat_id)
            await callback_query.edit_message_text(text, reply_markup=markup)

    elif data.startswith("edit_greet_"):
        chat_id = int(data.split("edit_greet_")[1])
        USER_STATE[user_id] = {"action": "edit_greet", "chat_id": chat_id}
        await callback_query.edit_message_text(
            "✏️ **Send the new Welcome Greeting message in your next text:**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_state_{chat_id}")]])
        )

    elif data.startswith("sub_farewell_"):
        chat_id = int(data.split("sub_farewell_")[1])
        text, markup = await get_farewell_panel(chat_id)
        await callback_query.edit_message_text(text, reply_markup=markup)

    elif data.startswith("toggle_farewell_"):
        chat_id = int(data.split("toggle_farewell_")[1])
        ch = await db.channels.find_one({"chat_id": chat_id})
        if ch:
            new_state = not ch.get("farewells_enabled", False)
            await db.channels.update_one({"chat_id": chat_id}, {"$set": {"farewells_enabled": new_state}})
            text, markup = await get_farewell_panel(chat_id)
            await callback_query.edit_message_text(text, reply_markup=markup)

    elif data.startswith("edit_farewell_"):
        chat_id = int(data.split("edit_farewell_")[1])
        USER_STATE[user_id] = {"action": "edit_farewell", "chat_id": chat_id}
        await callback_query.edit_message_text(
            "✏️ **Send the new Farewell message in your next text:**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_state_{chat_id}")]])
        )

    elif data.startswith("view_requests_"):
        chat_id = int(data.split("view_requests_")[1])
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
        chat_id = int(data.split("bulk_approve_")[1])
        await callback_query.answer("Processing requests...", show_alert=False)
        try:
            async for req in client.get_chat_join_requests(chat_id):
                try:
                    await client.approve_chat_join_request(chat_id, req.from_user.id)
                except Exception:
                    pass
            await callback_query.answer("✅ All join requests accepted successfully!", show_alert=True)
            text, markup = await get_channel_panel(client, chat_id)
            await callback_query.edit_message_text(text, reply_markup=markup)
        except Exception as e:
            await callback_query.answer(f"❌ Error: {e}", show_alert=True)

    elif data.startswith("copy_settings_"):
        await callback_query.answer("Settings can be mirrored to your other registered channels.", show_alert=True)

    elif data.startswith("remove_ch_"):
        chat_id = int(data.split("remove_ch_")[1])
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
