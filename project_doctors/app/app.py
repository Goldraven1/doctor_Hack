from flask import Flask, render_template, request

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    response.headers["Server"] = ""
    response.headers["X-Powered-By"] = ""
    return response

@app.route('/')
def index():
    return render_template('index.html', title='Index Page')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
