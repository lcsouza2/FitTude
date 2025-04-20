document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;
        
        
        realizarLogin(email, senha);
    });
});

function realizarLogin(email, senha) {
    fetch("https://fittude.onrender.com/api/user/login", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "login_key": email,
            "password": senha,
            "keep_login": true
            
        })
    })
    
    .then(response => {
        if (response.ok) {
            console.log("200 OK:", response);
        }
       
        else if (response.status == 400) {
            exibirMensagem('Erro ao realizar login. Tente novamente.', 'error');
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
        exibirMensagem('Erro ao realizar login', 'error');
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