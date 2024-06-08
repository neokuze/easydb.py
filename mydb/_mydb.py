from . import _modelos as _models 
import sys, os, sqlite3
from datetime import datetime
"""
Columns now is automatic updated id added in actual_models.py and make the change to the table.
"""

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __dir__(self):
        return [x for x in
                set(list(self.__dict__.keys()) + list(dir(type(self)))) if
                x[0] != '_']
        
w = "\\" if os.name == 'nt' else "/" 
fpath = "{}{}".format(os.getcwd(),f"{w}") # if imported from main, create config folder and __init__.py
conf = {
    "Guild": [f"{fpath}guilds.db", "Guild"], # last one is name of the table
    "User": [f"{fpath}users.db", "User"] # was created for discord but yeah aja
}

class DataBase:
    def __init__(self, table, config=None, models=None, now=True):
        """
        table must exist in config is conf right down in line 19
        models = load your own schemas, example in _models
        now = connect to database at creating object: default ON
        Every Table require two columns name, created_at] idk if fails.
     
        """
        
        self.path = config[table] if config else conf[table]
        self.metatable = None
        self._models = models or _models
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
        self.db_cursor.execute(getattr(self._models, self.path[1]))
        self.update_table_if_needed()
    
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
        base = getattr(self._models, self.path[1])
        param = base.split('(')[1].split(')')[0]
        r = []
        for sentence in param.replace('  ','').split(','):
            if 'INTEGER' in sentence:
                r.append(sentence.split('INTEGER')[0].strip().replace('\n',''))
            elif 'TEXT' in sentence:
                r.append(sentence.split('TEXT')[0].strip().replace('\n',''))
            elif 'BLOB' in sentence:
                r.append(sentence.split('BLOB')[0].strip().replace('\n',''))
            elif 'REAL' in sentence:
                r.append(sentence.split('REAL')[0].strip().replace('\n',''))
        return r

    def _covert_to_dict(self, resp):
        if resp:
            return {col: val for col, val in zip(self.metatable, resp) if col}
        return None

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

    def update_table_if_needed(self):
        table_name = self.path[1]
        self.db_cursor.execute(f"PRAGMA table_info({table_name})")
        existing_columns = [col[1] for col in self.db_cursor.fetchall()]

        base_columns = self.look_at_table()
        for column in base_columns:
            if column not in existing_columns:
                column_type = self.get_column_type(column)
                self.db_cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} {column_type}")
                self.db.commit()

    def get_column_type(self, column_name):
        column_type = "TEXT"  
        model_definition = getattr(self._models, self.path[1])
        if column_name in model_definition:
            column_definition = model_definition.split(column_name)[1].split(",")[0].strip()
            if "INTEGER" in column_definition:
                column_type = "INTEGER"
            elif "REAL" in column_definition:
                column_type = "REAL"
            elif "BLOB" in column_definition:
                column_type = "BLOB"

        return column_type
