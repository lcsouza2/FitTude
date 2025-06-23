import { authApiClient, tokenManager } from '../core/auth.js';
import { MuscleGroup } from '../core/mapping/muscleGroupMapping.js';

// Função utilitária para agrupar por group_name
function groupByGroupName(items) {
    const groups = {};
    items.forEach(item => {
        // Usa exercise_name como chave de agrupamento
        const group = item.group_name || item.exercise_name || 'Outros';
        if (!groups[group]) groups[group] = [];
        groups[group].push(item);
    });
    return groups;
}

// Busca exercícios, músculos e equipamentos juntos
async function fetchExercises() {
    try {
        const [exercisesResp, musclesResp, equipmentsResp] = await Promise.all([
            authApiClient.get('/api/data/exercises'),
            authApiClient.get('/api/data/muscles'),
            authApiClient.get('/api/data/equipment')
        ]);
        if (exercisesResp.ok && musclesResp.ok && equipmentsResp.ok) {
            // Agrupa cada resposta por group_name
            const exercisesByGroup = groupByGroupName(exercisesResp.body.filter(ex => ex.active));
            const musclesByGroup = groupByGroupName(musclesResp.body.filter(m => m.active));
            const equipmentsByGroup = groupByGroupName(equipmentsResp.body);
            renderExercisesGrouped(exercisesByGroup, musclesByGroup, equipmentsByGroup);
        
        } else {
            console.log('Erro ao buscar exercícios, músculos ou equipamentos');
        }
    } catch (error) {
        console.log('Erro ao buscar exercícios, músculos ou equipamentos');
        console.error('Erro ao buscar dados:', error);
    }
}

function renderExercisesGrouped(exercisesByGroup, musclesByGroup, equipmentsByGroup) {
    const row = document.querySelector('.row.g-4');
    // Limpa o conteúdo existente para evitar duplicação em recarregamentos
    row.innerHTML = '';
    Object.entries(exercisesByGroup).forEach(([groupName, exercises]) => {
        let itemsHtml = exercises.map(ex => {
            // Separa os músculos por vírgula e gera badge para cada
            let exerciseMuscles = [];
            if (musclesByGroup[groupName] && musclesByGroup[groupName].length > 0) {
                exerciseMuscles = musclesByGroup[groupName].flatMap(m => {
                    if (typeof m.muscle_name === 'string') {
                        return m.muscle_name.split(',').map(n => n.trim()).filter(Boolean);
                    }
                    return m.muscle_name ? [m.muscle_name] : [];
                });
            }
            const normalizedGroupName = (groupName).trim().toLowerCase();
            const foundGroup = Object.entries(equipmentsByGroup).find(([g]) => (g || '').trim().toLowerCase() === normalizedGroupName);
            let exerciseEquipments = [];
            if (foundGroup) { 
                const exerciseEquipment = foundGroup[1];
                exerciseEquipments = exerciseEquipment.map(e => e.equipment_name).filter(Boolean);
            }    
            return `
                <div class="col-lg-6">
                    <div class="card exercise-card">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h5 class="card-title mb-0">${ex.exercise_name}</h5>
                                <div class="dropdown">
                                    <button class="btn btn-outline-custom btn-sm" type="button" data-bs-toggle="dropdown">
                                        ⋯
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" data-id="${ex.exercise_id}" href="#">Editar</a></li>
                                        <li><a class="dropdown-item" data-id="${ex.exercise_id}" href="#">Excluir</a></li>
                                    </ul>
                                </div>
                            </div>
                            <p class="text-muted-custom mb-2">${ex.description || 'Sem descrição'}</p>
                            <div class="mb-2">
                                ${exerciseMuscles.map(m => `<span class=\"badge badge-custom\">${m}</span>`).join(' ')}
                            </div>
                            <div class="mb-2">
                                <small class="text-muted-custom">Equipamentos: ${exerciseEquipments.join(', ') || 'Nenhum equipamento encontrado'}</small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        const cardHtml = `${itemsHtml}`;
        row.insertAdjacentHTML('beforeend', cardHtml);
    });
    document.querySelectorAll('.dropdown-item[data-id][href="#"]').forEach(item => {
        item.addEventListener('click', async (e) => {
            e.preventDefault();
            const exerciseId = e.target.dataset.id;
            const action = e.target.textContent.trim(); // "Editar" ou "Excluir"

            if (action === 'Excluir') {
                if (confirm('Deseja excluir este exercício?')) {
                    await deleteExercise(exerciseId); // Certifique-se de que deleteExercise está definida
                }
            } else if (action === 'Editar') {
                console.log(`Editar exercício com ID: ${exerciseId}`);
                
            }
        });
    });
}

async function createExercise(data) {
    try {
        try {
            await MuscleGroup.create(data.name);
        }
        catch (error) {
            console.error('Erro ao criar grupamento de músculos:', error);
        }

        setTimeout(() => { 
        }, 3000);
    
        try {
            const response = await authApiClient.post('/api/data/equipment/new', {
                group_name: data.name,
                equipment_name: data.equipments
            });
            if (!response.ok) {
                return console.log('Erro ao criar equipamentos');
            }

            console.log("Equipamento criado com sucesso");

        } catch (error) {
            throw new Error('Erro ao criar equipamentos:', error);
        }
        try {
            const response = await authApiClient.post('/api/data/exercise/new', {
                exercise_name: data.name,
                description: data.description
            });
            if (response.ok) {
                fetchExercises();
                bootstrap.Modal.getInstance(document.getElementById('addExerciseModal')).hide();
            } else {
                error = await response.json();
                console.error('Erro ao criar exercício:', error);
            }
        } catch (error) {
            throw new Error('Erro ao criar exercício:', error);
        }

        try {
            const response = await authApiClient.post('/api/data/muscle/new', {
                group_name: data.name,
                muscle_name: data.muscle
            });

            if (!response.ok) {
                return console.log('Erro ao criar músculos');
            }
            console.log("Músculos criado com sucesso");
        } catch (error) {
            throw new Error('Erro ao criar músculos:', error);
        }

    } catch (error) {
        console.error(error);
    }
    
}

// Função para deletar exercício
async function deleteExercise(id) {
    try {
        const response = await authApiClient.delete(`/api/data/exericse/inactivate/${id}`);
        if (response.ok) {
            console.log("exercicio excluido com sucesso ");
        } else {
            console.log('Erro ao excluir exercício');
        }
    } catch (error) {
        console.error('Erro ao excluir exercício:', error);
    }
    setTimeout(() => {
        fetchExercises();
    }, 3000);

}

// Evento do botão de salvar exercício
document.getElementById('btnSubmitdados').addEventListener('click', async () => {
    const name = document.getElementById('exerciseName').value;
    const description = document.getElementById('exerciseDescription').value;
    // coloca os checkboxs em lista
    const muscletEls = document.querySelectorAll('input[name="parteCorpo"]:checked');
    const muscleaArr = Array.from(muscletEls).map(el => el.value);
    const muscle = muscleaArr.join(', ');
    // coloca os checkboxs em lista
    const equipmentEls = document.querySelectorAll('input[name="equipamento"]:checked');
    const equipmentsArr = Array.from(equipmentEls).map(el => el.value);
    const equipments = equipmentsArr.join(', ');

    console.log("Músculo selecionado:", muscle);
    console.log("Equipamentos selecionados:", equipments);

    if (!name || muscle.length === 0 || equipments.length === 0) {
        alert('Preencha o nome do exercício');
        return;
    } else {
        await createExercise({ name, description, muscle, equipments });
    }
});

fetchExercises();