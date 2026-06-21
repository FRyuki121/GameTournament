import os
from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret-key'
    
    db.init_app(app)
    
    from app.routes import bp
    app.register_blueprint(bp)
    
    with app.app_context():
        db.create_all()
        
    return app