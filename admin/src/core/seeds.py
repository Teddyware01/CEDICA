from src.core import board

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


