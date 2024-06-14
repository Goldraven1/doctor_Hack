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
}

class plan():
    def __init__(self, weeks_research):
        self.weeks_research = weeks_research

    def get_days_duty(self):
        current_month = datetime.datetime.now().month
        current_days = days_month[f"{current_month}"]
        days_duty = current_days % 7
        return days_duty
    
    def generate_plan(self):  

        current_month = datetime.datetime.now().month
        current_days = days_month[f"{current_month}"]

        weeks = current_days // 7
        days_duty = current_days % 7

        all_doing = []    
        plan_last_week = []
        coef = (7 / 100) * days_duty

        duty = self.weeks_research[-1]
        
        for i in duty:
            data = i * coef
            data = round(data)
            plan_last_week.append(data)

        while weeks > 0:
            for i in self.weeks_research:
                if weeks <= 0:
                    break
                all_doing.append(i)
                weeks -= 1
        all_doing.append(plan_last_week)
        return all_doing



weeks_research = db.get_weeks_research()

plan_ = plan(weeks_research)
plan_month = plan_.generate_plan()

global days_duty
days_duty = plan_.get_days_duty()


class employee_doctor():
    def __init__(self, rate):
        self.rate = rate

    def rate_calc(self):
        if self.rate == 1:
            doc_time_work = 8 # больше 8, но так, чтоб не больше 12 в неделю
            doc_time_chill = 60
            return [doc_time_work, doc_time_chill]
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
        self.doctors = doctors

    def calc(self):
        
        doc_power_without_ky = {
                "kt": 21.6,
                "mrt": 23,  
                "rg": 99.9,  
                "flg": 248,
                "mmg": 108.2,
                "dens": 110
            }
        doc_power_with_ky = {
                "kt": 16, 
                "mrt": 35.5, 
                "rg": 53.98,
                "flg": 150.65,
                "mmg": 57.98,
                "dens": 68.6
            }
        doc_power_with_ky_2_plus = {
                "kt": 15.58, 
                "mrt": 12.6, 
                "rg": 46.06,
                "flg": 111.5,
                "mmg": 57.06,
                "dens": 55.2
            }
    
        count = 0 
        for pl in plan_month:
            count += 1

            quantity_research_dens = pl[0]
            quantity_research_kt = pl[1]
            quantity_research_kt_ky_1 = pl[2]
            quantity_research_kt_ky_2 = pl[3] # 100
            quantity_research_mmg = pl[4]
            quantity_research_mrt = pl[5]
            quantity_research_mrt_ky_1 = pl[6] # 100
            quantity_research_mrt_ky_2 = pl[7] # 100
            quantity_research_rg = pl[8]
            quantity_research_flg = pl[9]
            
            print(pl)
            
            while quantity_research_flg > 0:
                for i in self.doctors[::-1]:  
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'ФЛГ' or (s.replace(' ', '') == 'ФЛГ'):
                            if quantity_research_flg > 0:
                                rate = i[3]
                                doc_power = doc_power_without_ky['flg']
                                doctor_name = i[0]
                                answer = db.add_work_day(doctor_name, rate, count, days_duty)
                                if answer != 0:
                                    quantity_research_flg -= doc_power
                                    print(doctor_name, 'day + doc')
                                print(quantity_research_flg,  "quantity_research_flg")

            while quantity_research_mmg > 0:
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'ММГ' or (s.replace(' ', '') == 'ММГ'):
                            if quantity_research_mmg > 0:
                                rate = i[3]
                                
                                
                                doc_power = doc_power_without_ky['mmg']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count,days_duty)

                                if answer != 0:
                                    quantity_research_mmg -= doc_power
                                    print(doctor_name, 'day + doc')

                                print(quantity_research_mmg, "quantity_research_mmg")

            while quantity_research_rg > 0:
                for i in self.doctors[::-1]:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')

                    for s in doc_extra_modality:
                        if i[1] == 'РГ' or (s.replace(' ', '') == 'РГ'):
                            if quantity_research_rg > 0:
                                rate = i[3]
                               
                                
                                doc_power = doc_power_without_ky['rg']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_rg -= doc_power
                                    print(doctor_name, 'day + doc')

                                print(quantity_research_rg, "quantity_research_rg")

            while quantity_research_dens > 0:
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')

                    for s in doc_extra_modality:
                        if (i[1] == 'Денситометрия') or (i[1] == 'Денс') or (s.replace(' ', '') == 'Денситометрия') or (s.replace(' ', '') == 'Денс'):
                            if quantity_research_dens > 0:
                                rate = i[3]
                               
                                doc_power = doc_power_without_ky['dens']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_dens -= doc_power
                                    print(doctor_name, 'day + doc')

                                print(quantity_research_dens, "| quantity_research_dens")


            while quantity_research_mrt_ky_2 > 0:
                for i in self.doctors[::-1]:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'МРТ' or (s.replace(' ', '') == 'МРТ'):
                            if quantity_research_mrt_ky_2 > 0:
                                rate = i[3]
                                
                                
                                doc_power = doc_power_with_ky_2_plus['mrt']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)
                                if answer != 0:
                                    quantity_research_mrt_ky_2 -= doc_power
                                    print(doctor_name, 'day + doc')

                            print(quantity_research_mrt_ky_2, "quantity_research_mrt_ky_2")


            while quantity_research_kt_ky_1 > 0:
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'КТ' or (s.replace(' ', '') == 'КТ'):
                            if quantity_research_kt_ky_1 > 0:
                                rate = i[3]
                                
                                doc_power = doc_power_with_ky['kt']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_kt_ky_1 -= doc_power
                                    print(doctor_name, 'day + doc')

                                print(quantity_research_kt_ky_1, "quantity_research_kt_ky_1")

            while quantity_research_kt_ky_2 > 0:
                for i in self.doctors[::-1]:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'КТ' or (s.replace(' ', '') == 'КТ'):
                            if quantity_research_kt_ky_2 > 0:
                                rate = i[3]
                                
                                
                                doc_power = doc_power_with_ky_2_plus['kt']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_kt_ky_2 -= doc_power
                                    print(doctor_name, 'day + doc')

                                print(quantity_research_kt_ky_2, "quantity_research_kt_ky_2")

            while quantity_research_mrt > 0:
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'МРТ' or (s.replace(' ', '') == 'МРТ'):
                            if quantity_research_mrt > 0:
                                rate = i[3]
                                
                                
                                doc_power = doc_power_without_ky['mrt']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count,days_duty)

                                if answer != 0:
                                    quantity_research_mrt -= doc_power
                                    print(doctor_name, 'day + doc')

                                print(quantity_research_mrt, "quantity_research_mrt")

            while quantity_research_kt > 0:
                for i in self.doctors[::-1]:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')
                    for s in doc_extra_modality:
                        if i[1] == 'КТ' or (s.replace(' ', '')  == 'КТ'):
                            if quantity_research_kt > 0:
                                rate = i[3]
                                
                                
                                doc_power = doc_power_without_ky['kt']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_kt -= doc_power
                                    print(doctor_name, 'day + doc')

                                print(quantity_research_kt, "quantity_research_kt")

            while quantity_research_mrt_ky_1 > 0:
                for i in self.doctors:
                    str_extra_modality = i[2]
                    if type(str_extra_modality) == str:
                        doc_extra_modality = str_extra_modality.split(',')

                    for s in doc_extra_modality:
                        if i[1] == 'МРТ' or (s.replace(' ', '') == 'МРТ'):
                            if quantity_research_mrt_ky_1 > 0:
                                rate = i[3]
                                
                                
                                doc_power = doc_power_with_ky['mrt']
                                doctor_name = i[0]

                                answer = db.add_work_day(doctor_name, rate, count, days_duty)

                                if answer != 0:
                                    quantity_research_mrt_ky_1 -= doc_power
                                    print(doctor_name, 'day + doc')

                                print(quantity_research_mrt_ky_1, "quantity_research_mrt_ky_1")

        
