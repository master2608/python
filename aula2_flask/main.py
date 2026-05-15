from flask import Flask , render_template

app = Flask(__name__) 


@app.route('/') 
def ola_mundo():
    return render_template('template.html')

@app.route('/sobre/<nome>')
def nome(nome):
    return f'Olá {nome}, bem vindo ao site!'

if __name__ == '__main__':
    app.run(debug=True)