from app.seeds.import_menu_categories import import_menu_categories
from app.seeds.import_status import import_status
from app.seeds.import_customer import import_customer
from app.seeds.import_menu import import_menu
from flask import Flask
from flask_restx import Api
from app.adapters.order_routes import order_routes, order_namespace
from app.adapters.menu_routes import menu_routes, menu_namespace
from app.adapters.customer_routes import customer_routes, customer_namespace
from app.models.db import db
import os


def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='API da Lanchonete BurgerQueen',
              description='Doc da API da Lanchonete BurgerQueen')
    app.config.from_pyfile('config.py')
    db.init_app(app)

    # Pasta onde o arquivo de controle será armazenado
    control_folder = 'control'

    # Verifique se o arquivo de controle já existe
    control_file = os.path.join(control_folder, 'initialized.txt')
    initialized = os.path.exists(control_file)

    # Inicializa o banco de dados
    with app.app_context():
        db.create_all()
        if not initialized:
            import_menu_categories(db)
            import_menu(db)
            import_customer(db)
            import_status(db)

            # Marque o arquivo de controle como criado
            os.makedirs(control_folder, exist_ok=True)
            with open(control_file, 'w') as f:
                f.write('initialized')

    # Registrar os blueprints para as rotas
    app.register_blueprint(order_routes)
    api.add_namespace(order_namespace)
    app.register_blueprint(menu_routes)
    api.add_namespace(menu_namespace)
    app.register_blueprint(customer_routes)
    api.add_namespace(customer_namespace)

    return app
