from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextField
from wtforms.validators import DataRequired, Length, Email


class SignupForm(FlaskForm):
    """Render and validate the signup form"""
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email format"), Length(max=32)])
    username = StringField("Username", validators=[DataRequired(), Length(2, 32)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=32)])


class LoginForm(FlaskForm):
    """Form to let users login"""
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email format"), Length(max=32)])
    password = PasswordField("Password", validators=[DataRequired(), Length(4, 32)])
    remember = BooleanField("Remember Me")


class ShoplistForm(FlaskForm):
    """Form to CRUd a  Shoplist"""
    name = StringField("Name", validators=[DataRequired()])
    description = TextField("Description", validators=[DataRequired()])


class ActivityForm(FlaskForm):
    """Form to CRUd a  Shoplist item"""
    title = StringField("Title", validators=[DataRequired()])
    description = TextField("Description", validators=[DataRequired()])
    status = BooleanField("Status", default=True)
