from datetime import datetime
from src.core import board
from src.core import auth
from src.core import jya
from src.core import equipo
from src.core import cobros
from src.core import contacto
from src.core.equipo.extra_models import Provincia,Localidad, Domicilio
from src.core.equipo.models import CondicionEnum
from src.core import pagos
from src.core.cobros.models import RegistroCobro
from src.core.jya.models import PensionEnum, DiagnosticoEnum, AsignacionEnum, DiasEnum, SedeEnum, TrabajoEnum, TiposDiscapacidadEnum, EscolaridadEnum
from datetime import datetime

from src.core.auth import Permisos
from datetime import datetime
from pathlib import Path


from src.core.database import db
from sqlalchemy import text
from src.core.jya.models import TipoDocumentoEnum

from src.core import ecuestre
from src.core.auth import Roles


from src.core import equipo
from src.core import auth
from src.core.equipo.extra_models import Provincia 

from src.core.database import db
from sqlalchemy import text

def ejecutar_sql_script(file_path):
    with open(file_path, "r", encoding="utf-8") as sql_file:
        sql_script = sql_file.read()

    with db.engine.connect() as connection:
        connection.execute(text(sql_script))
        connection.commit()

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

    user3 = auth.create_user(
        email="tecnica@hotmail",
        alias="tecnica",
        password="tecnica",
        system_admin=False,
        activo=True,
    )

    user4 = auth.create_user(
        email="voluntariado@hotmail",
        alias="voluntariado",
        password="voluntariado",
        system_admin=False,
        activo=True,
    )

    user5 = auth.create_user(
        email="ecuestre@hotmail",
        alias="ecuestre",
        password="ecuestre",
        system_admin=False,
        activo=True,
    )

    user6 = auth.create_user(
        email="admin@hotmail",
        alias="admin",
        password="admin",
        system_admin=True,
        activo=True,
    )

    board.assign_user(issue1, user1)
    board.assign_user(issue2, user2)
    board.assign_user(issue1, user3)
    board.assign_user(issue1, user4)
    board.assign_user(issue1, user5)
    board.assign_user(issue1, user6)

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

    

    auth.assign_rol(user1, [rol_administracion, rol_voluntariado])
    auth.assign_rol(
        user2, [rol_administracion, rol_voluntariado, rol_tecnica, rol_ecuestre]
    )
    auth.assign_rol(user3, [rol_tecnica])
    auth.assign_rol(user4, [rol_voluntariado])
    auth.assign_rol(user5, [rol_ecuestre])
    auth.assign_rol(user6, [rol_administracion])

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
    
    domicilio_ej4 = equipo.add_domiclio(
        calle="Diagonal 73",
        numero=1214,
        departamento="A",
        piso=5,
        localidad_id=232,
        provincia_id=2,
    )
        
    domicilio_ej5 = equipo.add_domiclio(
        calle="San Martin",
        numero=452,
        piso=1,
        localidad_id=101,
        provincia_id=8,
    )
        
    domicilio_ej6 = equipo.add_domiclio(
        calle="Belgrano",
        numero=23,
        departamento="C",
        localidad_id=531,
        provincia_id=18,
    )
    
    domicilio_ej7 = equipo.add_domiclio(
        calle="Av. 1",
        numero=12,
        departamento="E",
        piso=4,
        localidad_id=123,
        provincia_id=12,
    )

    # Contactos de Emergencia
    contacto_emergencia_ej1 = equipo.add_contacto_emergencia(
        nombre="Juan", apellido="Perez", telefono="2216546782"
    )

    contacto_emergencia_ej2 = equipo.add_contacto_emergencia(
        nombre="Pedro", apellido="Lopez", telefono="01112943232"
    )

    contacto_emergencia_ej3 = equipo.add_contacto_emergencia(
        nombre="Diego", apellido="Diaz", telefono="0542234545"
    )
    
    

    empleado1 = equipo.create_empleado(
        nombre="Ernesto",
        apellido="Gamboa",
        dni="25125945",
        email="ernesto.gamoa@gmail.com",
        telefono="549221692358",
        fecha_inicio=datetime(2020, 5, 1),
        fecha_cese=None,
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True,
        obra_social="OSDE",
        nro_afiliado=39463,
        profesion_id=1,
        puesto_laboral_id=2,
        domicilio=domicilio_ej1,
        contacto_emergencia=contacto_emergencia_ej1
    )

    empleado2 = equipo.create_empleado(
        nombre="María",
        apellido="Gómez",
        dni="32859360",
        email="maria.gomez@hotmail.com",
        telefono="01139876543",
        fecha_inicio=datetime(2019, 3, 15),
        fecha_cese=datetime(2024, 3, 15),
        condicion=CondicionEnum.PERSONAL_RENTADO,
        activo=True,
        obra_social="Swiss Medical",
        nro_afiliado=59842,
        profesion_id=2,
        puesto_laboral_id=3,
        domicilio=domicilio_ej2,
        contacto_emergencia=contacto_emergencia_ej2,
    )

    empleado3 = equipo.create_empleado(
        nombre="Carlos",
        apellido="López",
        dni="40294658",
        email="carlos.lopez@yahoo.com",
        telefono="1156784321",
        fecha_inicio=datetime(2021, 7, 22),
        fecha_cese=None,
        condicion=CondicionEnum.PERSONAL_RENTADO,
        activo=True,
        obra_social="PAMI",
        nro_afiliado=30284,
        profesion_id=3,
        puesto_laboral_id=7,
        domicilio=domicilio_ej3,
        contacto_emergencia=contacto_emergencia_ej3,
    )

    empleado4 = equipo.create_empleado(
        nombre="Ana",
        apellido="Martínez",
        dni="23456789012",
        email="ana.martinez@example.com",
        telefono="025419313",
        fecha_inicio=datetime(2018, 9, 30),
        fecha_cese=None,
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True,
        obra_social="OSDE",
        nro_afiliado=789654,
        profesion_id=4,
        puesto_laboral_id=5,
        domicilio_id=4,
        contacto_emergencia_id=1,
    )

    empleado5 = equipo.create_empleado(
        nombre="Lucía",
        apellido="Fernández",
        dni="34567890123",
        email="lucia.fernandez@gmail.com",
        telefono="1167895432",
        fecha_inicio=datetime(2022, 1, 10),
        condicion=CondicionEnum.PERSONAL_RENTADO,
        activo=True,
        obra_social="Galeno",
        nro_afiliado=979871,
        profesion_id=5,
        puesto_laboral_id=4,
        domicilio_id=1,
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
        {
            "beneficiario": "Ana Martínez",
            "monto": 1500.0,
            "fecha_pago": datetime(2024, 10, 23),
            "tipo_pago": "Gastos_varios",
            "descripcion": "Pagos varios",
        },
    ]

    pagos.guardar_pagos_seeds(pagos_datos)


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
    
    jya.add_direccion(
        calle="Olazabal",
        numero=3241,
        localidad_id=9,
        provincia_id=4,
    )
    
    jya.add_direccion(
        calle="Diagonal 77",
        numero=957,
        localidad_id=5,
        provincia_id=5,
    )
    sede1 = ecuestre.create_sede(
        nombre = "CASJ",
    )
    sede2 = ecuestre.create_sede(
        nombre = "HLP",
    )
    sede3 = ecuestre.create_sede(
        nombre = "OTRO",
    )
    
    caballo1 = ecuestre.create_ecuestre(
        nombre="Relámpago",
        fecha_nacimiento="2015-04-10",
        sexo=True,
        raza="Pura Sangre",
        pelaje="Negro",
        fecha_ingreso="2020-06-15",
        sede_id=3,
        tipoJyA ="MONTA_TERAPEUTICA"  # Asignando un tipo
    )

    caballo2 = ecuestre.create_ecuestre(
        nombre="Luna",
        fecha_nacimiento="2017-09-25",
        sexo=False,
        raza="Andaluz",
        pelaje="Blanco",
        fecha_ingreso="2021-03-10",
        sede_id=2,
        tipoJyA ="HIPOTERAPIA"  # Asignando un tipo
    )
    
    jya.create_jinete(
        nombre="Martin",
        apellido="Diaz",
        dni="37549102",
        edad=28,
        fecha_nacimiento=datetime(1996, 12, 1),
        localidad_nacimiento_id=1,
        provincia_nacimiento_id=10,
        domicilio_id=6,
        telefono="54911495620",
        contacto_emergencia=contacto_emergencia_ej1,
        becado=True,
        observaciones_becado="Becado desde el 28-04-2023.",
        certificado_discapacidad=False,
        beneficiario_pension=False,
        diagnostico=DiagnosticoEnum.otro,
        otro="escoliosis grave",
        asignacion_familiar=False,
        tipo_asignacion=AsignacionEnum.por_discapacidad,
        obra_social="OSDE",
        nro_afiliado=30576,
        curatela=False,
        observaciones_curatela="Hace 1 mes.",
        nombre_institucion = "Anexa",
        direccion_id=1,
        telefono_institucion = "4660228",
        grado = 2024,
        profesionales = "Psicologo y maestro",
        trabajo_institucional=TrabajoEnum.deporte,
        condicion=False,
        sede=SedeEnum.casj,
        profesor_o_terapeuta=empleado1,
        conductor_caballo=empleado2,
        auxiliar_pista=empleado3,
        caballo=caballo1,
    )
    

        
    jya.create_jinete(
        nombre="Carlos",
        apellido="Lopez",
        dni="987654321",
        edad=10,
        fecha_nacimiento=datetime(2020, 5, 1),
        domicilio_id=3,
        #nacimiento=nacimiento_2,
        localidad_nacimiento_id=1,
        provincia_nacimiento_id=1,
        telefono="12345654321",
        contacto_emergencia=contacto_emergencia_ej2,
        becado=True,
        observaciones_becado="Esto es el plan.",
        certificado_discapacidad=True,
        beneficiario_pension=True,
        pension=PensionEnum.nacional,
        diagnostico=DiagnosticoEnum.ecne,
        #tipos_discapacidad=[TiposDiscapacidadEnum.mental,TiposDiscapacidadEnum.motora],
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
        trabajo_institucional=TrabajoEnum.hipoterapia,
        condicion=True,
        sede=SedeEnum.hlp,
        profesor_o_terapeuta=empleado3,
        conductor_caballo=empleado5,
        auxiliar_pista=empleado4,
        caballo=caballo2,
    )
    
    jya.add_familiar( 
        parentesco_familiar="Tio",
        nombre_familiar="Juan",
        apellido_familiar="Diaz",
        dni_familiar="3498452",
        domicilio_familiar_id=3,
        celular_familiar="23446753",
        email_familiar="juan@diaz.com",
        nivel_escolaridad_familiar=EscolaridadEnum.primario,
        actividad_ocupacion_familiar="Empleado comercial"
    )

    jya.associate_jinete_familiar(1, 1)

    jya.add_familiar( 
        parentesco_familiar="Abuela",
        nombre_familiar="Alejandra",
        apellido_familiar="Gutierrez",
        dni_familiar="15203531",
        domicilio_familiar_id=5,
        celular_familiar="23446753",
        email_familiar="alegutierrez@gmail.com",
        nivel_escolaridad_familiar=EscolaridadEnum.universitario,
        actividad_ocupacion_familiar="Ingeniera"
    )

    jya.associate_jinete_familiar(2, 2)
    
    jya.add_dias(dias=DiasEnum.lunes)
    jya.add_dias(dias=DiasEnum.martes)
    jya.add_dias(dias=DiasEnum.miercoles)
    jya.add_dias(dias=DiasEnum.jueves)
    jya.add_dias(dias=DiasEnum.viernes)
    jya.add_dias(dias=DiasEnum.sabado)
    jya.add_dias(dias=DiasEnum.domingo)
    
    
    jya.associate_jinete_dias(1, 1)
    
    
    jya.associate_jinete_dias(1, 2)
    
    jya.add_discapacidades(tipos_discapacidad=TiposDiscapacidadEnum.mental)
    jya.add_discapacidades(tipos_discapacidad=TiposDiscapacidadEnum.motora)
    jya.add_discapacidades(tipos_discapacidad=TiposDiscapacidadEnum.sensorial)
    jya.add_discapacidades(tipos_discapacidad=TiposDiscapacidadEnum.visceral)
    
    
    jya.associate_jinete_discapacidad_id(1, 1)
    
    jya.add_discapacidades(
        tipos_discapacidad=TiposDiscapacidadEnum.sensorial,
    )
    
    jya.associate_jinete_discapacidad_id(1, 2)

    '''# Modulo ecuestre
    sede1 = ecuestre.create_sede(
        nombre = "CASJ",
    )
    sede2 = ecuestre.create_sede(
        nombre = "HLP",
    )
    sede3 = ecuestre.create_sede(
        nombre = "OTRO",
    )'''
    '''caballo1 = ecuestre.create_ecuestre(
        nombre="Relámpago",
        fecha_nacimiento="2015-04-10",
        sexo=True,
        raza="Pura Sangre",
        pelaje="Negro",
        fecha_ingreso="2020-06-15",
        sede_id=3,
        tipoJyA ="MONTA_TERAPEUTICA"  # Asignando un tipo
    )

    caballo2 = ecuestre.create_ecuestre(
        nombre="Luna",
        fecha_nacimiento="2017-09-25",
        sexo=False,
        raza="Andaluz",
        pelaje="Blanco",
        fecha_ingreso="2021-03-10",
        sede_id=2,
        tipoJyA ="HIPOTERAPIA"  # Asignando un tipo
    )'''

    caballo3 = ecuestre.create_ecuestre(
        nombre="Tormenta",
        fecha_nacimiento="2016-11-14",
        sexo=True,
        raza="Árabe",
        pelaje="Gris",
        fecha_ingreso="2021-07-20",
        sede_id=1,
        tipoJyA ="DEPORTE_EQUESTRE" # Asignando un tipo
    )

    caballo4 = ecuestre.create_ecuestre(
        nombre="Estrella",
        fecha_nacimiento="2018-05-30",
        sexo=False,
        raza="Cuarto de Milla",
        pelaje="Castaño",
        fecha_ingreso="2022-01-05",
        sede_id=1,
        tipoJyA ="ACTIVIDADES_RECREATIVAS"  # Asignando un tipo
    )

    caballo5 = ecuestre.create_ecuestre(
        nombre="Sombra",
        fecha_nacimiento="2014-02-18",
        sexo=True,
        raza="Frisón",
        pelaje="Negro",
        fecha_ingreso="2019-11-11",
        sede_id=2,
        tipoJyA ="EQUITACION"  # Asignando un tipo
    )

    caballo6 = ecuestre.create_ecuestre(
        nombre="Brisa",
        fecha_nacimiento="2019-08-21",
        sexo=False,
        raza="Mustang",
        pelaje="Palomino",
        fecha_ingreso="2022-09-09",
        sede_id=1,
        tipoJyA ="MONTA_TERAPEUTICA"  # Asignando un tipo
    )

    caballo7 = ecuestre.create_ecuestre(
        nombre="Fénix",
        fecha_nacimiento="2015-12-02",
        sexo=True,
        raza="Criollo",
        pelaje="Bayo",
        fecha_ingreso="2021-04-22",
        sede_id=3,
        tipoJyA ="HIPOTERAPIA"  # Asignando un tipo
    )

    caballo8 = ecuestre.create_ecuestre(
        nombre="Aurora",
        fecha_nacimiento="2017-03-11",
        sexo=False,
        raza="Lusitano",
        pelaje="Alazán",
        fecha_ingreso="2021-10-15",
        sede_id=2,
        tipoJyA ="ACTIVIDADES_RECREATIVAS"  # Asignando un tipo
    )

    caballo9 = ecuestre.create_ecuestre(
        nombre="Centella",
        fecha_nacimiento="2016-07-19",
        sexo=True,
        raza="Hannoveriano",
        pelaje="Castaño Oscuro",
        fecha_ingreso="2020-08-01",
        sede_id=3,
        tipoJyA ="DEPORTE_EQUESTRE"  # Asignando un tipo
    )

    caballo10 = ecuestre.create_ecuestre(
        nombre="Nube",
        fecha_nacimiento="2018-10-05",
        sexo=False,
        raza="Percherón",
        pelaje="Gris Claro",
        fecha_ingreso="2022-03-30",
        sede_id=1,
        tipoJyA ="EQUITACION"  # Asignando un tipo
    )


    ecuestre.asignar_empleado(caballo1, [empleado1,empleado2])
    ecuestre.asignar_empleado(caballo2, [empleado3,empleado1]) 
    ecuestre.asignar_empleado(caballo3, [empleado4,empleado2]) 
    ecuestre.asignar_empleado(caballo4, [empleado5,empleado3]) 
    ecuestre.asignar_empleado(caballo5, [empleado1,empleado5]) 
    ecuestre.asignar_empleado(caballo6, [empleado2,empleado4]) 
    ecuestre.asignar_empleado(caballo7, [empleado3,empleado2, empleado5])     
    ecuestre.asignar_empleado(caballo8, [empleado4,empleado2]) 
    ecuestre.asignar_empleado(caballo9, [empleado5,empleado2]) 
    ecuestre.asignar_empleado(caballo10, [empleado1,empleado2, empleado4]) 

    
    cobro1 = RegistroCobro(
        jinete_id=1,  
        fecha_pago=datetime(2024, 1, 15),
        medio_pago='efectivo',
        monto=1000.0,
        recibido_por=1,  
        observaciones="Primer pago del año."
    )

    cobro2 = RegistroCobro(
        jinete_id=2, 
        fecha_pago=datetime(2024, 2, 20),
        medio_pago='tarjeta_credito',
        monto=1500.0,
        recibido_por=2, 
        observaciones="Pago correspondiente a febrero."
    )

    cobro3 = RegistroCobro(
        jinete_id=1,  
        fecha_pago=datetime(2024, 3, 25),
        medio_pago='tarjeta_debito',
        monto=2000.0,
        recibido_por=1,  
        observaciones="Pago de honorarios."
    )

    cobro4 = RegistroCobro(
        jinete_id=1,  
        fecha_pago=datetime(2024, 6, 20),
        medio_pago='tarjeta_credito',
        monto=1000.0,
        recibido_por=2,  
        observaciones="Pago de Correspondiente a junio"
    )

    cobro5 = RegistroCobro(
        jinete_id=2,  
        fecha_pago=datetime(2024, 7, 27),
        medio_pago='tarjeta_credito',
        monto=3000.0,
        recibido_por=2,  
        observaciones="Pago de Correspondiente a julio"
    )

    cobros.guardar_cobros_seeds(cobro1, cobro2, cobro3, cobro4, cobro5)

    # Super_user que tiene todos los permisos. Utililizable para probar la pagina comodamente
    super_user = auth.create_user(
        email="super_user@hotmail.com",
        alias="super_user",
        password="super_user",
        system_admin=True,
        activo=True,
    )
    
    rol_system_admin = auth.create_roles(
        nombre="System Admin",
    )
    for perm in Permisos.query.all():
        auth.assign_permiso(rol_system_admin, perm)

    auth.assign_rol(super_user, [rol_system_admin])


    contacto.add_consulta( 
        nombre="Juan Diaz",
        email="juan@diaz.com",
        mensaje="Quiero averiguar precios para tener una sesion"
    )