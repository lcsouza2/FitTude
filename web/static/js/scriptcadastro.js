import { ApiClient } from './core/auth.js';
import { BaseUrl, exibirMensagem } from './core/utils.js';

const senhaInput = document.getElementById('senha');
const passwordRequirements = document.querySelector('.password-requirements');
const requirements = {
    length: document.getElementById('length-check'),
    uppercase: document.getElementById('uppercase-check'),
    lowercase: document.getElementById('lowercase-check'),
    number: document.getElementById('number-check'),
    special: document.getElementById('special-check')
};

function getRegisterFormData() {
    document.getElementById('confirmarSenha').value;

    return {
        email: document.getElementById('email').value,
        nome: document.getElementById('nome').value,
        senha: document.getElementById('senha').value,
        confirmarSenha: document.getElementById('confirmarSenha').value
    };
}


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



{
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


document.addEventListener('DOMContentLoaded', () => {
    const cadastroForm = document.getElementById('registerForm');
    cadastroForm.addEventListener('submit', event => {
        event.preventDefault();

    });
});

senhaInput.addEventListener('focus', function() {
    const container = document.querySelector('.password-requirements-container');
    container.classList.add('active');
    requestAnimationFrame(() => {
        document.querySelector('.password-requirements').classList.add('visible');
    });
});

senhaInput.addEventListener('blur', function() {
    if (this.value === '') {
        const container = document.querySelector('.password-requirements-container');
        document.querySelector('.password-requirements').classList.remove('visible');
        setTimeout(() => {
            container.classList.remove('active');
        }, 300); // Espera a transição terminar
    }
});

senhaInput.addEventListener('input', function() {
    const senha = this.value;
    
    if(senha.length >= 8) {
        requirements.length.classList.add('valid');
    } else {
        requirements.length.classList.remove('valid');
    }
    
    if(/[A-Z]/.test(senha)) {
        requirements.uppercase.classList.add('valid');
    } else {
        requirements.uppercase.classList.remove('valid');
    }
    
    if(/[a-z]/.test(senha)) {
        requirements.lowercase.classList.add('valid');
    } else {
        requirements.lowercase.classList.remove('valid');
    }
    
    if(/[0-9]/.test(senha)) {
        requirements.number.classList.add('valid');
    } else {
        requirements.number.classList.remove('valid');
    }
    
    if(/[!@#$%^&*(),.?":{}|<>/]/.test(senha)) {
        requirements.special.classList.add('valid');
    } else {
        requirements.special.classList.remove('valid');
    }
});