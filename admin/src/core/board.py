def list_issues():
    issues = [
        {   
            'id': 1,
            'email': 'user1@example.com',
            'title': 'Error en la página de inicio',
            'description': 'La página de inicio tarda mucho en cargar.',
            'status': 'abierto'
        },
        {
            'id': 2,
            'email': 'user2@example.com',
            'title': 'Problema con el inicio de sesión',
            'description': 'No se puede iniciar sesión con redes sociales.',
            'status': 'en progreso'
        },
        {
            'id': 3,
            'email': 'user3@example.com',
            'title': 'Bug en el formulario de contacto',
            'description': 'El botón de envío no responde al hacer clic.',
            'status': 'cerrado'
        },
        {
            'id': 4,
            'email': 'user4@example.com',
            'title': 'Fallo en la búsqueda',
            'description': 'Los resultados de búsqueda no se actualizan correctamente.',
            'status': 'abierto'
        },
        {
            'id': 5,
            'email': 'user5@example.com',
            'title': 'Problema con la visualización móvil',
            'description': 'El sitio web no se ajusta bien en dispositivos móviles.',
            'status': 'en progreso'
        },
        {
            'id': 6,
            'email': 'user6@example.com',
            'title': 'Error en el sistema de pagos',
            'description': 'Los pagos con tarjeta de crédito no se procesan.',
            'status': 'cerrado'
        }
    ]
    return issues