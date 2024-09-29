from src.core.database import db
from src.core.auth.user import Users
from src.core.auth.roles import Roles
from src.core.auth.permisos import Permisos

def list_users():
    User = Users.query.all()
    return User

def create_user(**kwargs):
    User = Users(**kwargs)
    db.session.add(User)
    db.session.commit()

    return User


def create_roles(**kwargs):
    Rol = Roles(**kwargs)
    db.session.add(Rol)
    db.session.commit()

    return Rol

def create_permisos(**kwargs):
    Permisos = Permisos(**kwargs)
    db.session.add(Permisos)
    db.session.commit()

    return Permisos


def assign_rol(user, rol):
    user.roles = rol
    db.session.add(user)
    db.session.commit()

    return user


def assign_permiso(rol, permiso):
    rol.permisos = permiso
    db.session.add(rol)
    db.session.commit()

    return rol