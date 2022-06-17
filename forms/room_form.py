from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, NumberRange


class RoomForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired('Name is required')])
    hotel_id = SelectField("Hotel", coerce=int, choices=[], validators=[InputRequired('Hotel is required')])
    max_person = IntegerField("Max Person", validators=[InputRequired("Max Person is required"), NumberRange(min=1)])
    price = IntegerField("Price", validators=[InputRequired('Price is required')])
    description = TextAreaField("Description", default="")

    submit = SubmitField("Submit")
