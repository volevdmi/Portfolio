import psycopg2

from config import database, password, host, user, port

connection = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port=port
)
#cursor = connection.cursor()

