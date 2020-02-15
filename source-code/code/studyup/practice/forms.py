from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired



TOPICS = [
        (1, 'Standards and units, Unit consistency, Uncertainty and significant figures'),
        (2, 'Vectors and vector addition, Components of vectors, Unit vectors'),
        (3, 'Displacement, time, and average velocity, Instantaneous velocity'),
        (4, 'Average and instantaneous acceleration'),
        (5, 'Motion with constant acceleration, Freely falling bodies'),
        (6, 'Position and velocity vectors, Acceleration vector'),
        (7, 'Projectile motion'),
        (8, 'Motion in a circle'),
        (9, 'Relative velocity'),
        (10, 'Force and interactions, Mass and weight, Newton\'s first law, Inertial frames of reference'),
        (11, 'Free-body diagrams, Newton\'s second law, Newton\'s third law'),
        (12, 'Newton\'s 1st law: particles in equilibrium'),
        (13, 'Newton\'s 2nd law: dynamics of particles'),
        (14, 'Frictional forces'),
        (15, 'Dynamics of circular motion'),
        (16, 'Scalar product, Work'),
        (17, 'Work and kinetic energy'),
        (18, 'Work and energy with varying forces, Power'),
        (19, 'Gravitational potential energy, Conservation of mechanical energy (gravitational force), Conservative and nonconservative forces'),
        (20, 'Elastic potential energy, Conservation of mechanical energy'),
        (21, 'Force and potential energy, Energy diagrams'),
        (22, 'Momentum and Impulse'),
        (23, 'Conservation of momentum, Momentum conservation and collisions'),
        (24, 'Elastic collisions'),
        (25, 'Center of mass'),
        (26, 'Angular velocity and acceleration, Rotation with constant angular acceleration'),
        (27, 'Relating linear and angular kinematics'),
        (28, 'Energy in rotational motion, Parallel-axis theorem'),
        (29, 'Vector product, Torque'),
        (30, 'Torque and Angular acceleration for a rigid body'),
        (31, 'Rigid-body rotation about a moving axis'),
        (32, 'Angular momentum, Conservation of angular momentum'),
        (33, 'Conditions for equilibrium, Center of gravity'),
        (34, 'Solving rigid-body equilibrium problems'),
        (35, 'Stress, strain, elastic moduli, Elasticity and plasticity'),
        (36, 'Density, Pressure in a fluid'),
        (37, 'Buoyancy'),
        (38, 'Fluid flow, Bernoulli\'s equation'),
        (39, 'Newton\'s law of gravitation, Weight'),
        (40, 'Gravitational potential energy, Motion of satellites'),
        (41, 'Kepler\'s laws and the motion of the planets'),
        (42, 'Describing oscillation, Simple harmonic motion'),
        (43, 'Energy in simple harmonic motion'),
        (44, 'Applications of simple harmonic motion, The simple pendulum, The physical pendulum'),
        (45, 'Damped Oscillations, Forced Oscillations'),
        (46, 'Types of mechanical waves, Periodic waves, Mathematical description of wave, Speed of a transverse wave'),
        (47, 'Energy in wave motion, Wave interference, boundary conditions, and superposition'),
        (48, 'Standing waves on a string, Normal modes of a string'),
        (49, 'Doppler Effect')
            ]


COURSES = [(1, 'Physics 71')]

class MultiCheckboxField(SelectMultipleField):
	widget			= ListWidget(prefix_label=False)
	option_widget	= CheckboxInput()


class SelectForm(FlaskForm):
    course_id = SelectField('Course', choices=COURSES, default=COURSES[0], coerce=int, validators=[DataRequired()])
    topicList = MultiCheckboxField('Topics', choices=TOPICS, validators=[DataRequired()], coerce=int) 
    submit = SubmitField('Continue')


class AnswerForm(FlaskForm):

    

    answer = RadioField('Choices', choices=[(1, '>'), (2, '>'),
                        (3, '>'), (4, '>')], validators=[DataRequired()], coerce=int)

    submit = SubmitField('Finish')



