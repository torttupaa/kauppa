from shop import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    color = db.Column(db.String(30), nullable=False)

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')


class Front(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_4 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_5 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_6 = db.Column(db.String(150), nullable=False, default='image.jpg')
    img_amount = db.Column(db.Integer, nullable=False, default=0)

db.create_all()