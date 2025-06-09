import { publicApiClient } from '../core/auth.js';

const cadastroForm = document.getElementById('registerForm');
const formEmail = document.getElementById('email');
const formNome = document.getElementById('nome');
const formSenha = document.getElementById('senha');
const formConfirmarSenha = document.getElementById('confirmarSenha');


async function realizarCadastro(nome, email, senha) {
    try {
        const response = await publicApiClient.post('/api/user/register', {
            email: email,
            password: senha,
            name: nome
        })

        if (!response.ok) {
            console.log(response)
            throw new Error('Erro ao realizar cadastro: ' + response.statusText);
        } else {
            window.location.href = '/check_mail';
        }
    }
    catch(error){
        console.error(error);
    }
}


cadastroForm.addEventListener('submit', async(event) => { 
    event.preventDefault();

    if (formSenha.value !== formConfirmarSenha.value) {
        document.getElementById('password-mismatch-error').style.display = 'block';
        return;
    }
    else {
        await realizarCadastro(formNome.value, formEmail.value, formSenha.value);
    }
});