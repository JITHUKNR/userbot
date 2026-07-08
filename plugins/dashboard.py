from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

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

def get_channel_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Post", callback_data="help_editpost"),
         InlineKeyboardButton("⏳ Auto-Delete Timer", callback_data="help_timer")],
        [InlineKeyboardButton("📊 Chat Info", callback_data="help_info")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")]
    ])

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

@Client.on_callback_query()
async def handle_all_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    
    if data == "menu_main":
        await callback_query.edit_message_text("👑 **ULTIMATE ADMIN CONTROL PANEL**\n\nSelect a category below:", reply_markup=get_main_menu())
    elif data == "menu_group":
        await callback_query.edit_message_text("🛡 **Group Management**\n\nClick a tool below:", reply_markup=get_group_menu())
    elif data == "menu_channel":
        await callback_query.edit_message_text("📢 **Channel Control**\n\nClick a tool below:", reply_markup=get_channel_menu())
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
        await callback_query.edit_message_text(f"Channel Tools info. Check Dashboard for details.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_channel")]]))

    elif data == "close_menu":
        await callback_query.message.delete()
    elif data == "group_share_task":
        pass
