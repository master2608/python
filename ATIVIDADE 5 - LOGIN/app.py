from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

USUARIOS_PERMITIDOS = [
    {"usuario": "20261234", "senha": "20261234"},
    {"usuario": "marcos", "senha": "cotemig2026"},
    {"usuario": "janaina", "senha": "cotemig2026"}
]

@app.route('/', methods=['GET', 'POST'])
def login():
    mensagem = ""
    status = ""
    
    if request.method == 'POST':
        usuario_digitado = request.form.get('usuario')
        senha_digitada = request.form.get('senha')
        
        acesso_concedido = False
        
        for credencial in USUARIOS_PERMITIDOS:
            if credencial["usuario"] == usuario_digitado and credencial["senha"] == senha_digitada:
                acesso_concedido = True
                break
        
        if acesso_concedido:
            return redirect(url_for('sucesso', nome=usuario_digitado))
        else:
            mensagem = "Acesso Negado! Usuário ou senha incorretos."
            status = "erro"

    return render_template('login.html', mensagem=mensagem, status=status)

@app.route('/sucesso')
def sucesso():
    nome_usuario = request.args.get('nome', 'Usuário')
    return render_template('sucesso.html', nome=nome_usuario)

if __name__ == '__main__':
    app.run(debug=True)
