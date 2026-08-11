import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tarefas.db')


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'pendente',
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')

    conn.commit()
    conn.close()


def buscar_usuario_por_email(email):
    conn = conectar()
    usuario = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
    conn.close()
    return usuario


def buscar_usuario_por_id(usuario_id):
    conn = conectar()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,)).fetchone()
    conn.close()
    return usuario


def criar_usuario(nome, email, senha_hash):
    conn = conectar()
    conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha_hash))
    conn.commit()
    conn.close()


def listar_tarefas(usuario_id, status=None):
    conn = conectar()
    if status and status != 'todas':
        tarefas = conn.execute(
            'SELECT * FROM tarefas WHERE usuario_id = ? AND status = ? ORDER BY id DESC',
            (usuario_id, status)
        ).fetchall()
    else:
        tarefas = conn.execute(
            'SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY id DESC',
            (usuario_id,)
        ).fetchall()
    conn.close()
    return tarefas


def buscar_tarefa(tarefa_id, usuario_id):
    conn = conectar()
    tarefa = conn.execute(
        'SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?',
        (tarefa_id, usuario_id)
    ).fetchone()
    conn.close()
    return tarefa


def criar_tarefa(titulo, descricao, status, usuario_id):
    conn = conectar()
    conn.execute(
        'INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)',
        (titulo, descricao, status, usuario_id)
    )
    conn.commit()
    conn.close()


def atualizar_tarefa(tarefa_id, titulo, descricao, status, usuario_id):
    conn = conectar()
    conn.execute(
        'UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ? AND usuario_id = ?',
        (titulo, descricao, status, tarefa_id, usuario_id)
    )
    conn.commit()
    conn.close()


def excluir_tarefa(tarefa_id, usuario_id):
    conn = conectar()
    conn.execute('DELETE FROM tarefas WHERE id = ? AND usuario_id = ?', (tarefa_id, usuario_id))
    conn.commit()
    conn.close()


def contar_tarefas_por_status(usuario_id):
    conn = conectar()
    linhas = conn.execute(
        'SELECT status, COUNT(*) as total FROM tarefas WHERE usuario_id = ? GROUP BY status',
        (usuario_id,)
    ).fetchall()
    conn.close()
    resultado = {'pendente': 0, 'em_andamento': 0, 'concluida': 0}
    for linha in linhas:
        resultado[linha['status']] = linha['total']
    return resultado
