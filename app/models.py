from flask_login import UserMixin
from app import db, login_manager, app
import datetime

# this will handle user session, so we don't need to do anything
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.username}"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20))

    items = db.relationship('MenuItem', backref='category')

    def __repr__(self):
        return f"{self.id} - {self.category_name}"

item_order = db.Table('item_order',
                    db.Column('item_id',
                                db.Integer,
                                db.ForeignKey('menu_item.id'), nullable=False),
                    db.Column('order_id',
                                db.Integer,
                                db.ForeignKey('menu_order.id')))


class ItemOrderQuantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('menu_order.id'))
    quantity = db.Column(db.Integer)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer, default=0)
    quantity = db.Column(db.Integer, default=0)
    weight = db.Column(db.Integer, default=0)
    available = db.Column(db.Integer, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    menu_items_quantity = db.relationship('ItemOrderQuantity', backref='item')

    def __repr__(self):
        return f"{self.name} - {self.price}"
    
class MenuOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(30))
    cost = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=datetime.datetime.now)
    is_complete = db.Column(db.Integer, default=0)
    wait_time = db.Column(db.Integer, default=10) # in minutes
    is_ready = db.Column(db.Integer, default=0)

    menu_items = db.relationship('MenuItem',
                            secondary=item_order,
                            backref=db.backref('menu_orders',
                                                lazy='dynamic'))

    menu_items_quantity = db.relationship('ItemOrderQuantity', backref='order')

    def __repr__(self):
        return f"{self.cost} - {self.is_complete}"

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(50), default="Restaurant Management")
    site_tagline = db.Column(db.String(300), default="Build with Flask")
    currency_sign = db.Column(db.String(10), default="Taka")
    admin_email = db.Column(db.String(60))