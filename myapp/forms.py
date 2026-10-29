from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .extensions import db
from .models import User


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 30)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField(
        "Konfirmasi Password",
        validators=[DataRequired(), EqualTo("password", message="Password tidak sama.")],
    )
    submit = SubmitField("Daftar")

    def validate_username(self, field):
        if db.session.scalar(db.select(User).where(User.username == field.data)):
            raise ValidationError("Username sudah dipakai.")

    def validate_email(self, field):
        email = field.data.lower()
        if db.session.scalar(db.select(User).where(User.email == email)):
            raise ValidationError("Email sudah terdaftar.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Ingat saya")
    submit = SubmitField("Masuk")
