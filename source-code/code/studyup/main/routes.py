"""
LICENSE
This is a course requirement for CS 192 Software Engineering II 
under the supervision of Asst. Prof. Ma. Rowena C. Solamo 
of the Department of Computer Science, College of Engineering, 
University of the Philippines, Diliman for the AY 2019-2020
AUTHORS: Ang, Karina Kylle L. 
         Kopio, Katrina Mae D. 
         Principio, Roberto Jr. D.

CODE HISTORY
01-23-2020 Principio - File created, code added, documentation added

INFO
File Creation Date: January 24, 2020
Development Group: Group 9 - StudyUP Team
Client Group: Ma'am Solamo, CS 192 Class
Purpose of the Software: To provide a collaborative learning
    environment in the courses of UP Diliman.
"""

from flask import Blueprint, render_template, request
from studyup.models import Question, Choice, Answer, User, Comment
from studyup import db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
def index():
    return render_template('index.html')

"""
Name: view_db
Creation Date: Jan 28, 2020
Purpose: views the whole database
Return value: questions table with choices
"""
@main.route("/db")
def view_db():
    questions = Question.query.all()
    choices = Choice.query.all()

    return render_template('db.html', questions=questions, choices=choices)

@main.route("/db-practice")
def view_practice_db():
    answers = Answer.query.all()

    return render_template('db-practice.html', answers=answers)

@main.route("/db-user")
def view_user_db():
    users = User.query.all()

    return render_template('db-user.html', users=users)

@main.route("/db-comment")
def view_comment_db():
    comments = Comment.query.all()

    return render_template('db-comment.html', comments=comments)


@main.route("/delete-practice-session")
def delete_session():
    Answer.query.delete()
    db.session.commit()
    return "successfully deleted"  

@main.route("/delete-qc")
def delete():
    Question.query.delete()
    Choice.query.delete()
    db.session.commit()
    return "successfully deleted" 