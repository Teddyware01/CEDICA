import psycopg2

try:
    connection = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432",
        database="grupo15"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Conectado a: {db_version}")
except Exception as error:
    print(f"Error conectando a la base de datos: {error}")
finally:
    if connection:
        cursor.close()
        connection.close()
