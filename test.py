#! /usr/bin/python3.9
import easydb 

# conf = {
#     "guilds": [os.getcwd()+f"{dir_div}guilds.db", "Guild"],
#     "users": [os.getcwd()+f"{dir_div}users.db", "User"]}

debug = True

users = easydb.DataBase("users")
guilds = easydb.DataBase("guilds", config=None, now = False)

"""
can load your own config, be sure to have same name in _modelos.py
"""

def add(name="test"):
    cuser = users.get_object(name, ex=dict(lang='en', prefix="/"))
    if debug:
        print(cuser.__dir__(), cuser.id, cuser.name, cuser.lang, cuser.prefix, cuser.created_at)

def set_to(database, name="test", what_to_change="prefix", value="."):
    """
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

def test():
    """eval test()"""
    add()
    set_to(users)
    add()

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