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
        
    
week_research = db.get_week_reseach()

plan_ = plan(week_research)
plan__ = plan_.get()
print(plan__)


class employee_doctor():
    def __init__(self, rate):
        self.rate = rate

    def rate_calc_without_ky(self):
        if self.rate == 1:
            doc_time_work = 8 # больше 8, но так, чтоб не больше 12 в неделю
            doc_time_chill = 60
            doc_power_hour = 181 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.75:
            doc_time_work = 6
            doc_time_chill = 30
            doc_power_hour =  181 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.5:
            doc_time_work = 4
            doc_time_chill = 30
            doc_power_hour =  181 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.25:
            doc_time_work = 2
            doc_time_chill = 15
            doc_power_hour =  181 // 8
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




class calculate_the_schedule():
    def __init__(self, doctors):
        self.doctors = doctors

    def calc(self):
        quantity_research_kt = plan__[1]
        quantity_research_kt_ky_1 = plan__[2]
        duty_arr = []
        

        for i in self.doctors :
            if i[1] == 'КТ':
                if quantity_research_kt > 0:
                    rate = i[3]
                    em = employee_doctor(rate)
                    arr = em.rate_calc_without_ky()

                    doc_power = arr[2] * arr[0]
                    quantity_research_kt -= doc_power

                    name = i[0]
                    start_time = "8:30"
                    end_time = int(start_time[0]) + arr[0]
                    end_time = f"{end_time}:30"
                    chill = arr[1]
                    schedule = f"{start_time} - {end_time} перерыв: {chill}"
                    # db.add_schedule_doc(name, schedule)
                if quantity_research_kt < 0:
                    remainder = 0
                    remainder += quantity_research_kt
                    remainder = -remainder
                    quantity_research_kt = 0

                    doc = i[0]
                    current_numb = doc[-1]
                    current_numb = int(current_numb) - 1
                    current_numb = str(current_numb)
                    doc = doc[0:6] + current_numb
                    duty_doc = {
                        "doc": doc,
                        "remainder": remainder
                    }
                    duty_arr.append(duty_doc)
                    

                if quantity_research_kt_ky_1 > 0:
                    rate = i[3]
                    em = employee_doctor(rate)
                    arr = em.rate_calc_with_ky()

                    doc_power = arr[2] * arr[0]
                    quantity_research_kt_ky_1 -= doc_power
                    
                    name = i[0]
                    start_time = "8:30"
                    end_time = int(start_time[0]) + arr[0]
                    end_time = f"{end_time} : 30"
                    chill = arr[1]
                    schedule = f"начало = {start_time} конец = {end_time} отдых = {chill}"
                    print(schedule)
                    print(quantity_research_kt_ky_1)
                    # db.add_schedule_doc(name, schedule)
                if quantity_research_kt_ky_1 < 0:
                    remainder = 0
                    remainder += quantity_research_kt_ky_1
                    remainder = -remainder
                    quantity_research_kt_ky_1 = 0

                    doc = i[0]
                    current_numb = doc[-1]
                    current_numb = int(current_numb) - 1
                    current_numb = str(current_numb)
                    doc = doc[0:6] + current_numb
                    print('this doctor', doc )

doctors = db.get_all_doctors()
doc_calc = calculate_the_schedule(doctors)
doc_calc.calc()
