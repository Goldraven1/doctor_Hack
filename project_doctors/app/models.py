import psycopg2
from psycopg2 import OperationalError

try:
    conn = psycopg2.connect(
        dbname="site",
        user="postgres",
        host="95.174.94.146",
        password="123",
        port="5432"
    )
    print("Подключение к базе данных успешно!")
except OperationalError as err:
    print("Подключение к базе данных не удалось:", err)
    conn = None
