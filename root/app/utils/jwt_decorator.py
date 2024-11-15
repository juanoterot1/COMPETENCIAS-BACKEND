from functools import wraps
from flask import request, jsonify, g
import jwt
from app.config import Config

def jwt_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"msg": "Token is missing"}), 401

        try:
            # Elimina el prefijo "Bearer " si es necesario
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            g.current_user = decoded_token  # Guarda los datos del token en 'g' para acceso global
        except jwt.ExpiredSignatureError:
            return jsonify({"msg": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"msg": "Invalid token"}), 401

        return func(*args, **kwargs)
    return decorated_function