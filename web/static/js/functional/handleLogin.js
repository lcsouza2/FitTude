import { publicApiClient, tokenManager } from '../core/auth.js';

const loginForm = document.getElementById('loginForm');
const formEmail = document.getElementById('email');
const formSenha = document.getElementById('senha');
const formLembrar = document.getElementById('remember');
const mensagemElement = document.getElementById('mensagem');

loginForm.addEventListener('submit', async function(event) {
    event.preventDefault(); // Isso impede o recarregamento da página

    try {
        if (formEmail.value && formSenha.value) {
            await realizarLogin(formEmail.value, formSenha.value, formLembrar.checked);
        } else {
            mensagemElement.innerHTML = `
                <div class="alert alert-danger mt-3" role="alert">
                    Por favor, preencha todos os campos.
                </div>
            `;
        }
    } catch (error) {
        console.error("Erro no submit:", error);
    }
});

async function realizarLogin(email, senha, lembrar) {
    // Limpar mensagem de erro anterior
    mensagemElement.innerHTML = '';
    
    try {
        const response = await publicApiClient.post('/api/user/login', {
            email: email,
            password: senha,
            keep_login: lembrar
        });

        // Se a resposta não for bem-sucedida, mostra mensagem de erro
        if (!response.ok) {
            mensagemElement.innerHTML = `
                <div class="alert alert-danger mt-3" role="alert">
                    Email ou senha incorretos. Por favor, tente novamente.
                </div>
            `;
            formSenha.value = '';
            return;
        }

        const bruteToken = response.headers.get("Authorization");
        if (!bruteToken) {
            throw new Error('Token de sessão não encontrado na resposta');
        }

        const cleanToken = bruteToken.split(' ')[1];
        tokenManager.setSessionToken(cleanToken, response.body.expires_in);
        window.location.href = "/dashboard";

    } catch (error) {
        console.error("[Login] Erro ao realizar login:", error.message);
        
        // Mostrar mensagem de erro para o usuário
        mensagemElement.innerHTML = `
            <div class="alert alert-danger mt-3" role="alert">
                Email ou senha incorretos. Por favor, tente novamente.
            </div>
        `;
        
        // Limpar o campo de senha
        formSenha.value = '';
    }
}



