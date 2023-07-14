# easydb.py
### Features

- Read by line for line a .py file. or variable. its explained better in _modelos.py
- can set easy with some config

# Example buiding a config class for a bot.
```
import os
import mydb

class telegramConfig:
    def __init__(self):
        conf = {
            "telegram_groups": [os.getcwd()+"/data/in/telegram/guilds.db", "TelegramGroup"], >
            "telegram_users": [os.getcwd()+"/data/in/telegram/users.db", "TelegramUser"] # wa>
        }
        self.users = mydb.DataBase("telegram_users", conf)
        self.guilds = mydb.DataBase("telegram_groups", conf)
        # rest of the code.

  def get_room(self, name, ex={}):
        r = self.guilds.create_if_doesnt_exist(name, ex)
        if r:
            return Struct(**r)
        return None

  def get_user(self, name, ex={}):
        r = self.users.create_if_doesnt_exist(name, ex)
        if r:
            return Struct(**r)
        return None


```

## for handling in on_message events...

"""

"""
