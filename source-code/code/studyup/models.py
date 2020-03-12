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

from datetime import datetime
from studyup import db
from flask import current_app

#This creates a table for the questions being added to the module
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('choice.id'), nullable=False)
    
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    image_file = db.Column(db.String(20), nullable=True)
    #unit_no = db.Column(db.Integer, nullable=False)
    topic_no = db.Column(db.Integer, nullable=False)
    # time = db.Column(db.DateTime, nullable=True) 
    # not sure if DateTime is best type
    time = db.Column(db.Integer, nullable=True)
    choices = db.relationship('Choice', back_populates='question')


    def __repr__(self):
        return f"Question([{self.id}], topic-{self.topic_no} '{self.body}', 'Image:{self.image_file}, [C:{self.solution_id}])"

#This creates a table for the choices per question in the module    
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', back_populates='choices')
    
    def __repr__(self):
        return f"Choice([{self.id}], '{self.body}', [Q:{self.question_id}]')"

# This creates a table for the course selection
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

# This creates a table for the correct answer for a question
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'), nullable=False)
    
    def __repr__(self):
        return f"Answer([{self.id}], '{self.choice_id}', [Q:{self.question_id}]')"

# This creates a table for our users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='static/img/user/default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.Integer, primary_key=True)
        #student_user = 1
        #moderator_user = 2
    comments = db.relationship('Comment', back_populates='author')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

#This creates a table for a comment a user gives
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='comments')
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
        # corresponds to question comment was asked on

    def __repr__(self):
        return f"Comment('{self.date_posted}', '{self.comment}')"