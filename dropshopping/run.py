from shop import app
#from multiprocessing import Process, Queue
import time
from shop.carts.models import Order
from shop import db

def website():
    app.run(debug=True)

def tilausohjelma(order_jono):
    while True:
        time.sleep(5)
        tilaus_id = order_jono.get()
        print(tilaus_id)
        orders = Order.query.all()
        for order in orders:
            if order.id == tilaus_id:
                order.is_ordered = 1
                db.session.commit()
                time.sleep(1)
                print(order.item_quantities)

if __name__ == "__main__":
    app.run(debug=True)
