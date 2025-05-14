from flask import Flask
from flask_login import LoginManager
from .firebase import db  # your Firestore client

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'WONKA'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        doc = db.collection('Users').document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            from .models import User
            return User(id=doc.id, email=data['email'])
        return None

    return app
