from models import Database
from flask import request, redirect

db = Database()

def doctor(request=request):
    try:
        # метод записи врачей в базу: имя, специализация, контактная информация
        if request.method == 'POST':
            name = request.form['name']
            specialization = request.form['specialization']
            contact = request.form['contact']
            db.add_doctor(name, specialization, contact)
            print("Врач успешно добавлен!")
            return redirect('/'), 200
    except Exception as e:
        print("Врач не добавлен", e)

def del_doctor():
    try:
        #метод удаления врачей по их id
        if request.method == 'POST':
            doctor_id = request.form['doctor_id']
            db.delete_doctor(doctor_id)
            print("Врач успешно удалён!")
            return redirect('/')
    except Exception as e:
        print("Врач не был удалён", e)

def unforeseen_circumstances(request=request):
    try:
        #метод обработки непредвиденных обстоятельств
        if request.method == 'POST':
            doctor_id = request.form['doctor_id']
            type = request.form['type']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            approved = request.form['approved']
            db.add_unforeseen_circumstances(doctor_id, type, start_date, end_date, approved)  
            print("Обстоятельства успешно обработаны!")
            return redirect('/'), 200
    except Exception as e:
        print("Обстоятельства не обработаны", e)

def schedule(request=request):
    try:
        # добавление нового расписания
        if request.method == 'POST':
            doctor_id = request.form['doctor_id']
            date = request.form['date']
            shift = request.form['shift']
            db.add_schedule(doctor_id, date, shift)
            print("Расписание успешно добавлено!")
            return redirect('/'), 200
    except Exception as e:
        print("Расписание не добавлено", e)


def hr_worker_add_employee(request=request):
    try:
        if request.method == 'POST':
            name = request.form['name']
            surname = request.form['surname']
            patronymic = request.form['patronymic']
            change_rate = request.form['change_rate']
            minus_employee = request.form['minus_employee']
            res = db.check_employee(name, surname, patronymic)
            if res == False:
                db.hr_worker_add_employee(name, surname, patronymic, change_rate, minus_employee)
                print("Сотрудник успешно добавлен!")
            else:
                db.hr_worker_update_employee(change_rate, minus_employee)
                print('Данные сотрудника обновлены')
            return redirect('/'), 200
    except Exception as e:
        print("Сотрудник не добавлен:", e)