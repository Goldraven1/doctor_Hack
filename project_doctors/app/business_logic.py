import datetime
import random
from models import Database

db = Database()

days_month = {
    "1": 31,
    "2": 28,
    "3": 31,
    "4": 30,
    "5": 31,
    "6": 30,
    "7": 31,
    "8": 31,
    "9": 30,
    "10": 31,
    "11": 30,
    "12": 31
}  # сколько дней в каждом месяце

class plan():
    def __init__(self, weeks_research):
        self.weeks_research = weeks_research  # стартовые данные = план недельных(всех недель) исследований

    def get_days_duty(self):
        current_month = datetime.datetime.now().month  # данный месяц
        current_days = days_month[f"{current_month}"]  # текущие дни
        days_duty = current_days % 7  # процент от недели
        return days_duty  # долг дней по последней неделе
    
    def generate_plan(self):  

        current_month = datetime.datetime.now().month  # текущий месяц
        current_days = days_month[f"{current_month}"]  # сколько всего дней

        weeks = current_days // 7  # сколько недель надо работать
        days_duty = current_days % 7  # сколько дней надо работать (в последней неделе)

        all_doing = []     #  всего сделали
        plan_last_week = []  # план последней недели
        coef = (7 / 100) * days_duty  # коэф дней по долгу

        duty = self.weeks_research[-1]  #  долг ласт недели
        
        for i in duty:  # бежим по долгу
            data = i * coef  # получение данные по коэфу
            data = round(data)  # округляем
            plan_last_week.append(data)  #  добавляем в послелнюю неделю

        while weeks > 0:  # цикл пока недель больше 0
            for i in self.weeks_research:  # бежим по недельному плану исследований
                if weeks <= 0:  # если их становится меньше или равно 0, то ломаем всё
                    break
                all_doing.append(i)  # добавляем в "всего делать"
                weeks -= 1  # минус неделя
        all_doing.append(plan_last_week) # добавление ласт недели
        return all_doing  # вернем сколько всего делать



weeks_research = db.get_weeks_research()  # получим план исследований

plan_ = plan(weeks_research)  # создание сущности класса plan и добавление аргументa всех исследований
plan_month = plan_.generate_plan()  # генерируем план на месяц

global days_duty  # делаем глобальной переменную 
days_duty = plan_.get_days_duty()  # получаем долг по ласт неделе


class employee_doctor():
    def __init__(self, rate):
        self.rate = rate # инициализируем ставку

    def rate_calc(self):
        if self.rate == 1:  # ставка = 1, выполняем код ниже и так по аналогии с остальными ставками
            doc_time_work = 8 # время работы
            doc_time_chill = 60  # время отдыха
            return [doc_time_work, doc_time_chill]  #  лист с данными о работе по данной ставке
        elif self.rate == 0.75:
            doc_time_work = 6
            doc_time_chill = 30
            return [doc_time_work, doc_time_chill]
        elif self.rate == 0.5:
            doc_time_work = 4
            doc_time_chill = 30
            return [doc_time_work, doc_time_chill]
        elif self.rate == 0.25:
            doc_time_work = 2
            doc_time_chill = 15
            return [doc_time_work, doc_time_chill]
        elif self.rate == 0.1:
            doc_time_work = 2
            doc_time_chill = 15
            return [doc_time_work, doc_time_chill]


