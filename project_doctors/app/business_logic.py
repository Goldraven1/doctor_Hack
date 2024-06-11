import datetime
from models import Database

db = Database()


class plan():
    def __init__(self, week_reseach):
        self.week_reseach = week_reseach

    def get(self):
        w_r = self.week_reseach[0]
        w_r = w_r[3:]
        return w_r
        
    
week_research = db.get_week_research()

plan_ = plan(week_research)
plan__ = plan_.get()

class employee_doctor():
    def __init__(self, rate):
        self.rate = rate

    def rate_calc_without_ky(self):
        if self.rate == 1:
            doc_time_work = 8 # больше 8, но так, чтоб не больше 12 в неделю
            doc_time_chill = 60
            doc_power_hour = 181 // doc_time_work
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.75:
            doc_time_work = 6
            doc_time_chill = 30
            doc_power_hour =  181 // doc_time_work
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.5:
            doc_time_work = 4
            doc_time_chill = 30
            doc_power_hour =  181 // doc_time_work
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.25:
            doc_time_work = 2
            doc_time_chill = 15
            doc_power_hour =  181 // doc_time_work
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.1:
            doc_time_work = 2
            doc_time_chill = 15
            doc_power_hour =  155 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]


    def rate_calc_with_ky(self):
        if self.rate == 1:
            doc_time_work = 8 # больше 8, но так, чтоб не больше 12 в неделю
            doc_time_chill = 1
            doc_power_hour = 165 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.75:
            doc_time_work = 6
            doc_time_chill = 30
            doc_power_hour =  165 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.5:
            doc_time_work = 4
            doc_time_chill = 30
            doc_power_hour =  165 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.25:
            doc_time_work = 2
            doc_time_chill = 15
            doc_power_hour =  165 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.1:
            doc_time_work = 2
            doc_time_chill = 15
            doc_power_hour =  155 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]

        
    def rate_calc_with_ky_2_plus(self):
        if self.rate == 1:
            doc_time_work = 8 # больше 8, но так, чтоб не больше 12 в неделю
            doc_time_chill = 1
            doc_power_hour = 155 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.75:
            doc_time_work = 6
            doc_time_chill = 30
            doc_power_hour =  155 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.5:
            doc_time_work = 4
            doc_time_chill = 30
            doc_power_hour =  155 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.25:
            doc_time_work = 2
            doc_time_chill = 15
            doc_power_hour =  155 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.1:
            doc_time_work = 2
            doc_time_chill = 15
            doc_power_hour =  155 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]




