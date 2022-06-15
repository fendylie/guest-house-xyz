from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import InputRequired


class BookingForm(FlaskForm):
    user_id = SelectField("User", coerce=int, choices=[], validators=[InputRequired('User is required')])
    room_id = SelectField("Room", coerce=int, choices=[], validators=[InputRequired('Room is required')])
    person = IntegerField("Person", validators=[InputRequired('Person is required')])
    check_in = DateField("Check In", validators=[InputRequired('Check In is required')])
    check_out = DateField("Check Out", validators=[InputRequired('Check Out is required')])

    submit = SubmitField("Submit")


class UserBookingForm(FlaskForm):
    room_id = SelectField("Room", coerce=int, choices=[], validators=[InputRequired('Room is required')])
    person = IntegerField("Person", validators=[InputRequired('Person is required')])
    check_in = DateField("Check In", validators=[InputRequired('Check In is required')])
    check_out = DateField("Check Out", validators=[InputRequired('Check Out is required')])

    submit = SubmitField("Submit")
