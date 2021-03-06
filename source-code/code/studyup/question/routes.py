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
01-30-2020 Kopio - Made feature to add photos to the question creation

INFO
File Creation Date: January 24, 2020
Development Group: Group 9 - StudyUP Team
Client Group: Ma'am Solamo, CS 192 Class
Purpose of the Software: To provide a collaborative learning
    environment in the courses of UP Diliman.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from studyup import db
from studyup.question.forms import QuestionForm, UpdateQuestionForm
from studyup.models import Question, Choice, Answer
from flask_uploads import UploadSet, IMAGES
from datetime import datetime
from flask_login import current_user
from studyup.dashboard.routes import dashboard

question = Blueprint('question', __name__) #variable for questions
photos = UploadSet('photos', IMAGES) #variable for the images


"""
Name: topic
Creation Date: Jan 26, 2020
Purpose: to return a list of topics for the course
Return value: render to html
"""
@question.route("/topic/<string:unit>")
def topic(unit):
    TOPICS = [
        (1, 1, 1, 'Standards and units, Unit consistency, Uncertainty and significant figures'),
        (1, 1, 2, 'Vectors and vector addition, Components of vectors, Unit vectors'),
        (1, 2, 3, 'Displacement, time, and average velocity, Instantaneous velocity'),
        (1, 2, 4, 'Average and instantaneous acceleration'),
        (1, 2, 5, 'Motion with constant acceleration, Freely falling bodies'),
        (1, 3, 6, 'Position and velocity vectors, Acceleration vector'),
        (1, 3, 7, 'Projectile motion'),
        (1, 3, 8, 'Motion in a circle'),
        (1, 3, 9, 'Relative velocity'),
        (1, 4, 10, 'Force and interactions, Mass and weight, Newton\'s first law, Inertial frames of reference'),
        (1, 4, 11, 'Free-body diagrams, Newton\'s second law, Newton\'s third law'),
        (1, 5, 12, 'Newton\'s 1st law: particles in equilibrium'),
        (1, 5, 13, 'Newton\'s 2nd law: dynamics of particles'),
        (1, 5, 14, 'Frictional forces'),
        (1, 5, 15, 'Dynamics of circular motion'),
        (2, 6, 16, 'Scalar product, Work'),
        (2, 6, 17, 'Work and kinetic energy'),
        (2, 6, 18, 'Work and energy with varying forces, Power'),
        (2, 7, 19, 'Gravitational potential energy, Conservation of mechanical energy (gravitational force), Conservative and nonconservative forces'),
        (2, 7, 20, 'Elastic potential energy, Conservation of mechanical energy'),
        (2, 7, 21, 'Force and potential energy, Energy diagrams'),
        (2, 8, 22, 'Momentum and Impulse'),
        (2, 8, 23, 'Conservation of momentum, Momentum conservation and collisions'),
        (2, 8, 24, 'Elastic collisions'),
        (2, 8, 25, 'Center of mass'),
        (2, 9, 26, 'Angular velocity and acceleration, Rotation with constant angular acceleration'),
        (2, 9, 27, 'Relating linear and angular kinematics'),
        (2, 9, 28, 'Energy in rotational motion, Parallel-axis theorem'),
        (2, 10, 29, 'Vector product, Torque'),
        (2, 10, 30, 'Torque and Angular acceleration for a rigid body'),
        (2, 10, 31, 'Rigid-body rotation about a moving axis'),
        (2, 10, 32, 'Angular momentum, Conservation of angular momentum'),
        (3, 11, 33, 'Conditions for equilibrium, Center of gravity'),
        (3, 11, 34, 'Solving rigid-body equilibrium problems'),
        (3, 11, 35, 'Stress, strain, elastic moduli, Elasticity and plasticity'),
        (3, 12, 36, 'Density, Pressure in a fluid'),
        (3, 12, 37, 'Buoyancy'),
        (3, 12, 38, 'Fluid flow, Bernoulli\'s equation'),
        (3, 13, 39, 'Newton\'s law of gravitation, Weight'),
        (3, 13, 40, 'Gravitational potential energy, Motion of satellites'),
        (3, 13, 41, 'Kepler\'s laws and the motion of the planets'),
        (3, 14, 42, 'Describing oscillation, Simple harmonic motion'),
        (3, 14, 43, 'Energy in simple harmonic motion'),
        (3, 14, 44, 'Applications of simple harmonic motion, The simple pendulum, The physical pendulum'),
        (3, 14, 45, 'Damped Oscillations, Forced Oscillations'),
        (3, 15, 46, 'Types of mechanical waves, Periodic waves, Mathematical description of wave, Speed of a transverse wave'),
        (3, 15, 47, 'Energy in wave motion, Wave interference, boundary conditions, and superposition'),
        (3, 15, 48, 'Standing waves on a string, Normal modes of a string'),
        (3, 16, 49, 'Doppler Effect')
            ]

    topicTemp = []
    for topic in TOPICS:
        if str(topic[0]) == unit:
            topicTemp.append(topic)
    topicArray = []

    for topic in topicTemp:
        topicObj = {}
        topicObj['id'] = topic[2]
        topicObj['name'] = topic[3]
        topicObj['chapNo'] = topic[1]
        topicArray.append(topicObj)
    return jsonify({'topics' : topicArray})


