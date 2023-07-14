# easydb.py
### Features

- Read by line for line a .py file. or variable. its explained better in _modelos.py
- can set easy with some config
# You can create your own models like this, lets named telegram_models.py
```
TelegramGroup = """
    CREATE TABLE IF NOT EXISTS TelegramGroup (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        lang TEXT,
        created_at TEXT
    )
"""

TelegramUser = """
    CREATE TABLE IF NOT EXISTS TelegramUser (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        lang TEXT,
        prefix TEXT,
        nick TEXT,
        birthday TEXT,
        created_at TEXT
    )
"""
```
# Example buiding a config class for a bot.
```
import os
import mydb
from . import telegram_models

class telegramConfig:
    def __init__(self):
        conf = {
            "telegram_groups": [os.getcwd()+"/data/in/telegram/guilds.db", "TelegramGroup"], >
            "telegram_users": [os.getcwd()+"/data/in/telegram/users.db", "TelegramUser"] # wa>
        }
        self.users = mydb.DataBase("telegram_users", config=conf, models=telegram_models)
        self.guilds = mydb.DataBase("telegram_groups", config=conf, models=telegram_models)
        # rest of the code.

  def get_room(self, name, ex={}):
        r = self.guilds.create_if_doesnt_exist(name, ex)
        if r:
            return mydb.Struct(**r)
        return None

  def get_user(self, name, ex={}):
        r = self.users.create_if_doesnt_exist(name, ex)
        if r:
            return mydb.Struct(**r)
        return None


```

## for handling in on_message events...
```
async def on_message(self, messagae):
    croom = self.config.get_room(message.room.name, ex=dict(suffix=csuffix, lang="en"))

     # when changing something in database I just do
     #when get user its get it like Class thats why its the object cuser that i get with the get_user
     if cmd == "lang" and args == "en":
     self.config.guilds.update_row(lcs.cuser.id, 'lang', 'en')

```
