from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class registrationForm(FlaskForm):
    # Form for user registration
    username = StringField('Username', validators=[DataRequired(),
                                                  Length(min=4, max=20)] ,render_kw={"placeholder": "*Must be 4 characters long"})
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3)] ,render_kw={"placeholder": "*Must be 3 characters long"})
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
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')