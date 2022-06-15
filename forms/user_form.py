from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length


class UserRegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired('Name is required')])
    phone_number = StringField("Phone Number", validators=[Length(min=10, max=13)])
    email = EmailField("Email", validators=[InputRequired('Email is required')])
    password = PasswordField("Password", validators=[InputRequired('Password is required'), Length(min=6)])

    submit = SubmitField("Submit")


class UserLoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired('Email is required')])
    password = PasswordField("Password", validators=[InputRequired('Password is required'), Length(min=6)])

    submit = SubmitField("Login")


# class UserForm(FlaskForm):
#     name = StringField("Name", validators=[InputRequired('Name is required')])
#     phone_number = StringField("Phone Number", validators=[Length(min=10, max=13)])
#     email = EmailField("Email", validators=[InputRequired('Email is required')])
#     password = PasswordField("Password", validators=[InputRequired('Password is required'), Length(min=6)])
#
#     submit = SubmitField("Submit")