from datetime import datetime
from src.core import board
from src.core import auth
from src.core import jya
from src.core import equipo
from src.core.equipo.extra_models import Provincia, Domicilio
from src.core.equipo.models import CondicionEnum
from src.core.auth import Permisos
from src.core.jya.models import PensionEnum, DiagnosticoEnum, TiposDiscapacidadEnum, AsignacionEnum
from datetime import datetime
from pathlib import Path
from src.core.database import db
from sqlalchemy import text
from src.core.jya import legajo
from src.core.jya.legajo.models import TipoDocumentoEnum


def ejecutar_sql_script(file_path):
    with open(file_path, "r", encoding="utf-8") as sql_file:
        sql_script = sql_file.read()

    with db.engine.connect() as connection:
        connection.execute(text(sql_script))
        connection.commit()

from src.core import equipo
from src.core import auth
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

    # Roles
    rol_tecnica = auth.create_roles(
        nombre="Tecnica",
    )

    rol_ecuestre = auth.create_roles(
        nombre="ecuestre",
    )

    rol_voluntariado = auth.create_roles(
        nombre="Voluntariado",
    )

    rol_administracion = auth.create_roles(
        nombre="Administracion",
    )

    
    rol_system_admin = auth.create_roles(
        nombre="System Admin",
    )

    auth.assign_rol(user1, [rol_administracion, rol_voluntariado])
    auth.assign_rol(
        user2, [rol_administracion, rol_voluntariado, rol_tecnica, rol_ecuestre]
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
    ejecutar_sql_script(sql_provincias)

    # Localidades
    sql_localidades = Path(__file__).parent.joinpath("./sql/insert_localidades.sql")
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

    # Tema permisos y roles (esto debe quedar definido. No se borra.)
    # Permisos
    # Modulo 2
    user_index = auth.create_permisos(nombre="user_index")
    user_new = auth.create_permisos(nombre="user_new")
    user_destroy =  auth.create_permisos(nombre="user_destroy")
    user_update = auth.create_permisos(nombre="user_update")
    user_show = auth.create_permisos(nombre="user_show")

    # Modulo 4
    empleado_index = auth.create_permisos(nombre="empleado_index")
    empleado_show =  auth.create_permisos(nombre="empleado_show")
    empleado_update =  auth.create_permisos(nombre="empleado_update")
    empleado_create =   auth.create_permisos(nombre="empleado_create")
    empleado_destroy =   auth.create_permisos(nombre="empleado_destroy")

    # Modulo 5
    pago_index =  auth.create_permisos(nombre="pago_index")
    pago_show =   auth.create_permisos(nombre="pago_show")
    pago_update = auth.create_permisos(nombre="pago_update")
    pago_create = auth.create_permisos(nombre="pago_create")
    pago_destroy = auth.create_permisos(nombre="pago_destroy")

    # Modulo 6
    jya_index =  auth.create_permisos(nombre="jya_index")
    jya_show =    auth.create_permisos(nombre="jya_show")
    jya_update =  auth.create_permisos(nombre="jya_update")
    jya_create =    auth.create_permisos(nombre="jya_create")
    jya_destroy =     auth.create_permisos(nombre="jya_destroy")


    # Modulo 7
    cobro_index =   auth.create_permisos(nombre="cobro_index")
    cobro_show =  auth.create_permisos(nombre="cobro_show")
    cobro_update =  auth.create_permisos(nombre="cobro_update")
    cobro_create =   auth.create_permisos(nombre="cobro_create")
    cobro_destroy =    auth.create_permisos(nombre="cobro_destroy")


    # Modulo 8
    ecuestre_index =  auth.create_permisos(nombre="ecuestre_index")
    ecuestre_show = auth.create_permisos(nombre="ecuestre_show")
    ecuestre_update = auth.create_permisos(nombre="ecuestre_update")
    ecuestre_create = auth.create_permisos(nombre="ecuestre_create")
    ecuestre_destroy = auth.create_permisos(nombre="ecuestre_destroy")



    # Asignacion a roles
    # rol sys_admin
    for permiso in Permisos.query.all():
        auth.assign_permiso(rol_system_admin, permiso)
        
    # rol administracion
    auth.assign_permiso(rol_administracion, empleado_index)
    auth.assign_permiso(rol_administracion, empleado_show)
    auth.assign_permiso(rol_administracion, empleado_update)
    auth.assign_permiso(rol_administracion, empleado_create )
    auth.assign_permiso(rol_administracion, empleado_destroy)

    auth.assign_permiso(rol_administracion, pago_index )
    auth.assign_permiso(rol_administracion, pago_show )
    auth.assign_permiso(rol_administracion, pago_update )
    auth.assign_permiso(rol_administracion, pago_create )
    auth.assign_permiso(rol_administracion, pago_destroy )

    auth.assign_permiso(rol_administracion, jya_index)
    auth.assign_permiso(rol_administracion, jya_update)
    auth.assign_permiso(rol_administracion, jya_show)
    auth.assign_permiso(rol_administracion, jya_create)
    auth.assign_permiso(rol_administracion, jya_destroy)

    auth.assign_permiso(rol_administracion, cobro_index)
    auth.assign_permiso(rol_administracion, cobro_show)
    auth.assign_permiso(rol_administracion, cobro_create)
    auth.assign_permiso(rol_administracion, cobro_update)
    auth.assign_permiso(rol_administracion, cobro_destroy)

    auth.assign_permiso(rol_administracion, ecuestre_index)
    auth.assign_permiso(rol_administracion, ecuestre_show)

    
    # rol tecnica
    auth.assign_permiso(rol_tecnica,jya_index)
    auth.assign_permiso(rol_tecnica,jya_update)
    auth.assign_permiso(rol_tecnica,jya_show)
    auth.assign_permiso(rol_tecnica,jya_create)
    auth.assign_permiso(rol_tecnica,jya_destroy)
    
    auth.assign_permiso(rol_tecnica, cobro_index)
    auth.assign_permiso(rol_tecnica, cobro_show)


    auth.assign_permiso(rol_tecnica, ecuestre_index)
    auth.assign_permiso(rol_tecnica, ecuestre_show)


    # rol voluntariado
    auth.assign_permiso(rol_voluntariado,jya_index )
    auth.assign_permiso(rol_voluntariado, jya_show)


    # rol ecuestre
    auth.assign_permiso(rol_ecuestre, ecuestre_index)
    auth.assign_permiso(rol_ecuestre, ecuestre_show)
    auth.assign_permiso(rol_ecuestre, ecuestre_update)
    auth.assign_permiso(rol_ecuestre, ecuestre_create)
    auth.assign_permiso(rol_ecuestre, ecuestre_destroy)
    direccion_1 = jya.add_direccion(
        calle="Olazabal",
        numero=4321,
        localidad_id=9,
        provincia_id=4,
    )
    
    direccion_2 = jya.add_direccion(
        calle="Diagonal 73",
        numero=1234,
        localidad_id=5,
        provincia_id=5,
    )
        
    jya.create_jinete(
        nombre="Martin",
        apellido="Diaz",
        dni="12345678",
        edad=10,
        fecha_nacimiento=datetime(2020, 5, 1),
        localidad_nacimiento_id=1,
        provincia_nacimiento_id=1,
        domicilio_id=1,
        telefono="12345654321",
        contacto_emergencia=contacto_emergencia_ej1,
        becado=True,
        observaciones_becado="Esto es el plan.",
        certificado_discapacidad=False,
        pension=PensionEnum.provincial,
        diagnostico=DiagnosticoEnum.otro,
        tipos_discapacidad=["mental","motora"],
        asignacion_familiar=False,
        tipo_asignacion=AsignacionEnum.por_discapacidad,
        obra_social="OSDE",
        nro_afiliado=123456,
        curatela=False,
        observaciones_curatela="Hace 1 mes.",
        nombre_institucion = "Anexa",
        direccion_id =1,
        telefono_institucion = "1234567890",
        grado = "2024",
        observaciones_institucion = "Nada.",
        profesionales = "Psicologa y maestra",
    )
    
    jya.create_jinete(
        nombre="Carlos",
        apellido="Lopez",
        dni="987654321",
        edad=10,
        fecha_nacimiento=datetime(2020, 5, 1),
        domicilio_id=3,
        localidad_nacimiento_id=2,
        provincia_nacimiento_id=2,
        telefono="12345654321",
        contacto_emergencia=contacto_emergencia_ej2,
        becado=True,
        observaciones_becado="Esto es el plan.",
        certificado_discapacidad=True,
        pension=PensionEnum.nacional,
        diagnostico=DiagnosticoEnum.ecne,
        tipos_discapacidad=["mental","sensorial"],
        asignacion_familiar=True,
        tipo_asignacion=AsignacionEnum.por_hijo,
        obra_social="IOMA",
        nro_afiliado=112233,
        curatela=True,
        observaciones_curatela="Ninguna.",
        nombre_institucion = "Liceo Victor Mercante",
        direccion_id = 2,
        telefono_institucion = "0987654321",
        grado = "2020",
        observaciones_institucion = "ASDF.",
        profesionales = "Terapeuta y docente",
    )
    
    legajo.create_documento(
        titulo="Curriculum Vitae",
        tipo=TipoDocumentoEnum.evaluacion,
        jinete_id=1,
    )