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
            )  # инициализируем подклюсение к бд
            self.engine = create_engine('postgresql://postgres:kWOWtIb_@176.123.160.78/postgres')  # делаем движоk для sqlALchemy
            print("Подключение к базе данных успешно!")
        except OperationalError as err: # отлов ошибки
            print("Подключение к базе данных не удалось:", err)  # сообщение об ошибке
            self.conn = None # нет подключения
            self.engine = None # нет движка

    
    def get_work_days_doctors(self, number): # получаем рабочие дни доктора
        try:
            day = 'days_' + str(number) # формируем навзвание столбца в бд
            self.__cur = self.conn.cursor() # делаем курсо для работы с бд
            self.__cur.execute(f"SELECT name, {day}, rate FROM work_days_doc")  # выбираем данные по столбцам из бд
            res = self.__cur.fetchall() # парсим данные с запроса
            return res # возвращаем данные
        except Exception as err: # отлов ошибки
            print('error: ', err) # сообщение об ошибке
            return False # возврат лжи тк вышла ошибка
        
    def add_schedule_doc(self, doc, lst_days, doc_schedule, count):
        try:
            number_week = {
                "1": 0,
                "2": 7,
                "3": 14,
                "4": 21,
                "5": 28
            } # недели начинаются по дням
            for day_ in lst_days:  # бежим по рабочим дням
                c = number_week[f"{count}"] # номер недели
                day = 'day' + str(c + day_) # делаем название столбца в таблице
                start_time = '8:30'  # стартовое время рабочего дня
                end_time = (510 + (doc_schedule[0] * 60) + doc_schedule[1]) / 60 # вычисление конца рабочего дня
                if int(end_time * 10) % 10 != 0: # если число имеет знак после запятой
                    end_time = round(end_time) # то округляем его
                    end_time = f"{end_time}:30" # подставляем ту же дробную часть только в минутах
                    
                self.__cur = self.conn.cursor() # получение курсора
                self.__cur.execute(f"UPDATE complete_schedule SET {day} = '{start_time} - {end_time}, отдых = {doc_schedule[1]}' WHERE name = '{doc}'") # запрос н обновление данных в расписании
                self.conn.commit() # коммитим изменения
                self.__cur.close() # закрываем курсос
        except Exception as err: # отлов ошибки
            print('error: ', err)
            return False
    
    def add_work_day(self, doctor_name, rate, count, days_duty): # добавляем рабочий день
        try:
            days = 'days_' + str(count) #  получение названия столбца в бд
            self.__cur = self.conn.cursor() # получение курсора
            self.__cur.execute(f"SELECT {days} FROM work_days_doc WHERE name = '{doctor_name}'") # выбираем рабочие дни по дням
            work_days = self.__cur.fetchall() # парсим данные с запроса
            work_days = work_days[0] # получение кортежа с днями
            work_days = work_days[0] # получение дней
            self.__cur.execute(f"SELECT rate FROM work_days_doc WHERE name = '{doctor_name}'")  #  выбираем ставку врача
            rate_doc = self.__cur.fetchall() # парсим ставку с запроса
            rate_doc = rate_doc[0] # делаем корректный формат ставки
            rate_doc = rate_doc[0]# делаем корректный формат ставки
            if count == 5:# если счетчик = 5 то есть ласт неделя то у нас особые условия
                if work_days < days_duty and rate_doc == 1:# проверка условия ставки и рабочих дней
                    self.__cur.execute(f"UPDATE work_days_doc SET {days} = {days} + 1  WHERE name = '{doctor_name}' ")# обновление данных по рабочим дням
                    self.__cur.execute(f"UPDATE work_days_doc SET rate =  {rate}  WHERE name = '{doctor_name}' ")# обновление ставки
                    self.conn.commit()# коммитим условия
                    self.__cur.close()# закрываем курсос
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
            if work_days < 5 and rate_doc == 1:# проверка точности кол-ва рабочих дней
                self.__cur.execute(f"UPDATE work_days_doc SET {days} = {days} + 1  WHERE name = '{doctor_name}' ") # обновление раб дней
                self.__cur.execute(f"UPDATE work_days_doc SET rate =  {rate}  WHERE name = '{doctor_name}' ") # обновление ставки
                self.conn.commit() # коммит дней
                self.__cur.close() # закрываем курсор
                return True # подверждение успешного выполнения всего выше
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
            self.__cur.execute("SELECT name, modality, additional_modality, rate FROM doctor_schedule WHERE rate > 0") # выбор всех данных по врачам и их самих
            res = self.__cur.fetchall()
            return res
        except Exception as err:
            print(f"Ошибка: {err}")
            return False

    def get_weeks_research(self):
        try:
            self.__cur = self.conn.cursor()
            self.__cur.execute("SELECT densitometer, kt, kt_ky_1_zone,kt_ky_2_plus_zone, mmg, mrt, mrt_ky_1_zone, mrt_ky_2_plus_zone, rg, fluorography FROM monthly_research") # выбираем все исследования на месяц
            res = self.__cur.fetchall()
            return res
        except Exception as err:
            print(f"Ошибка: {err}")
            return False
        
    def add_user(self, name, email, hpsw, role):
        try:
            self.__cur = self.conn.cursor()
            self.__cur.execute(f"SELECT COUNT(*) FROM users WHERE email LIKE '{email}'") # проверка на наличие уже в системе 
            res = self.__cur.fetchone()
            if res[0] > 0:
                print("Пользователь с таким email уже существует")
                return False

            self.__cur.execute("INSERT INTO users(name, email, psw, role) VALUES(%s, %s, %s, %s)", (name, email, hpsw, role)) # вставляем нового юзера
            self.conn.commit()
            self.__cur.close()
        except Exception as err:
            print(f"Ошибка при добавлении пользователя в БД: {err}")
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cursor = self.conn.cursor()
            self.__cursor.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1") # получаем юзера по айди
            res = self.__cursor.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except Exception as err:
            print(f"Ошибка при получении данных из БД: {err}")

        return True

    def get_user_email(self, email):
        try:
            __cur = self.conn.cursor()
            __cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1") # получаем юзера где есть совпадения по емаил
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
            ) # вставка доктора в таблицу
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
            ) # удаление доктора по айди
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
            ) # добавление непредвиденных обстоятельств
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
            ) # вставка расписания для доктора
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
                    connection.execute(text("CREATE ROLE head_of_the_center_reference WITH LOGIN PASSWORD '12345';")) # создание роли админа
                    connection.execute(text("CREATE ROLE hr_worker;")) # создания роли кадрового работника
                    connection.execute(text("CREATE ROLE doctor;")) # создание роли доктора
                    print("Роли успешно созданы")

                    connection.execute(text("INSERT INTO users (name, email, psw) VALUES ('head_of_the_center_reference', 'head@center.com', '12345');")) # вставка админа
                    connection.execute(text("INSERT INTO users (name, email, psw) VALUES ('hr_worker', 'hr@worker.com', NULL);")) # вставка кадрового работника
                    connection.execute(text("INSERT INTO users (name, email, psw) VALUES ('doctor', 'doctor@hospital.com', NULL);")) # вставка доктора
                    print("Пользователи успешно созданы!")
                    
                    return True
            except Exception as err:
                print("Ошибка при создании ролей и пользователей:", err)
                return False
    
    def get_doc_schedule(self, id):
        try:
            __cur = self.conn.cursor()
            __cur.execute(f"SELECT * FROM complete_schedule WHERE id = '{id}' LIMIT 1") # выбор расписания по айди для одного доктора
            res = __cur.fetchone()
            json1_str = json.dumps(res)
            print(json1_str)
            print("Расписание успешно предоставлено!")
            return json1_str
        except Exception as err:
            print("Ошибка при получении расписания:", err)
            return False
        
    def check_employee(self, name, surname, patronymic):
        try:
            __cur = self.conn.cursor()
            __cur.execute(f"SELECT id FROM news_employee WHERE name = {name}, surname = {surname}, patronymic = {patronymic}") # проверка наличия сотрудника в системе
            res = __cur.fetchone()
            print(res)
            print("Сотрудник найден!")
            return True
        except Exception as err:
                    print("Ошибка при обнаружении сотрудника:", err)
                    return False

    def hr_worker_add_employee(self, name, surname, patronymic, change_rate, minus_employee):
        try:
            __cur = self.conn.cursor()
            __cur.execute(f"INSERT INTO news_employee(name, surname, patronymic, change_rate, minus_employee) VALUES({name, surname, patronymic, change_rate, minus_employee})") # вставка нового сотрудника
            self.conn.commit()
            self.__cur.close()
            print("Сотрудник успешно добавлен!")
            return True
        except Exception as err:
            print("Ошибка при добавлении сотрудника:", err)
            return False
        
    def hr_worker_update_employee(self, name, surname, patronymic, change_rate, minus_employee):
        try:
            __cur = self.conn.cursor()
            __cur.execute(f"INSERT INTO news_employee(name, surname, patronymic, change_rate, minus_employee) VALUES({name, surname, patronymic, change_rate, minus_employee})") # обновление данных сотрудника
            self.conn.commit()
            self.__cur.close()
            print("Сотрудник успешно добавлен!")
            return True
        except Exception as err:
            print("Ошибка при обновлении сотрудника:", err)
            return False
        
    def get_schedule(self):
        try:
            __cur = self.conn.cursor()
            __cur.execute("SELECT * FROM complete_schedule") # получение всего расписания (для админа)
            res = __cur.fetchall()
            print("Данные успешно получены!")
            return res
        except Exception as err:
            print("Ошибка при обновлении сотрудника:", err)
            return False
        
    def clear_work_days(self):
        try:
            for i in range(1, 6):
                __cur = self.conn.cursor()
                __cur.execute(f"UPDATE work_days_doc SET days_{i} = 0") # очищаем рабочие дни
                self.conn.commit()
                self.__cur.close()
            return True
        except Exception as err:
            print("Ошибка:", err)
            return False
        
    def clear_schedule(self):
        try:
            for i in range(1, 32):
                __cur = self.conn.cursor()
                __cur.execute(f"UPDATE complete_schedule SET day{i} = null") # обновляем расписание
                self.conn.commit()
                self.__cur.close()
            return True
        except Exception as err:
            print("Ошибка:", err)
            return False