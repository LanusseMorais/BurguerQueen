from app.models import db, Order


class OrderService:
    def __init__(self, external_payment_service):
        self.external_payment_service = external_payment_service

    def create_order(self, customer, items):

        new_order = Order(customer=customer, items=items, status="preparação")
        db.session.add(new_order)
        db.session.commit()

        payment_status = self.external_payment_service.process_payment(
            customer, new_order)

        if payment_status == "pago":
            new_order.status = "pronto"
            db.session.commit()
            return new_order
        else:
            db.session.delete(new_order)
            db.session.commit()
            return None
