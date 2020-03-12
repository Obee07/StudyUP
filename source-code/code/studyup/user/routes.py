from flask import Blueprint, render_template, flash, redirect, url_for
#, request, jsonify, session
from studyup import db, bcrypt
from studyup.user.forms import RegistrationForm, LoginForm
from studyup.main.routes import index
from studyup.models import User 
from sqlalchemy import func

user = Blueprint('user', __name__)

@user.route("/register", methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		# hash password
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		# user = User(username=form.username.data, email=form.email.data, password=hashed_pw, user_type=form.usertype.data)
		

		print(form.username.data)
		print(form.email.data)
		print(form.password.data)
		print(form.usertype.data)
		user = User()
		# user.id = None
		user.username=form.username.data
		user.email = form.email.data
		user.password = hashed_pw
		if (form.usertype.data == 's'):
			user.user_type = 1
		else:
			user.user_type = 2
			
		db.session.add(user)
		db.session.commit()
		flash('Your account has been successfully created!', 'success')
		return redirect(url_for('user.login'))
	return render_template('register.html', title='Register', form=form)

@user.route("/login", methods=['GET','POST'])
def login():
	form = LoginForm()
	# if form.validate_on_submit():

	return render_template('login.html', title='Login', form=form)

