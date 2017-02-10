# _*_ coding: utf-8 _*_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import required, Length, Email,Regexp, EqualTo
from wtforms import ValidationError
from ..models.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[required(), Length(1, 64),Email()])
    password = PasswordField('Password', validators=[required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[required(), Length(1, 64),Email()])
    username = StringField('Username', validators=[required(), Length(1, 64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                                                     'Usernames must have only letters,'
                                                                                     'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')