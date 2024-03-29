from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    from .database import db
    db.init_app(app)

    from .controllers import (auth, pets, vacinas)

    app.register_blueprint(auth.bp)
    pets.bp.register_blueprint(vacinas.bp)
    app.register_blueprint(pets.bp)

    return app
