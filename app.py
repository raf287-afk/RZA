from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = "tl_S2403367_database"

    # Fixed database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://tl_S2403367:tl_S2403367@ND-COMPSCI/tl_s2403367_rza"

    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app
