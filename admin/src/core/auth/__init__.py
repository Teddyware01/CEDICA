from src.core.database import db
from src.core.auth.user import Users
from src.core.auth.roles import Roles
from src.core.auth.permisos import Permisos
from sqlalchemy import func


def find_user_by_email_and_password(email, password):
    user = Users.query.filter_by(email=email, password=password).first()
    return user

def find_user_by_email(email):
    user = Users.query.filter_by(email=email).first()
    return user
def filtrado_roles(role_filter, exact_match=False):
    users = Users.query.all()
    filtered_users = []
    for user in users:
        # Obtener los roles del usuario en una lista
        user_roles = [role.nombre for role in user.roles]  # Asumiendo que 'roles' es una relación con el modelo 'Roles'

        if exact_match:
            # Filtrar por roles exactamente iguales
            if sorted(user_roles) == sorted(role_filter):  # Ordenamos para asegurar que el orden no afecte
                filtered_users.append(user)
        else:
            # Filtrar por al menos uno de los roles seleccionados
            if any(role in role_filter for role in user_roles):
                filtered_users.append(user)

    return filtered_users

def list_users(status_filter, role_filter=None, exact_match=None, sort_by=None, search=None, page=1, per_page=5):
    query = Users.query

    # Filtrar por roles
    if role_filter:
        if exact_match:
            # Filtrar usuarios con exactamente los roles seleccionados
            filtered_users = filtrado_roles(role_filter, exact_match=True)
            # Convertir la lista de usuarios filtrados en un query compatible para paginación
            user_ids = [user.id for user in filtered_users]
            query = query.filter(Users.id.in_(user_ids))
        else:
            # Filtrar usuarios que tienen al menos uno de los roles seleccionados
            query = query.filter(Users.roles.any(Roles.nombre.in_(role_filter)))

    # Filtrar por estado (activo/inactivo)
    if status_filter == 'active':
        query = query.filter(Users.activo == True)
    elif status_filter == 'inactive':
        query = query.filter(Users.activo == False)

    # Filtrar por búsqueda (por email)
    if search:
        query = query.filter(Users.email.like(f"%{search}%"))

    # Aplicar ordenación
    if sort_by:
        if sort_by == "email_asc":
            query = query.order_by(Users.email.asc())
        elif sort_by == "email_desc":
            query = query.order_by(Users.email.desc())
        elif sort_by == "created_at_asc":
            query = query.order_by(Users.fecha_creacion.asc())
        elif sort_by == "created_at_desc":
            query = query.order_by(Users.fecha_creacion.desc())

    # Paginación
    paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)
    return paginated_query


def create_user(**kwargs):
    User = Users(**kwargs)
    db.session.add(User)
    db.session.commit()

    return User


def delete_user(user_id):
    User = Users.query.get(user_id)
    if User:
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
    permisos = Permisos(**kwargs)
    db.session.add(permisos)
    db.session.commit()

    return permisos

# Asigna, no agrega. (Sobreescribira los roles que tenia asignados, por los nuevos)
def assign_rol(user, rol):
    user.roles = rol
    db.session.add(user)
    db.session.commit()

    return user


# Agrega un permiso (se suma a los ya asignados).
def assign_permiso(rol, permiso):
    rol.permisos.append(permiso)
    db.session.add(rol)
    db.session.commit()

    return rol


def traer_usuario(user_id):
    user = Users.query.get(user_id)
    return user

def traer_roles(user_id):
    user = traer_usuario(user_id)
    return user.roles

def actualizar_roles(user_id, selected_roles):
    user = traer_usuario(user_id)
   
    roles_usuario = [rol.nombre for rol in user.roles]
    print(f"Roles actuales del usuario: {roles_usuario}")
   
    roles_a_agregar = [rol for rol in selected_roles if rol not in roles_usuario]
    print(f"Roles a agregar: {roles_a_agregar}")
    
    roles_a_quitar = [rol for rol in roles_usuario if rol not in selected_roles]
    print(f"Roles a quitar: {roles_a_quitar}")
    
    for rol_nombre in roles_a_agregar:
        rol = Roles.query.filter_by(nombre=rol_nombre).first()  
        if rol:
            print(f"Agregando rol: {rol_nombre} (ID: {rol.id})")
            user.roles.append(rol)  
        else:
            print(f"Error: No se encontró el rol con nombre {rol_nombre}")
    
    for rol_nombre in roles_a_quitar:
        rol = Roles.query.filter_by(nombre=rol_nombre).first()  
        if rol:
            print(f"Eliminando rol: {rol_nombre} (ID: {rol.id})")
            user.roles.remove(rol)  
        else:
            print(f"Error: No se encontró el rol con nombre {rol_nombre}")
   
    db.session.commit()
        
def permisos_del_rol(rol):
    return rol.permisos


# Falta comprobar funcionamiento... 
def get_permissions(user):
    roles_usuario = user.roles
    permisos_usuario = []

    for rol in roles_usuario:
        for permiso in permisos_del_rol(rol):
            permisos_usuario.append(permiso.nombre)


    print(f"Get permissions user.id= ",  user.id, "   user.email= ", user.email)
    print(f"Get roles= ", roles_usuario)
    print(f"Get permisos= ",permisos_usuario)
    return permisos_usuario

def all_roles():
    roles = Roles.query.all()
    return roles