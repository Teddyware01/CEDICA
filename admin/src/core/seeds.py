from src.core import board
from src.core import auth

from src.core import equipo
from src.core.equipo.extra_models import Provincia, Domicilio
from src.core.equipo.models import CondicionEnum
from src.core.pagos.models import Pago
from datetime import datetime
from pathlib import Path


from src.core.database import db
from sqlalchemy import text


def ejecutar_sql_script(file_path):
    with open(file_path, "r", encoding="utf-8") as sql_file:
        sql_script = sql_file.read()

    with db.engine.connect() as connection:
        connection.execute(text(sql_script))
        connection.commit()

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
    sql_provincias = Path(__file__).parent.joinpath("./sql/insert_provincias.sql")
    print("Print prueba: ", sql_provincias)
    ejecutar_sql_script(sql_provincias)

    # Localidades
    sql_localidades = Path(__file__).parent.joinpath("./sql/insert_localidades.sql")
    print("Print prueba: ", sql_localidades)
    ejecutar_sql_script(sql_localidades)


    # Empleados ejemplo (primero las tablas que deben crearse primero)
    # Domicilios
    domicilio_ej1 = equipo.add_domiclio(
        calle=15,
        numero=15,
        departamento=15,
        piso=15,
        localidad_id=15,
        provincia_id=15,
    )
    domicilio_ej2 = equipo.add_domiclio(
        calle="122",
        numero="42",
        localidad_id=111,
        provincia_id=1,
    )

    domicilio_ej3 = equipo.add_domiclio(
        calle="Flores",
        numero=124,
        departamento=15,
        piso=15,
        localidad_id=15,
        provincia_id=12,
    )

    # Contactos de Emergencia
    contacto_emergencia_ej1 = equipo.add_contacto_emergencia(
        nombre="juan", apellido="perez", telefono="11111111111"
    )

    contacto_emergencia_ej2 = equipo.add_contacto_emergencia(
        nombre="jj", apellido="lopez", telefono="22222222222"
    )

    contacto_emergencia_ej3 = equipo.add_contacto_emergencia(
        nombre="diego", apellido="marado", telefono="33333333333"
    )

    # Empleados, efectivamente...
    equipo.create_empleado(
        nombre="Juan",
        apellido="Pérez",
        dni="12345678901",
        email="juan.perez@example.com",
        telefono="1123456789",
        fecha_inicio=datetime(2020, 5, 1),
        fecha_cese=None,
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True,
        obra_social="OSDE",
        nro_afiliado=123456,
        profesion_id=1,
        puesto_laboral_id=2,
        domicilio=domicilio_ej1,
        contacto_emergencia=contacto_emergencia_ej1,
    )

    equipo.create_empleado(
        nombre="María",
        apellido="Gómez",
        dni="10987654321",
        email="maria.gomez@example.com",
        telefono="1139876543",
        fecha_inicio=datetime(2019, 3, 15),
        fecha_cese=datetime(2024, 3, 15),
        condicion=CondicionEnum.PERSONAL_RENTADO,
        activo=True,
        obra_social="Swiss Medical",
        nro_afiliado=654321,
        profesion_id=2,
        puesto_laboral_id=3,
        domicilio=domicilio_ej2,
        contacto_emergencia=contacto_emergencia_ej2,
    )

    equipo.create_empleado(
        nombre="Carlos",
        apellido="López",
        dni="12121212121",
        email="carlos.lopez@example.com",
        telefono="1156784321",
        fecha_inicio=datetime(2021, 7, 22),
        fecha_cese=None,
        condicion=CondicionEnum.PERSONAL_RENTADO,
        activo=True,
        obra_social="PAMI",
        nro_afiliado=112233,
        profesion_id=3,
        puesto_laboral_id=7,
        domicilio=domicilio_ej3,
        contacto_emergencia=contacto_emergencia_ej3,
    )

    equipo.create_empleado(
        nombre="Ana",
        apellido="Martínez",
        dni="23456789012",
        email="ana.martinez@example.com",
        telefono="1145678932",
        fecha_inicio=datetime(2018, 9, 30),
        fecha_cese=None,
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True,
        obra_social="OSDE",
        nro_afiliado=789654,
        profesion_id=4,
        puesto_laboral_id=5,
        domicilio_id=2,
        contacto_emergencia_id=1,
    )

    equipo.create_empleado(
        nombre="Lucía",
        apellido="Fernández",
        dni="34567890123",
        email="lucia.fernandez@example.com",
        telefono="1167895432",
        fecha_inicio=datetime(2022, 1, 10),
        condicion=CondicionEnum.PERSONAL_RENTADO,
        activo=True,
        obra_social="Galeno",
        nro_afiliado=998877,
        profesion_id=5,
        puesto_laboral_id=4,
        domicilio_id=3,
        contacto_emergencia_id=2,
    )

    pagos_datos = [
        {
            "beneficiario": "Juan Pérez",
            "monto": 1000.0,
            "fecha_pago": datetime(2024, 10, 1),
            "tipo_pago": "Honorario",
            "descripcion": "Pago por servicio de asesoría",
        },
        {
            "beneficiario": "María Gómez",
            "monto": 1500.0,
            "fecha_pago": datetime(2024, 10, 5),
            "tipo_pago": "Gastos_varios",
            "descripcion": "Pago por compra de insumos",
        },
        {
            "beneficiario": "Carlos López",
            "monto": 2000.0,
            "fecha_pago": datetime(2024, 10, 10),
            "tipo_pago": "Gastos_varios",
            "descripcion": "Pago por servicios de mantenimiento",
        },
    ]

    for pago in pagos_datos:
        nuevo_pago = Pago(
            beneficiario=pago["beneficiario"],
            monto=pago["monto"],
            fecha_pago=pago["fecha_pago"],
            tipo_pago=pago["tipo_pago"],
            descripcion=pago["descripcion"],
        )
        db.session.add(nuevo_pago)  # Agregar el pago a la sesión
    db.session.commit()  # Confirmar todos los cambios en la base de datos
