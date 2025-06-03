import { ApiClient } from './core/auth.js';
import { BaseUrl , exibirMensagem } from './core/utils.js';

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;
        const lembrar = document.getElementById('remember').checked;
        const token = sessionStorage.getItem('token');
        if (token) {
            window.location.href = "dashboard.html"; // Redireciona para a página de dashboard se o token estiver presente
        }
        else {
            if (email && senha) {
                realizarLogin(email, senha, lembrar);
            }
            else {
                exibirMensagem('Preencha todos os campos.', 'error');
            }
        }
    });
});

function realizarLogin(email, senha, lembrar) {
    const api = new ApiClient(BaseUrl)
    api.post('user/login', {
        email: email,
        password: senha,
        keep_login: lembrar
    }).then(response => {
        console.log("Esse é",response)
        if (data) {
            token = response.access_token
            sessionStorage.setItem(token);

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 2000);
    }});
}
