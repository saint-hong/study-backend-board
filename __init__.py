import jump2.config as config

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

#from flaskext.markdown import Markdown

# SQLite error solution : MetaData, naming_convention
naming_convention = {
    "ix": "ix_%(column_0_labels)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# db = SQLAlchemy()
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app() : 
    
    app = Flask(__name__)
    app.config.from_object(config)
    
    # ORM
    ## SQLite error solution : migrate.init_app(app, db, render_as_batch=True)
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite") :
        migrate.init_app(app, db, render_as_batch=True)
    else :
        migrate.init_app(app, db)
    from jump2 import models   # create table
    
    # blueprint : endpoint
    from jump2.views import main_view, question_view, answer_view, auth_view
    app.register_blueprint(main_view.bp)
    app.register_blueprint(question_view.bp)
    app.register_blueprint(answer_view.bp)
    app.register_blueprint(auth_view.bp)
    
    # filter
    from jump2.filter import filter_datetime
    app.jinja_env.filters['datetime'] = filter_datetime
    
    # markdown
    #Markdown(app, extensions=['nl2br', 'fenced_code'])
    
    return app
      
