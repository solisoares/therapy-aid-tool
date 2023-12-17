from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy()


def create_app(config):
    app.config.from_object(config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

        return app