class calculate_work_days():
    def __init__(self, doctors):
        self.doctors = doctors

    def calc(self):
        quantity_research_dens = plan__[0]
        quantity_research_kt = plan__[1]
        quantity_research_kt_ky_1 = plan__[2]
        quantity_research_kt_ky_2 = plan__[3]
        quantity_research_mmg = plan__[4]
        quantity_research_mrt = plan__[5]
        quantity_research_mrt_ky_1 = plan__[6]
        quantity_research_mrt_ky_2 = plan__[7]
        quantity_research_rg = plan__[8]
        quantity_research_flg = plan__[9]
        duty_arr = []

        while quantity_research_kt > 0:
            for i in self.doctors:
                if i[1] == 'КТ':
                    if quantity_research_kt > 0:
                        rate = i[3]
                        em = employee_doctor(rate)
                        doc_capabilities = em.rate_calc_without_ky()

                        doc_power = doc_capabilities[2] * doc_capabilities[0]
                        quantity_research_kt -= doc_power

                        doctor_name = i[0]
                        db.add_work_day(doctor_name)
                        
                        print(quantity_research_kt, "quantity_research_kt")
        while quantity_research_kt_ky_1 > 0:
            for i in self.doctors:
                if i[1] == 'КТ':
                    if quantity_research_kt_ky_1 > 0:
                        rate = i[3]
                        em = employee_doctor(rate)
                        doc_capabilities = em.rate_calc_with_ky()

                        doc_power = doc_capabilities[2] * doc_capabilities[0]
                        quantity_research_kt_ky_1 -= doc_power

                        doctor_name = i[0]
                        db.add_work_day(doctor_name)
                        print(doctor_name, 'day + doc')
                        
                        print(quantity_research_kt_ky_1, "quantity_research_kt_ky_1")

        while quantity_research_kt_ky_2 > 0:
            for i in self.doctors:
                if i[1] == 'КТ':
                    if quantity_research_kt_ky_2 > 0:
                        rate = i[3]
                        em = employee_doctor(rate)
                        doc_capabilities = em.rate_calc_with_ky_2_plus()

                        doc_power = doc_capabilities[2] * doc_capabilities[0]
                        quantity_research_kt_ky_2 -= doc_power

                        doctor_name = i[0]
                        db.add_work_day(doctor_name)
                        print(doctor_name, 'day + doc')
                        
                        print(quantity_research_kt_ky_2, "quantity_research_kt_ky_2")

        while quantity_research_mmg > 0:
            for i in self.doctors:
                if i[1] == 'ММГ':
                    if quantity_research_mmg > 0:
                        rate = i[3]
                        em = employee_doctor(rate)
                        doc_capabilities = em.rate_calc_without_ky()

                        doc_power = doc_capabilities[2] * doc_capabilities[0]
                        quantity_research_mmg -= doc_power

                        doctor_name = i[0]
                        db.add_work_day(doctor_name)
                        print(doctor_name, 'day + doc')
                        
                        print(quantity_research_mmg, "quantity_research_mmg")
                        
        while quantity_research_mrt > 0:
            for i in self.doctors:
                if i[1] == 'МРТ':
                    if quantity_research_mrt > 0:
                        rate = i[3]
                        em = employee_doctor(rate)
                        doc_capabilities = em.rate_calc_without_ky()

                        doc_power = doc_capabilities[2] * doc_capabilities[0]
                        quantity_research_mrt -= doc_power

                        doctor_name = i[0]
                        db.add_work_day(doctor_name)
                        print(doctor_name, 'day + doc')
                        
                        print(quantity_research_mrt, "quantity_research_mrt")

        while quantity_research_mrt_ky_1 > 0:
            for i in self.doctors:
                if i[1] == 'МРТ':
                    if quantity_research_mrt_ky_1 > 0:
                        rate = i[3]
                        em = employee_doctor(rate)
                        doc_capabilities = em.rate_calc_with_ky()

                        doc_power = doc_capabilities[2] * doc_capabilities[0]
                        quantity_research_mrt_ky_1 -= doc_power

                        doctor_name = i[0]
                        db.add_work_day(doctor_name)
                        print(doctor_name, 'day + doc')
                        
                        print(quantity_research_mrt_ky_1, "quantity_research_mrt_ky_1")

        while quantity_research_mrt_ky_2 > 0:
            for i in self.doctors:
                if i[1] == 'МРТ':
                    if quantity_research_mrt_ky_2 > 0:
                        rate = i[3]
                        em = employee_doctor(rate)
                        doc_capabilities = em.rate_calc_with_ky_2_plus()

                        doc_power = doc_capabilities[2] * doc_capabilities[0]
                        quantity_research_mrt_ky_2 -= doc_power

                        doctor_name = i[0]
                        db.add_work_day(doctor_name)
                        print(doctor_name, 'day + doc')
                        
                        print(quantity_research_mrt_ky_2, "quantity_research_mrt_ky_2")
                        
        
        while quantity_research_rg > 0:
            for i in self.doctors:
                if i[1] == 'РГ':
                    if quantity_research_rg > 0:
                        rate = i[3]
                        em = employee_doctor(rate)
                        doc_capabilities = em.rate_calc_without_ky()

                        doc_power = doc_capabilities[2] * doc_capabilities[0]
                        quantity_research_rg -= doc_power

                        doctor_name = i[0]
                        db.add_work_day(doctor_name)
                        print(doctor_name, 'day + doc')
                        
                        print(quantity_research_rg, "quantity_research_rg")

        while quantity_research_flg > 0:
            for i in self.doctors:
                str_extra_modality = i[2]
                if type(str_extra_modality) == str:
                    doc_extra_modality = str_extra_modality.split(',')
            
                for s in doc_extra_modality:
                    if i[1] == 'ФЛГ' or (s == ' ФЛГ'):
                        if quantity_research_flg > 0:
                            rate = i[3]
                            em = employee_doctor(rate)
                            doc_capabilities = em.rate_calc_without_ky()

                            doc_power = doc_capabilities[2] * doc_capabilities[0]
                            quantity_research_flg -= doc_power

                            doctor_name = i[0]
                            db.add_work_day(doctor_name)
                            print(doctor_name, 'day + doc')
                        
                        print(quantity_research_flg, "quantity_research_flg")
        

        while quantity_research_dens > 0:
            for i in self.doctors:
                str_extra_modality = i[2]
                if type(str_extra_modality) == str:
                    doc_extra_modality = str_extra_modality.split(',')

                for s in doc_extra_modality:
                    if (i[1] == 'Денситометрия') or (s == ' Денситометрия'):
                        print(1)
                        if quantity_research_dens > 0:
                            rate = i[3]
                            em = employee_doctor(rate)
                            doc_capabilities = em.rate_calc_without_ky()

                            doc_power = doc_capabilities[2] * doc_capabilities[0]
                            quantity_research_dens -= doc_power

                            doctor_name = i[0]
                            db.add_work_day(doctor_name)
                            print(doctor_name, 'day + doc')
                        
                            print(quantity_research_dens, "quantity_research_dens")
        

        
doctors = db.get_all_doctors()
doc_calc = calculate_work_days(doctors)
doc_calc.calc()
