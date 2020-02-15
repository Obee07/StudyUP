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
    

    def __repr__(self):
        return f"Question([{self.id}], topic-{self.topic_no} '{self.body}', 'Image:{self.image_file}, [C:{self.solution_id}])"

#This creates a table for the choices per question in the module    
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
   
    def __repr__(self):
        return f"Choice([{self.id}], '{self.body}', [Q:{self.question_id}]')"

# This creates a table for the course selection
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'), nullable=False)
    
    def __repr__(self):
        return f"Answer([{self.id}], '{self.choice_id}', [Q:{self.question_id}]')"

