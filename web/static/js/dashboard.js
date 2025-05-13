// Dados para o gráfico de progresso

const ctx = document.getElementById('progressChart').getContext('2d');

// const token = sessionStorage.getItem('token');
// if (!token) {
//     window.location.href = "login.html"; // Redireciona para a página de login se o token não estiver presente
// }
// else {
//     fetch("https://fittude-api.onrender.com/api/user/me", {
//         method: 'GET',
//         headers: {
//             'Authorization': `Bearer ${token}`
//         }
//     })
//     .then(response => {
//         if (response.ok) {
//             console.log("200 OK:", response);
//         } else if (response.status == 401) {
//             exibirMensagem('Token inválido ou expirado. Faça login novamente.', 'error');
//             sessionStorage.removeItem('token'); // Remove o token do sessionStorage
//             window.location.href = "login.html"; // Redireciona para a página de login
//             return;
//         } else if (response.status == 500) {
//             exibirMensagem('Erro interno do servidor. Tente novamente mais tarde.', 'error');
//             return;
//         }
//         return response.json();
// })};
https://prod.liveshare.vsengsaas.visualstudio.com/join?736891C353F78512611A237C1DE90DE43A8B
        

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
