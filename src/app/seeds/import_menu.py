import json
# from app.models import db
from app.models.menu_item import MenuItem
import os


def import_menu(db):
    with open('app/resources/menu.json', 'r') as menu_file:
        menu_data = json.load(menu_file)
        menu_items = menu_data.get("menu_items", [])

        for item_data in menu_items:
            menu_item = MenuItem(
                name=item_data["name"],
                description=item_data["description"],
                category_id=item_data["category_id"],
                ingredients=item_data.get("ingredients", ""),
                extras=item_data.get("extras", ""),
                price=item_data["price"]
            )
            db.session.add(menu_item)
        db.session.commit()
