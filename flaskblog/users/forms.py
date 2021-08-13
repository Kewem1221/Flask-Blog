from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, ValidationError, data_required, length, equal_to
from flaskblog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', [data_required(), length(min=2, max=20)])
    email = StringField('Email', [data_required(), Email()])
    password = PasswordField('Password', [data_required()])
    confirm_password = PasswordField(
        'Confirm Password', [data_required(), equal_to('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken.')


class LoginForm(FlaskForm):
    email = StringField('Email', [data_required(), Email()])
    password = PasswordField('Password', [data_required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username', [data_required(), length(min=2, max=20)])
    email = StringField('Email', [data_required(), Email()])
    picture = FileField('Update profile picture', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', [data_required(), Email()])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email is not registered.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', [data_required()])
    confirm_password = PasswordField(
        'Confirm Password', [data_required(), equal_to('password')])
    submit = SubmitField('Reset password')
