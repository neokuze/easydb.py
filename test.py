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

def testing():
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
            #print(ret)
        elif cmd in ['q', 'quit']:
            break
testing()