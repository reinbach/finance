import sys

from finance.models.user import User
from finance.models.mapper import set_model_mapping
from finance import db

def create_db(args):
    print("Creating database...")
    set_model_mapping()
    db.metadata.create_all(bind=db.get_engine())
    print("done.")


def create_user(args):
    print("Creating user...")
    username = args[0] if len(args) > 0 else 'admin'
    password = args[1] if len(args) > 1 else 'secret'
    u = User(username, password)
    db.session.add(u)
    db.session.commit()
    print("done.")


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
