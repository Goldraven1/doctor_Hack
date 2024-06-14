from flask import json
import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine, text

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                host="176.123.160.78",
                password="kWOWtIb_",
                port="5432"
            )
            self.engine = create_engine('postgresql://postgres:kWOWtIb_@176.123.160.78/postgres')
            print("Подключение к базе данных успешно!")
        except OperationalError as err:
            print("Подключение к базе данных не удалось:", err)
            self.conn = None
            self.engine = None

    
    def get_work_days_doctors(self, number):
        try:
            day = 'days_' + str(number)
            self.__cur = self.conn.cursor()
            self.__cur.execute(f"SELECT name, {day}, rate FROM work_days_doc")
            res = self.__cur.fetchall()
            return res
        except Exception as err:
            print('error: ', err)
            return False
        
    def add_schedule_doc(self, doc, lst_days, doc_schedule, count):
        try:
            number_week = {
                "1": 0,
                "2": 7,
                "3": 14,
                "4": 21,
                "5": 28
            }
            for day_ in lst_days:
                c = number_week[f"{count}"]
                day = 'day' + str(c + day_)
                start_time = '8:30'
                end_time = (510 + (doc_schedule[0] * 60) + doc_schedule[1]) / 60
                if int(end_time * 10) % 10 != 0:
                    end_time = round(end_time)
                    end_time = f"{end_time}:30"
                    
                self.__cur = self.conn.cursor()
                self.__cur.execute(f"UPDATE complete_schedule SET {day} = '{start_time} - {end_time}, отдых = {doc_schedule[1]}' WHERE name = '{doc}'")
                self.conn.commit()
                self.__cur.close()
        except Exception as err:
            print('error: ', err)
            return False
    
    def add_work_day(self, doctor_name, rate, count, days_duty):
        try:
            days = 'days_' + str(count)
            self.__cur = self.conn.cursor()
            self.__cur.execute(f"SELECT {days} FROM work_days_doc WHERE name = '{doctor_name}'")
            work_days = self.__cur.fetchall()
            work_days = work_days[0]
            work_days = work_days[0]
            self.__cur.execute(f"SELECT rate FROM work_days_doc WHERE name = '{doctor_name}'")
            rate_doc = self.__cur.fetchall()
            rate_doc = rate_doc[0]
            rate_doc = rate_doc[0]
            if count == 5:
                if work_days < days_duty and rate_doc == 1:
                    self.__cur.execute(f"UPDATE work_days_doc SET {days} = {days} + 1  WHERE name = '{doctor_name}' ")
                    self.__cur.execute(f"UPDATE work_days_doc SET rate =  {rate}  WHERE name = '{doctor_name}' ")
                    self.conn.commit()
                    self.__cur.close()
                elif work_days < days_duty and rate_doc == 0.75:
                    self.__cur.execute(f"UPDATE work_days_doc SET {days} = {days} + 1  WHERE name = '{doctor_name}' ")
                    self.__cur.execute(f"UPDATE work_days_doc SET rate =  {rate}  WHERE name = '{doctor_name}' ")
                    self.conn.commit()
                    self.__cur.close()
                    return True
                elif work_days < days_duty:
                    self.__cur.execute(f"UPDATE work_days_doc SET {days} = {days} + 1  WHERE name = '{doctor_name}' ")
                    self.__cur.execute(f"UPDATE work_days_doc SET rate =  {rate}  WHERE name = '{doctor_name}' ")
                    self.conn.commit()
                    self.__cur.close()
                    return True
                else:
                    return 0
            if work_days < 5 and rate_doc == 1:
                self.__cur.execute(f"UPDATE work_days_doc SET {days} = {days} + 1  WHERE name = '{doctor_name}' ")
                self.__cur.execute(f"UPDATE work_days_doc SET rate =  {rate}  WHERE name = '{doctor_name}' ")
                self.conn.commit()
                self.__cur.close()
                return True
            elif work_days < 5 and rate_doc == 0.75:
                self.__cur.execute(f"UPDATE work_days_doc SET {days} = {days} + 1  WHERE name = '{doctor_name}' ")
                self.__cur.execute(f"UPDATE work_days_doc SET rate =  {rate}  WHERE name = '{doctor_name}' ")
                self.conn.commit()
                self.__cur.close()
                return True
            elif work_days < 5:
                self.__cur.execute(f"UPDATE work_days_doc SET {days} = {days} + 1  WHERE name = '{doctor_name}' ")
                self.__cur.execute(f"UPDATE work_days_doc SET rate =  {rate}  WHERE name = '{doctor_name}' ")
                self.conn.commit()
                self.__cur.close()
                return True
            else:
                return 0
        except Exception as err:
            print(f"Ошибка: {err}")
            return False

    def get_all_doctors(self):
        try:
            self.__cur = self.conn.cursor()
            self.__cur.execute("SELECT name, modality, additional_modality, rate FROM doctor_schedule WHERE rate > 0")
            res = self.__cur.fetchall()
            return res
        except Exception as err:
            print(f"Ошибка: {err}")
            return False

    def get_weeks_research(self):
        try:
            self.__cur = self.conn.cursor()
            self.__cur.execute("SELECT densitometer, kt, kt_ky_1_zone,kt_ky_2_plus_zone, mmg, mrt, mrt_ky_1_zone, mrt_ky_2_plus_zone, rg, fluorography FROM monthly_research")
            res = self.__cur.fetchall()
            return res
        except Exception as err:
            print(f"Ошибка: {err}")
            return False
        
    def add_user(self, name, email, hpsw):
        try:
            self.__cur = self.conn.cursor()
            self.__cur.execute(f"SELECT COUNT(*) FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res[0] > 0:
                print("Пользователь с таким email уже существует")
                return False


            self.__cur.execute("INSERT INTO users(name, email, psw) VALUES(%s, %s, %s)", (name, email, hpsw))
            self.conn.commit()
            self.__cur.close()
        except Exception as err:
            print(f"Ошибка при добавлении пользователя в  БД: {err}")
            return False
        return True

    def getUser(self, user_id):
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

    def get_user_email(self, email):
        try:
            __cur = self.conn.cursor()
            __cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = __cur.fetchone()
            if not res:
                print('пользователь не найден')
                return False
            
            return res
        except Exception as err:
            print(err)
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

    def create_role(self):
            if not self.engine:
                print("Отсутствует подключение к базе данных")
                return False
            
            try:
                with self.engine.begin() as connection:
                    connection.execute(text("CREATE ROLE head_of_the_center_reference WITH LOGIN PASSWORD '12345';"))
                    connection.execute(text("CREATE ROLE hr_worker;"))
                    connection.execute(text("CREATE ROLE doctor;"))
                    print("Роли успешно созданы")

                    connection.execute(text("INSERT INTO users (name, email, psw) VALUES ('head_of_the_center_reference', 'head@center.com', '12345');"))
                    connection.execute(text("INSERT INTO users (name, email, psw) VALUES ('hr_worker', 'hr@worker.com', NULL);"))
                    connection.execute(text("INSERT INTO users (name, email, psw) VALUES ('doctor', 'doctor@hospital.com', NULL);"))
                    print("Пользователи успешно созданы!")
                    
                    return True
            except Exception as err:
                print("Ошибка при создании ролей и пользователей:", err)
                return False
    
    def get_doc_schedule(self, id):
        try:
            __cur = self.conn.cursor()
            __cur.execute(f"SELECT * FROM complete_schedule WHERE id = '{id}' LIMIT 1")
            res = __cur.fetchone()
            json1_str = json.dumps(res)
            print(json1_str)
            print("Расписание успешно предоставлено!")
            return json1_str
        except Exception as err:
            print("Ошибка при получении расписания:", err)
            return False