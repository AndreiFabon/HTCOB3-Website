import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

#data base initlization
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()  # Creates all tables if they don’t exist
        print("Database connected and tables created!")

    return app