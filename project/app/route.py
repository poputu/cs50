from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/new')
def new():
    return render_template("new.html")


if __name__ == "__main__":
    app.run(debug=True)
