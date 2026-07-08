from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

# മെയിൻ ഡാഷ്‌ബോർഡ് ബട്ടണുകൾ
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛡 Group Management", callback_data="menu_group"),
         InlineKeyboardButton("📢 Channel Control", callback_data="menu_channel")],
        [InlineKeyboardButton("🚀 Viral Marketing", callback_data="menu_viral"),
         InlineKeyboardButton("⚙️ Bot Info", callback_data="menu_info")],
        [InlineKeyboardButton("Close Dashboard ❌", callback_data="close_menu")]
    ])

@Client.on_message(filters.command(["start", "menu"]) & filters.private)
async def start_menu(client: Client, message: Message):
    text = (
        "👑 **ULTIMATE ADMIN CONTROL PANEL**\n\n"
        "Welcome to your Master Bot. This bot helps you control your groups, "
        "manage your channels, and run viral marketing campaigns.\n\n"
        "Select a category below to view available commands:"
    )
    await message.reply_text(text, reply_markup=get_main_menu())

@Client.on_callback_query(filters.regex("^menu_"))
async def navigate_menu(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    
    if data == "menu_main":
        text = (
            "👑 **ULTIMATE ADMIN CONTROL PANEL**\n\n"
            "Select a category below to view available commands:"
        )
        await callback_query.edit_message_text(text, reply_markup=get_main_menu())
        
    elif data == "menu_group":
        text = (
            "🛡 **Group Management Commands**\n\n"
            "Use these commands directly in your group (Bot must be Admin):\n"
            "▫️ `/ban` - Reply to a user to ban them.\n"
            "▫️ `/mute` - Reply to restrict a user.\n"
            "▫️ `/purge` - Reply to a message to delete everything below it.\n"
            "▫️ `/pin` - Reply to pin a message.\n"
            "▫️ `/lock` - Lock group (Only Admins can send messages).\n"
            "▫️ `/unlock` - Unlock group for everyone."
        )
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=btn)
        
    elif data == "menu_channel":
        text = (
            "📢 **Channel Control Commands**\n\n"
            "Manage your channel like a pro:\n"
            "▫️ `/editpost [Post-Link] [New Text]` - Edit a channel post directly from Bot PM.\n"
            "▫️ `/timer [minutes]` - Reply to a message in group/channel to auto-delete it after X minutes (Great for limited offers!).\n"
            "▫️ `/info` - Get Chat ID and member count."
        )
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=btn)
        
    elif data == "menu_viral":
        text = (
            "🚀 **Viral Marketing Task (Share to Unlock)**\n\n"
            "Run these commands in Bot PM to set up the viral post:\n"
            "1️⃣ `/settarget @your_group` - Set where the post goes.\n"
            "2️⃣ `/setlinks [Share-Link] [VIP-Link]` - Set the task links.\n"
            "3️⃣ Send an Image/Video here, then reply to it with `/makepost` to send it to the group with the Task Button!"
        )
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=btn)
        
    elif data == "menu_info":
        text = (
            "⚙️ **System Status**\n\n"
            "✅ **Auto-Approve Join Requests:** Active\n"
            "✅ **Plugin System:** Running smoothly\n"
            "✅ **Status:** Online & Ready."
        )
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")]])
        await callback_query.edit_message_text(text, reply_markup=btn)

@Client.on_callback_query(filters.regex("close_menu"))
async def close_menu(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()
