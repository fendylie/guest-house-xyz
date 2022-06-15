from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange


class HotelForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired('Name is required')])
    phone_number = StringField("Phone Number", validators=[InputRequired('Phone Number is required'), Length(min=10, max=13)])
    location = StringField("Location", validators=[InputRequired('Location is required')])
    rating = IntegerField("Rating", validators=[InputRequired("Rating is required"), NumberRange(min=0, max=5)])

    submit = SubmitField("Submit")
