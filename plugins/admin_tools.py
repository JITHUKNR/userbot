import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions

# 1. GROUP MODERATION
@Client.on_message(filters.command("ban") & filters.group)
async def ban_user(client: Client, message: Message):
    if message.reply_to_message:
        try:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply_text(f"🔨 Successfully banned {message.reply_to_message.from_user.mention}!")
        except Exception:
            await message.reply_text("❌ Failed to ban. I need Admin rights.")

@Client.on_message(filters.command("mute") & filters.group)
async def mute_user(client: Client, message: Message):
    if message.reply_to_message:
        try:
            await client.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
            await message.reply_text(f"🔇 Muted {message.reply_to_message.from_user.mention}.")
        except Exception:
            await message.reply_text("❌ Failed to mute. I need Admin rights.")

@Client.on_message(filters.command("purge") & filters.group)
async def purge_msgs(client: Client, message: Message):
    if message.reply_to_message:
        start_id = message.reply_to_message.id
        message_ids = [i for i in range(start_id, message.id + 1)]
        try:
            await client.delete_messages(message.chat.id, message_ids)
            msg = await client.send_message(message.chat.id, f"🗑 Purged {len(message_ids)} messages.")
            await asyncio.sleep(3)
            await msg.delete()
        except Exception:
            pass

@Client.on_message(filters.command("pin") & filters.group)
async def pin_msg(client: Client, message: Message):
    if message.reply_to_message:
        try:
            await message.reply_to_message.pin()
            await message.reply_text("📌 Message pinned.")
        except Exception:
            await message.reply_text("❌ Cannot pin message.")

@Client.on_message(filters.command("lock") & filters.group)
async def lock_chat(client: Client, message: Message):
    try:
        await client.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=False))
        await message.reply_text("🔒 Group Locked. Only Admins can send messages now.")
    except Exception:
        await message.reply_text("❌ Failed to lock group.")

@Client.on_message(filters.command("unlock") & filters.group)
async def unlock_chat(client: Client, message: Message):
    try:
        await client.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True))
        await message.reply_text("🔓 Group Unlocked. Everyone can send messages.")
    except Exception:
        pass

# 2. CHANNEL CONTROLS
@Client.on_message(filters.command("editpost") & filters.private)
async def edit_ch_post(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text("Usage: `/editpost [Post-Link] [New Text]`")
    try:
        args = message.text.split(" ", 2)
        link_parts = args[1].split("/")
        chat_id, msg_id = "@" + link_parts[-2], int(link_parts[-1])
        await client.edit_message_text(chat_id=chat_id, message_id=msg_id, text=args[2])
        await message.reply_text("✅ Post edited successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Edit failed: {e}")

@Client.on_message(filters.command("timer"))
async def auto_delete_timer(client: Client, message: Message):
    if not message.reply_to_message or len(message.command) < 2:
        return await message.reply_text("Reply to a message with `/timer [minutes]`")
    try:
        minutes = int(message.command[1])
        msg_to_delete = message.reply_to_message
        confirm_msg = await message.reply_text(f"⏳ This message will auto-delete in {minutes} minutes.")
        await message.delete()
        await asyncio.sleep(minutes * 60)
        await msg_to_delete.delete()
        await confirm_msg.delete()
    except Exception:
        pass

# 3. AUTO APPROVE JOIN REQUESTS
@Client.on_chat_join_request()
async def auto_approve_req(client: Client, message):
    try:
        await client.approve_chat_join_request(message.chat.id, message.from_user.id)
        welcome_text = f"Hello {message.from_user.first_name}, Welcome to {message.chat.title}! 🥳"
        await client.send_message(message.from_user.id, welcome_text)
    except Exception:
        pass
