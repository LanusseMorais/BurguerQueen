from app.models.order import Order


def payment_validation(order_id):
    order = Order.query.get(order_id)

    if order is None:
        return False

    return True
