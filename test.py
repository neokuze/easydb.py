#! /usr/bin/python3.9
import easydb 

# conf = {
#     "guilds": [os.getcwd()+f"{dir_div}guilds.db", "Guild"],
#     "users": [os.getcwd()+f"{dir_div}users.db", "User"]}

debug = True

users = easydb.DataBase("users")
guilds = easydb.DataBase("guilds", config=None, models=None, now = False) # you can read the source if you doesn't understand

"""
can load your own config, be sure to have same name in _modelos.py
can load your own models you can use the _modelos.py as an example.
"""

def add(database, name: str):
    """
    @params
    database: from easydb.Database(table)
    name: str,
    """
    cuser = database.get_object(name, ex=dict(lang='en', prefix="/"))
    if debug:
        print(cuser.__dir__(), cuser.id, cuser.name, cuser.lang, cuser.prefix, cuser.created_at)

def set_to(database, name="test1", what_to_change="prefix", value="."):
    """
    @params
    database: class where is the database,
    name: of the key to search in the database
    what_to_change: the key must be on the _modelos that was loaded to the database.
    value: this can be string or int, be sure of what you are saving
 
    This is just an example of making changes to a user in database but I used in my bots.
    Exmple;
    eval set_to(users, name, what_to_change, value)
    eval set_to(guilds, name, what_to_change, value)
    """
    if value:
        if len(value) <=2:
            database.update_row_by_name(name, what_to_change, value)
            msg = "{} changed to {} for user {}".format(what_to_change, value, name)
        else: msg = "prefix is long..."
    else:
        msg = "eval set_to('user1', what_to_change='lang', value='es')"
    if debug:
        print(msg)

def test(name: str = "test1"):
    """THis is just going to create a user in users database"""
    add(users, name) # databases are converted in class
    set_to(users, name) # this is just a test, im not going to complicate.
    add(guilds, name) # using guilds as database

def testing():
    """write; eval test()"""
    while True:
        _input = str(input(">>"))
        if len(_input.split(' ')) > 1:
            cmd, args = _input.split(' ', 1)
            args = args.split()
        else:
            cmd = _input.lower()
            args = []
        if cmd == "eval" and args:
            try:
                ret = repr(eval(" ".join(args)))
            except Exception as e:
                ret = str(e)
            print(repr(ret))
        elif cmd in ['q', 'quit']:
            break
testing()
