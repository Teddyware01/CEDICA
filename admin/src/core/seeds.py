from src.core import board
from src.core import auth


def run():
    issue1 = board.create_issue(
        email = "user1@example.com",
        title = "Error en la página de inicio",
        description = "La página de inicio no carga correctamente cuando se utiliza el navegador X.",
    )
    
    issue2 = board.create_issue(
        email = "user2@example.com",
        title = "Problema de autenticación",
        description = "Los usuarios no pueden iniciar sesión después de la última actualización.",
        status = "In_Progress",
    )


    issue3 = board.create_issue(
        email = "user3@example.com",
        title = "Optimización de base de datos",
        description = "Se requiere optimizar las consultas SQL en la base de datos para mejorar el rendimiento.",
        status = "Closed",

    )

    issue4 = board.create_issue(
        email = "user4@example.com",
        title = "Actualización del sistema de pagos",
        description = "El sistema de pagos necesita una actualización para cumplir con las nuevas normativas.",
        status = "Open",
    )

    user1 = auth.create_user(
        email = "manulc@hotmail",
        alias = "manulc",
        password = "manulc",
        system_admin = False,
        activo = True,
    )

    user2 = auth.create_user(
        email = "manulc2@hotmail",
        alias = "manulc2",
        password = "manulc2",
        system_admin = True,
        activo = True,
    )

    

    board.assign_user(issue1, user1)
    board.assign_user(issue2, user2)
    

    label1 = board.create_label(
        title = "urgente",
        description = "isda irge 24hs",
    )
    
    label2 = board.create_label(
        title = "Soporte",
        description = "is 19hs how",
    )

    rol_tecnica = auth.create_roles(
        nombre = "Tecnica",
    )

    rol_encuestre = auth.create_roles(
        nombre = "Encuestre",
    )

    rol_voluntariado = auth.create_roles(
        nombre = "Voluntariado",
    )

    rol_administracion = auth.create_roles(
        nombre = "Administracion",
    )

    auth.assign_rol(user1, [rol_administracion, rol_voluntariado])
    auth.assign_rol(user2, [rol_administracion, rol_voluntariado, rol_tecnica, rol_encuestre])
    board.assign_labels(issue1, [label1])
    board.assign_labels(issue2, [label1,label2])
