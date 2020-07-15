from flask import Flask

app = Flask(__name__)


def counter(x):
    return [x*x]

@app.route("/")
def hello():
    r = counter(10)
    return f'{r}'



