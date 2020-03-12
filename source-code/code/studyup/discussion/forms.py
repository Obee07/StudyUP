from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, SelectMultipleField, TextAreaField
from wtforms.widgets import ListWidget, CheckboxInput, TextArea
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Comment')