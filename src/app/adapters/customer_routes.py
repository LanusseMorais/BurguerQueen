from flask import Blueprint, request
from flask_restx import Resource, Namespace, fields
from app.models.db import db
from app.models.customer import Customer
from validate_docbr import CPF
import re
customer_routes = Blueprint('customer_routes', __name__)
customer_namespace = Namespace(
    'customer', description='Operações relacionadas a clientes')

customer_model = customer_namespace.model('Customer', {
    'cpf': fields.String(description='CPF do cliente', example="788.612.610-60"),
    'name': fields.String(description='Nome do cliente', example="Mariana"),
    'email': fields.String(description='E-mail do cliente', example="mariana@gmail.com"),
})


@customer_namespace.route('')
class CustomerResource(Resource):
    @customer_namespace.expect(customer_model)
    @customer_namespace.doc(responses={201: 'Cliente criado com sucesso'})
    def post(self):
        data = customer_namespace.payload
        cpf = data['cpf']
        name = data['name']
        email = data['email']

        if not CPF().validate(cpf):
            return {'error': 'CPF inválido'}, 400

        if not re.match(r'^\S+@\S+\.\S+$', email):
            return {'error': 'E-mail inválido'}, 400

        existing_customer = Customer.query.filter_by(cpf=cpf).first()
        if existing_customer:
            return {'error': 'CPF já cadastrado'}, 400

        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            return {'error': 'E-mail já cadastrado'}, 400

        new_customer = Customer(cpf=cpf, name=name, email=email)
        db.session.add(new_customer)
        db.session.commit()

        return {'message': 'Cliente criado com sucesso', 'customer_id': new_customer.id}, 201

    @customer_namespace.doc(responses={200: 'Lista de clientes'})
    def get(self):
        customers = Customer.query.all()
        customer_list = [{'id': customer.id, 'cpf': customer.cpf, 'name': customer.name, 'email': customer.email, 'registration_date': customer.registration_date}
                         for customer in customers]
        return customer_list, 200


@customer_namespace.route('/<int:customer_id>')
class CustomerResourceDetail(Resource):
    @customer_namespace.doc(responses={200: 'Detalhes do cliente'})
    def get(self, customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Cliente não encontrado'}, 404
        customer_details = {
            'id': customer.id,
            'cpf': customer.cpf,
            'name': customer.name,
            'email': customer.email,
            'registration_date': customer.registration_date
        }
        return customer_details, 200

    @customer_namespace.expect(customer_model)
    @customer_namespace.doc(responses={200: 'Cliente atualizado com sucesso'})
    def put(self, customer_id):
        data = customer_namespace.payload
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Cliente não encontrado'}, 404
        customer.cpf = data['cpf']
        customer.name = data['name']
        customer.email = data['email']

        if not CPF().validate(data['cpf']):
            return {'error': 'CPF inválido'}, 400

        if not re.match(r'^\S+@\S+\.\S+$', data['email']):
            return {'error': 'E-mail inválido'}, 400

        existing_customer = Customer.query.filter_by(cpf=data['cpf']).first()
        if existing_customer:
            return {'error': 'CPF já cadastrado'}, 400

        existing_customer = Customer.query.filter_by(
            email=data['email']).first()
        if existing_customer:
            return {'error': 'E-mail já cadastrado'}, 400

        db.session.commit()
        return {'message': 'Cliente atualizado com sucesso'}, 200

    @customer_namespace.doc(responses={204: 'Cliente excluído com sucesso'})
    def delete(self, customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Cliente não encontrado'}, 404
        db.session.delete(customer)
        db.session.commit()
        return '', 204


@customer_namespace.route('/<int:customer_id>/orders', methods=['GET'])
class CustomerOrdersResource(Resource):
    @customer_namespace.doc(responses={200: 'Pedidos do cliente'})
    def get(self, customer_id):

        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Cliente não encontrado'}, 404

        orders = customer.orders

        order_list = [{'id': order.id, 'status': order.status}
                      for order in orders]

        return order_list, 200
