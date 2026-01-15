import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db, jwt
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.comments import comments_bp
from routes.tests import tests_bp
from routes.forum import forum_bp
from routes.chat import chat_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///humanbio.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-key')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(tests_bp, url_prefix='/api/tests')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
