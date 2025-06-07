export function exibirMensagem(mensagem, tipo) {
    const div = document.getElementById('mensagem');
    div.style.visibility = 'visible';
    div.textContent = mensagem;
    div.style.display = 'block';
    // Reset animation
    div.style.animation = 'none';
    div.offsetHeight; // Trigger reflow
    if (tipo == 'danger') {
        div.style.color = 'red'
    }
    else if (tipo == 'success') {
        div.style.color = 'blue'
    } else {

    }

}



export const BASE_URL = 'http://localhost:8000/';