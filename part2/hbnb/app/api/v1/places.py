from flask import Blueprint, jsonify
bp = Blueprint('places', __name__, url_prefix='/api/v1/places')

@bp.route('/', methods=['GET'])
def get_places():
    return jsonify({"message": "List of places"})
