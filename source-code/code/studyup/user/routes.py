import secrets, os
from PIL import Image
from flask import Blueprint, render_template, flash, redirect, url_for, request
from studyup import db, bcrypt
from studyup.user.forms import RegistrationForm, LoginForm, UpdateAccountForm
from studyup.main.routes import index
from studyup.models import User
from sqlalchemy import func
from flask_login import login_user, current_user, logout_user, login_required

user = Blueprint('user', __name__)

@user.route("/register", methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if current_user.is_authenticated:
		return redirect(url_for('main.index')) #should go to index
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User()
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


@user.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.index'))
			flash('Login Successful. Welcome!')
			return redirect(url_for('main.index'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

def save_picture(form_picture):
	#randomize name of image
	random_hex = secrets.token_hex(8)
	#renaming uploaded filename and save to folder
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(user.root_path, '../static/img/user', picture_fn)

	output_size = (125, 125)
	img = Image.open(form_picture)
	img.thumbnail(output_size)
	img.save(picture_path)

	return picture_fn

@user.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		#updating profile picture
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		#updating username and email
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('user.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename=f'img/user/{current_user.image_file}')
	return render_template('account.html', title='Account', image_file=image_file, form=form)