from flask import Flask
from backend.inventory_routes import inventory_bp

app = Flask(__name__)
app.register_blueprint(inventory_bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
