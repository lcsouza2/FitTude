// Dados para o gráfico de progresso

const ctx = document.getElementById('progressChart').getContext('2d');

const token = sessionStorage.getItem('token');
if (!token) {
    window.location.href = "login.html"; // Redireciona para a página de login se o token não estiver presente
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
