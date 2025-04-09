import { secureRequest } from "./core/auth";

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

async function handleLogin(event) {
    event.preventDefault();
    
    try {
        const response = await secureRequest("/api/user/login", {
            method: "POST",
            data: {
                email: loginForm.email.value,
                password: loginForm.password.value
            }
        });

        if (response.status === 200) {
            // Redirect to dashboard or home
            window.location.href = "/dashboard";
        }
    } catch (error) {
        // Show error message
        alert("Erro no login, verifique suas credenciais.");
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    // Basic validation
    if (registerForm.Senha.value !== registerForm.ConfirmarSenha.value) {
        const errorDiv = document.getElementById("registerError");
        if (errorDiv) {
            errorDiv.textContent = "Passwords do not match";
            errorDiv.style.display = "block";
        }
        return;
    }

    try {
        const response = await secureRequest("/api/user/register", {
            method: "POST",
            data: {
                email: registerForm.email.value,
                password: registerForm.password.value,
                name: registerForm.name.value
            }
        });

        if (response.status === 201) {
            // Show success message and redirect
            window.location.href = "/login?registered=true";
        }
    } catch (error) {
        const errorDiv = document.getElementById("registerError");
        if (errorDiv) {
            errorDiv.textContent = "Registration failed. Please try again.";
            errorDiv.style.display = "block";
        }
    }
}

// Event listeners
loginForm?.addEventListener("submit", handleLogin);
registerForm?.addEventListener("submit", handleRegister);