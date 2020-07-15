from flask import request, Flask
from flask import render_template



app = Flask(__name__)

from app import routes