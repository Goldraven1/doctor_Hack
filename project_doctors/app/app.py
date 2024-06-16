from flask import Flask, render_template, redirect, url_for, request, abort
from services import doctor, unforeseen_circumstances, schedule, del_doctor, hr_worker_add_employee
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from UserLogin import UserLogin
from models import Database
from functools import wraps

db = Database() # создаем сущность БД, при помощи которой мы будем с нею связываться

app = Flask(__name__) # получаем app для запуска приложения
Bootstrap(app) # обертка, которая позволяет использовать Bootstrap при верстке 
 
app.config['SECRET_KEY'] = '4aa58657559c70f9956627007f99e93a2daf4f32' # ключ для управления сессией клиента

login_manager = LoginManager(app) # это позволяет нам использовать сущность ЮЗЕРА для работы с авторизованными пользотелями и не только

# Свяжите функции с маршрутами Flask
app.add_url_rule('/add_doctor', view_func=doctor, methods=['GET', 'POST']) # по данному эндпоинту отрабатывает функция doctor 
app.add_url_rule('/add_unforeseen_circumstances', view_func=unforeseen_circumstances, methods=['GET', 'POST']) # по данному эндпоинту отрабатывает функция unforeseen_circumstances
app.add_url_rule('/add_schedule', view_func=schedule, methods=['GET', 'POST']) # по данному эндпоинту отрабатывает функция schedule
app.add_url_rule('/delete_doctor', view_func=del_doctor, methods=['GET', 'POST']) # по данному эндпоинту отрабатывает функция del_doctor
app.add_url_rule('/hr_worker_add_employee', view_func=hr_worker_add_employee, methods=['GET', 'POST']) # по данному эндпоинту отрабатывает функция hr_worker_add_employee
app.add_url_rule('/get_schedule', view_func=db.get_schedule, methods=['GET']) # по данному эндпоинту отрабатывает функция get_schedule

@login_manager.user_loader # декоратор для расширения возможностей ниже
def load_user(user_id): # функция передачи юзер айди и "получения" инфомарции о юзере
    return UserLogin().fromDB(user_id, db) # само "получение"

def role_required(*roles): # функция ролей
    def decorator(f): # функция декоратора
        @wraps(f) # декоратор
        def decorated_function(*args, **kwargs): # передача n аргументов данной функции
            if not current_user.is_authenticated or (current_user.get_role() not in roles and 'admin' not in roles): # условие, если роли не сходятся 
                abort(403) # выкидываем соответствующий статус код
            return f(*args, **kwargs) # возвращаем аргументы
        return decorated_function # возвращаем функцию
    return decorator # возвращаем функцию декоратора

@app.route('/login', methods=['POST', 'GET']) # роут на эндпоинт login + методы пост и гет
def login(): # функция логин
    if request.method == 'POST': # если поступает пост запрос
        user = db.get_user_email(request.form['email']) # получаем данные юзера из бд (для проверки ниже)
        if user and check_password_hash(user[3], request.form['psw']): # проверка на то, есть ли юзер в бд и проверка пароля  
            user_login = UserLogin().create(user) # если всё сходится мы создаем сущность юзера 
            login_user(user_login) # понимание авторизации сущности юзера
            role = user_login.get_role() # выдача роли юзеру
            if role == 'admin': # проверка роли юзера на админа
                return redirect(url_for('admin')) # если правда, то перенаправляем на страничку админа 
            elif role == 'doctor': # проверка роли юзера
                return redirect(url_for('doctor_portal')) # если правда, то перенаправляем на cоответсвующую страничку
            elif role == 'hr_worker': # проверка роли юзера
                return redirect(url_for('hr_portal')) # если правда, то перенаправляем на cоответсвующую страничку
            else: # обработка условий в противном случае 
                return redirect(url_for('profile')) # перенаправление в профиль
        else: # если проверка пароля и логина не прошла
            print("неверная пара логин/пароль") # пишем про данную ошибку
    return render_template("login.html", title="Авторизация") # отдаем страницу авторизации по запросу

@app.route('/register', methods=['POST', 'GET']) # роут на эндпоинт register + методы пост и гет
def register(): # функция регистрации
    if request.method == 'POST': # обработка пост запроса
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']: # валидация данных
            hashed_password = generate_password_hash(request.form['psw']) # хэш пароля
            res = db.add_user(request.form['name'], request.form['email'], hashed_password, request.form['role']) # добавление юзера
            if res: 
                print("Вы успешно зарегистрированы", "success") # пишет если всё успешно
                return redirect(url_for('login')) # вернет если всё успешно
            else: 
                print("Ошибка при добавлении в БД", "error") # вернет если прошло безуспешно
        else: 
            print("Неверно заполнены поля", "error") # вернет если прошло безуспешно
    return render_template("register.html", title="Регистрация") # вернет страничку авторизации

