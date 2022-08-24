from . import _modelos as models
import sys, os, sqlite3
from datetime import datetime

if os.name == 'nt':
    dir_div = "\\"
else: dir_div = "/"

conf = {
    "guilds": [os.getcwd()+f"{dir_div}guilds.db", "Guild"],
    "users": [os.getcwd()+f"{dir_div}users.db", "User"]}

"""
be sure to have the same name as models table in your _modelos.py and conf.
"""

class Struct: # thx linkkg
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __dir__(self):
        return [x for x in
                set(list(self.__dict__.keys()) + list(dir(type(self)))) if
                x[0] != '_']

class DataBase:
    def __init__(self, table, config=None, now=True):
        self.path = config[table] if config else conf[table]
        self.metatable = None
        if now:
            self.connect_to_db()

    def __repr__(self):
        return f"<{self.path[1]}>"

    def get_object(self, name, ex={}):
        r = self.create_if_doesnt_exist(name, ex)
        if r: return Struct(**r)
        return None

    def connect_to_db(self):
        if not self.metatable:
            self.metatable = self.look_at_table()
        self.db = sqlite3.connect(self.path[0])
        self.db_cursor = self.db.cursor()
        self.db_cursor.execute(getattr(models, self.path[1]))
    
    def create_if_doesnt_exist(self, name, ex={}):
        table_name = self.path[1]
        self.db_cursor.execute(f"SELECT * FROM {table_name} WHERE name=?", (name,))
        response = self.db_cursor.fetchone()
        if not response:
            default_names = ['name','created_at']+list(ex.keys())
            default_values = list(ex.values())
            values = ",".join(['?' for i in range(len(default_names))])
            value_names = ",".join([str(x) for x in default_names])
            date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            self.db_cursor.execute(f"INSERT INTO {table_name}({value_names}) VALUES ({values})",
                (name, date, *default_values))
            self.db.commit()
            return self.create_if_doesnt_exist(name, ex)
        return self._covert_to_dict(response)

    def select_from_all(self, name):
        self.db_cursor.execute(f"SELECT * FROM {self.path[1]} WHERE name=?", (name,))
        response = self.db_cursor.fetchone()
        return response

    def look_at_table(self):
        base = getattr(models, self.path[1])
        param = base.split('(')[1].split(')')[0]
        r = []
        for sentence in param.replace('  ','').split(','):
            if 'INTEGER' in sentence:
                r.append(sentence.split('INTEGER')[0].strip().replace('\n',''))
            elif 'TEXT' in sentence:
                r.append(sentence.split('TEXT')[0].strip().replace('\n',''))
        return r

    def _covert_to_dict(self, resp):
        r = {}
        if resp:
            for i in range(len(resp)):
                r[self.metatable[i]] = resp[i]
        return r or None

    def update_row(self, uid, k, v):
        sql = f'''UPDATE {self.path[1]} SET {k} = ? WHERE id = ? '''
        self.db_cursor.execute(sql, (v, uid))
        self.db.commit()

    def update_row_by_name(self, uname, k, v):
        sql = f'''UPDATE {self.path[1]} SET {k} = ? WHERE name = ? '''
        self.db_cursor.execute(sql, (v, uname))
        self.db.commit()

    def check_if_exist(self, name):
        table_name = self.path[1]
        self.db_cursor.execute(f"SELECT * FROM {table_name} WHERE name=?", (name,))
        response = self.db_cursor.fetchone()
        if response: 
            return True
        return False

    def delete_row(self, name):
        table_name = self.path[1]
        if self.check_if_exist(name):
            self.db_cursor.execute(f"DELETE FROM {table_name} WHERE name=?", (name,))
            self.db.commit()
            return True
        return False
