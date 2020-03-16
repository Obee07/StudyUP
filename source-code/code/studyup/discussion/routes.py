from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, abort
from studyup.models import Question, Choice, Answer, Comment, User
from studyup import db
from studyup.discussion.forms import CommentForm
from flask_login import login_required, current_user
from datetime import datetime

discussion = Blueprint('discussion', __name__)
comment = Blueprint('comment', __name__)

#returns topic name of given topicNo
@discussion.route("/api/topic/<int:topic_no>")
def topic(topic_no):
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

    return jsonify({'name': TOPICS[topic_no - 1][3]})


@discussion.route("/api/topic/<int:topic_num>/questions")
def questionPerTopic(topic_num):
    q = Question.query.filter_by(topic_no=int(topic_num)).all()

    qList = []
    for question in q:
        questionObj = {}
        questionObj['id'] = question.id
        questionObj['body'] = question.body
        qList.append(questionObj)
    return jsonify({'questions': qList})

@discussion.route('/discussion')
def select():
    return render_template('discussion.html')

@discussion.route('/discussion/<int:question_id>', methods=['GET','POST'])
@login_required
def add_comment(question_id):
    form = CommentForm()
    question = Question.query.filter_by(id=question_id).first()
    if form.validate_on_submit():
        comment = Comment()
        comment.time_posted = datetime.utcnow()
        comment.comment = form.body.data
        user = User.query.filter_by(username=current_user.username).first()
        comment.user_id = user.id
        comment.question_id = question_id 
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
        comments = Comment.query.filter_by(question_id=question_id).all()
        return redirect(url_for('discussion.add_comment', question_id=question_id, comments=comments))
    comments = Comment.query.filter_by(question_id=question_id).all()
    return render_template('view-question.html', form=form, question=question, comments=comments)

@discussion.route('/discussion/<int:question_id>/edit/<int:comment_id>', methods=['GET','POST'])
@login_required
def edit_comment(question_id, comment_id):
    question = Question.query.filter_by(id=question_id).first()
    comments = Comment.query.filter_by(question_id=question_id).all()
    comment = Comment.query.filter_by(id=comment_id).first()
    form = CommentForm()
    if form.validate_on_submit():
        comment.comment = form.body.data
        comment.edited = True
        db.session.commit()
        flash('Comment edited', 'success')
    return render_template('view-question.html', question=question, form=form, comments=comments)

# current_user_comments = [comment for comment in comments if comment.user_id == current_user.id]