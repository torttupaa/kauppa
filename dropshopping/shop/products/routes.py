from flask import redirect, render_template, url_for, flash,request,session, current_app
from shop import db, app, photos
from .models import Product, Front
from shop.carts.models import Order
from .forms import Addproducts, Frontpage
import random
import os

@app.route('/', methods=['GET','POST'])
def front():
    frontti = Front.query.get_or_404(1)
    return render_template('/products/front.html', title='home', frontti=frontti)


@app.route('/frontedit', methods=['GET','POST'])
def front_edit():
    form = Frontpage(request.form)
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))

    if request.method == 'POST':  # and form.validate():
        try:
            frontti = Front.query.get_or_404(1)
            print(frontti.image_1)
            if request.files.get('image_1'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + frontti.image_1))
                    frontti.image_1 = photos.save(request.files.get('image_1'), name=randomletters(30) + ".jpg")
                except:
                    print("kuvan poisto ei onnistunut", frontti.image_1)
                    frontti.image_1 = photos.save(request.files.get('image_1'), name=randomletters(30) + ".jpg")
            if request.files.get('image_2'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + frontti.image_2))
                    frontti.image_2 = photos.save(request.files.get('image_2'), name=randomletters(30) + ".jpg")
                except:
                    print("kuvan poisto ei onnistunut", frontti.image_2)
                    frontti.image_2 = photos.save(request.files.get('image_2'), name=randomletters(30) + ".jpg")
            if request.files.get('image_3'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + frontti.image_3))
                    frontti.image_3 = photos.save(request.files.get('image_3'), name=randomletters(30) + ".jpg")
                except:
                    print("kuvan poisto ei onnistunut", frontti.image_3)
                    frontti.image_3 = photos.save(request.files.get('image_3'), name=randomletters(30) + ".jpg")
            if request.files.get('image_4'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + frontti.image_4))
                    frontti.image_4 = photos.save(request.files.get('image_4'), name=randomletters(30) + ".jpg")
                except:
                    print("kuvan poisto ei onnistunut", frontti.image_4)
                    frontti.image_4 = photos.save(request.files.get('image_4'), name=randomletters(30) + ".jpg")
            if request.files.get('image_5'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + frontti.image_5))
                    frontti.image_5 = photos.save(request.files.get('image_5'), name=randomletters(30) + ".jpg")
                except:
                    print("kuvan poisto ei onnistunut", frontti.image_5)
                    frontti.image_5 = photos.save(request.files.get('image_5'), name=randomletters(30) + ".jpg")
            if request.files.get('image_6'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + frontti.image_6))
                    frontti.image_6 = photos.save(request.files.get('image_6'), name=randomletters(30) + ".jpg")
                except:
                    print("kuvan poisto ei onnistunut", frontti.image_6)
                    frontti.image_6 = photos.save(request.files.get('image_6'), name=randomletters(30) + ".jpg")

            frontti.color = form.img_amount.data
            db.session.commit()

        except:
            image_1 = photos.save(request.files.get('image_1'), name=randomletters(30) + ".jpg")
            image_2 = photos.save(request.files.get('image_2'), name=randomletters(30) + ".jpg")
            image_3 = photos.save(request.files.get('image_3'), name=randomletters(30) + ".jpg")
            image_4 = photos.save(request.files.get('image_4'), name=randomletters(30) + ".jpg")
            image_5 = photos.save(request.files.get('image_5'), name=randomletters(30) + ".jpg")
            image_6 = photos.save(request.files.get('image_6'), name=randomletters(30) + ".jpg")
            img_amount = form.img_amount.data
            frontti = Front(image_1 = image_1,image_2 = image_2,image_3 = image_3,image_4 = image_4,image_5 = image_5,image_6 = image_6, img_amount=img_amount)
            db.session.add(frontti)
            db.session.commit()
            print("post")
    return render_template('/products/front_edit.html', title='home', form=form)


