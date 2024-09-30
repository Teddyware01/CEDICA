from src.core.database import db
from src.core.auth.user import Users
from src.core.auth.roles import Roles
from src.core.auth.permisos import Permisos



def list_users(sort_by=None):
    query = Users.query
    if sort_by:
        if sort_by == 'email_asc':
            query = query.order_by(Users.email.asc())
        elif sort_by == 'email_desc':
            query = query.order_by(Users.email.desc())
        elif sort_by == 'created_at_asc':
            query = query.order_by(Users.fecha_creacion.asc())
        elif sort_by == 'created_at_desc':
            query = query.order_by(Users.fecha_creacion.desc())
    return query.all()


def create_user(**kwargs):
    User = Users(**kwargs)
    db.session.add(User)
    db.session.commit()

    return User

def delete_user(user_id):
    User = Users.query.get(user_id)
    if(User):
        db.session.delete(User)
        db.session.commit()
        return True
    return False


def edit_user(user_id, **kwargs):
    User = Users.query.get(user_id)
    for key, value in kwargs.items():
        if hasattr(User, key):
            setattr(User, key, value)
    db.session.commit()
  
    

def user_email_exists(email, user_id=None):
    query = Users.query.filter_by(email=email)
    if user_id: 
        query = query.filter(Users.id != user_id)  
    return query.first() is not None

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