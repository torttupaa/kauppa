from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField


class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])

    image_1 = FileField('Image_1', validators=[FileAllowed(['jpg', 'png'], message="asd")])
    image_2 = FileField('Image_2', validators=[FileAllowed(['jpg', 'png'], message="asd")])


class Frontpage(Form):
    image_1 = FileField('Image_1', validators=[FileAllowed(['jpg', 'png'], message="asd")])
    image_2 = FileField('Image_2', validators=[FileAllowed(['jpg', 'png'], message="asd")])
    image_3 = FileField('Image_3', validators=[FileAllowed(['jpg', 'png'], message="asd")])
    image_4 = FileField('Image_4', validators=[FileAllowed(['jpg', 'png'], message="asd")])
    image_5 = FileField('Image_5', validators=[FileAllowed(['jpg', 'png'], message="asd")])
    image_6 = FileField('Image_6', validators=[FileAllowed(['jpg', 'png'], message="asd")])
    img_amount = IntegerField('Number of Images shown', default=0)