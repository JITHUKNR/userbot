from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

# ==========================================
# മെനു ബട്ടണുകൾ ഉണ്ടാക്കുന്ന ഫംഗ്ഷനുകൾ
# ==========================================

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛡 Group Management", callback_data="menu_group"),
         InlineKeyboardButton("📢 Channel Control", callback_data="menu_channel")],
        [InlineKeyboardButton("📡 Broadcast System", callback_data="menu_broadcast"),
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

def get_broadcast_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📡 How to Broadcast", callback_data="help_broadcast")],
        [InlineKeyboardButton("🔗 Set Viral Links", callback_data="help_setlinks")],
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
        "manage your channels, and run broadcasts.\n\n"
        "Select a category below:"
    )
    await message.reply_text(text, reply_markup=get_main_menu())

# ==========================================
# ബട്ടൺ ക്ലിക്കുകൾ
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
        
    elif data == "menu_broadcast":
        text = "📡 **Broadcast System**\n\nClick a button below to see how to use the broadcast feature:"
        await callback_query.edit_message_text(text, reply_markup=get_broadcast_menu())
        
    elif data == "menu_info":
        text = (
            "⚙️ **System Status**\n\n"
            "✅ **Auto-Approve Join Requests:** Active\n"
            "✅ **Plugin System:** Running smoothly\n"
            "✅ **Status:** Online & Ready."
        )
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    # --- ഹെൽപ്പ് ഇൻസ്ട്രക്ഷനുകൾ ---
    elif data == "help_ban":
        text = "🔨 **Ban User**\n\nUsage: Reply to a user's message in your group with `/ban` to remove them permanently."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_mute":
        text = "🔇 **Mute User**\n\nUsage: Reply to a user's message with `/mute`."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_purge":
        text = "🗑 **Purge Messages**\n\nUsage: Reply to a message with `/purge` to delete everything below it."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_pin":
        text = "📌 **Pin Message**\n\nUsage: Reply to a message with `/pin`."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_lock":
        text = "🔒 **Lock Group**\n\nUsage: Type `/lock` in the group."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_unlock":
        text = "🔓 **Unlock Group**\n\nUsage: Type `/unlock` in the group."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Group Menu", callback_data="menu_group")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_editpost":
        text = "✏️ **Edit Channel Post**\n\nFormat: `/editpost [Post-Link] [New Text]`\n\nExample:\n`/editpost https://t.me/WETFLAX/123 New Text Here!`"
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Channel Menu", callback_data="menu_channel")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_timer":
        text = "⏳ **Auto-Delete Timer**\n\nUsage: Reply to a message with `/timer 10` (will delete after 10 mins)."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Channel Menu", callback_data="menu_channel")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_info":
        text = "📊 **Chat Info**\n\nUsage: Type `/info` in group/channel."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Channel Menu", callback_data="menu_channel")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_broadcast":
        text = "📡 **Broadcast Message**\n\nUsage: Reply to a photo/video/text and type `/broadcast` followed by Channel Username, ID or Link.\n\nExamples:\n`/broadcast @WETFLAX`\n`/broadcast -100123456789`\n`/broadcast https://t.me/WETFLAX`"
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Broadcast Menu", callback_data="menu_broadcast")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "help_setlinks":
        text = "🔗 **Set Task Links**\n\nUsage: `/setlinks [Share-Link] [VIP-Link]`\n(Sets the links for the button that goes with the broadcast)."
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Broadcast Menu", callback_data="menu_broadcast")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

    elif data == "close_menu":
        await callback_query.message.delete()
        
    elif data == "group_share_task":
        pass
