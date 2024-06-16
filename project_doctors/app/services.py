from models import Database
from flask import request, redirect

db = Database()

def doctor(request=request):
    try:
        # метод записи врачей в базу: имя, специализация, контактная информация
        if request.method == 'POST': # обработка пост запроса
            name = request.form['name'] # получение имени с формы
            specialization = request.form['specialization'] # получение специализации с формы
            contact = request.form['contact']  # получение контакта с формы
            db.add_doctor(name, specialization, contact)  # добавление доктора
            print("Врач успешно добавлен!")
            return redirect('/'), 200
    except Exception as e: # отлов ошибки
        print("Врач не добавлен", e)# письмо об ошибке

def del_doctor():
    try:
        #метод удаления врачей по их id
        if request.method == 'POST':  #  обработка пост запроса
            doctor_id = request.form['doctor_id']  # прием данных с формы
            db.delete_doctor(doctor_id)  # удаление доктора
            print("Врач успешно удалён!")
            return redirect('/')  # перенаправление на /
    except Exception as e:# отлов ошибки
        print("Врач не был удалён", e)# письмо об ошибке

def unforeseen_circumstances(request=request): # функция непредвиденных об-ств
    try:
        #метод обработки непредвиденных обстоятельств
        if request.method == "POST":
            doctor_id = request.form["doctor_id"]  # прием данных формы
            type = request.form["type"] # прием данных формы
            start_date = request.form["start_date"] # прием данных формы
            end_date = request.form['end_date'] # прием данных формы
            approved = False  # обозначение стандартного подтверждения обстоятельств
            db.add_unforeseen_circumstances(doctor_id, type, start_date, end_date, approved)  # добавление непредвиденных об-ств  
            print("Обстоятельства успешно обработаны!") 
            return redirect('/doctor_portal'), 200 # перенапрявление и возврат успешного кода
    except Exception as e:# отлов ошибки
        print("Обстоятельства не обработаны", e)# письмо об ошибке

def schedule(request=request):
    try:
        # добавление нового расписания
        if request.method == 'POST': # обработка пост запроса
            doctor_id = request.form['doctor_id'] # прием данных с формы
            date = request.form['date'] # прием данных с формы
            shift = request.form['shift']  # прием данных с формы
            db.add_schedule(doctor_id, date, shift)  # добавление расписания
            print("Расписание успешно добавлено!")
            return redirect('/'), 200 # перенаправление и возврат успешного статус кода 
    except Exception as e: # отлов ошибки
        print("Расписание не добавлено", e) # письмо об ошибке


def hr_worker_add_employee(request=request): # кадровый сотрудник добавляет доктора в систему как боеквую единицу
    try:
        if request.method == 'POST': # обработка пост запроса
            name = request.form['name'] # получение данные с формы
            surname = request.form['surname'] # получение данные с формы
            patronymic = request.form['patronymic'] # получение данные с формы
            change_rate = request.form['change_rate'] # получение данные с формы 
            minus_employee = request.form['minus_employee'] # получение данные с формы
            res = db.check_employee(name, surname, patronymic) # чек сотрудника
            if res == False: # если не было такого то мы добавляем ниже
                db.hr_worker_add_employee(name, surname, patronymic, change_rate, minus_employee)
                print("Сотрудник успешно добавлен!")
            else:
                db.hr_worker_update_employee(change_rate, minus_employee) # если был уже то просто обновляем данные
                print('Данные сотрудника обновлены')
            return redirect('/'), 200 # если все успешно то отдаем статус код
    except Exception as e:  # отлов ошибки
        print("Сотрудник не добавлен:", e)  # письмо об ошибке