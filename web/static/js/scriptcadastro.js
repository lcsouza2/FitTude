function realizarCadastro(username, email, senha) {
    fetch("https://fittude.onrender.com/api/user/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "username": username,
            "email": email,
            "password": senha
        })
    })
    .then(response => {
        if (response.ok) {
            console.log("200 OK:", response);
        }
        if (response.status == 409) {
            exibirMensagem('Email já cadastrado.', 'error');
            return;
        }
        else if (response.status == 400) {
            exibirMensagem('Erro ao cadastrar usuário. Tente novamente.', 'error');
            return;
        }
        else if (response.status == 500) {
            exibirMensagem('Erro interno do servidor. Tente novamente mais tarde.', 'error');
            return;
        }
        return response.json();
    })
    .then(data => {
        console.log("Sucesso:", data);
        if (data.sucesso) {
            exibirMensagem('Cadastro realizado com sucesso!', 'sucesso');
            
        } else {
            exibirMensagem('Erro ao cadastrar usuário. Tente novamente.', 'error');
        }
    })
    .catch(error => {
        console.error(error);
        exibirMensagem("MANO DEU RUIM", 'error');

    });
}
function consoleloger(sela, sela2,sela3) {
    console.log(sela,sela2,sela3);
}

function exibirMensagem(mensagem, tipo) {
    const mensagemElement = document.getElementById('mensagem');

    if (mensagemElement.style.opacity === '1') {
        // Se a mensagem já está visível, não reinicia a animação
        return;
    }

    mensagemElement.textContent = mensagem;
    mensagemElement.style.transition = 'none'; // Remove transições anteriores
    mensagemElement.style.opacity = '0'; // Reseta a opacidade
    mensagemElement.style.transform = 'translateY(-100%)'; // Reseta a posição
    void mensagemElement.offsetWidth; // Força o reflow para reiniciar a animação

    mensagemElement.style.transition = 'transform 0.5s ease-in-out, opacity 0.5s ease-in-out';
    mensagemElement.style.opacity = '1';
    mensagemElement.style.transform = 'translateY(0)';
    mensagemElement.className = `mensagem ${tipo}`; 
    mensagemElement.style.display = 'block';

    if (tipo == 'sucesso') {
        mensagemElement.style.color = 'lightgreen';
    } else if (tipo == 'error') {
        mensagemElement.style.color = '#ff6666'; // Vermelho claro
    }

    setTimeout(() => {
        mensagemElement.style.opacity = '0';
        mensagemElement.style.transform = 'translateY(-100%)';
    }, 10000); // Tempo antes de ocultar a mensagem (10 segundos)
}

document.addEventListener('DOMContentLoaded', function() {
    const cadastroForm = document.getElementById('registerForm');
    
    cadastroForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        //const username = document.getElementById('username').value; faça o o campo de username ana julia
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;
        const confirmarSenha = document.getElementById('confirmarSenha').value;

        
        username = "RAFAEL"
        
        function validarSenha(senha) {
            const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
            return regex.test(senha);
        }

        if (!validarSenha(senha)) {
            exibirMensagem('A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos.', 'error');
            return;
        }
        if (senha !== confirmarSenha) {
            exibirMensagem('As senhas não coincidem.', 'error');
            return;
        }
        else {
            realizarCadastro(username, email, senha);
        }
        
    });
});