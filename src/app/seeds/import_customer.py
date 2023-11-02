import json
# from app.models import db
from app.models.customer import Customer


def import_customer(db):
    with open('app/resources/customer.json', 'r') as json_file:
        customer_data = json.load(json_file)

    for data in customer_data:
        cpf = data.get('cpf', '')
        name = data.get('name', '')
        email = data.get('email', '')
        registration_date = data.get(
            'registration_date', '')
        new_customer = Customer(
            cpf=cpf, name=name, email=email, registration_date=registration_date)

        db.session.add(new_customer)
    db.session.commit()
