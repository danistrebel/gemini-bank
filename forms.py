from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, TextAreaField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional


class RegisterForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(),Email()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Retype password", validators=[DataRequired(),EqualTo("password1")])
    submit = SubmitField("Register user")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log in")

class CreateAccountForm(FlaskForm):
    submit = SubmitField("Create Account")

class TransactionForm(FlaskForm):
    description = TextAreaField("Description", validators=[DataRequired()])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0)], places=2, rounding=None)
    currency = SelectField("Currency", validators=[DataRequired()], choices=[
        ("EUR", "EUR"), ("USD", "USD"), ("GBP", "GBP"), ("CHF", "CHF"),
        ("SEK", "SEK"), ("NOK", "NOK"), ("DKK", "DKK"), ("PLN", "PLN"),
        ("CZK", "CZK"), ("HUF", "HUF"), ("RON", "RON"), ("BGN", "BGN")
    ], default="EUR")
    type = SelectField("Transaction Type", validators=[DataRequired()], choices=[("deposit","Deposit"),("transfer","Transfer")])
    submit = SubmitField("Make Transaction")

class RecurringPaymentForm(FlaskForm):
    description = TextAreaField("Description", validators=[DataRequired()])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0)], places=2, rounding=None)
    currency = SelectField("Currency", validators=[DataRequired()], choices=[
        ("EUR", "EUR"), ("USD", "USD"), ("GBP", "GBP"), ("CHF", "CHF"),
        ("SEK", "SEK"), ("NOK", "NOK"), ("DKK", "DKK"), ("PLN", "PLN"),
        ("CZK", "CZK"), ("HUF", "HUF"), ("RON", "RON"), ("BGN", "BGN")
    ], default="EUR")
    frequency = SelectField("Frequency", validators=[DataRequired()], choices=[
        ("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly"), ("yearly", "Yearly")
    ])
    start_date = DateField("Start Date", validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField("End Date", validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField("Set Recurring Payment")