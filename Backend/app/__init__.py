import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Initialisation des extensions
    mongo.init_app(app)
    jwt.init_app(app)
    
    # Configuration JWT
    from app.utils.auth import configure_jwt
    configure_jwt(jwt)
    
    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.plan import plan_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plan_bp, url_prefix='/api/plan')
    
    return app