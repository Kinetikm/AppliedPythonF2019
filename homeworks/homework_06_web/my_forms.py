from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import Required, NumberRange, Optional


class NewFlight(FlaskForm):
    class Meta:
        csrf = False
    departure_time = IntegerField('dep_time', [Required(), NumberRange(min=0)])
    arrival_time = IntegerField('arr_time', [Required(), NumberRange(min=0)])
    flight_time = IntegerField('flight_time', [Required(), NumberRange(min=0)])
    destination_airport = StringField('dest_airport', [Required()])


class EditFlight(FlaskForm):
    class Meta:
        csrf = False
    departure_time = IntegerField('dep_time', [Optional(), NumberRange(min=0)])
    arrival_time = IntegerField('arr_time', [Optional(), NumberRange(min=0)])
    flight_time = IntegerField('flight_time', [Optional(), NumberRange(min=0)])
    destination_airport = StringField('dest_airport', [Optional()])
    if (not (departure_time or arrival_time or flight_time or destination_airport)):
        raise ValidationError('Nothing to edit')
