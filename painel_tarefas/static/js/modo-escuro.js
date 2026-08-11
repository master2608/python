const botaoModoEscuro = document.getElementById('botaoModoEscuro');
const preferencia = localStorage.getItem('modoEscuro');

if (preferencia === 'ativo') {
    document.body.classList.add('modo-escuro');
}

if (botaoModoEscuro) {
    botaoModoEscuro.addEventListener('click', function () {
        document.body.classList.toggle('modo-escuro');
        const ativo = document.body.classList.contains('modo-escuro');
        localStorage.setItem('modoEscuro', ativo ? 'ativo' : 'inativo');
    });
}
