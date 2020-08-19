from flask import Blueprint, request, jsonify
from pprint import pprint
from app.models import MenuItem, MenuOrder, ItemOrderQuantity, Settings
from app import app, db

api = Blueprint("api", __name__)

settings = Settings.query.first()

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
    # pprint(data)

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

    response = {}
    response['order_id'] = order.id
    response['order_cost'] = order.cost
    response['customer_name'] = order.customer_name
    response['updated'] = order.updated
    response['is_complete'] = order.is_complete
    response['wait_time'] = order.wait_time
    response['is_ready'] = order.is_ready

    return jsonify({"message": "Order submitted successfully",
                    "status": "OK",
                    "response": response})


@app.route("/api/status/order", methods=['POST'])
def check_order_status():

    data = request.get_json()
    order_id = data['order_id']

    order = MenuOrder.query.get(order_id)
    
    response = {}

    if not order:
        return jsonify({"message": "Oops! Order not found",
                    "status": "error",
                    "response": response}) 

    response['order_id'] = order.id
    response['order_cost'] = str(order.cost) + " " + settings.currency_sign
    response['customer_name'] = order.customer_name
    response['updated'] = order.updated.strftime("%d-%m-%Y %I:%M %p")
    response['is_complete'] = "Yes" if order.is_complete else "Not Yet"
    response['wait_time'] = "Almost Ready" if order.wait_time < 2 else str(order.wait_time) + " Minute(s)"
    response['is_ready'] = "Yes" if order.is_ready else "Not Yet"

    response['items'] = []
    for item_quantity in order.menu_items_quantity:
        item_quantity_dict = {}
        item = MenuItem.query.filter_by(id=item_quantity.item_id).first()
        item_quantity_dict['id'] = item_quantity.id
        item_quantity_dict['item_name'] = item.name
        item_quantity_dict['item_price'] = item.price
        item_quantity_dict['quantity'] = item_quantity.quantity
        response['items'].append(item_quantity_dict)

    print(response)

    return jsonify({"message": "Order Info",
                    "status": "OK",
                    "response": response})



