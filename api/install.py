import sys

from finance.database import DB
from finance.models.user import User

db = DB()


def create_db(args):
    db.init_db()


def create_user(args):
    username = args[0] if len(args) > 0 else 'admin'
    password = args[1] if len(args) > 1 else 'secret'
    u = User(username, password)
    db.session.add(u)
    db.session.commit()


COMMANDS = {
    'initdb': create_db,
    'user': create_user,
}

if __name__ == "__main__":
    try:
        cmd = sys.argv[1]
    except KeyError:
        print("Missing required command\n")
        sys.exit(1)
    else:
        COMMANDS[cmd](sys.argv[2:])
