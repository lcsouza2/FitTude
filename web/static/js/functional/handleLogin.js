import { publicApiClient, tokenManager } from '../core/auth.js';

const loginForm = document.getElementById('loginForm');

const formEmail = document.getElementById('email');
const formSenha = document.getElementById('senha');
const formLembrar = document.getElementById('remember');

loginForm.addEventListener('submit', function(event) {
    event.preventDefault();

    if (email && senha) {
            realizarLogin(formEmail.value, formSenha.value, formLembrar.checked);
        }
    }
);

async function realizarLogin(email, senha, lembrar) {
    try {
        const response = await publicApiClient.post('/api/user/login', {
            email: email,
            password: senha,    
            keep_login: lembrar
        });

        const bruteToken = response.headers.get('Authorization');
        if (!bruteToken) {
            throw new Error('Token de sessão não encontrado na resposta');
        }

        const cleanToken = bruteToken.split(' ')[1];
        tokenManager.setSessionToken(cleanToken, response.body.expires_in);
        window.location.href = "/dashboard";

    } catch (error) {
        console.error("[Login] Erro ao realizar login:", error.message);
        return;
    }
}



