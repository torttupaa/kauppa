from shop import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(180), unique=False, nullable=False)
    zipcode = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.String(25), unique=False, nullable=False)
    item_quantities = db.Column(db.String(200), unique=False, nullable=False)
    is_ordered = db.Column(db.Integer, unique=False, nullable=False)
    is_sent = db.Column(db.Integer, unique=False, nullable=False)


db.create_all()