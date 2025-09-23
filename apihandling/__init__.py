from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config



db = SQLAlchemy()

migrate = Migrate()

def create_app(): # 애플리케이션 팩토리
    app = Flask(__name__)
    app.config.from_object(config)

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0930@localhost:5432/connecterDB'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    
    from .views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
