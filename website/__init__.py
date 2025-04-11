from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'WONKA'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/accounts_dbmsproject'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note


    with app.app_context():# so that flask knows the app youre talking about
        #whether its a config database or a route 
        # just to create the apps context for flask
        db.create_all()# creates the tables defined in the models file into the 
        # postgres database
        print(' Tables created in PostgreSQL!')
        #only creates the missing tables in the database
    return app
