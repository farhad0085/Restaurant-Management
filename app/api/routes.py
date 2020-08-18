from flask import Blueprint, request, jsonify
from pprint import pprint
from app.models import MenuItem, MenuOrder, ItemOrderQuantity
from app import app, db

api = Blueprint("api", __name__)

@api.route("/api/orders", methods=['POST'])
def new_order():
    """
    REST INPUT
    {
        item: [
            {
                food_id : 1,
                quantity: 5
            },
            {
                food_id: 2,
                quantity: 2
            }
        ],
        customer_name: "Farhad"
    }
    """
    data = request.get_json()
    pprint(data)

    customer_name = data['customer_name']

    totalPrice = 0
    order = MenuOrder(customer_name=customer_name)
    for item in data['item']:
        if item['food_checked']:
            item_id = item['food_id'][10:]
            quantity = int(item['quantity'])
            
            item = MenuItem.query.get(item_id)
            if not item or not item.available:
                return jsonify({"status": "error", "message": "Food not available"})
            totalPrice = totalPrice + (item.price * quantity)
            order.cost = totalPrice
            order.menu_items.append(item)
            db.session.add(order)
            db.session.commit()
            order_item_quantity = ItemOrderQuantity(item_id=item.id,
                                                    order_id=order.id,
                                                    quantity=quantity)
            db.session.add(order_item_quantity)
    db.session.commit()

    return jsonify({"message": "Success", "status": "OK"})
