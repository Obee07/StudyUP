from flask import Blueprint, render_template, flash, redirect, url_for, abort
from studyup import db
from studyup.main.routes import index
from studyup.models import User, Question, Choice, Answer, Comment
from flask_login import current_user, login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/dashboard", methods=['GET', 'POST'])
@login_required
def mod_dashboard():
	if current_user.user_type != 2: ## if not moderator
		abort(403)
	users = User.query.all()
	questions = Question.query.all()
	choices = Choice.query.all()
	answers = Answer.query.all()
	comments = Comment.query.all()
	return render_template('dashboard.html', users=users, questions=questions, choices=choices, answers=answers, comments=comments)


@dashboard.route("/delete-user/<int:user_id>", methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
	if current_user.user_type != 2: ## if not moderator
		abort(403)
	user = User.query.filter_by(id=user_id).first()
	comments = Comment.query.filter_by(user_id=user_id).all()

	for comment in comments:
		db.session.delete(comment)
	db.session.delete(user)
	db.session.commit()
	flash('User has been deleted!', 'success')


	return redirect(url_for('dashboard.mod_dashboard'))

@dashboard.route("/delete-question/<int:q_id>", methods=['GET', 'POST'])
@login_required
def delete_question(q_id):
	if current_user.user_type != 2: ## if not moderator
		abort(403)
	question = Question.query.filter_by(id=q_id).first()
	comments = Comment.query.filter_by(user_id=q_id).all()

	for comment in comments:
		db.session.delete(comment)
	db.session.delete(question)
	db.session.commit()
	flash('Question has been deleted!', 'success')


	return redirect(url_for('dashboard.mod_dashboard'))

@dashboard.route("/reset", methods=['GET', 'POST'])
@login_required
def reset():
	if current_user.user_type != 2: ## if not moderator
		abort(403)
	User.query.delete()
	Question.query.delete()
	Choice.query.delete()
	Answer.query.delete()
	Comment.query.delete()
	db.session.commit()
	return render_template('index.html')