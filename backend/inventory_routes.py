from flask import Blueprint, jsonify, request
from backend.deepseek_integration import generate_response

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/api/login", methods=["POST"])
def login():
    """
    Endpoint para simular el login de un usuario.
    """
    try:
        data = request.json
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "Falta el parámetro 'user_id'"}), 400

        # Aquí podríamos validar el user_id con la base de datos, pero lo simularemos
        return jsonify({
            "status": "success",
            "message": f"Usuario con ID {user_id} autenticado correctamente."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inventory_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    Endpoint para interactuar con el asistente virtual usando consultas en lenguaje natural.
    """
    try:
        data = request.json
        user_id = data.get("user_id")
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "Falta el mensaje del usuario"}), 400

        # Generar respuesta con la IA
        response = generate_response(user_message, user_id)

        if response.get("status") == "error":
            return jsonify({"error": response.get("message")}), 500

        return jsonify({
            "status": "success",
            "response": response.get("response")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inventory_bp.route("/api/recommendations", methods=["GET"])
def recommendations():
    """
    Genera recomendaciones basadas en el historial del usuario o generales si no hay login.
    """
    try:
        user_id = request.args.get("user_id", type=int)  # Obtener user_id (si existe)

        # Si no hay user_id, generar recomendaciones generales
        if not user_id:
            user_message = "Genera recomendaciones generales para los usuarios."
        else:
            user_message = "Genera recomendaciones personalizadas basadas en mi historial."

        # Generar respuesta usando la IA
        response = generate_response(user_message, user_id)

        if response.get("status") == "error":
            return jsonify({"error": response.get("message")}), 500

        # Responder con las recomendaciones categorizadas
        return jsonify({
            "status": "success",
            "recommendations": response.get("response")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
