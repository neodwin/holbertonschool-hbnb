from flask import Blueprint, jsonify
bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@bp.route('/', methods=['GET'])
def get_users():
    return jsonify({"message": "List of users"})
