from flask import Flask, flash, render_template, redirect, url_for, request
from services import doctor, unforeseen_circumstances, schedule, del_doctor
from werkzeug.security import generate_password_hash, check_password_hash
# import flask_login
# from flask_bootstrap import Bootstrap
# from flask_login import LoginManager 
# from UserLogin import UserLogin

from models import Database 
db = Database()


app = Flask(__name__)
# Bootstrap(app)
app.config['SECRET_KEY'] = '4aa58657559c70f9956627007f99e93a2daf4f32'
# login_manager = LoginManager()

# login_manager.init_app(app)

# Свяжите функции с маршрутами Flask
app.add_url_rule('/add_doctor', view_func=doctor, methods=['GET', 'POST'])
app.add_url_rule('/add_unforeseen_circumstances', view_func=unforeseen_circumstances, methods=['GET', 'POST'])
app.add_url_rule('/add_schedule', view_func=schedule, methods=['GET', 'POST'])
app.add_url_rule('/delete_doctor', view_func=del_doctor, methods=['GET', 'POST'])


# @login_manager.user_loader
# def load_user(user_id):
#     return UserLogin().fromDB(user_id, db)


@app.route('/login')
def login():
    return render_template("login.html", title="Авторизация")

@app.route("/register", methods=['POST', 'GET'])
def register(request=request):
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = db.add_user(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно авторизированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html", title="Регистрация")

@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return redirect(url_for('test'))  
    else:
        return render_template('test.html', title='test Page')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
