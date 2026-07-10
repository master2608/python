from models import Colecionador, Figurinha, db


def popular_dados_iniciais():
    if Colecionador.query.first():
        return  # banco já populado

    colecionadores = [
        Colecionador(apelido="joaosilva", cidade="Belo Horizonte", email="joao@email.com"),
        Colecionador(apelido="mariaoliveira", cidade="Contagem", email="maria@email.com"),
        Colecionador(apelido="pedrosantos", cidade="São Paulo", email="pedro@email.com"),
    ]

    figurinhas = [
        Figurinha(numero=1, jogador="Alisson", selecao="Brasil"),
        Figurinha(numero=10, jogador="Neymar Jr.", selecao="Brasil"),
        Figurinha(numero=7, jogador="Mbappé", selecao="França"),
        Figurinha(numero=9, jogador="Haaland", selecao="Noruega"),
        Figurinha(numero=11, jogador="Messi", selecao="Argentina"),
    ]

    db.session.add_all(colecionadores + figurinhas)
    db.session.commit()
