from flask import Blueprint, render_template, request
from studyup.models import Question, Choice

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
def index():
    return render_template('index.html')
