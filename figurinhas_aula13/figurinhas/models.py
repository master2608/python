from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Colecionador(db.Model):
    __tablename__ = "colecionadores"

    id = db.Column(db.Integer, primary_key=True)
    apelido = db.Column(db.String(80), nullable=False)
    cidade = db.Column(db.String(80))
    email = db.Column(db.String(120))

    @staticmethod
    def listar():
        return Colecionador.query.order_by(Colecionador.apelido).all()

    @staticmethod
    def buscar_por_id(colecionador_id):
        return Colecionador.query.get(colecionador_id)

    def to_dict(self):
        return {
            "id": self.id,
            "apelido": self.apelido,
            "cidade": self.cidade,
            "email": self.email,
        }

    def __repr__(self):
        return f"<Colecionador {self.apelido}>"


class Figurinha(db.Model):
    __tablename__ = "figurinhas"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    jogador = db.Column(db.String(80), nullable=False)
    selecao = db.Column(db.String(80))

    @staticmethod
    def listar():
        return Figurinha.query.order_by(Figurinha.numero).all()

    @staticmethod
    def buscar_por_id(figurinha_id):
        return Figurinha.query.get(figurinha_id)

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "jogador": self.jogador,
            "selecao": self.selecao,
        }

    def __str__(self):
        return f"#{self.numero} - {self.jogador} ({self.selecao})"


class OfertaTroca(db.Model):
    __tablename__ = "ofertas_troca"

    id = db.Column(db.Integer, primary_key=True)
    colecionador_id = db.Column(db.Integer, db.ForeignKey("colecionadores.id"), nullable=False)
    observacao = db.Column(db.String(255))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    colecionador = db.relationship("Colecionador", backref="ofertas")
    itens = db.relationship("ItemOferta", backref="oferta", cascade="all, delete-orphan")

    @staticmethod
    def listar_com_colecionador():
        return OfertaTroca.query.order_by(OfertaTroca.data_criacao.desc()).all()

    @staticmethod
    def buscar_por_id(oferta_id):
        return OfertaTroca.query.get(oferta_id)

    def figurinha_oferecida(self):
        item = next((i for i in self.itens if i.tipo == "oferece"), None)
        return item.figurinha if item else None

    def figurinha_desejada(self):
        item = next((i for i in self.itens if i.tipo == "deseja"), None)
        return item.figurinha if item else None

    def to_dict(self):
        oferece = self.figurinha_oferecida()
        deseja = self.figurinha_desejada()
        return {
            "id": self.id,
            "colecionador": self.colecionador.apelido if self.colecionador else None,
            "cidade": self.colecionador.cidade if self.colecionador else None,
            "observacao": self.observacao,
            "data_criacao": self.data_criacao.strftime("%d/%m/%Y %H:%M") if self.data_criacao else None,
            "figurinha_oferece": oferece.to_dict() if oferece else None,
            "figurinha_deseja": deseja.to_dict() if deseja else None,
        }


class ItemOferta(db.Model):
    __tablename__ = "itens_oferta"

    id = db.Column(db.Integer, primary_key=True)
    oferta_id = db.Column(db.Integer, db.ForeignKey("ofertas_troca.id"), nullable=False)
    figurinha_id = db.Column(db.Integer, db.ForeignKey("figurinhas.id"), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # "oferece" ou "deseja"

    figurinha = db.relationship("Figurinha")
