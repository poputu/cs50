from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

from app import route

class task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(1000), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    important = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    pushup = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return '<User %r>' % self.id