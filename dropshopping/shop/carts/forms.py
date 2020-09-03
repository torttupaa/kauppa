from wtforms import Form, BooleanField, StringField, validators, IntegerField

class ShippingForm(Form):
    username = StringField('Name', [validators.DataRequired(),validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.DataRequired(),validators.Length(min=6, max=69), validators.Email('Not valid email')])
    address = StringField('Address', [validators.DataRequired(),validators.Length(min=4, max=25)])
    postcode = IntegerField('Zipcode', [validators.DataRequired()])
    phone = StringField('Phone num', [validators.Length(min=4, max=25)])