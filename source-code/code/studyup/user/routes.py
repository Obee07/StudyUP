from flask import Blueprint, render_template, flash, redirect, url_for
#, request, jsonify, session
from studyup import db
from studyup.user.forms import RegistrationForm, LoginForm
from studyup.main.routes import index
# from studyup.models import 
from sqlalchemy import func

user = Blueprint('user', __name__)

@user.route("/register", methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		# return redirect(url_for(main.index)) #-> idk how to make this work
		return render_template('index.html')
	return render_template('register.html', title='Register', form=form)

@user.route("/login", methods=['GET','POST'])
def login():
	form = LoginForm()
	# if form.validate_on_submit():

	return render_template('login.html', title='Login', form=form)