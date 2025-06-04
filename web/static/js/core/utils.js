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
     
    console.log("Mensagem de erro : ", div, " tipo: ", tipo); // debug line 
}



export const BaseUrl = 'https://fittude-api-wn11.onrender.com/api/';