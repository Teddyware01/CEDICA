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
         email = "user11@example.com",
         password = "sdad123",
    )

    user2 = auth.create_user(
        email = "user22@example.com",
        password = "12313213",
    )

    user3 = auth.create_user(
        email = "user33@example.com",
        password = "123",
    )

    board.assign_user(issue1, user1)
    board.assign_user(issue2, user2)
    board.assign_user(issue3, user3)

    label1 = board.create_label(
        title = "urgente",
        description = "isda irge 24hs",
    )
    
    label2 = board.create_label(
        title = "Soporte",
        description = "is 19hs how",
    )

    board.assign_labels(issue1, [label1])
    board.assign_labels(issue2, [label1,label2])
