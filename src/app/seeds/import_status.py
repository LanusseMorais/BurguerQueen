import json
# from app.models import db
from app.models.order import OrderStatus


def import_status(db):
    with open('app/resources/status.json', 'r') as json_file:
        status_data = json.load(json_file)

    for data in status_data:
        new_status = OrderStatus(name=data['name'])
        db.session.add(new_status)
    db.session.commit()
