from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class SingInForm(FlaskForm):
    email=StringField("email", validators=[DataRequired()])
    password = PasswordField("passowrd", validators=[DataRequired()])
    name=StringField("name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")
    
class LogInForm(FlaskForm):
    email=StringField("email", validators=[DataRequired()])
    password = PasswordField("passowrd", validators=[DataRequired()])
    submit = SubmitField(" LOG IN!")
    