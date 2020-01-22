from datetime import datetime
from studyup import db
from flask import current_app

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('choice.id'), nullable=False)
    
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    image_file = db.Column(db.String(20), nullable=True)
    unit_no = db.Column(db.Integer, nullable=False)
    topic_no = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return f"Question([{self.id}],unit-{self.unit_no}, topic-{self.topic_no} '{self.body}', 'Image:{self.image_file}, [C:{self.solution_id}])"

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
   
    def __repr__(self):
        return f"Choice([{self.id}], '{self.body}', [Q:{self.question_id}]')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