doctors = db.get_all_doctors()

# chunk_size = len(doctors) // 3
# chunks = np.array_split(doctors, len(doctors) // chunk_size)
# f_doc = chunks[0]
# s_doc = chunks[1]
# t_doc = chunks[2]

doc_calc = calculate_work_days(doctors)
# doc_calc.calc()




class calculate_schedule():
    def __init__(self) -> None:
        pass

    def calc(self):
        for _ in range(1, 6):
            work_days_doctors = db.get_work_days_doctors(_)

            for i in work_days_doctors:
                doc = i[0]
                work_days = i[1]
                rate = i[2]
                if _ == 5:
                    lst_days = []
                    count__ = _ - 2
                    for i in range(count__):
                        lst_days.append(i)
                    work_days = 0
                while work_days > 0:
                        check = False
                        while check == False:
                            lst_days = [random.randint(1, 7) for k in range(work_days)] 
                            s = set(lst_days)
                            if len(lst_days) == len(s):
                                lst_days.sort()
                                if 2 not in lst_days and len(lst_days) == work_days:
                                    if 1 not in lst_days:
                                        check = True
                                if 7 not in lst_days and len(lst_days) == work_days:
                                    if 6 not in lst_days:
                                        check = True
                                last = 1000000000000000000000000000
                                for i in lst_days:
                                    if i - last >= 3:
                                        check = True
                                    last = i
                            else:
                                check = False
                        work_days = 0

                em = employee_doctor(rate)
                doc_schedule = em.rate_calc()
                
                db.add_schedule_doc(doc, lst_days, doc_schedule, _)
            

calc_schedule = calculate_schedule()
# calc_schedule.calc()