"""
Name: success()
Creation Date: Jan 26, 2020
Purpose: to return a successful creation of a question
Return value: render to html
"""
@question.route("/create-success", methods=['GET'])
def success():
    recentQ = Question.query.order_by(Question.id.desc()).first()
    recentC = Choice.query.filter_by(question_id=recentQ.id)

    return render_template('question-success.html', recentQ=recentQ, recentC=recentC)


"""
Name: create_question()
Creation Date: Jan 26, 2020
Purpose: to create a valid question with 4 choices
Return value: render to html
"""
@question.route("/create-question", methods=['GET', 'POST'])
def create_question():
    form = QuestionForm()
    if current_user.user_type != 2: ## if not moderator
        abort(403)
    if request.method == "POST":
        print("QUESTION MADE!")
        q = Question()
        q.body = form.body.data
        q.course_id = 1
        #q.course_id = form.course_id.data

        
        q.solution_id = 0 #temporary


        # q.unit_no = form.unit_no.data
        q.topic_no = form.topic_no.data

        image = request.files.get('image')
        try:
            filename = photos.save(image)
            file_url = photos.url(filename)
        except:
            flash("No photo.", category='warning')
        else:
            q.image_file = filename

        q.time = 60 # temporary -- moderator will set up time
        # q.time = datetime.time(second=59)
        db.session.add(q)
        db.session.commit()

        c_1 = Choice()
        c_1.body = form.choice_1.data

        c_1.question_id = q.id
        db.session.add(c_1)
        db.session.commit()

        c_2 = Choice()
        c_2.body = form.choice_2.data
        c_2.question_id = q.id
        db.session.add(c_2)
        db.session.commit()

        c_3 = Choice()
        c_3.body = form.choice_3.data
        c_3.question_id = q.id
        db.session.add(c_3)
        db.session.commit()

        c_4 = Choice()
        c_4.body = form.choice_4.data
        c_4.question_id = q.id
        db.session.add(c_4)
        db.session.commit()

        
        num = form.solution_id.data

        if num == 1:
            q.solution_id = c_1.id
        elif num == 2:
            q.solution_id = c_2.id
        elif num == 3:
            q.solution_id = c_3.id
        elif num == 4:
            q.solution_id = c_4.id
        

        db.session.commit()

        flash('Your question has been added!','success')
       
        return redirect(url_for('question.success'))
    return render_template('question.html', form=form)

def get_choices(solution_id, question_id):
    correct = Choice.query.filter_by(id=solution_id).first()
    other_choices = Choice.query.filter_by(question_id=question_id).all()
    other_choices.remove(correct)
    return correct, other_choices

@question.route('/question/update/<int:question_id>', methods=['GET','POST'])
def update_question(question_id):
    form = UpdateQuestionForm()
    question = Question.query.filter_by(id=question_id).first()
    correct, other_choices = get_choices(question.solution_id, question_id)

    if form.validate_on_submit():
        question.body = form.body.data

        correct.body = form.correct.data
        other_choices[0].body = form.other_1.data
        other_choices[1].body = form.other_2.data
        other_choices[2].body = form.other_3.data

        if form.picture.data:
            filename = photos.save(form.picture.data)
            file_url = photos.url(filename)
            question.image_file = filename
        db.session.commit()
        flash('Question has been updated', 'success')
        return redirect(url_for('dashboard.mod_dashboard'))
    elif request.method == 'GET':
        form.body.data = question.body
        form.correct.data = correct.body
        form.other_1.data = other_choices[0].body
        form.other_2.data = other_choices[1].body
        form.other_3.data = other_choices[2].body

    if question.image_file is not None:
        image_file = url_for('static', filename=f'img/{question.image_file}')
    else:
        image_file = None

    return render_template('question-edit.html', form=form, question=question, image_file=image_file)

@question.route('/question/delete_photo/<int:question_id>', methods=['GET','POST'])
def delete_photo(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if current_user.user_type != 2: # not a moderator 
        abort(403)
    question.image_file = None
    db.session.commit()
    flash('Photo has been deleted!', 'success')
    return redirect(url_for('question.update_question', question_id=question_id))



# def findCorrectAnswer(form, choice_1, choice_2, choice_3, choice_4, choice_5):
#     num = form.solution.data
#     if num == '1':
#         return choice_1
#     elif num == '2':
#         return choice_2
#     elif num == '3':
#         return choice_3
#     elif num == '4':
#         return choice_4
#     elif num == '5':
#         return choice_5




















# choice_1 = Choice(body=form.choice_1.data, question_id=q.id)
        # choice_2 = Choice(body=form.choice_2.data, question_id=q.id)
        # choice_3 = Choice(body=form.choice_3.data, question_id=q.id)
        # choice_4 = Choice(body=form.choice_4.data, question_id=q.id)

        # db.session.add(choice_1)
        # db.session.add(choice_2)
        # db.session.add(choice_3)
        # db.session.add(choice_4)

        # if form.choice_5.data:
        #     choice_5 = Choice(body=form.choice_5.data, question_id=q.id)
        #     db.session.add(choice_5)
        
        # db.session.commit()

        # if form.choice_5.data:
        #     q.solution_id = findCorrectAnswer(form, choice_1.id, choice_2.id, choice_3.id, choice_4.id, choice_5.id)
        # else:
        #     q.solution_id = findCorrectAnswer(form, choice_1.id, choice_2.id, choice_3.id, choice_4.id, 0)
       
        # db.session.commit()
