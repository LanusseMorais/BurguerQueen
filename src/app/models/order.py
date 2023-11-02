from app.models.db import db
from sqlalchemy import DateTime


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'))

    status_id = db.Column(db.Integer, db.ForeignKey(
        'order_status.id'), nullable=False)
    consumption = db.Column(db.String(10))
    total = db.Column(db.Float, nullable=False, default=0.0)
    time = db.Column(DateTime)

    customer = db.relationship('Customer', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order')
    status = db.relationship('OrderStatus', backref='orders')


class OrderStatus(db.Model):
    __tablename__ = 'order_status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'menu_items.id'), nullable=False)

    extras = db.relationship(
        'OrderItemExtras', backref='order_item', lazy='dynamic')
    removed_ingredients = db.relationship(
        'OrderItemRemovedIngredients', backref='order_item', lazy='dynamic')

    order = db.relationship('Order', back_populates='items')
    item = db.relationship('MenuItem', back_populates='order_items')


class OrderItemRemovedIngredients(db.Model):
    __tablename__ = 'order_item_removed_ingredients'
    id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_items.id'))
    removed_ingredient = db.Column(db.String(50), nullable=False)


class OrderItemExtras(db.Model):
    __tablename__ = 'order_item_extras'

    id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer, db.ForeignKey(
        'order_items.id'), nullable=False)
    extra_name = db.Column(db.String(100), nullable=False)
