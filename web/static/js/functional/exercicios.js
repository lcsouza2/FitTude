import { authApiClient, tokenManager } from '../core/auth.js';

// Busca exercícios e músculos juntos
async function fetchExercises() {
    try {
        const [exercisesResp, musclesResp] = await Promise.all([
            authApiClient.get('/api/data/exercises'),
            authApiClient.get('/api/data/muscles')
        ]);
        if (exercisesResp.ok && musclesResp.ok) {
            renderExercises(exercisesResp.body, musclesResp.body);
        } else {
            alert('Erro ao buscar exercícios ou músculos');
        }
    } catch (error) {
        alert('Erro ao buscar exercícios ou músculos');
    }
}

// Renderiza os cards de exercícios dinamicamente
function renderExercises(exercises, muscles) {
    const row = document.querySelector('.row.g-4');
    // Filtra apenas exercícios ativos
    const activeExercises = exercises.filter(ex => ex.active);
    activeExercises.forEach(ex => {
        // Associa músculos pelo id
        let exerciseMuscleNames = [];
        if (ex.muscles && Array.isArray(ex.muscles)) {
            exerciseMuscleNames = ex.muscles.map(muscleId => {
                const muscle = muscles.find(m => m.id === muscleId);
                return muscle ? muscle.name : '';
            }).filter(Boolean);
        }
        row.innerHTML += `
        <div class="col-lg-6">
            <div class="card exercise-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title mb-0">${ex.exercise_name}</h5>
                        <div class="dropdown">
                            <button class="btn btn-outline-custom btn-sm" type="button" data-bs-toggle="dropdown">⋯</button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item btn-edit" data-id="${ex.exercise_id}" href="#">Editar</a></li>
                                <li><a class="dropdown-item btn-delete" data-id="${ex.exercise_id}" href="#">Excluir</a></li>
                            </ul>
                        </div>
                    </div>
                    <p class="text-muted-custom mb-2">${ex.description || ''}</p>
                    <div class="mb-2">
                        ${exerciseMuscleNames.map(m => `<span class="badge badge-custom">${m}</span>`).join('')}
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
        // Cria o exercício
        const response = await authApiClient.post('/api/data/exercise/new',{
            exercise_name: data.name,
            description: data.description
        });
        if (response.ok) {
            const muscleGroupMap = {
                    'peitoral': 'Peito',
                    'triceps': 'Braço',
                    'ombros': 'Ombro',
                    'costas': 'Costas',
                    'biceps': 'Braço'
                };
            const exerciseId = response.body.id || response.body.exercise_id;
            console.log("Exercício criado com ID:", exerciseId);
            for (const muscleKey of data.muscles) {
                const muscle_group = muscleGroupMap[muscleKey] || 'Outro';
                const labelEl = document.querySelector(`label[for=${muscleKey}]`);
                console.log("Label encontrado:", labelEl);
                if (!labelEl) continue; // segurança
                const muscle_name = labelEl.textContent;
                console.log("Criando músculo:", muscle_name, muscle_group);

                

                if (createResp.ok && createResp.body && createResp.body.id) {
                    await authApiClient.post('/api/data/exercise/bind_muscle', {
                        exercise_id: exerciseId,
                        muscle_id: createResp.body.id
                    });
                }
            }
            
            // Associa equipamentos existentes
            if (data.equipments && data.equipments.length > 0 && exerciseId) {
                const equipmentsResp = await authApiClient.get('/api/data/equipment');
                if (equipmentsResp.ok) {
                    const allEquipments = equipmentsResp.body;
                    await Promise.all(data.equipments.map(async (equipmentName) => {
                        const equipment = allEquipments.find(eq => eq.name === equipmentName || eq.equipment_name === equipmentName);
                        if (equipment) {
                            await authApiClient.post('/api/data/exercise/bind_equipment', {
                                exercise_id: exerciseId,
                                equipment_id: equipment.id
                            });
                        }
                    }));
                }
            }
            fetchExercises();
            bootstrap.Modal.getInstance(document.getElementById('addExerciseModal')).hide();
        } else {
            error = await response.json();
            console.error('Erro ao criar exercício:', error);
        }
    } catch (error) {
        console.error('Erro ao criar exercício:', error);
        alert('Erro ao criar exercício');
    }
}

// Função para deletar exercício
async function deleteExercise(id) {
    try {
        const response = await authApiClient.delete(`/api/data/exericse/inactivate/${id}`);
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
document.getElementById('btnSubmitdados').addEventListener('click', async () => {
    const name = document.getElementById('exerciseName').value;
    const description = document.getElementById('exerciseDescription').value;

    // Envia os IDs (não o label text)
    const muscles = [];
    ['peitoral', 'triceps', 'ombros', 'costas', 'biceps'].forEach(id => {
        if (document.getElementById(id).checked) muscles.push(id);
    });

    const equipments = [];
    ['barra', 'halter', 'maquina', 'cabo', 'peso-corpo'].forEach(id => {
        if (document.getElementById(id).checked) equipments.push(document.querySelector(`label[for=${id}]`).textContent);
    });

    if (!name) {
        alert('Preencha o nome do exercício');
        return;
    } else {
        await createExercise({ name, description, muscles, equipments });
    }
});


// Logout
document.getElementById('logoff').addEventListener('click', () => {
    tokenManager.logout();
});

// Carrega os exercícios ao abrir a página
fetchExercises();