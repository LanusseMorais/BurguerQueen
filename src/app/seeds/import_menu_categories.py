import json
# from app.models import db
from app.models.menu_item import MenuCategory


def import_menu_categories(db):
    with open('app/resources/categories.json', 'r') as json_file:
        categories_data = json.load(json_file)

    for data in categories_data:
        category = MenuCategory(name=data['name'])
        db.session.add(category)
    db.session.commit()
