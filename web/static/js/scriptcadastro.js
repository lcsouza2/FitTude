document.addEventListener('DOMContentLoaded', function() {
    const cadastroForm = document.getElementById('registerForm');
    
    cadastroForm.addEventListener('submit', function(e) {
        e.preventDefault();
        

        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;
        const confirmarSenha = document.getElementById('confirmarSenha').value;

        
        username = "RAFAEL OFICIAL"
        
        if (senha !== confirmarSenha) {
            exibirMensagem('As senhas não coincidem.', 'error');

            return;
        }
        if (senha.length < 6) {
            exibirMensagem('A senha deve ter pelo menos 6 caracteres.', 'error');
            return;
        }
        
        realizarCadastro(username, email, senha);
    });
});


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
        setTimeout(() => {
        } , 5000); // 3 segundos de espera antes do redirecionamento
        if (response.status === 400) {
            throw new Error("Email já cadastrado");
        } else if (response.status === 500) {
            throw new Error("Erro interno do servidor");
        } else if (response.status === 200) {
            return response.json();
        } else if (response.status === 201) {
            return response.json();
        } else if (response.status === 401) {
            throw new Error("Email ou senha inválidos");
        } else if (response.status === 403) {
            throw new Error("Acesso negado");
        } else if (response.status === 404) {
            throw new Error("Recurso não encontrado");
        }
        return response.json();
    })
    .then(data => {
        alert(data.message); // mostra: "Email de verificação enviado..."
        console.log("Sucesso:", data);
        exibirMensagem('Cadastro realizado com sucesso! Verifique seu email para ativar sua conta.', 'sucesso');
        setTimeout(() => {
            // Redirecionar para a página de login após cadastro
            window.location.href = 'login.html';
        }, 5000); // 3 segundos de espera antes do redirecionamento
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Erro ao registrar usuário. Tente novamente.");
    });
}
function consoleloger(sela, sela2,sela3) {
    console.log(sela,sela2,sela3);
}

function exibirMensagem(mensagem, tipo) {
    const mensagemElement = document.getElementById('mensagem');
    mensagemElement.textContent = mensagem;
    mensagemElement.style.opacity = '1';
    if (mensagemElement.style.transform == 'translateY(0)'){
        mensagemElement.style.transform = 'translateY(-100%)';
    }
    else {
        mensagemElement.style.transform = 'translateY(0)';
    }
    mensagemElement.style.transition = 'transform 0.5s ease-in-out, opacity 0.5s ease-in-out';
    mensagemElement.className = `mensagem ${tipo}`; 
    mensagemElement.style.display = 'block';
    if (tipo == 'sucesso') {
        mensagemElement.style.color = 'lightgreen';
    }
    else if (tipo == 'error') {
        mensagemElement.style.color = '#ff6666'; // Vermelho claro
    }
    setTimeout(() => {
        mensagemElement.style.opacity = '0';
        setTimeout(() => {
            mensagemElement.style.display = 'none';
        }, 500); // Tempo para ocultar a mensagem após a animação
    }, 3000); // Tempo antes de ocultar a mensagem (3 segundos)
    mensagemElement.style.transform = 'translateY(0)';
}
