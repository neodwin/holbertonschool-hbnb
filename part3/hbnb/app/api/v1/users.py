from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='User password')
})

# Define the user update model (password optional)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address'),
    'password': fields.String(description='User password')
})

# Define the user response model (no password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='Unique identifier of the user'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

# Define login model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='User password')
})

# Define token response model
token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token')
})

@api.route('/login')
class UserLogin(Resource):
    @api.doc('user_login')
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful', token_model)
    @api.response(401, 'Invalid credentials')
    def post(self):
        """User login endpoint"""
        data = api.payload
        try:
            token = facade.authenticate_user(data['email'], data['password'])
            if not token:
                api.abort(401, 'Invalid credentials')
            return {'access_token': token}
        except Exception as e:
            api.abort(500, str(e))

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """List all users (public endpoint)"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users]

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user (public endpoint)"""
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
    def get(self, user_id):
        """Get user details by ID (public endpoint)"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.response(200, 'User successfully updated', user_response_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Permission denied')
    @jwt_required()
    def put(self, user_id):
        """Update user details (authenticated endpoint)"""
        user_data = api.payload
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Only allow users to update their own profile unless they are admin
        if current_user_id != user_id and not is_admin:
            api.abort(403, 'Permission denied')
            
        try:
            user = facade.update_user(user_id, user_data)
            if not user:
                api.abort(404, 'User not found')
            return user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))
