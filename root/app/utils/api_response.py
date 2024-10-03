# api_response.py

from flask import jsonify

class ApiResponse:

    @staticmethod
    def ok(result=None, message="OK", status=200, total=None, page=None, per_page=None, has_next=None, has_prev=None):
        response_data = {
            "result": result,
            "message": message,
            "success": True,
            "status": status
        }
        # Añadir campos opcionales si están presentes
        if total is not None:
            response_data["total"] = total
        if page is not None:
            response_data["page"] = page
        if per_page is not None:
            response_data["per_page"] = per_page
        if has_next is not None:
            response_data["has_next"] = has_next
        if has_prev is not None:
            response_data["has_prev"] = has_prev

        return jsonify(response_data), status

    @staticmethod
    def created(result=None, message="Resource created successfully.", status=201):
        response_data = {
            "result": result,
            "message": message,
            "success": True,
            "status": status
        }
        return jsonify(response_data), status

    @staticmethod
    def bad_request(message="Invalid request parameters.", status=400):
        response_data = {
            "message": message,
            "success": False,
            "status": status
        }
        return jsonify(response_data), status

    @staticmethod
    def not_found(resource, resource_id=None, message=None, status=404):
        if not message:
            if resource_id:
                message = f"{resource} with ID {resource_id} not found."
            else:
                message = f"{resource} not found."
        response_data = {
            "message": message,
            "success": False,
            "status": status
        }
        return jsonify(response_data), status

    @staticmethod
    def internal_server_error(message="An internal server error occurred. Please try again later.", status=500):
        response_data = {
            "message": message,
            "success": False,
            "status": status
        }
        return jsonify(response_data), status

    # Puedes agregar más métodos según sea necesario...
