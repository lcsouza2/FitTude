import { authApiClient } from "../core/auth.js";

const textemail = document.getElementById('useremail');
const email = window.sessionStorage.getItem('user_email')
const fullname = window.sessionStorage.getItem('user_fullname');
const changePasswordForm = document.getElementById('changePasswordForm');
textemail.value = email;


changePasswordForm.addEventListener('submit', async function(event) {
    event.preventDefault();
    const oldPassword = document.getElementById('oldPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmNewPassword = document.getElementById('confirmNewPassword').value;
    const msg = document.getElementById('changePasswordMessage');

    if (newPassword !== confirmNewPassword) {
        msg.className = 'alert alert-danger';
        msg.textContent = 'As novas senhas não coincidem.';
        msg.classList.remove('d-none');
        return;
    }
    try {
        const response = await authApiClient.put('/api/user/change-password', {
            email: email,
            password: oldPassword,
            name: fullname,
            new_password: newPassword
        });

        if (response.ok) {
            msg.className = 'alert alert-success';
            msg.textContent = 'Senha alterada com sucesso!';
            msg.classList.remove('d-none');this.dataset;
            changePasswordForm.reset();
        } else {
            msg.className = 'alert alert-danger';
            msg.textContent = 'Erro ao alterar senha.';
            msg.classList.remove('d-none');
        }
    } catch (error) {
        console.error("Erro ao alterar senha:", error);
        msg.className = 'alert alert-danger';
        msg.textContent = 'Erro ao alterar senha.';
        msg.classList.remove('d-none');
    }
})