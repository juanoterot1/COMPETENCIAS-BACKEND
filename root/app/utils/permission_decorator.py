from functools import wraps
from flask import request, jsonify
from app.models import User, Role, Permission
from app.extensions import db
from app.utils.jwt_utils import get_jwt_identity  # Utiliza el JWT para obtener la identidad del usuario

def requires_permission(permission_name):
    """
    Decorador para verificar si el usuario tiene el permiso requerido.
    :param permission_name: El nombre del permiso requerido para acceder a la ruta.
    """

    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            # Obtener la identidad del usuario desde el JWT
            user_id = get_jwt_identity()  # Suponiendo que el JWT tiene la identidad del usuario

            # Obtener el usuario desde la base de datos
            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 404

            # Obtener el rol del usuario
            role = user.role
            if not role:
                return jsonify({"message": "Role not assigned"}), 400

            # Verificar si el rol tiene el permiso requerido
            has_permission = any(perm.name == permission_name for perm in role.permissions)
            if not has_permission:
                return jsonify({"message": "Permission denied"}), 403

            # Si tiene el permiso, continuar con la ejecución de la vista
            return f(*args, **kwargs)

        return wrapped_function
    return decorator
