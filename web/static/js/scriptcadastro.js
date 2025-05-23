import { ApiClient } from './core/auth.js';
import { BaseUrl, exibirMensagem } from './core/utils.js';

function realizarCadastro(username, nome, email, senha) {
    const api = new ApiClient(BaseUrl)
    api.post('user/register', {
        username: username,
            nome: nome,
            email: email,
            password: senha
    }).then(response => {
        if (response.success) {
            exibirMensagem('Cadastro realizado com sucesso! Você será redirecionado para a página de login.', 'success');
            setTimeout(() => {
                window.location.href = "login.html";
            }, 3000);
    }});
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