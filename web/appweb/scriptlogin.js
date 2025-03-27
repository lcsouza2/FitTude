document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const senhaInput = document.getElementById('senha');

    loginForm.addEventListener('submit', (evento) => {
        evento.preventDefault();

        const email = emailInput.value;
        const senha = senhaInput.value;

        if (email && senha) {
            console.log('Login tentado com:', email);
            // Adicione aqui a lógica de autenticação
        } else {
            alert('Por favor, preencha todos os campos');
        }
    });
});