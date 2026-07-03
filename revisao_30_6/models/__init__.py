from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .base import ModeloBase
from .jogador import Jogador

__all__ = ["ModeloBase", "Jogador"]