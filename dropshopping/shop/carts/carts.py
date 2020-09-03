from flask import redirect, render_template, url_for, flash,request,session, current_app, jsonify
from shop import db, app, photos
from shop.products.models import Product
from .forms import ShippingForm
from .models import Order
import paypalrestsdk


def combdicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1+dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items())+ list(dict2.items()))
    return False

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and color and request.method=='POST':
            DictItems = {product_id:{"name": product.name, "price": float(product.price), "discount": product.discount,
                                     "color": color, "quantity":quantity,"image":product.image_1,"colors":product.color }}
            #print(DictItems)

            if 'Shoppingcart' in session:
                #print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    flash("Product already in cart")
                else:
                    session['Shoppingcart'] = combdicts(session['Shoppingcart'],DictItems)
                    flash(product.name + ' added to cart')
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                flash(product.name + ' added to cart')
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/cart')
def getCart():
    if ('Shoppingcart' not in session) or (len(session['Shoppingcart'])) <= 0:
        return redirect(url_for('home'))
    total = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100)*float(product['price'])
        total += float((product['price'])-discount)*int(product['quantity'])

    return render_template('products/cart.html', total=total)

@app.route('/update/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shopppingcart'])<=0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity']=quantity
                    item['color']=color
                    flash(item['name']+' updated')
                    return redirect(url_for('getCart'))

        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
        return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/shipinfo', methods=['GET', 'POST'])
def shipping():
    if ('Shoppingcart' not in session) or (len(session['Shoppingcart'])) <= 0:
        return redirect(url_for('home'))
    form = ShippingForm(request.form)
    if request.method == 'POST' and form.validate():
        DictItems = {"name": form.username.data, "email": form.email.data, "addres": form.address.data,
                                  "zipcode": form.postcode.data, "phone": form.phone.data}
        session['Shipinfo'] = DictItems
        #print(session['Shipinfo']['name'])
        return redirect(url_for('payment'))
    return render_template('products/shipping.html', form=form)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if ('Shoppingcart' not in session) or (len(session['Shoppingcart'])) <= 0:
        return redirect(url_for('home'))
    total = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100)*float(product['price'])
        total += float((product['price'])-discount)*int(product['quantity'])
        total = round(total,2)
    if request.method == 'POST':
        print(total)
        #TASSAKOHDASSA LAHTEE NII VITUSTI SAHKOPOSTIA TILAUKSESTA

    return render_template('products/payment.html',total=total)

@app.route('/paymentt', methods=['POST'])
def paymentt():

    items = []
    total = 0
    price = 0
    sku = 345

    #generate payment
    for key, product in session['Shoppingcart'].items():
        #print(product['name'])
        #[{"name": "testitem","sku": "123545","price": "10.00","currency": "USD","quantity": 1}]
        price = round((float(product['price'])-((float(product['discount']))/100)*float(product['price'])),2)
        items.append({"name": str(product['name'])+" "+str(product['color']),"price": str(price),"currency": "EUR","quantity": int(product['quantity'])})
        total += (price* int(product['quantity']))
        sku += 1
        #print(str(price* int(product['quantity'])))
    #print(round(total,2))

    #"shipping_address":{"recipient_name": "Brian Robinson","line1": "4th Floor","line2": "Unit #34","city": "San Jose","country_code": "US","postal_code": "95131","phone": "011862212345678","state": "CA"}

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:5000/",
            "cancel_url": "http://localhost:5000/"},
        "transactions": [{
            "item_list": {
                "items": items},
            "amount": {
                "total": str(round(total,2)),
                "currency": "EUR"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment create success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
        item_quantities = ""
        for key, product in session['Shoppingcart'].items():
            item_quantities+=str(str(product['quantity'])+" "+ str(product['name']) + "-" + str(product['color']) + " ")
            #item_quantities.append([str(product['quantity']), str(product['name']) + " " + str(product['color'])])

        order = Order(name=str(session['Shipinfo']['name']), email=str(session['Shipinfo']['email']),address=str(session['Shipinfo']['addres']), zipcode=str(session['Shipinfo']['zipcode']),phone=str(session['Shipinfo']['phone']), item_quantities=item_quantities, is_ordered=0, is_sent=0)
        db.session.add(order)
        db.session.commit()

        session.clear()
        flash("SUCCESFUL PAYMENT")
    else:
        print(payment.error)

    return jsonify({'success' : success})

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)