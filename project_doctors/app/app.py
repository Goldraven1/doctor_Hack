from flask import Flask, render_template, redirect, url_for
from flask import request
from services import doctor, unforeseen_circumstances, schedule, del_doctor
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# Свяжите функции с маршрутами Flask
app.add_url_rule('/add_doctor', view_func=doctor, methods=['GET', 'POST'])
app.add_url_rule('/add_unforeseen_circumstances', view_func=unforeseen_circumstances, methods=['GET', 'POST'])
app.add_url_rule('/add_schedule', view_func=schedule, methods=['GET', 'POST'])
app.add_url_rule('/delete_doctor', view_func=del_doctor, methods=['GET', 'POST'])

@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return redirect(url_for('test'))  
    else:
        return render_template('test.html', title='test Page')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
