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


# for i in plan__:
#     print(i)


# class Rules():
#     def __init__(self, norm_hours_month, norm_hours_schedule, max_hours_week):
#         self.max_hours_month = norm_hours_month
#         self.norm_hours_schedule = norm_hours_schedule
#         self.max_hours_week = max_hours_week
#         self.norm_hours_schedule = 
        

class employee_doctor():
    def __init__(self, rate):
        self.rate = rate
        # self. modality = modality

    def rate_calc(self):
        if self.rate == 1:
            doc_time_work = 8 # больше 8, но так, чтоб не больше 12 в неделю
            doc_time_chill = 1
            doc_power_hour = 181 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]
        elif self.rate == 0.75:
            doc_time_work = 6
            doc_time_chill = 30
            doc_power_hour =  181 // 8
            return [doc_time_work, doc_time_chill, doc_power_hour]




class calculate_the_schedule():
    def __init__(self, doctors):
        self.doctors = doctors

    def calc(self):
        quantity_research_kt = plan__[1]
        doc_power = 100

        for i in self.doctors :
            if i[1] == 'КТ':
                if quantity_research_kt > 0:
                    quantity_research_kt -= doc_power
                    # self.doc_health -= 8
                if quantity_research_kt < 0:
                    r = 0
                    r += quantity_research_kt
                    quantity_research_kt = 0
                    print(r)
                    print('this doctor')
                rate = i[3]
                em = employee_doctor(rate)
                arr = em.rate_calc()
                print(arr)
                print(quantity_research_kt)
                
                

doctors = db.get_all_doctors()
doc_calc = calculate_the_schedule(doctors)
doc_calc.calc()

# class implementation_schedule(employee_doctor):
#     def __init__(self, p, d) :
#         self.p = p
#         self.d = d

#     def show(self):
#         return super().show()

# em = employee_doctor('ФИО', 'rg', ['kt', 'mmg', 'flg', 'dens'], 1, 181)
# em.show()

# p = plan(1970, 4437, 508, 541, 19061, 1675, 817, 14, 67021, 40364)
# d = employee_doctor('ФИО', 'rg', ['kt', 'mmg', 'flg', 'dens'], 1, 181)

# im = implementation_schedule(p, d)


    # def choose_doc_dens(self):
        # for i in self.d:
            # print(i)
        # print(self.p)
        # print(self.d.modality)

# print(implementation_schedule(p, d).choose_doc_dens())
# modality = d.modality
# print(modality)
# print(p['rg'])

# count = 0
# arr = []
# day_doc = 1
# start_doc_hours = 8
# start_doc_min = 30
# end_doc_hours = 20
# end_doc_min = 30
# year = datetime.datetime.now().year
# month = datetime.datetime.now().month
# while p.dens > count:
#     p.dens -= d.doc_power
#     if d.rate == 1:
#         start_date = datetime.datetime(year, month, day_doc, start_doc_hours, start_doc_min)
#         end_date = datetime.datetime(year, month, day_doc, end_doc_hours, end_doc_min)

#         # start_date = datetime.datetime.strptime(f"6/{day_doc}/24", "%m/%d/%y")
#         day_doc += 1
#         # end_date = start_date + datetime.timedelta(days=1)
#         print(start_date)
#         print(end_date)
# print(p.dens)


