function realizarCadastro(username, nome, email, senha) {
    fetch("https://fittude-api.onrender.com/api/user/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "username": username,
            "nome": nome,
            "email": email,
            "password": senha
        })
    })
    .then(response => {
        console.log("Resposta do servidor");
        if (response.ok) {
            console.log("200 OK:", response);
        }
        else if(response.status == 409) {
            exibirMensagem('Email já cadastrado.', 'danger');
            return;
        }
        else if (response.status == 400) {
            exibirMensagem('Erro ao cadastrar usuário. Tente novamente.', 'danger');
            return;
        }else if (response.status == 404) {
            exibirMensagem('Falha na comunição com o servido', 'danger');
            return;
        }   
        else if (response.status == 500) {
            exibirMensagem('Erro interno do servidor. Tente novamente mais tarde.', 'danger');
            return;
        }
        else {
            return response.json();
        }
        
    })
    .then(data => {

        if (data.sucesso) {
            exibirMensagem('Cadastro realizado com sucesso!', 'success');
            
        } else {
            exibirMensagem('Erro ao cadastrar usuário. Tente novamente.', 'danger');
        }
    })
    .catch(error => {
        console.error("Erro informado:",error);
        exibirMensagem("Erro criando seu registro!", 'danger');

    });
}

class Main {

    constructor(main) {
        this.main = main;
    }

}


function exibirMensagem(mensagem, tipo) {
    const mensagemElement = document.getElementById('mensagem');
    mensagemElement.textContent = mensagem;
    mensagemElement.style.transition = 'none'; // Remove transições anteriores
    mensagemElement.style.opacity = '0'; // Reseta a opacidade
    mensagemElement.style.transform = 'translateY(-100%)'; // Reseta a posição
    void mensagemElement.offsetWidth; // Força o reflow para reiniciar a animação
    mensagemElement.style.transition = 'transform 0.5s ease-in-out, opacity 0.5s ease-in-out';
    mensagemElement.style.opacity = '1';
    mensagemElement.style.transform = 'translateY(0)';
    mensagemElement.className = `alert-${tipo}`; 
    mensagemElement.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
    const cadastroForm = document.getElementById('registerForm');
    
    cadastroForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const nome = document.getElementById('nome').value;
        const senha = document.getElementById('senha').value;
        const confirmarSenha = document.getElementById('confirmarSenha').value;

        
        function validarSenha(senha) {
            const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
            return regex.test(senha);
        }
        if (username.length < 3) {
            exibirMensagem('O nome de usuário deve ter pelo menos 3 caracteres.', 'danger');
            return;
        }

        if (!validarSenha(senha)) {
            exibirMensagem('A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos.', 'danger');
            return;
        }
        if (senha !== confirmarSenha) {
            exibirMensagem('As senhas não coincidem.', 'danger');
            return;
        }
        else {
            realizarCadastro(username, nome, email, senha);
        }
        
    });
});