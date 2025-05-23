export function exibirMensagem(mensagem, tipo) {
    const mensagemElement = document.getElementById('mensagem');
    mensagemElement.textContent = mensagem;
    mensagemElement.style.display = 'block';
    if (tipo == 'sucesso') {
        mensagemElement.style.color = 'lightgreen';
    }
    else if (tipo == 'danger') {
        mensagemElement.style.color = '#ff6666'; // Vermelho claro
    }
    console.log("Mensagem de erro : ",mensagem)
}

export const BaseUrl = 'https://fittude-api-wn11.onrender.com/api/';