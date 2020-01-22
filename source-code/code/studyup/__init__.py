from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from studyup.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app) 

    #Blueprints
    from studyup.main.routes import main 
    from studyup.question.routes import question
    
    app.register_blueprint(main)
    app.register_blueprint(question)

    return app