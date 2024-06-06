import psycopg2
from psycopg2 import OperationalError

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="site",
                user="postgres",
                host="95.174.94.146",
                password="123",
                port="5432"
            )
            print("Подключение к базе данных успешно!")
        except OperationalError as err:
            print("Подключение к базе данных не удалось:", err)
            self.conn = None

    def getUser(self):
        try:
            self.__cursor = self.conn.cursor()
            self.__cursor.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cursor.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except Exception as err:
            print(f"Ошибка при получении данных из БД: {err}")

        return False
    def add_doctor(self, name, specialization, contact):
        # Здесь должен быть код для добавления врача в базу данных
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO doctors (name, specialization, contact_info) VALUES (%s, %s, %s)",
                (name, specialization, contact)
            )
            self.conn.commit()
            cursor.close()
            print("Врач успешно добавлен!")
            return True
        except Exception as err:
            print("Ошибка при добавлении врача:", err)
            return False
        
    def delete_doctor(self, doctor_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"DELETE FROM doctors WHERE id = {doctor_id}"
            )
            self.conn.commit()
            cursor.close()
            print("Врач успешно удалён!")
            return True
        except Exception as err:
            print("Ошибка при удалении врача:", err)
            return False

    def add_unforeseen_circumstances(self, doctor_id, type, start_date, end_date, approved):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO unforeseen_circumstances (doctor_id, type, start_date, end_date, approved) VALUES (%s, %s, %s, %s, %s)",
                (doctor_id, type, start_date, end_date, approved)
            )
            self.conn.commit()
            cursor.close()
            print("Непредвиденные обстоятельства успешно добавлены!")
            return True
        except Exception as err:
            print("Ошибка при добавлении непредвиденных обстоятельств:", err)
            return False
        
    def add_schedule(self, doctor_id, date, shift):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO schedules (doctor_id, shift_date, shift_type) VALUES (%s, %s, %s)",
                (doctor_id, date, shift)
            )
            self.conn.commit()
            cursor.close()
            print("расписание успешно добавлено!")
            return True
        except Exception as err:
            print("Ошибка при добавлении расписания:", err)
            return False