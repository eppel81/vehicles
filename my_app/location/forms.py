from wtforms import Form, StringField, PasswordField, BooleanField, IntegerField, \
    SelectMultipleField, SelectField, DateField, DateTimeField
from wtforms.validators import InputRequired, EqualTo
from datetime import datetime


class RegistrationForm(Form):
    login = StringField('Login', [InputRequired()])
    name = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(Form):
    login = StringField('Login', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])


class ManageUser(Form):
    """
    Form for manage user's parameters
    """
    user_id = IntegerField('User ID')
    login = StringField('Login')
    password = PasswordField('Password')
    name = StringField('Username')
    locked = BooleanField('Locked')
    admin = SelectField('Admin status', coerce=int)
    # user_vehicles = SelectMultipleField('Vehicles', choices=[('1', '8am'), ('2', '10am'),])


class ChangePass(Form):
    old_pass = PasswordField('Old password', [InputRequired()])
    new_pass = PasswordField('New password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm password', [InputRequired()])


class UpdateSettings(Form):
    """
    Form for manage system parameters
    """
    name = StringField('Configuration name')
    description = StringField('Description')
    max_objects = IntegerField('Max vehicles on map')
    max_points = IntegerField('Max points on map')


class ReportVehicle(Form):
    """
    Form for selection vehicle and show report for period for time
    """
    vehicles = SelectField('Vehicles', [InputRequired()], coerce=int)
    # date_from = DateTimeField('Date from', [InputRequired()], format='%d-%m-%Y %H:%M:%S')
    # date_to = DateTimeField('Date to', [InputRequired()], format='%d-%m-%Y %H:%M:%S')
    date_from = DateField('Date from', [InputRequired()], format='%d-%m-%Y', default=datetime.today)
    date_to = DateField('Date to', [InputRequired()], format='%d-%m-%Y', default=datetime.today)

