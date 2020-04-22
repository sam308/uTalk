from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from passlib.hash import pbkdf2_sha256
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User

def invalid_credentials(form, field):
    """ USERNAME and PASSWORD checker"""
    e_username = form.username.data
    e_password = field.data

    user_object = User.query.filter_by(username=e_username).first()
    if user_object is None:
        raise ValidationError("Username or Password is incorrect!")

    elif not pbkdf2_sha256.verify(e_password, user_object.password):
        raise ValidationError("Username or Password is incorrect!")

    



class RegistrationForm(FlaskForm):
    """ The general registration form """

    username=StringField('label_username', validators=[InputRequired(message="Username can't remain empty"), Length(min=4, max=15, message="Username must be between 4 and 15 characters!")] )
    password=PasswordField('label_password', validators=[InputRequired(message="Password can't remain empty"), Length(min=6, message="Password must be of atleast 6 characters!")])
    confirm_password=PasswordField('label_confirm_password', validators=[InputRequired(message="Password can't remain empty"), EqualTo('password', message="Passwords must match!")])
    submit_button=SubmitField('Create User')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username is already taken. Try another one!")


class LoginForm(FlaskForm):
    """The general login form"""

    username=StringField('label_username', validators=[InputRequired(message="Username required!")])
    password=PasswordField('label_password', validators=[InputRequired(message="Password required!"), invalid_credentials])
    submit_button=SubmitField('Log In')