from flask import Blueprint, jsonify
from flask_restx import Resource, Namespace, fields
from app.models.menu_item import MenuItem
from app.models.db import db

menu_routes = Blueprint('menu_routes', __name__)
menu_namespace = Namespace(
    'menu', description='Operações relacionadas ao menu')

menu_item_model = menu_namespace.model('MenuItem', {
    'name': fields.String(description='Nome do item', example="Bolo de chocolate"),
    'description': fields.String(description='Descrição do item', example="Bolo de chocolate quetinho"),
    'category_id': fields.String(description='Categoria do item', example="sobremesa"),
    'ingredients': fields.String(description='Ingredientes do item separados por vírgula', example="bolo de chocolate, calda de chocolate"),
    'extras': fields.String(description='Extras disponíveis separados por vírgula', example="calda de chocolate"),
    'price': fields.Float(description='Preço do item', example=3.0)
})


@menu_namespace.route('')
class MenuItemResource(Resource):
    @menu_namespace.expect(menu_item_model)
    @menu_namespace.doc(responses={201: 'Item de menu criado com sucesso'})
    def post(self):
        data = menu_namespace.payload
        name = data['name']
        description = data['description']
        category_id = data['category_id']
        ingredients = data['ingredients']
        extras = data['extras']
        price = data['price']

        new_menu_item = MenuItem(
            name=name,
            description=description,
            category_id=category_id,
            ingredients=ingredients,
            extras=extras,
            price=price
        )
        db.session.add(new_menu_item)
        db.session.commit()

        return {'message': 'Item de menu criado com sucesso', 'item_id': new_menu_item.id}, 201

    @menu_namespace.doc(responses={200: 'Lista de itens de menu'})
    def get(self):
        menu_items = MenuItem.query.all()
        menu_list = [{'id': item.id, 'name': item.name, 'description': item.description, 'category_id': item.category_id, 'ingredients': item.ingredients, 'extras': item.extras, 'price': item.price}
                     for item in menu_items]
        return menu_list, 200


@menu_namespace.route('/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
class MenuItemDetailResource(Resource):
    @menu_namespace.doc(responses={200: 'Detalhes do item de menu'})
    def get(self, item_id):
        item = MenuItem.query.get(item_id)
        if not item:
            return {'error': 'Item de menu não encontrado'}, 404

        item_details = {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'category_id': item.category_id,
            'ingredients': item.ingredients,
            'extras': item.extras,
            'price': item.price,
        }
        return item_details, 200

    @menu_namespace.expect(menu_item_model)
    @menu_namespace.doc(responses={200: 'Item de menu atualizado com sucesso'})
    def put(self, item_id):
        item = MenuItem.query.get(item_id)
        if not item:
            return {'error': 'Item de menu não encontrado'}, 404

        data = menu_namespace.payload
        item.name = data['name']
        item.description = data['description']
        item.category_id = data['category_id']
        item.ingredients = data['ingredients']
        item.extras = data['extras']
        item.price = data['price']
        db.session.commit()

        return {'message': 'Item de menu atualizado com sucesso'}, 200

    @menu_namespace.doc(responses={200: 'Item de menu excluído com sucesso'})
    def delete(self, item_id):
        item = MenuItem.query.get(item_id)
        if not item:
            return {'error': 'Item de menu não encontrado'}, 404

        db.session.delete(item)
        db.session.commit()

        return {'message': 'Item de menu excluído com sucesso'}, 200


@menu_namespace.route('/items/<int:category_id>', methods=['GET'])
class MenuItemsByCategory(Resource):
    @menu_namespace.doc(responses={200: 'Itens do menu por categoria'})
    def get(self, category_id):
        # Consulte os itens do menu com a categoria especificada
        items = MenuItem.query.filter_by(category_id=category_id).all()

        # Mapeie os itens do menu para o modelo definido
        menu_items = [{'id': item.id, 'name': item.name, 'description': item.description, 'category_id': item.category_id,
                       'ingredients': item.ingredients, 'extras': item.extras, 'price': item.price} for item in items]

        return menu_items, 200
