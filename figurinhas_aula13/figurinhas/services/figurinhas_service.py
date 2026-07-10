from models import Colecionador, Figurinha, ItemOferta, OfertaTroca, db


def criar_oferta(colecionador_id, figurinha_oferece_id, figurinha_deseja_id, observacao=""):
    colecionador = Colecionador.buscar_por_id(colecionador_id)
    if not colecionador:
        raise ValueError("Colecionador não encontrado")

    figurinha_oferece = Figurinha.buscar_por_id(figurinha_oferece_id)
    if not figurinha_oferece:
        raise ValueError("Figurinha oferecida não encontrada")

    figurinha_deseja = Figurinha.buscar_por_id(figurinha_deseja_id)
    if not figurinha_deseja:
        raise ValueError("Figurinha desejada não encontrada")

    oferta = OfertaTroca(colecionador_id=colecionador.id, observacao=observacao)
    oferta.itens.append(ItemOferta(figurinha_id=figurinha_oferece.id, tipo="oferece"))
    oferta.itens.append(ItemOferta(figurinha_id=figurinha_deseja.id, tipo="deseja"))

    db.session.add(oferta)
    db.session.commit()

    return oferta
