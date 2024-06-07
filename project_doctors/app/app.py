from flask import Flask, render_template, redirect, url_for, request
from services import doctor, unforeseen_circumstances, schedule, del_doctor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user 
from UserLogin import UserLogin
from models import Database 

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


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, db)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = db.get_user_email(request.form['email'])
        if user and check_password_hash(psw_from_db, request.form['psw']):
            UserLogin = UserLogin().create(user)
            login_user(UserLogin)
            return redirect('test')
        
        else:
            print("неверная пара логин/пароль")

    return render_template("login.html", title="Авторизация")

@app.route("/register", methods=['POST', 'GET'])
def register(request=request):
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = db.add_user(request.form['name'], request.form['email'], hash)
            if res:
                print("Вы успешно авторизированы", "success")
                return redirect(url_for('login'))
            else:
                print("Ошибка при добавлении в БД", "error")
        else:
            print("Неверно заполнены поля", "error")

    return render_template("register.html", title="Регистрация")

@app.route('/', methods=['GET', 'POST'])
@login_required
def test():
    if request.method == 'POST':
        return redirect(url_for('test'))  
    else:
        return render_template('test.html', title='test Page')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
