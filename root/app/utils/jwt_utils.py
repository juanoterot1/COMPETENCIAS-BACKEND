import jwt
from datetime import datetime, timedelta

# Define una clave secreta (asegúrate de mantener esta clave segura)
SECRET_KEY = "your_secret_key"  # Cambia esto por una clave secreta segura

def create_jwt_token(data, expires_in=60):
    """
    Genera un token JWT con datos y una fecha de expiración.

    :param data: Diccionario con datos a incluir en el token.
    :param expires_in: Tiempo en minutos para que expire el token.
    :return: Token JWT como cadena.
    """
    expiration = datetime.utcnow() + timedelta(minutes=expires_in)
    payload = {**data, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt_token(token):
    """
    Decodifica un token JWT y verifica su validez.

    :param token: El token JWT a decodificar.
    :return: Los datos dentro del token si es válido.
    :raises: jwt.ExpiredSignatureError si el token expiró.
             jwt.InvalidTokenError si el token no es válido.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("El token ha expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token no válido")
