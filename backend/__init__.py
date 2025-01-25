from flask import Flask
from backend.inventory_routes import inventory_bp  # Importa los endpoints desde inventory_routes

def create_app():
    app = Flask(__name__)

    # Registrar blueprints
    app.register_blueprint(inventory_bp)

    return app
