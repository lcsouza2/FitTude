import { publicApiClient } from '../core/auth.js';
import { setPasswordRequirementsVisible, setPasswordRequirementsHidden } from '../visual/registerAssets.js';


const passwordContainer = document.querySelector('.password-requirements-container');
const passwordRequirements = document.querySelector('.password-requirements');
const cadastroForm = document.getElementById('registerForm');

const senhaInput = document.getElementById('senha');
const requirements = {
    length: document.getElementById('length-check'),
    uppercase: document.getElementById('uppercase-check'),
    lowercase: document.getElementById('lowercase-check'),
    number: document.getElementById('number-check'),
    special: document.getElementById('special-check')
};


async function realizarCadastro(nome, email, senha) {
    try {
        const {headers, body} = await publicApiClient.post('/api/user/register', {
            email: email,
            password: senha,
            name: nome
        })

        if (!headers.ok) {
            throw new Error('Erro ao realizar cadastro: ' + headers.statusText);
        } else {
            window.location.href = '/check_mail';
        }
    }

    catch(error){
        console.error("[Cadastro] Erro ao realizar cadastro:", error.message);
    }
}


cadastroForm.addEventListener('submit', async(event) => { 
    event.preventDefault();

    const email = document.getElementById('email').value;
    const nome = document.getElementById('nome').value;
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmarSenha').value;

    if (senha !== confirmarSenha) {
        document.getElementById('password-mismatch-error').style.display = 'block';
        return;
    }
    else {
        await realizarCadastro(nome, email, senha);
    }
});

senhaInput.addEventListener('focus', function() {
        setPasswordRequirementsVisible(passwordContainer);

        requestAnimationFrame(() => {
        passwordRequirements.classList.add('visible');
    });
});

senhaInput.addEventListener('blur', function() {
    setPasswordRequirementsHidden( passwordContainer);

    
    setTimeout(() => {
        passwordContainer.classList.remove('active');
    }, 300); 
    
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