from flask import Flask, render_template, redirect, url_for, request, abort
from services import doctor, unforeseen_circumstances, schedule, del_doctor, hr_worker_add_employee
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from UserLogin import UserLogin
from models import Database
from functools import wraps

db = Database()

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = '4aa58657559c70f9956627007f99e93a2daf4f32'

login_manager = LoginManager(app)

# Свяжите функции с маршрутами Flask
app.add_url_rule('/add_doctor', view_func=doctor, methods=['GET', 'POST'])
app.add_url_rule('/add_unforeseen_circumstances', view_func=unforeseen_circumstances, methods=['GET', 'POST'])
app.add_url_rule('/add_schedule', view_func=schedule, methods=['GET', 'POST'])
app.add_url_rule('/delete_doctor', view_func=del_doctor, methods=['GET', 'POST'])
app.add_url_rule('/hr_worker_add_employee', view_func=hr_worker_add_employee, methods=['GET', 'POST'])

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, db)

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or (current_user.get_role() not in roles and 'admin' not in roles):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = db.get_user_email(request.form['email'])
        if user and check_password_hash(user[3], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            role = user_login.get_role()
            if role == 'admin':
                return redirect(url_for('admin'))
            elif role == 'doctor':
                return redirect(url_for('doctor_portal'))
            elif role == 'hr_worker':
                return redirect(url_for('hr_portal'))
            else:
                return redirect(url_for('profile'))
        else:
            print("неверная пара логин/пароль")
    return render_template("login.html", title="Авторизация")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hashed_password = generate_password_hash(request.form['psw'])
            res = db.add_user(request.form['name'], request.form['email'], hashed_password, request.form['role'])
            if res:
                print("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                print("Ошибка при добавлении в БД", "error")
        else:
            print("Неверно заполнены поля", "error")
    return render_template("register.html", title="Регистрация")

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    print('выход из аккаунта')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return f"""
    <p><a href="{url_for('logout')}">Выйти из профиля</a></p>
    <p>user info: {current_user.get_id()}</p>
    <p>role: {current_user.get_role()}</p>
    """

@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    return render_template('admin.html', title='Admin Page')

@app.route('/doctor_portal')
@login_required
@role_required('doctor', 'admin')
def doctor_portal():
    return render_template('doctor_portal.html', title='Doctor Portal')

@app.route('/hr_portal')
@login_required
@role_required('hr_worker', 'admin')
def hr_portal():
    return render_template('hr_portal.html', title='HR Portal')

@app.route('/add_user', methods=['POST'])
@login_required
@role_required('admin')
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_password = generate_password_hash(password)
        res = db.add_user(name, email, hashed_password, role)
        if res:
            return redirect(url_for('admin'))
        else:
            return "Ошибка при добавлении пользователя"
    return render_template('add_user.html')

@app.route('/admin_functionality')
@login_required
@role_required('admin')
def admin_functionality():
    return render_template('admin.html', title='Admin Functionality')

@app.route('/doctor_functionality')
@login_required
@role_required('doctor', 'admin')
def doctor_functionality():
    return render_template('doctor_portal.html', title='Doctor Functionality')

@app.route('/hr_functionality')
@login_required
@role_required('hr_worker', 'admin')
def hr_functionality():
    return render_template('hr_portal.html', title='HR Functionality')

@app.route('/test')
@login_required
@role_required('doctor', 'hr_worker', 'admin')
def test():
    return render_template('test.html', title='Test Page')

@app.route('/doc_schedule/<int:doc_id>', methods=['GET'])
def doc_schedule(doc_id):
    try:
        # получение расписания
        if request.method == 'GET':
            res = db.get_doc_schedule(doc_id)
            print("Расписание успешно предоставлено!")
            return res
    except Exception as e:
        print("Расписание не получено: ", e)
        
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
