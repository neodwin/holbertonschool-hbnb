from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask import request

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address')
})

# Define the user response model
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='Unique identifier of the user'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    @jwt_required()  # Only authenticated users can access this endpoint
    def get(self):
        """List all users"""
        current_user = get_jwt_identity()
        
        # Ensure the user is an admin before listing all users
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        users = facade.get_all_users()
        return [user.to_dict() for user in users]

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Invalid input data')
    @jwt_required()  # Only authenticated users can create a new user
    def post(self):
        """Create a new user"""
        current_user = get_jwt_identity()
        
        # Ensure the user is an admin before creating a new user
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        try:
            user_data = api.payload
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'Success', user_response_model)
    @api.response(404, 'User not found')
    @jwt_required()  # Only authenticated users can access this
    def get(self, user_id):
        """Get user details by ID"""
        current_user = get_jwt_identity()
        
        # Ensure the user is an admin before accessing user details
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'User successfully updated', user_response_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # Only authenticated users can modify users
    def put(self, user_id):
        """Update user details"""
        current_user = get_jwt_identity()
        
        # Ensure the user is an admin before updating user data
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload
        try:
            user = facade.update_user(user_id, user_data)
            if not user:
                api.abort(404, 'User not found')
            return user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