@app.route('/', methods=['GET', 'POST']) # роут на эндпоинт / + методы пост и гет
def index(): # функция индекс
    if current_user.is_authenticated: # проверка аутефикации
        return redirect(url_for('profile')) # перенаправление в профиль
    return redirect(url_for('login')) # перенаправление на логин

@app.route('/logout', methods=['GET', 'POST']) # роут на эндпоинт logout + методы пост и гет
@login_required # обязательна авторизация
def logout(): # функция лог аут
    logout_user() # непостредственный лог аут из система
    print('выход из аккаунта') # пояснения если все успешно
    return redirect(url_for('login')) # перенаправление на логин

@app.route('/profile', methods=['GET', 'POST']) # роут на эндпоинт profile + методы пост и гет
@login_required # обозначение обязательной авторизации
def profile():  # функция профиля
    return f""" 
    <p><a href="{url_for('logout')}">Выйти из профиля</a></p>
    <p>user info: {current_user.get_id()}</p>
    <p>role: {current_user.get_role()}</p>
    <a href="/admin">admin</a>
    """ # вернуть разметку

@app.route('/admin') # роут на эндпоинт admin + методы пост и гет
@login_required
@role_required('admin')  # проверка роли админ
def admin():  # функция админ
    return render_template('admin.html', title='Admin Page')  # возравт шаблона 

@app.route('/doctor_portal') # роут на эндпоинт doctor_portal + методы пост и гет
@login_required
@role_required('doctor', 'admin')  # проверка ролей
def doctor_portal():  # функция доктора
    return render_template('doctor_portal.html', title='Doctor Portal')  # возврат шаблона

@app.route('/hr_portal') # роут на эндпоинт hr_portal + методы пост и гет
@login_required
@role_required('hr_worker', 'admin') # проверка ролей
def hr_portal(): # функция кадр работника
    return render_template('hr_portal.html', title='HR Portal') # возврат шаблона

@app.route('/add_user', methods=['POST']) # роут на эндпоинт add_user + методы пост и гет
@login_required # обязательное присутсвие авторизации в сервисе
@role_required('admin') # обязательное присутсвие роли
def add_user(): # функция добавления юзера
    if request.method == 'POST': # обработка пост запроса
        name = request.form['name'] # имя с формы
        email = request.form['email'] # маил с формы
        password = request.form['password'] # пароль с формы
        role = request.form['role'] # роль с формы
        hashed_password = generate_password_hash(password) # хэш пароля
        res = db.add_user(name, email, hashed_password, role) # получение результата по функции добавления юзера в бд
        if res:
            return redirect(url_for('admin')) # проверка пройдена - перенаправление на страницу
        else:
            return "Ошибка при добавлении пользователя" # cообщение об ошибке
    return render_template('add_user.html') # воюзерврат страницы адд_юзер

@app.route('/admin_functionality') # роут на эндпоинт admin_functionally + методы пост и гет
@login_required
@role_required('admin')
def admin_functionality():
    return render_template('admin.html', title='Admin Functionality') # возврат страницы админа

@app.route('/doctor_functionality') # роут на эндпоинт doctor_functionality + методы пост и гет
@login_required
@role_required('doctor', 'admin')
def doctor_functionality():
    return render_template('doctor_portal.html', title='Doctor Functionality') # возврат страницы доктора

@app.route('/hr_functionality') # роут на эндпоинт hr_functionality + методы пост и гет
@login_required
@role_required('hr_worker', 'admin')
def hr_functionality():
    return render_template('hr_portal.html', title='HR Functionality') # возврат страницы кадрового работника

@app.route('/test') # роут на эндпоинт test + методы пост и гет
@login_required
@role_required('doctor', 'hr_worker', 'admin')
def test():
    return render_template('test.html', title='Test Page') # возврат страницы тест

@app.route('/doc_schedule/<int:doc_id>', methods=['GET']) # роут на эндпоинт doc_schedule/id + методы пост и гет
def doc_schedule(doc_id):
    try:
        # получение расписания 
        if request.method == 'GET': # обработка гет запроса
            res = db.get_doc_schedule(doc_id) # получение информации
            print("Расписание успешно предоставлено!") # письмо об успешном действии
            return res # вернет результат
    except Exception as e: # отлов ошибки
        print("Расписание не получено: ", e) # письмо об ощибке
        
if __name__ == '__main__': # базовое условие для запуска приложения
    app.run(debug=True, host='localhost', port=5000) # запуск приложения с определенными параметрами
