from flask import Flask, jsonify, render_template_string
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from config import config
from app.extensions import bcrypt, jwt, db
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the namespaces
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    # Add a custom 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        # You can return a custom HTML page
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>HBnB API - Not Found</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f5f5f5;
                    overflow: hidden;
                    position: relative;
                }
                .container {
                    text-align: center;
                    padding: 40px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    z-index: 10;
                }
                h1 {
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                p {
                    color: #333;
                    margin-bottom: 20px;
                    line-height: 1.6;
                }
                a {
                    display: inline-block;
                    color: white;
                    background-color: #3498db;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                }
                a:hover {
                    background-color: #2980b9;
                }
                
                /* Duck styles */
                .duck {
                    position: absolute;
                    font-size: 40px;
                    animation: dance 3s infinite alternate;
                    z-index: 1;
                    cursor: pointer;
                }
                
                @keyframes dance {
                    0% { transform: translateY(0) rotate(0deg); }
                    25% { transform: translateY(-20px) rotate(10deg); }
                    50% { transform: translateY(0) rotate(-10deg); }
                    75% { transform: translateY(-10px) rotate(5deg); }
                    100% { transform: translateY(0) rotate(0deg); }
                }
                
                .quack {
                    position: absolute;
                    color: #e67e22;
                    font-weight: bold;
                    font-size: 24px;
                    opacity: 0;
                    animation: fadeOut 2s forwards;
                    z-index: 5;
                }
                
                @keyframes fadeOut {
                    0% { opacity: 0; transform: scale(0.5); }
                    10% { opacity: 1; transform: scale(1); }
                    80% { opacity: 1; transform: scale(1.1) translateY(-20px); }
                    100% { opacity: 0; transform: scale(1) translateY(-40px); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Page Not Found</h1>
                <p>The page you are looking for does not exist. This is an API server, not a website.</p>
                <p>Please visit the API documentation to learn how to use the API.</p>
                <a href="/api/v1/">Go to API Documentation</a>
            </div>
            
            <script>
                // Create 5 dancing ducks
                for (let i = 0; i < 5; i++) {
                    createDuck();
                }
                
                // Function to create a duck at random position
                function createDuck() {
                    const duck = document.createElement('div');
                    duck.className = 'duck';
                    duck.innerHTML = '🦆';
                    duck.style.left = Math.random() * 100 + '%';
                    duck.style.top = Math.random() * 100 + '%';
                    duck.style.animationDelay = Math.random() * 2 + 's';
                    document.body.appendChild(duck);
                    
                    // Make the duck quack randomly
                    setInterval(() => {
                        if (Math.random() > 0.7) {
                            quack(duck);
                        }
                    }, 3000);
                    
                    // Make the duck quack when clicked
                    duck.addEventListener('click', () => {
                        quack(duck);
                    });
                }
                
                // Function to make a duck quack
                function quack(duck) {
                    const quackElem = document.createElement('div');
                    quackElem.className = 'quack';
                    quackElem.innerHTML = 'COIN!';
                    quackElem.style.left = duck.style.left;
                    quackElem.style.top = duck.style.top;
                    document.body.appendChild(quackElem);
                    
                    // Remove the quack element after animation
                    setTimeout(() => {
                        quackElem.remove();
                    }, 2000);
                }
            </script>
        </body>
        </html>
        '''
        return render_template_string(html), 404
    
    # Add a root route that redirects to the API documentation
    @app.route('/')
    def index():
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>HBnB API</title>
            <meta http-equiv="refresh" content="0;url=/api/v1/" />
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <p>Redirecting to API documentation...</p>
            <p>If you are not redirected automatically, <a href="/api/v1/">click here</a>.</p>
        </body>
        </html>
        ''')

    return app 