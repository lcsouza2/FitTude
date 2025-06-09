import { publicApiClient } from '../core/auth.js';

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
    try {
        const {headers, body} = await api.post('user/login', {
            email: email,
            password: senha,
            keep_login: lembrar
        });

        if (!headers.get('Authorization')) {
            throw new Error('Header de autorização não encontrado');
        }

        const tokenHeader = headers.get('Authorization');
        if (tokenHeader?.startsWith("Bearer ")) {
            const token = tokenHeader.replace("Bearer ", "").trim();
            localStorage.setItem("token", token);
            exibirMensagem("login realizado com sucesso!", "success");

            setTimeout(() => {
                window.location.href = "dashboard"; // Redireciona para a página de dashboard após 5 segundos
            }, 5000);
        } else {
            throw new Error('Token inválido ou mal formatado');
        }

    } catch (error) {
        console.error("[Login] Erro ao realizar login:", error.message);
        exibirMensagem('Erro ao realizar login. Verifique suas credenciais.', 'danger');
        return;
    }
}



