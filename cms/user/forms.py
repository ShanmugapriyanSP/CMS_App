from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from cms.models import DB


class RegistrationForm(FlaskForm):
    '''
    Validates the registration details
    '''
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = DB.is_user_exist(username.data)
        if user:
            raise ValidationError('Entered username is already taken.  Choose a different one.')

    def validate_email(self, email):
        user = DB.is_email_exist(email.data)
        if user:
            raise ValidationError('Entered email is already taken.  Choose a different one.')


class LoginForm(FlaskForm):
    '''
    Validates the login details
    '''
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    '''
    Validates the updated user details
    '''
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Upload Display Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.user_json['name']:
            user = DB.is_user_exist(username)
            if user:
                raise ValidationError('Entered username is already taken.  Choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.user_json['email']:
            user = DB.is_email_exist(email)
            if user:
                raise ValidationError('Entered email is already taken.  Choose a different one.')
