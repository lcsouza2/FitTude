export function exibirMensagem(mensagem, tipo) {
    const mensagemElement = document.getElementById('mensagem');
    mensagemElement.style.visibility = 'visible';
    mensagemElement.textContent = mensagem;
    mensagemElement.style.display = 'block';
    // Reset animation
    mensagemElement.style.animation = 'none';
    mensagemElement.offsetHeight; // Trigger reflow
    
    if (tipo == 'sucesso') {
        mensagemElement.style.color = '#510FEB';
        mensagemElement.style.animation = 'slideIn 0.5s ease-in-out';
    }
    else if (tipo == 'danger') {
        mensagemElement.style.color = 'black';
        mensagemElement.style.animation = 'shake 0.5s ease-in-out';
    }
    
    console.log("Mensagem de erro : ", mensagem);
}



export const BaseUrl = 'https://fittude-api-wn11.onrender.com/api/';