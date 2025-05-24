import { ApiClient } from './core/auth.js';
import { BaseUrl, exibirMensagem } from './core/utils.js';

function realizarCadastro(nome, email, senha) {
    const api = new ApiClient(BaseUrl)
    api.post('user/register', {
        email: email,
        password: senha,
        name: nome
    }).then(response => {
        if (response.success) {
            exibirMensagem('Cadastro realizado com sucesso! Você será redirecionado para a página de login.', 'success');
            setTimeout(() => {
                window.location.href = "login.html";
            }, 7000);
    }});
}

document.addEventListener('DOMContentLoaded', function() {
    const cadastroForm = document.getElementById('registerForm');
    
    cadastroForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const nome = document.getElementById('nome').value;
        const senha = document.getElementById('senha').value;
        const confirmarSenha = document.getElementById('confirmarSenha').value;

    
        function validarSenha(senha) {
            const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
            return regex.test(senha);
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
            realizarCadastro(nome, email, senha);
        }
        
    });
});