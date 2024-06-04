from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Index Page')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
