from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from studyup import db
from studyup.practice.forms import SelectForm, AnswerForm
from studyup.models import Question, Choice, Answer
from sqlalchemy import func

practice = Blueprint('practice', __name__)



@practice.route("/api/available-topics")
def getAvailableTopics():
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

    
    availableTopics = Question.query.all()
    if availableTopics is None:
        return "No available topics"

    topicIdTemp = []
    for topic in availableTopics:
        topicIdTemp.append(topic.topic_no)

    topicTemp = []
    for topic in TOPICS:
        if topic[2] in topicIdTemp:
            topicTemp.append(topic)
    topicArray = []

    for topic in topicTemp:
        topicObj = {}
        topicObj['id'] = topic[2]
        topicObj['name'] = topic[3]
        topicArray.append(topicObj)
    return jsonify({'topics' : topicArray})



isNewSession = 0 #Boolean Flag if practice session is a new one 
practiceSessionChoices = [] #Array that contains arrays of choices per question
practiceSessionQuestionIdList = [] #Array that contains the id of question
#Idea: practiceSessionChoices and practiceSessionQuestionIdList is mapped one to one (by index)


#this API shows the choices of a specific question given a question_id, calls this API per question
@practice.route("/api/choices-<int:question_id>")
def getChoices(question_id):
    choice = Choice.query.filter_by(question_id=question_id).order_by(func.random()).all() #gets all choices of specific question in a random order
    question = Question.query.filter_by(id=question_id).first()
    global practiceSessionQuestionIdList
    global practiceSessionChoices
    global isNewSession
    
    if (isNewSession == 1):
        isNewSession = 0
        practiceSessionChoices = []
        practiceSessionQuestionIdList = []
            
    choiceArray = []
    choiceIdArray = []
    
    for item in choice:
        choiceArray.append(item.body)
        choiceIdArray.append(item.id)
        if (item.id == question.solution_id):
            correctText = item.body

    practiceSessionChoices.append(choiceIdArray)
    practiceSessionQuestionIdList.append(question_id)

    print("<<API>>")
    print(practiceSessionChoices)
    print(practiceSessionQuestionIdList)
    
    return jsonify({'choices' : choiceArray, 'correctText' : correctText })

#selecting topics
@practice.route("/practice", methods=['GET', 'POST'])
def select():
    form = SelectForm()

    if form.validate_on_submit():
        global isNewSession
        
        session['practice-topics'] = form.topicList.data
        #session['practice-topics] is an array of topic_no's
        isNewSession = 1

        return redirect(url_for('practice.test'))
    
    return render_template('practice.html', form=form)


@practice.route("/practice-test", methods=['GET', 'POST'])
def test():
    form = AnswerForm()

    if 'practice-topics' in session:

        print('Topics Chosen:',session['practice-topics'])
        
        questionArray = []
        questionIdArray = []
        time = 0 #total time of questions in session
        
        for num in session['practice-topics']:
            q = Question.query.filter_by(topic_no=num).order_by(func.random()).first() 
            print("Question for topic ", num)
            print(q)                                      
            questionArray.append(q)
            questionIdArray.append(q.id)
            time += q.time
        
        #formArray is an array of forms (one form per question)
        formArray = []
        for i in range(len(questionArray)):
            form = AnswerForm()
            formArray.append(form)

        length = len(questionArray)
        session['practice-length'] = length
        session.pop('practice-topics')


        timeLeft=time
        print("GOING TO ANSWER")
        print("questionIdArray")
        print(questionIdArray)
      
      
        return render_template('practice-test.html', formArray=formArray, questionArray=questionArray, questionIdArray=questionIdArray, length=length, timeLeft=time)

    
    else:
        if request.method == "POST":
            global practiceSessionChoices
            global practiceSessionQuestionIdList
            length = session['practice-length']
            session.pop('practice-length')

            print("=================POST========================")
            print("practiceSessionChoices:",practiceSessionChoices)
            print(practiceSessionQuestionIdList)
            
            for i in range(length):
                #Data is 1-based index of choice
                data = request.form.get(str(i))
                print("practice-lengthData:", data)
                if data == None: #no answer
                    pass
                else:
                    a = Answer()
                    a.question_id = practiceSessionQuestionIdList[i]

                    a.choice_id = practiceSessionChoices[i][int(data) - 1]
                    db.session.add(a)
                    print(a)
                    db.session.commit()
            
            session['practice-session-done'] = True
            
            return redirect(url_for('practice.result'))
    return redirect(url_for('practice.select'))



@practice.route("/practice-result", methods=['GET','POST'])
def result():

    if (session['practice-session-done'] == True):
        session['practice-session-done'] = False


        print("RESULTS")
        global practiceSessionQuestionIdList
        print(practiceSessionQuestionIdList)
        answers = Answer.query.all()
        answersArray = []

        #Store Answer Python Object in answerArray
        for answer in answers:
            answersArray.append(Choice.query.filter_by(id=answer.choice_id).first().body)
        
        correctAnswerArray = []

        questionArray = []
        #Store questions from practiceSession
        for num in practiceSessionQuestionIdList:
            q = Question.query.filter_by(id=num).first()
            questionArray.append(q)
            correctAnswerArray.append(Choice.query.filter_by(id=q.solution_id).first().body)
        

        Answer.query.delete()
        db.session.commit()
        print("DELETED!")

        print(questionArray)
        
        return render_template('practice-result.html', answersArray=answersArray, questionArray=questionArray, correctAnswerArray=correctAnswerArray, length=len(questionArray))
    else:
        return redirect(url_for('practice.select'))