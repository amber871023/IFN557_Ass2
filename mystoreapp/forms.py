from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired

# form used in basket
class CheckoutForm(FlaskForm):
    firstname = StringField("Your first name", validators=[InputRequired()])
    lastname = StringField("Your last name", validators=[InputRequired()])
    email = StringField("Your email", validators=[InputRequired()])
    phone = StringField("Your phone number", validators=[InputRequired()])
    submit = SubmitField("Submit")
