import { authApiClient, tokenManager } from '../core/auth.js';

// Exemplo de função para buscar exercícios da API
async function fetchExercises() {
    try {
        const response = await authApiClient.get('/api/data/exercises' ,{
        
        });
        if (response.ok) {
            renderExercises(response.body);
        } else {
            alert('Erro ao buscar exercícios');
        }
    } catch (error) {
        alert('Erro ao buscar exercícios');
    }
}

// Renderiza os cards de exercícios dinamicamente
function renderExercises(exercises) {
    const row = document.querySelector('.row.g-4');
    row.innerHTML = '';
    exercises.forEach(ex => {
        row.innerHTML += `
        <div class="col-lg-6">
            <div class="card exercise-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title mb-0">${ex.name}</h5>
                        <div class="dropdown">
                            <button class="btn btn-outline-custom btn-sm" type="button" data-bs-toggle="dropdown">⋯</button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item btn-edit" data-id="${ex.id}" href="#">Editar</a></li>
                                <li><a class="dropdown-item btn-delete" data-id="${ex.id}" href="#">Excluir</a></li>
                            </ul>
                        </div>
                    </div>
                    <p class="text-muted-custom mb-2">${ex.description || ''}</p>
                    <div class="mb-2">
                        ${(ex.muscles || []).map(m => `<span class="badge badge-custom">${m}</span>`).join('')}
                    </div>
                    <div class="mb-2">
                        <small class="text-muted-custom">Equipamentos: ${(ex.equipments || []).join(', ')}</small>
                    </div>
                </div>
            </div>
        </div>`;
    });

    // Adiciona eventos de exclusão
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            if (confirm('Deseja excluir este exercício?')) {
                await deleteExercise(btn.dataset.id);
            }
        });
    });
}

// Função para criar um novo exercício
async function createExercise(data) {
    try {
        const response = await authApiClient.post('/api/data/exercises/new', data);
        if (response.ok) {
            fetchExercises();
            bootstrap.Modal.getInstance(document.getElementById('addExerciseModal')).hide();
        } else {
            alert('Erro ao criar exercício');
        }
    } catch (error) {
        alert('Erro ao criar exercício');
    }
}

// Função para deletar exercício
async function deleteExercise(id) {
    try {
        const response = await authApiClient.delete(`/api/data/exercises/delete/${id}`);
        if (response.ok) {
            fetchExercises();
        } else {
            alert('Erro ao excluir exercício');
        }
    } catch (error) {
        alert('Erro ao excluir exercício');
    }
}

// Evento do botão de salvar exercício
document.querySelector('.button-style').addEventListener('click', async () => {
    const name = document.getElementById('exerciseName').value;
    const description = document.getElementById('exerciseDescription').value;
    const muscles = [];
    ['peitoral', 'triceps', 'ombros', 'costas', 'biceps'].forEach(id => {
        if (document.getElementById(id).checked) muscles.push(document.querySelector(`label[for=${id}]`).textContent);
    });
    const equipments = [];
    ['barra', 'halter', 'maquina', 'cabo', 'peso-corpo'].forEach(id => {
        if (document.getElementById(id).checked) equipments.push(document.querySelector(`label[for=${id}]`).textContent);
    });

    if (!name) {
        alert('Preencha o nome do exercício');
        return;
    }

    await createExercise({ name, description, muscles, equipments });
});

// Logout
document.getElementById('logoff').addEventListener('click', () => {
    tokenManager.logout();
});

// Carrega os exercícios ao abrir a página
fetchExercises();