class calculate_work_days():
    def __init__(self, doctors):
        self.doctors = doctors  # инициализируем докторов

    def calc(self):
        
        doc_power_without_ky = {
                "kt": 30.6,
                "mrt": 33,  
                "rg": 109.9,  
                "flg": 278,
                "mmg": 128.2,
                "dens": 130
            } # план выполнения докторами исследований за смену (8 часов)
        doc_power_with_ky = {
                "kt": 26, 
                "mrt": 45.5, 
                "rg": 63.98,
                "flg": 180.65,
                "mmg": 70.98,
                "dens": 78.6
            }# план выполнения докторами исследований за смену (8 часов) с КУ
        doc_power_with_ky_2_plus = {
                "kt": 25.58, 
                "mrt": 18.6, 
                "rg": 54.06,
                "flg": 121.5,
                "mmg": 67.06,
                "dens": 65.2
            } # план выполнения докторами исследований за смену (8 часов) с КУ +2
    
        count = 0  #счетчик 
        for pl in plan_month:  # бежим по плану на месяц
            count += 1  # инкремент счетчика

            # ниже идет запись каждого исследования в отдельную переменную
            quantity_research_dens = pl[0]  
            quantity_research_kt = pl[1]
            quantity_research_kt_ky_1 = pl[2]
            quantity_research_kt_ky_2 = pl[3] 
            quantity_research_mmg = pl[4]
            quantity_research_mrt = pl[5]
            quantity_research_mrt_ky_1 = pl[6] 
            quantity_research_mrt_ky_2 = pl[7] 
            quantity_research_rg = pl[8]
            quantity_research_flg = pl[9]
            
            while quantity_research_flg > 0: # выполняем всё ниже пока не закроем план по исследованиям
                for i in self.doctors[::-1]:  # бежим по докторам, перевернув их 
                    str_extra_modality = i[2] # получаем доп модальности
                    if type(str_extra_modality) == str: # проверка на тип модальностей (если их нет, то тип null)
                        doc_extra_modality = str_extra_modality.split(',') # пихаем в переменную доп модальности 
                    for s in doc_extra_modality:  #  бежим по экстра модальностям
                        if i[1] == 'ФЛГ' or (s.replace(' ', '') == 'ФЛГ'):  #  проверка основной и доп модальностей врача на совпадение с модальностью текущего исследования
                            if quantity_research_flg > 0:  # если список еще не выполнен
                                rate = i[3]  #  получение ставки

                                em = employee_doctor(rate)  # сущность работника доктора 
                                emm = em.rate_calc()  # вычисление рабочего дня
                                
                                doc_power = doc_power_without_ky['flg'] / 8 * emm[0] # сила доктора для закрытия плана
                                
                                doctor_name = i[0]  # имя доктора
                                answer = db.add_work_day(doctor_name, rate, count, days_duty) # пытаемся добавить в бд рабочий день доктора
                                if answer != 0:  # если успешно добавился день
                                    quantity_research_flg -= doc_power  # то мы наносим урон плану и он уменьшается
                     # ниже по аналогии делается та же самая работа для закрытия плана и добавления рабочих дней врачу, на основе которых потом мы высчитаем им график
                                print('doc + day')
                        print('--> next doc -->')
                print('ФЛГ')
            while quantity_research_mmg > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'ММГ' or (s.replace(' ', '') == 'ММГ'):
                            if quantity_research_mmg > 0:
                                rate = i[3]
                                
                                em = employee_doctor(rate)
                                emm = em.rate_calc()
                                
                                doc_power = doc_power_without_ky['mmg'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count,days_duty)

                                if answer != 0:
                                    quantity_research_mmg -= doc_power
                print('MMG')

            while quantity_research_rg > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors[::-1]:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')

                    for s in doc_extra_modality:
                        if i[1] == 'РГ' or (s.replace(' ', '') == 'РГ'):
                            if quantity_research_rg > 0:
                                rate = i[3]
                                em = employee_doctor(rate)
                                emm = em.rate_calc()
                                
                                doc_power = doc_power_without_ky['rg'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_rg -= doc_power
                print('RG')

            while quantity_research_dens > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')

                    for s in doc_extra_modality:
                        if (i[1] == 'Денситометрия') or (i[1] == 'Денс') or (s.replace(' ', '') == 'Денситометрия') or (s.replace(' ', '') == 'Денс'):
                            if quantity_research_dens > 0:
                                rate = i[3]
                                em = employee_doctor(rate)
                                emm = em.rate_calc()
                            
                                doc_power = doc_power_without_ky['dens'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_dens -= doc_power
                print('DENS')

            while quantity_research_mrt_ky_2 > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors[::-1]:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'МРТ' or (s.replace(' ', '') == 'МРТ'):
                            if quantity_research_mrt_ky_2 > 0:
                                rate = i[3]
                                em = employee_doctor(rate)
                                emm = em.rate_calc()
                                
                                doc_power = doc_power_with_ky_2_plus['mrt'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)
                                if answer != 0:
                                    quantity_research_mrt_ky_2 -= doc_power
                print('MRT2')

            while quantity_research_kt_ky_1 > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'КТ' or (s.replace(' ', '') == 'КТ'):
                            if quantity_research_kt_ky_1 > 0:
                                rate = i[3]
                                em = employee_doctor(rate)
                                emm = em.rate_calc()

                                doc_power = doc_power_with_ky['kt'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_kt_ky_1 -= doc_power
                print('KT1')

            while quantity_research_kt_ky_2 > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors[::-1]:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'КТ' or (s.replace(' ', '') == 'КТ'):
                            if quantity_research_kt_ky_2 > 0:
                                rate = i[3]
                                em = employee_doctor(rate)
                                emm = em.rate_calc()

                                doc_power = doc_power_with_ky_2_plus['kt'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_kt_ky_2 -= doc_power
                print('KT2')
            while quantity_research_mrt > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'МРТ' or (s.replace(' ', '') == 'МРТ'):
                            if quantity_research_mrt > 0:
                                rate = i[3]
                                em = employee_doctor(rate)     
                                emm = em.rate_calc()                           
                                
                                doc_power = doc_power_without_ky['mrt'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count,days_duty)

                                if answer != 0:
                                    quantity_research_mrt -= doc_power
                print('MRT')

            while quantity_research_kt > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors[::-1]:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'КТ' or (s.replace(' ', '')  == 'КТ'):
                            if quantity_research_kt > 0:
                                rate = i[3]
                                em = employee_doctor(rate)
                                emm = em.rate_calc()

                                doc_power = doc_power_without_ky['kt'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_kt -= doc_power
                print('KT')       

            while quantity_research_mrt_ky_1 > 0:# выполняем всё ниже пока не закроем план по исследованиям модальности
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')

                    for s in doc_extra_modality:
                        if i[1] == 'МРТ' or (s.replace(' ', '') == 'МРТ'):
                            if quantity_research_mrt_ky_1 > 0:
                                rate = i[3]
                                em = employee_doctor(rate)
                                emm = em.rate_calc()
                                
                                doc_power = doc_power_with_ky['mrt'] / 8 * emm[0]
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_mrt_ky_1 -= doc_power
                print('MMG1')     
        
doctors = db.get_all_doctors()  # получение всех докторов

doc_calc = calculate_work_days(doctors)  # сущность - расчет рабочих дней врачей

db.clear_work_days() # очищение предыдущих рабочих дней  
doc_calc.calc()  #  запуск расчета рабочий дней 


class calculate_schedule():
    def __init__(self) -> None:
        pass

    def calc(self):
        for _ in range(1, 6):  # бежим от 1 до 6
            work_days_doctors = db.get_work_days_doctors(_)  # получаем все рабочие дни

            for i in work_days_doctors: # бежим по рабочим дням
                doc = i[0]  # определяем доктора
                work_days = i[1]  # определяем его рабочие дни
                rate = i[2]  #  определяем его ставку
                lst_days = []  # определяем лист рабочих дней
                if _ == 5:  # последний шаг в цикле мы обрабатываем иначе
                    count__ = _ - 2  #  минусуем счетчик
                    for i in range(count__):  # бежим по нему
                        lst_days.append(i)  # добавляем дни
                    work_days = 0 # делаем условие, чтоб всё завершилось ниже
                while work_days > 0:  # ниже по условию реализован алгоритм подбора 2 выходных в неделю подряд
                        check = False  # чекер по стандарту = ложь
                        while check == False:  # пока он ложь делаем все, что ниже
                            lst_days = [random.randint(1, 7) for k in range(work_days)]  # формируем массив рандом чисел в диапозоне 
                            s = set(lst_days)  # делаем все уникальным
                            if len(lst_days) == len(s):  # если все уникальные символы
                                lst_days.sort()  #  то сортируем лист
                                 # ниже условия на составление недели с двумя подряд выходными
                                if 2 not in lst_days and len(lst_days) == work_days:  
                                    if 1 not in lst_days:
                                        check = True  # если 1 и 2 нет в списке то нам подходит
                                if 7 not in lst_days and len(lst_days) == work_days:
                                    if 6 not in lst_days:
                                        check = True # если 7 и 6 нет в списке то нам подходит
                                last = 1000000000000000000000000000
                                for i in lst_days:
                                    if i - last >= 3:
                                        check = True # если разрыв между числами идущими по порядку равен 2 и больше то нам подходит
                                    last = i
                            else:
                                check = False # в противном случае оставляем ложь и перебираем дальше
                        work_days = 0 # заканчиваем, если все успешно

                em = employee_doctor(rate) # создаем сущность работника
                doc_schedule = em.rate_calc() # вычисляем ставку
                
                db.add_schedule_doc(doc, lst_days, doc_schedule, _)  # добавляем расписание в бд
            

calc_schedule = calculate_schedule() # создаем сущность класс calculate_schedule 
db.clear_schedule() # очищаем прошлое расписание
calc_schedule.calc() # вычисляем новое