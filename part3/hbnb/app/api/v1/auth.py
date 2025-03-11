from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('auth', description='Authentication operations')

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
class Login(Resource):
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