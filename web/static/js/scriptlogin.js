document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;
        
        
        realizarLogin(email, senha);
    });
});

function realizarLogin(email, senha) {
    fetch('Fiz_o_test_tatudofuncionando.com', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, senha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            exibirMensagem('Login realizado com sucesso!', 'sucesso');
            setTimeout(() => {
                // Redirecionar para a página principal após login
                window.location.href = 'dashboard.html'; // Altere para o caminho correto do seu dashboard
            }, 3000); // 2 segundos de espera antes do redirecionamento
            // Redirecionar para a página principal após login
        } else {
            exibirMensagem('Email ou senha inválidos', 'error');
        }
    })
    .catch(error => {
        exibirMensagem('Erro ao realizar login', 'error');
        console.error('Erro:', error);
    });
}

function exibirMensagem(mensagem, tipo) {
    const mensagemElement = document.getElementById('mensagem');
    mensagemElement.textContent = mensagem;
    mensagemElement.className = `mensagem ${tipo}`; 
    mensagemElement.style.display = 'block';
    if (tipo == 'sucesso') {
        mensagemElement.style.color = 'lightgreen';
    }
    else if (tipo == 'error') {
        mensagemElement.style.color = '#ff6666'; // Vermelho claro
    }
}