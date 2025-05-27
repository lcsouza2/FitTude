// Dados para o gráfico de progresso
import { ApiClient } from './core/auth.js';
import { BaseUrl } from './core/utils.js';
const ctx = document.getElementById('progressChart').getContext('2d');

function verifacar_login(){
    const api = new ApiClient(BaseUrl)
    const token = sessionStorage.getItem('token'); // Obtém o token do sessionStorage
    api.get('user/validate_token',{
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(
        response => {
            if (response.status === 200) {
                console.log("Token válido, usuário autenticado.");
            } else if (response.status === 401) {
                console.error("Token inválido ou expirado. Redirecionando para a página de login.");
                sessionStorage.removeItem('token'); // Remove o token do sessionStorage
                window.location.href = "login.html"; // Redireciona para a página de login
            } else {
                console.error("Erro ao validar o token:", response.status);
            }
        },
        error => {
            console.error("Erro ao fazer a requisição:", error);
        }
    )
}

const progressChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['10/Jan', '17/Jan', '24/Jan', '31/Jan', '07/Fev', '14/Fev', '21/Fev', '28/Fev', '07/Mar', '14/Mar', '21/Mar', '28/Mar'],
        datasets: [{
            label: 'Carga (kg)',
            data: [80, 82.5, 85, 85, 87.5, 90, 92.5, 92.5, 95, 97.5, 100, 105],
            backgroundColor: 'rgba(81, 15, 235, 0.2)',
            borderColor: 'rgba(81, 15, 235, 1)',
            borderWidth: 2,
            tension: 0.3,
            pointBackgroundColor: '#fff',
            pointBorderColor: 'rgba(81, 15, 235, 1)',
            pointRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: false,
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                    color: '#adb5bd'
                }
            },
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                    color: '#adb5bd'
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: '#fff'
                }
            }
        }
    }
});
