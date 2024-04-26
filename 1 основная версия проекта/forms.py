from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# Этот код определяет класс формы регистрации пользователей для веб-приложения, используя библиотеки Flask-WTF и WTForms. Класс RegistrationForm наследуется от FlaskForm и содержит следующие поля:

# name: строковое поле для ввода имени пользователя.
# surname: строковое поле для ввода фамилии пользователя.
# age: поле типа целого числа для ввода возраста пользователя.
# address: строковое поле для ввода адреса пользователя.
# email: строковое поле для ввода адреса электронной почты пользователя с валидацией формата почты.
# password: поле типа пароля для ввода пароля пользователя с валидацией минимальной длины в 8 символов.
# submit: кнопка отправки формы с меткой "Register".



class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')



