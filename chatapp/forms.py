from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from chatapp.models import User


class registrationForm(FlaskForm):
    # Form for user registration
    username = StringField('Username', validators=[DataRequired(),
                                                  Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])
    avatar = RadioField('Avatar', choices=[
        ('avatar1.png', 'Male 1'),
        ('avatar2.png', 'Female 1'),
        ('avatar3.png', 'Male 2'),
        ('avatar4.png', 'Female 2'),
        ('avatar5.png', 'Male 3'),
        ('avatar6.png', 'Female 3'),
        ('avatar7.png', 'Male 4'),
        ('avatar8.png', 'Female 4')
    ])
    submit = SubmitField('Sign up')


class loginForm(FlaskForm):
    # Form for user login
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')