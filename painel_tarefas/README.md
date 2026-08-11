# Painel de Controle de Tarefas

Aplicação em Flask para gerenciar tarefas, com autenticação de usuários, banco SQLite, integração com API externa, filtro dinâmico, modo escuro e dashboard de progresso com Chart.js.

## Como rodar

```
pip install -r requirements.txt
python app.py
```

A aplicação sobe em `http://127.0.0.1:5000`. O banco `tarefas.db` é criado automaticamente na primeira execução.

## Estrutura

```
painel_tarefas/
├── app.py
├── database.py
├── requirements.txt
├── static/
│   ├── css/style.css
│   └── js/modo-escuro.js
└── templates/
    ├── base.html
    ├── login.html
    ├── registro.html
    ├── dashboard.html
    ├── nova_tarefa.html
    ├── editar_tarefa.html
    ├── progresso.html
    └── partials/_lista_tarefas.html
```

## Rotas principais

- `/login`, `/registro`, `/logout`
- `/dashboard` — lista de tarefas do usuário logado, com frase motivacional vinda da API adviceslip
- `/nova_tarefa`, `/editar/<id>`, `/excluir/<id>`
- `/api/tarefas?status=` — retorna JSON usado pelo filtro sem recarregar a página
- `/progresso` e `/api/progresso` — dashboard visual com Chart.js
- `/api/rest/tarefas` e `/api/rest/tarefas/<id>` — versão REST completa (desafio avançado)

## Segurança

- Senhas armazenadas com hash via `werkzeug.security`
- `SECRET_KEY` configurável por variável de ambiente
- `DEBUG=False`
- Rotas internas protegidas por sessão (`session` do Flask)
