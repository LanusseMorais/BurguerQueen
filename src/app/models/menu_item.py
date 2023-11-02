from app.models.db import db


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    ingredients = db.Column(db.String(255))
    extras = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_categories.id'))

    order_items = db.relationship('OrderItem', back_populates='item')
    category = db.relationship('MenuCategory', back_populates='menu_items')

    def __init__(self, name, description, category_id, ingredients, extras, price):
        self.name = name.lower()
        self.description = description
        self.ingredients = ingredients
        self.extras = extras
        self.price = price
        self.category_id = category_id

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category.name,
            'ingredients': self.ingredients,
            'extras': self.extras,
            'price': self.price
        }

    def __repr__(self):
        return f'<MenuItem {self.name}>'


class MenuCategory(db.Model):
    __tablename__ = 'menu_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    menu_items = db.relationship('MenuItem', back_populates='category')

    def __init__(self, name):
        self.name = name
