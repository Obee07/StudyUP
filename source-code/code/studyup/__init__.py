import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from studyup.config import Config
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

db = SQLAlchemy()

from studyup.question.routes import photos

def create_app(config_class=Config):
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)

    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/img')
    app.config.from_object(Config)

    configure_uploads(app, photos)
    patch_request_class(app)  # set maximum file size as 16MB

    db.init_app(app) 

    #Blueprints
    from studyup.main.routes import main 
    from studyup.question.routes import question
    
    app.register_blueprint(main)
    app.register_blueprint(question)

    return app