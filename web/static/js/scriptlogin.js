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

async function realizarLogin(email, senha, lembrar) {
    const api = new ApiClient(BaseUrl);
    try {
        const resultado = await api.post('user/login', {
            email: email,
            password: senha,
            keep_login: lembrar
        });
        const tokenHeader = resultado.header.get("Authorization");
        if (tokenHeader && tokenHeader.startsWith("Bearer ")) {
            const token = tokenHeader.replace("Bearer ", "").trim();
            localStorage.setItem("token", token);
            console.log("Token armazenado.")
        }
        else {
            exibirMensagem('Login falhou. Verifique suas credenciais.', 'danger'); // Exibe mensagem de erro
            console.error("Erro no login: ", resultado);
            return;
        }
    } catch (error) {
        console.error("[Login] Erro ao realizar login:", error);
        exibirMensagem('Erro ao realizar login. Verifique suas credenciais.', 'danger'); 
        return;
    }
}



