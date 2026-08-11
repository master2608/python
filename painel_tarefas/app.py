from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests
import os
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'troque-esta-chave-em-producao')
app.config['DEBUG'] = False

database.criar_tabelas()


def login_obrigatorio(funcao):
    @wraps(funcao)
    def envolvida(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return funcao(*args, **kwargs)
    return envolvida


@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        if not nome or not email or not senha:
            flash('Preencha todos os campos.', 'danger')
            return redirect(url_for('registro'))

        if database.buscar_usuario_por_email(email):
            flash('Já existe uma conta com esse e-mail.', 'danger')
            return redirect(url_for('registro'))

        senha_hash = generate_password_hash(senha)
        database.criar_usuario(nome, email, senha_hash)
        flash('Conta criada com sucesso. Faça login para continuar.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        usuario = database.buscar_usuario_por_email(email)

        if usuario and check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            return redirect(url_for('dashboard'))

        flash('E-mail ou senha inválidos.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_obrigatorio
def dashboard():
    status_filtro = request.args.get('status', 'todas')
    tarefas = database.listar_tarefas(session['usuario_id'], status_filtro)

    try:
        resposta = requests.get('https://api.adviceslip.com/advice', timeout=3)
        frase = resposta.json()['slip']['advice']
    except Exception:
        frase = 'Continue firme, cada tarefa concluída é um passo à frente.'

    return render_template('dashboard.html', tarefas=tarefas, frase=frase, status_filtro=status_filtro)


@app.route('/nova_tarefa', methods=['GET', 'POST'])
@login_obrigatorio
def nova_tarefa():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        status = request.form.get('status', 'pendente')

        if not titulo:
            flash('O título da tarefa é obrigatório.', 'danger')
            return redirect(url_for('nova_tarefa'))

        database.criar_tarefa(titulo, descricao, status, session['usuario_id'])
        flash('Tarefa criada com sucesso.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('nova_tarefa.html')


@app.route('/editar/<int:tarefa_id>', methods=['GET', 'POST'])
@login_obrigatorio
def editar(tarefa_id):
    tarefa = database.buscar_tarefa(tarefa_id, session['usuario_id'])

    if not tarefa:
        flash('Tarefa não encontrada.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        status = request.form.get('status', 'pendente')

        if not titulo:
            flash('O título da tarefa é obrigatório.', 'danger')
            return redirect(url_for('editar', tarefa_id=tarefa_id))

        database.atualizar_tarefa(tarefa_id, titulo, descricao, status, session['usuario_id'])
        flash('Tarefa atualizada com sucesso.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('editar_tarefa.html', tarefa=tarefa)


@app.route('/excluir/<int:tarefa_id>')
@login_obrigatorio
def excluir(tarefa_id):
    database.excluir_tarefa(tarefa_id, session['usuario_id'])
    flash('Tarefa removida.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/api/tarefas')
@login_obrigatorio
def api_tarefas():
    status_filtro = request.args.get('status', 'todas')
    tarefas = database.listar_tarefas(session['usuario_id'], status_filtro)
    lista = [dict(t) for t in tarefas]
    return jsonify(lista)


@app.route('/progresso')
@login_obrigatorio
def progresso():
    return render_template('progresso.html')


@app.route('/api/progresso')
@login_obrigatorio
def api_progresso():
    dados = database.contar_tarefas_por_status(session['usuario_id'])
    return jsonify(dados)


@app.route('/api/rest/tarefas', methods=['GET', 'POST'])
@login_obrigatorio
def rest_tarefas():
    if request.method == 'GET':
        status_filtro = request.args.get('status', 'todas')
        tarefas = database.listar_tarefas(session['usuario_id'], status_filtro)
        return jsonify([dict(t) for t in tarefas])

    dados = request.get_json(silent=True) or {}
    titulo = dados.get('titulo', '').strip()
    descricao = dados.get('descricao', '').strip()
    status = dados.get('status', 'pendente')

    if not titulo:
        return jsonify({'erro': 'O título é obrigatório.'}), 400

    database.criar_tarefa(titulo, descricao, status, session['usuario_id'])
    return jsonify({'mensagem': 'Tarefa criada com sucesso.'}), 201


@app.route('/api/rest/tarefas/<int:tarefa_id>', methods=['GET', 'PUT', 'DELETE'])
@login_obrigatorio
def rest_tarefa_unica(tarefa_id):
    tarefa = database.buscar_tarefa(tarefa_id, session['usuario_id'])

    if not tarefa:
        return jsonify({'erro': 'Tarefa não encontrada.'}), 404

    if request.method == 'GET':
        return jsonify(dict(tarefa))

    if request.method == 'PUT':
        dados = request.get_json(silent=True) or {}
        titulo = dados.get('titulo', tarefa['titulo'])
        descricao = dados.get('descricao', tarefa['descricao'])
        status = dados.get('status', tarefa['status'])
        database.atualizar_tarefa(tarefa_id, titulo, descricao, status, session['usuario_id'])
        return jsonify({'mensagem': 'Tarefa atualizada com sucesso.'})

    database.excluir_tarefa(tarefa_id, session['usuario_id'])
    return jsonify({'mensagem': 'Tarefa removida com sucesso.'})


if __name__ == '__main__':
    app.run(debug=False)
