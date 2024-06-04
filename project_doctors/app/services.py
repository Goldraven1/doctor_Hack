from models import Database
from flask import request, redirect

db = Database()

def doctor(request):
    try:
        # метод записи врачей в базу: имя, специализация, контактная информация
        if request.method == 'POST':
            name = request.form['name']
            specialization = request.form['specialization']
            contact = request.form['contact']
            Database.add_doctor(name, specialization, contact)
            print("Врач успешно добавлен!")
            return redirect('/')
    except Exception as e:
        print("Врач не добавлен", e)

def unforeseen_circumstances(request):
    try:
        #метод обработки непредвиденных обстоятельств
        if request.method == 'POST':
            doctor_id = request.form['doctor_id']
            type = request.form['type']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            approved = request.form['approved']
            Database.unforeseen_circumstances(doctor_id, type, start_date, end_date, approved)  
            print("Обстоятельства успешно обработаны!")
            return redirect('/')
    except Exception as e:
        print("Обстоятельства не обработаны", e)

def shedule(request):
    try:
        #метод записи  расписания врачей
        if request.method == 'POST':
            doctor_id = request.form['doctor_id']
            date = request.form['date']
            shift = request.form['shift']
            Database.shedule(doctor_id, date, shift)
            print("Расписание успешно добавлено!")
            return redirect('/')
    except Exception as e:
        print("Расписание не добавлено", e)

# def shedule_update(request):
