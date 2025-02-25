from flask import Blueprint, jsonify
bp = Blueprint('reviews', __name__, url_prefix='/api/v1/reviews')

@bp.route('/', methods=['GET'])
def get_reviews():
    return jsonify({"message": "List of reviews"})
