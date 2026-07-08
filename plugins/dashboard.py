from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

# ==========================================
# മെനു ബട്ടണുകൾ ഉണ്ടാക്കുന്ന ഫംഗ്ഷനുകൾ
# ==========================================

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛡 Group Management", callback_data="menu_group"),
         InlineKeyboardButton("📢 Channel Control", callback_data="menu_channel")],
        [InlineKeyboardButton("🚀 Viral Marketing", callback_data="menu_viral"),
         InlineKeyboardButton("⚙️ Bot Info", callback_data="menu_info")],
        [InlineKeyboardButton("Close Dashboard ❌", callback_data="close_menu")]
    ])

def get_group_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔨 Ban User", callback_data="help_ban"), 
         InlineKeyboardButton("🔇 Mute User", callback_data="help_mute")],
        [InlineKeyboardButton("🗑 Purge Messages", callback_data="help_purge"), 
         InlineKeyboardButton("📌 Pin Message", callback_data="help_pin")],
        [InlineKeyboardButton("🔒 Lock Group", callback_data="help_lock"), 
         InlineKeyboardButton("🔓 Unlock Group", callback_data="help_unlock")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")]
    ])

def get_channel_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Post", callback_data="help_editpost")],
        [InlineKeyboardButton("⏳ Auto-Delete Timer", callback_data="help_timer")],
        [InlineKeyboardButton("📊 Get Chat Info", callback_data="help_info")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")]
    ])

def get_viral_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Set Target Chat", callback_data="help_settarget")],
        [InlineKeyboardButton("🔗 Set Task Links", callback_data="help_setlinks")],
        [InlineKeyboardButton("🖼 Make Poster Post", callback_data="help_makepost")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")]
    ])

# ==========================================
# മെനു കമാൻഡ്
# ==========================================

@Client.on_message(filters.command(["start", "menu"]) & filters.private)
async def start_menu(client: Client, message: Message):
    text = (
        "👑 **ULTIMATE ADMIN CONTROL PANEL**\n\n"
        "Welcome to your Master Bot. This bot helps you control your groups, "
        "manage your channels, and run viral marketing campaigns.\n\n"
        "Select a category below:"
    )
    await message.reply_text(text, reply_markup=get_main_menu())

# ==========================================
# ബട്ടൺ ക്ലിക്കുകൾ നിയന്ത്രിക്കുന്ന ഭാഗം
# ==========================================

@Client.on_callback_query()
async def handle_all_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    
    # --- മെയിൻ മെനുകൾ ---
    if data == "menu_main":
        text = "👑 **ULTIMATE ADMIN CONTROL PANEL**\n\nSelect a category below:"
        await callback_query.edit_message_text(text, reply_markup=get_main_menu())
        
    elif data == "menu_group":
        text = "🛡 **Group Management**\n\nClick a tool below to see how to use it:"
        await callback_query.edit_message_text(text, reply_markup=get_group_menu())
        
    elif data == "menu_channel":
        text = "📢 **Channel Control**\n\nClick a tool below to see how to use it:"
        await callback_query.edit_message_text(text, reply_markup=get_channel_menu())
        
    elif data == "menu_viral":
        text = "🚀 **Viral Marketing Setup**\n\nClick a step below to see instructions:"
        await callback_query.edit_message_text(text, reply_markup=get_viral_menu())
        
    elif data == "menu_info":
        text = (
            "⚙️ **System Status**\n\n"
            "✅ **Auto-Approve Join Requests:** Active\n"
            "✅ **Plugin System:** Running smoothly\n"
            "✅ **Status:** Online & Ready."
        )
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    # --- ഹെൽപ്പ് ഇൻസ്ട്രക്ഷനുകൾ (ഓരോ ബട്ടണിലും ഞെക്കുമ്പോൾ വരുന്നത്) ---
    elif data == "help_ban":
        text = "🔨 **Ban User**\n\nUsage: Reply to a user's message in your group with `/ban` to remove them permanently."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_mute":
        text = "🔇 **Mute User**\n\nUsage: Reply to a user's message with `/mute` to stop them from sending messages."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_purge":
        text = "🗑 **Purge Messages**\n\nUsage: Reply to a message with `/purge` to delete that message and all messages sent after it."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_pin":
        text = "📌 **Pin Message**\n\nUsage: Reply to a message with `/pin` to pin it to the top of the chat."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_lock":
        text = "🔒 **Lock Group**\n\nUsage: Type `/lock` in the group. Normal members won't be able to send messages, only Admins can."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_unlock":
        text = "🔓 **Unlock Group**\n\nUsage: Type `/unlock` to allow everyone to send messages again."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_editpost":
        text = "✏️ **Edit Channel Post**\n\nUsage: Send the command in this bot's PM.\nFormat: `/editpost [Post-Link] [New Text]`\n\nExample:\n`/editpost https://t.me/WETFLAX/123 This is the new text!`"
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Channel Menu", callback_data="menu_channel")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_timer":
        text = "⏳ **Auto-Delete Timer**\n\nUsage: Reply to any message in your group with `/timer [minutes]`.\n\nExample: `/timer 10` will delete that message automatically after 10 minutes."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Channel Menu", callback_data="menu_channel")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_info":
        text = "📊 **Chat Info**\n\nUsage: Type `/info` in your group or channel to get the Chat ID and total member count."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Channel Menu", callback_data="menu_channel")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_settarget":
        text = "🎯 **Set Target Chat**\n\nUsage: Tell the bot where to send the viral post.\nCommand: `/settarget @your_group_username`"
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Viral Menu", callback_data="menu_viral")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_setlinks":
        text = "🔗 **Set Task Links**\n\nUsage: Set the share link and the final VIP join link.\nCommand: `/setlinks [Share-Link] [VIP-Link]`"
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Viral Menu", callback_data="menu_viral")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_makepost":
        text = "🖼 **Make Viral Poster**\n\nUsage: First, send an image or video to the bot. Then, reply to that image with the command `/makepost`. The bot will automatically add the Share Button and send it to your target group!"
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Viral Menu", callback_data="menu_viral")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "close_menu":
        await callback_query.message.delete()
        
    # ഗ്രൂപ്പിലെ ടാസ്ക് ബട്ടണിൽ ക്ലിക്ക് ചെയ്താൽ വർക്ക് ചെയ്യാനുള്ള കോഡ് വൈറൽ ഫയലിൽ ഉള്ളതുകൊണ്ട് അത് പാസ് ചെയ്യുന്നു
    elif data == "group_share_task":
        pass
