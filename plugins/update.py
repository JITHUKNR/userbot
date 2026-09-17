import os
from pyrogram import Client, filters

# Replace with your actual Telegram User ID below
OWNER_ID = 7567364364 

# Only the OWNER_ID can use this command in the bot's PM
@Client.on_message(filters.command("update") & filters.user(OWNER_ID))
async def update_bot(client, message):
    m = await message.reply_text("🔄 **Pulling latest code from GitHub...**")
    
    try:
        # Run git pull command
        stream = os.popen('git pull')
        output = stream.read()
        
        if "Already up to date" in output:
            await m.edit("✅ **Bot is already up to date!** No new updates available.")
        else:
            await m.edit(f"✅ **Code updated successfully!**\n\n`{output}`\n\n🚀 **Restarting bot... It will be active again in a few seconds!**")
            # Restart bot using PM2
            os.system("pm2 restart userbot")
    except Exception as e:
        await m.edit(f"❌ **An error occurred:**\n`{e}`")
