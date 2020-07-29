from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from  flask_login import LoginManager
from app.config import Config
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'filesystem','CACHE_DIR': "E:\cache",'CACHE_DEFAULT_TIMEOUT': 5})
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    from app.users.routes import users
    from app.search.routes import searchs
    from app.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(searchs)
    app.register_blueprint(main)

    return app