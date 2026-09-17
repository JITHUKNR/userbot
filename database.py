from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.channels = self.db.channels  # ചാനലുകൾ സേവ് ചെയ്യാൻ

# ബോട്ടിനുള്ള ഡാറ്റാബേസ് കണക്ഷൻ
db = Database(Config.MONGO_URL, "UserBotDB")
