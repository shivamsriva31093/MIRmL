from flask import Flask
from flask import make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def hello_world():
    response = make_response('<h1> This response contains a cookie! </h1>')
    return response


@app.route('/<user_name>')
def user(user_name):
    return '<h1> Hello %s </h1>' % user_name


if __name__ == '__main__':
    app.run()
