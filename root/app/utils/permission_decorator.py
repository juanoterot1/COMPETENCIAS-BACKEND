from functools import wraps
from flask import jsonify, g
from app.models.user import User

def requires_permission(name):
    """
    Decorador para verificar si el usuario tiene el permiso requerido.
    
    :param name: Nombre del permiso requerido para acceder a la ruta.
    """
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            try:
                # Asegúrate de que el decorador jwt_required haya llenado g.current_user
                user_data = getattr(g, "current_user", None)
                if not user_data:
                    return jsonify({"msg": "Unauthorized"}), 401

                # Obtener el usuario desde la base de datos
                user = User.query.get(user_data.get("user_id"))
                if not user:
                    return jsonify({"msg": "User not found"}), 404

                # Verificar si el usuario tiene un rol asignado
                role = user.role
                if not role:
                    return jsonify({"msg": "Role not assigned"}), 400

                # Verificar si el rol tiene el permiso requerido
                has_permission = any(perm.name == name for perm in role.permissions)
                if not has_permission:
                    return jsonify({"msg": "Permission denied"}), 403

                # Si tiene el permiso, continuar con la ejecución de la vista
                return f(*args, **kwargs)

            except Exception as e:
                return jsonify({"msg": "Internal server error", "details": str(e)}), 500

        return wrapped_function
    return decorator
