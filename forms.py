from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm) : 
    
    subject = StringField('subject', validators=[DataRequired('insert subject')])
    content = TextAreaField('content', validators=[DataRequired('insert content')])
    
class AnswerForm(FlaskForm) : 
    
    content = TextAreaField('content', validators=[DataRequired('insert content')])
    
class UserCreateForm(FlaskForm) : 
    
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('password', validators=[DataRequired(), EqualTo('password2', 'not correct password')])
    password2 = PasswordField('checkpassword', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    
class UserLoginForm(FlaskForm) : 
    
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('password', validators=[DataRequired()])
    