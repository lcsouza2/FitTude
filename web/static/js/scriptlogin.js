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
        }
    });
});

function realizarLogin(email, senha, lembrar) {
    fetch("https://fittude-api.onrender.com/api/user/login", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "email": email,
            "password": senha,
            "keep_login": lembrar // Adiciona o campo "lembrar" no corpo da requisição

        })
    })
    
    .then(response => {
        if (response.ok) {
            console.log("200 OK:", response);
        }
       
        else if (response.status == 400) {
            exibirMensagem('Erro ao realizar login. Tente novamente.: 01', 'error');
            return;
        }
        else if (response.status == 500) {
            exibirMensagem('Erro interno do servidor. Tente novamente mais tarde.', 'error');
            return;
        }
        return response.json();

    })
    .then(data => {
        
        if (data) {
            if (data.detail) {
                exibirMensagem(data.detail, 'error');
                return;
            }
            else if (data.access_token) {
                exibirMensagem('Login realizado com sucesso!', 'sucesso');  
                sessionStorage.setItem("token", data.access_token);  //chegamos nos finalmentes

                setTimeout(() => {
                    window.location.href = "dashboard.html"; 
                }, 2000); // Aguarda 2 segundos antes de redirecionar
                
            } else {
                exibirMensagem('Erro ao realizar login. Tente novamente.', 'error');
                return;
            }; 
            //eu odeio javascript
            
        } else {
           console.log("Resposta vazia ou não JSON:", data);
        }
    })
    .catch(error => {
        exibirMensagem('Erro ao realizar login: 01', 'error');
        console.error('Erro:', error);
    });
}

function exibirMensagem(mensagem, tipo) {
    const mensagemElement = document.getElementById('mensagem');
    mensagemElement.textContent = mensagem;
    mensagemElement.className = `mensagem ${tipo}`; 
    mensagemElement.style.display = 'block';
    if (tipo == 'sucesso') {
        mensagemElement.style.color = 'lightgreen';
    }
    else if (tipo == 'error') {
        mensagemElement.style.color = '#ff6666'; // Vermelho claro
    }
}