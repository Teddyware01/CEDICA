from src.core.database import db
from src.core.auth.user import Users

def list_users():
    Users = Users.query.all()

    return Users

def create_user(**kwargs):
    User = Users(**kwargs)
    db.session.add(User)
    db.session.commit()

    return User