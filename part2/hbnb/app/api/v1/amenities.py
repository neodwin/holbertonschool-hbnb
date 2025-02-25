from flask import Blueprint, jsonify
bp = Blueprint('amenities', __name__, url_prefix='/api/v1/amenities')

@bp.route('/', methods=['GET'])
def get_amenities():
    return jsonify({"message": "List of amenities"})
