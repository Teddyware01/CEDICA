from functools import wraps
from flask import abort
from flask import redirect, url_for
from flask import session
from src.core.auth import Roles, Permisos
from src.core import auth


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

def is_authenticated(session):
    return session.get("user") is not None

def check(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not check_permission(session,permission):
                return abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator



def check_permission(session, permission):
    user_email = session["user"]
    user = auth.find_user_by_email(user_email)
    if(user.system_admin):
        return True
    permissions = auth.get_permissions(user)

    return user is not None and permission in permissions