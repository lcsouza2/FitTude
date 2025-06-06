// Dados para o gráfico de progresso
import { ApiClient } from './core/auth.js';
import { BaseUrl } from './core/utils.js';

validateToken()

async function validateToken() {
    const api = new ApiClient(BaseUrl)
    try {
        const token = sessionStorage.getItem('token'); // Obtém o token do sessionStorage
        const {headers , body} = await api.get('user/validate_token',{
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
    
        if (body.message === 'Token is valid') {
            return;
        } else {
            console.error("Token inválido, redirecionando para login...");
            setTimeout(() => {
                window.localation.href = "login"; 
            }, 3000);

        }
    } catch (error) {
        console.error("[Dashboard] Erro ao validar token:", error);
        setTimeout(() => {
             window.localation.href = "login"; 
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('progressChart').getContext('2d');
    
    const chartData = {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        datasets: [{
            label: 'Carga (kg)',
            data: [60, 65, 70, 72, 75, 80],
            borderColor: '#510feb',
            backgroundColor: 'rgba(81, 15, 235, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: '#510feb',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#510feb',
            pointRadius: 5,
            pointHoverRadius: 7
        }]
    };

    const chartConfig = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    top: 20,
                    right: 25,
                    bottom: 20,
                    left: 15
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#ececec',
                        padding: 10,
                        font: {
                            size: 12,
                            family: '"Kanit", sans-serif'
                        }
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#ececec',
                        padding: 10,
                        font: {
                            size: 12,
                            family: '"Kanit", sans-serif'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#ececec',
                        font: {
                            size: 12,
                            family: '"Kanit", sans-serif'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(20, 20, 20, 0.9)',
                    titleFont: {
                        size: 14,
                        family: '"Kanit", sans-serif'
                    },
                    bodyFont: {
                        size: 13,
                        family: '"Kanit", sans-serif'
                    },
                    padding: 12,
                    displayColors: false
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            elements: {
                line: {
                    borderJoinStyle: 'round'
                }
            }
        }
    };

    const progressChart = new Chart(ctx, chartConfig);
});