export function exibirMensagem(mensagem, tipo) {
    const mensagemElement = document.getElementById('mensagem');
    mensagemElement.textContent = mensagem;
    mensagemElement.className = `mensagem-${tipo}`; 
    mensagemElement.style.display = 'block';
    // if (tipo == 'sucesso') {
    //     mensagemElement.style.color = 'lightgreen';
    // }
    // else if (tipo == 'error') {
    //     mensagemElement.style.color = '#ff6666'; // Vermelho claro
    // }
    console.log(mensagem)
}

export const BaseUrl = 'https://fittude-api-wn11.onrender.com/api/S';