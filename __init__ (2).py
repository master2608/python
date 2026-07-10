from flask import Blueprint, jsonify, request

from models import Colecionador, Figurinha, OfertaTroca, db
from services.figurinhas_service import criar_oferta

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@api_v1_bp.route("/colecionadores", methods=["GET"])
def listar_colecionadores():
    colecionadores = Colecionador.listar()
    return jsonify([c.to_dict() for c in colecionadores]), 200


@api_v1_bp.route("/figurinhas", methods=["GET"])
def listar_figurinhas():
    figurinhas = Figurinha.listar()
    return jsonify([f.to_dict() for f in figurinhas]), 200


@api_v1_bp.route("/ofertas", methods=["GET"])
def listar_ofertas():
    ofertas = OfertaTroca.listar_com_colecionador()
    return jsonify([o.to_dict() for o in ofertas]), 200


@api_v1_bp.route("/ofertas/<int:oferta_id>", methods=["GET"])
def buscar_oferta(oferta_id):
    oferta = OfertaTroca.buscar_por_id(oferta_id)
    if not oferta:
        return jsonify({"erro": "Oferta não encontrada"}), 404
    return jsonify(oferta.to_dict()), 200


@api_v1_bp.route("/ofertas", methods=["POST"])
def criar_oferta_api():
    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = ["colecionador_id", "figurinha_oferece_id", "figurinha_deseja_id"]
    faltando = [c for c in campos_obrigatorios if c not in dados]
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios faltando: {', '.join(faltando)}"}), 400

    try:
        oferta = criar_oferta(
            colecionador_id=dados["colecionador_id"],
            figurinha_oferece_id=dados["figurinha_oferece_id"],
            figurinha_deseja_id=dados["figurinha_deseja_id"],
            observacao=dados.get("observacao", ""),
        )
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404

    return jsonify(oferta.to_dict()), 201


@api_v1_bp.route("/ofertas/<int:oferta_id>", methods=["DELETE"])
def remover_oferta(oferta_id):
    oferta = OfertaTroca.buscar_por_id(oferta_id)
    if not oferta:
        return jsonify({"erro": "Oferta não encontrada"}), 404

    db.session.delete(oferta)
    db.session.commit()
    return jsonify({"mensagem": "Oferta removida com sucesso"}), 200


@api_v1_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "API está funcionando"}), 200
