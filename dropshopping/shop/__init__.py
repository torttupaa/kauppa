from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
import paypalrestsdk

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AZGDhsIWJShUZn5N1MgPHrU90vZ274Xatnu0anUmhi5sm16pDwK2wptKXxzv7-eyrGdzdSZzf8IYgsS6",
  "client_secret": "ECJbULZYxa-5ajDRm4YxFbjBn5kodZ4p2mB6ZPYchrzfv-9SN75d-m8hlu83-1PiF-nx_nLHBcRuN7rv" })


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'ui546h4jhio46oi46ioj45'


app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app, 32 * 1024 * 1024)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from shop.admin import routes
from shop.products import routes
from shop.carts import carts