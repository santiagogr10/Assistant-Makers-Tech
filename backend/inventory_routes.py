from flask import Blueprint, jsonify, request
from backend.deepseek_integration import generate_response

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/api/login", methods=["POST"])
def login():
    """
    Endpoint to simulate user login.
    """
    try:
        data = request.json
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "The 'user_id' parameter is missing"}), 400

        # Here we could validate the user_id with the database, but we will simulate it
        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"User with ID {user_id} successfully authenticated.",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    Endpoint to interact with the virtual assistant using natural language queries.
    """
    try:
        data = request.json
        user_id = data.get("user_id")
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "The user's message is missing"}), 400

        # Generate a response with AI
        response = generate_response(user_message, user_id)

        if response.get("status") == "error":
            return jsonify({"error": response.get("message")}), 500

        return jsonify({"status": "success", "response": response.get("response")}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_bp.route("/api/recommendations", methods=["GET"])
def recommendations():
    """
    Generates recommendations based on the user's history or general suggestions if not logged in.
    """
    try:
        user_id = request.args.get("user_id", type=int)  # Retrieve user_id (if provided)

        # Generate general recommendations if no user_id is provided
        if not user_id:
            user_message = "Generate general recommendations for users."
        else:
            user_message = "Generate personalized recommendations based on my history."

        # Generate a response using AI
        response = generate_response(user_message, user_id)

        if response.get("status") == "error":
            return jsonify({"error": response.get("message")}), 500

        # Respond with categorized recommendations
        return jsonify({"status": "success", "recommendations": response.get("response")}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