@app.route('/products')
def home():
    page = request.args.get('page',1 ,type=int)
    nakyy = 1
    products = Product.query.filter(Product.stock > 0).paginate(page=page, per_page=nakyy)
    tuotteita = int(Product.query.filter(Product.stock > 0).count())
    return render_template('products/products.html', title="Products", products=products, nakyy = nakyy, tuotteita=tuotteita )

@app.route('/product/<int:id>')
def details(id):
    product = Product.query.get_or_404(id)
    return render_template('products/details.html', title="Details", product=product)


@app.route('/Addproduct', methods=['GET','POST'])
def addproduct():

    form = Addproducts(request.form)
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))
    if request.method == 'POST':# and form.validate():
        image_1 = photos.save(request.files.get('image_1'), name=randomletters(30) + ".jpg")
        image_2 = photos.save(request.files.get('image_2'), name=randomletters(30) + ".jpg")
        product = Product(name=form.name.data, price=form.price.data, discount=form.discount.data, stock=form.stock.data, description=form.description.data, color=form.colors.data, image_1 = image_1,image_2 = image_2)
        db.session.add(product)
        db.session.commit()
        flash(str(form.name.data) +' Added')
    return render_template('products/addproduct.html', title="Add product page", form = form)


#tavallaan kuuluu kyl varmaa adminhommiin :--D
@app.route('/showproducts', methods=['GET','POST'])
def show_db():
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))
    products = Product.query.all()
    if request.method=='POST':
        print("mitävittua")


    return render_template('products/dbshow.html', title="Product db", products=products)

@app.route('/ordershow', methods=['GET','POST'])
def show_order():
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))
    orders = Order.query.all()
    if request.method=='POST':
        print("mitävittua")
    return render_template('products/ordershow.html', title="order db", orders=orders)

@app.route('/updateorder_ordered/<int:code>', methods=['POST'])
def updateorder_ordered(code):
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))
    try:
        order = Order.query.get_or_404(code)
        if order.is_ordered == 1:
            order.is_ordered = 0
        else:
            order.is_ordered = 1
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('show_order'))


@app.route('/updateorder_sent/<int:code>', methods=['POST'])
def updateorder_sent(code):
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))
    try:
        order = Order.query.get_or_404(code)
        if order.is_sent == 1:
            order.is_sent = 0
        else:
            order.is_sent = 1
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('show_order'))


@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))

    product = Product.query.get_or_404(id)
    form = Addproducts(request.form)

    if request.method == 'POST':  # and form.validate():
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.description = form.description.data
        product.color = form.colors.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=randomletters(30) + ".jpg")
            except:
                print("kuvan poisto ei onnistunut",product.image_1)
                product.image_1 = photos.save(request.files.get('image_1'), name=randomletters(30) + ".jpg")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+ product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=randomletters(30) + ".jpg")
            except:
                print("kuvan poisto ei onnistunut",product.image_2)
                product.image_2 = photos.save(request.files.get('image_2'), name=randomletters(30) + ".jpg")
        db.session.commit()
        flash(str(form.name.data) + ' Updated')
        return redirect(url_for("show_db"))


    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.description
    form.colors.data = product.color




    return render_template('products/updateproduct.html', title="Edit", form = form, product=product)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    try:
        if 'Admin' not in session['username']:
            return redirect(url_for('login'))
    except:
        print("nobodys session")
        return redirect(url_for('login'))
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
        except:
            print("kuvan poisto ei onnistunut", product.image_1)
        db.session.delete(product)
        db.session.commit()

        flash(str(product.name) + ' Deleted')
        return redirect(url_for("show_db"))
    return redirect(url_for("show_db"))



def randomletters(maara):
    aakkosetnumerot = "1234567890qwertyuiopasdfghjklzxcvbnm"
    rand_merkit = ""
    for i in range(maara):
        rand_merkit += aakkosetnumerot[random.randint(0,len(aakkosetnumerot)-1)]
    return rand_merkit
