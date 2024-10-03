from src.core import board
from src.core import auth

from src.core import equipo
from src.core.equipo.extra_models import Provincia 

from src.core.database import db
from sqlalchemy import text
def ejecutar_sql_script(file_path):
    with open(file_path, 'r',encoding='utf-8') as sql_file:
        sql_script = sql_file.read()
    
    with db.engine.connect() as connection:
        connection.execute(text(sql_script))
        connection.commit()

def run():
    issue1 = board.create_issue(
        email="user1@example.com",
        title="Error en la página de inicio",
        description="La página de inicio no carga correctamente cuando se utiliza el navegador X.",
    )

    issue2 = board.create_issue(
        email="user2@example.com",
        title="Problema de autenticación",
        description="Los usuarios no pueden iniciar sesión después de la última actualización.",
        status="In_Progress",
    )

    issue3 = board.create_issue(
        email="user3@example.com",
        title="Optimización de base de datos",
        description="Se requiere optimizar las consultas SQL en la base de datos para mejorar el rendimiento.",
        status="Closed",
    )

    issue4 = board.create_issue(
        email="user4@example.com",
        title="Actualización del sistema de pagos",
        description="El sistema de pagos necesita una actualización para cumplir con las nuevas normativas.",
        status="Open",
    )

    user1 = auth.create_user(
        email="manulc@hotmail",
        alias="manulc",
        password="manulc",
        system_admin=False,
        activo=True,
    )

    user2 = auth.create_user(
        email="manulc2@hotmail",
        alias="manulc2",
        password="manulc2",
        system_admin=True,
        activo=True,
    )

    board.assign_user(issue1, user1)
    board.assign_user(issue2, user2)

    label1 = board.create_label(
        title="urgente",
        description="isda irge 24hs",
    )

    label2 = board.create_label(
        title="Soporte",
        description="is 19hs how",
    )

    rol_tecnica = auth.create_roles(
        nombre="Tecnica",
    )

    rol_encuestre = auth.create_roles(
        nombre="Encuestre",
    )

    rol_voluntariado = auth.create_roles(
        nombre="Voluntariado",
    )

    rol_administracion = auth.create_roles(
        nombre="Administracion",
    )

    auth.assign_rol(user1, [rol_administracion, rol_voluntariado])
    auth.assign_rol(
        user2, [rol_administracion, rol_voluntariado, rol_tecnica, rol_encuestre]
    )
    board.assign_labels(issue1, [label1])
    board.assign_labels(issue2, [label1, label2])

    # Profesiones
    equipo.add_profesion(nombre="Psicologo/a")
    equipo.add_profesion(nombre="Psicomotricista")
    equipo.add_profesion(nombre="Medico/a")
    equipo.add_profesion(nombre="Kinesiologo/a")
    equipo.add_profesion(nombre="Terapista Ocupacional")
    equipo.add_profesion(nombre="Psicopedagogo/a")
    equipo.add_profesion(nombre="Docente")
    equipo.add_profesion(nombre="Profesor/a")
    equipo.add_profesion(nombre="Fonoaudiólogo/a")
    equipo.add_profesion(nombre="Veterinario")
    equipo.add_profesion(nombre="Otro")

    # Puestos laborales
    equipo.add_puesto_laboral(nombre="Administrativo/a")
    equipo.add_puesto_laboral(nombre="Terapeuta")
    equipo.add_puesto_laboral(nombre="Conductor")
    equipo.add_puesto_laboral(nombre="Auxiliar de pista")
    equipo.add_puesto_laboral(nombre=" Herrero")
    equipo.add_puesto_laboral(nombre="Entrenador de Caballos")
    equipo.add_puesto_laboral(nombre="Domador")
    equipo.add_puesto_laboral(nombre="Profesor de Equitación")
    equipo.add_puesto_laboral(nombre="Docente de Capacitación")
    equipo.add_puesto_laboral(nombre="Auxiliar de mantenimiento")
    equipo.add_puesto_laboral(nombre="Otro")
    
    
    # Provincias
    
    ejecutar_sql_script('src\core\sql\insert_provincias.sql')
    # Localidades
    ejecutar_sql_script('src\core\sql\insert_localidades.sql')
    
    
    
