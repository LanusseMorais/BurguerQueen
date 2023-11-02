from flask import Blueprint
from flask_restx import Resource, Namespace, fields
from app.adapters.payment_adapter import payment_validation
from app.models.order import Order, OrderItem, OrderItemRemovedIngredients, OrderItemExtras, OrderStatus
from app.models.menu_item import MenuItem
from app.models.customer import Customer
from app.models.db import db
from datetime import datetime

order_routes = Blueprint('order_routes', __name__)

order_namespace = Namespace(
    'order', description='Operações relacionadas a pedidos')

order_item_model = order_namespace.model('OrderItem', {
    'item_id': fields.Integer(description='ID do item', required=True, example=1),
    'extras': fields.List(fields.String, description='Lista de extras', example=["Bacon"]),
    'removed_ingredients': fields.List(fields.String, description='Lista de ingredientes removidos', example=["alface"])
})

order_model = order_namespace.model('Order', {
    'customer_cpf': fields.String(description='CPF do cliente', required=False, example="788.612.610-60"),
    'consumption': fields.String(description='Forma de consumo sendo elas local ou viagem', required=True, example="local"),
    'order_items': fields.List(fields.Nested(order_item_model), description='Itens do pedido', required=True),
})

order_post_model = order_namespace.model('', {
    'status': fields.String(required=True, description='Status do pedido. Use "f" para "Pronto" ou "n" para "Finalizado.', example='p')
})


@order_namespace.route('', methods=['GET', 'POST'])
class OrderResource(Resource):
    @order_namespace.expect(order_model)
    @order_namespace.doc(responses={201: 'Pedido criado com sucesso'})
    def post(self):
        data = order_namespace.payload
        customer_cpf = data.get('customer_cpf', None)
        consumption = data.get('consumption')
        order_items = data.get('order_items')

        new_order = Order()
        new_order.consumption = consumption
        if customer_cpf:
            customer = Customer.query.filter_by(cpf=customer_cpf).first()
            if customer is None:
                new_order.customer_cpf = customer_cpf
            else:
                new_order.customer = customer

        total_price = 0.0
        for item_data in order_items:
            item_id = item_data['item_id']
            extras = item_data.get('extras', [])
            removed_ingredients = item_data.get('removed_ingredients', [])

            menu_item = MenuItem.query.get(item_id)
            if not menu_item:
                return {'error': f'Item de menu com ID {item_id} não foi encontrado'}, 404

            item_price = menu_item.price

            item_price += len(extras)

            for ingredient_name in removed_ingredients:
                if ingredient_name not in menu_item.ingredients:
                    return {'error': f'{ingredient_name} não é um ingrediente válido para o item de menu {menu_item.name}'}, 400

            total_price += item_price

            new_order_item = OrderItem()
            new_order_item.item = menu_item

            for extra_name in extras:
                extra = OrderItemExtras(extra_name=extra_name)
                new_order_item.extras.append(extra)

            for ingredient_name in removed_ingredients:
                removed_ingredient = OrderItemRemovedIngredients(
                    removed_ingredient=ingredient_name)
                new_order_item.removed_ingredients.append(removed_ingredient)

            new_order.items.append(new_order_item)

        new_order.total = total_price
        new_order.status = OrderStatus.query.get(1)
        new_order.time = datetime.now()

        session = db.session
        session.add(new_order)
        session.commit()

        return {'message': f'Pedido {new_order.id} criado Pendente Pagamento'}, 201

    @order_namespace.doc(responses={200: 'Lista de todos os pedidos'})
    def get(self):
        orders = Order.query.all()
        order_list = []
        for order in orders:

            current_time = datetime.now()
            wait_time = current_time - order.time

            order_details = {
                'id': order.id,
                'status': order.status.name,
                'wait_time': wait_time.total_seconds()
            }
            order_list.append(order_details)

        return order_list, 200


@order_namespace.route('/<int:order_id>/payment', methods=['POST', 'GET'])
class OrderPaymentResource(Resource):
    @order_namespace.doc(params={'order_id': '1'}, responses={200: 'Pagamento processado com sucesso', 400: 'Erro na validação de pagamento'})
    def post(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return {'error': 'Pedido não encontrado'}, 404

        if payment_validation(order.id):
            order.status = OrderStatus.query.get(2)
            db.session.commit()
            return {'message': f'Pagamento processado com sucesso para o Pedido {order.id}'}, 200
        else:
            db.session.commit()
            return {'error': 'Erro na validação de pagamento'}, 400

    @order_namespace.doc(params={'order_id': '1'}, responses={200: 'Status do pagamento do pedido', 404: 'Pedido não encontrado'})
    def get(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return {'error': 'Pedido não encontrado'}, 404

        return {'payment_status': order.status.name}, 200


@order_namespace.route('/<int:order_id>', methods=['GET', 'POST'])
class OrdersResourceDetailed(Resource):
    @order_namespace.doc(responses={200: 'Detalhes do pedido'})
    def get(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return {'error': 'Pedido não encontrado'}, 404

        current_time = datetime.now()
        wait_time = current_time - order.time

        order_details = {
            'id': order.id,
            'customer_cpf': order.customer_id,
            'status': order.status.name,
            'wait_time': wait_time.total_seconds(),
            'items': []
        }

        for order_item in order.items:
            item_details = {
                'item_id': order_item.id,
                'extras': [extra.extra_name for extra in order_item.extras],
                'removed_ingredients': [ingredient.removed_ingredient for ingredient in order_item.removed_ingredients]
            }
            order_details['items'].append(item_details)

        return order_details, 200

    @order_namespace.doc(responses={200: 'Pedido atualizado com sucesso', 404: 'Pedido não encontrado', 400: 'Status inválido. Use "p" para "Pronto" ou "f" para "Finalizado.'}, description='Atualiza o status do pedido (POST)')
    @order_namespace.expect(order_post_model)
    def post(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return {'error': 'Pedido não encontrado'}, 404

        data = order_namespace.payload
        status = data.get('status', '').lower()

        if status == 'p':
            order.status = OrderStatus.query.get(3)
        elif status == 'f':
            order.status = OrderStatus.query.get(4)
        else:
            return {'error': 'Status inválido. Use "p" para "Pronto" ou "f" para "Finalizado.'}, 400

        db.session.commit()

        return {'message': f'Pedido #{order_id} atualizado com sucesso'}, 200
