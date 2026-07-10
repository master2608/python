import os

from flask import Flask

from controllers import api_v1_bp, figurinhas_bp
from models import db


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'figurinhas.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "chave-secreta-aula-figurinhas"

    db.init_app(app)

    app.register_blueprint(figurinhas_bp)
    app.register_blueprint(api_v1_bp)

    with app.app_context():
        db.create_all()
        from dados_iniciais import popular_dados_iniciais

        popular_dados_iniciais()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
