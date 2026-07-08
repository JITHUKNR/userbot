import logging
from pyrogram import Client
from config import Config
from keep_alive import keep_alive

# ബോട്ടിന്റെ പ്രവർത്തനങ്ങൾ ലോഗ് ചെയ്യാൻ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# പ്ലഗിൻ ഫോൾഡർ സെറ്റ് ചെയ്യുന്നു (ഇതിലെ ഫയലുകളാണ് ബോട്ട് റൺ ചെയ്യുന്നത്)
plugins = dict(root="plugins")

# ബോട്ട് ഇനിഷ്യലൈസ് ചെയ്യുന്നു
app = Client(
    "ultimate_master_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=plugins
)

if __name__ == "__main__":
    logger.info("🚀 Ultimate Pro Bot is starting... Loading plugins...")
    # Render-ൽ 24/7 ആക്റ്റീവ് ആക്കാൻ
    keep_alive()
    # ബോട്ട് റൺ ചെയ്യുന്നു
    app.run()
