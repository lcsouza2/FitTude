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
            const musclesByGroup = groupByGroupName(musclesResp.body);
            const equipmentsByGroup = groupByGroupName(equipmentsResp.body);
            console.log('Exercícios agrupados:', exercisesByGroup);
            console.log('Músculos agrupados:', musclesByGroup);
            console.log('Equipamentos agrupados:', equipmentsByGroup);
            renderExercisesGrouped(exercisesByGroup, musclesByGroup, equipmentsByGroup);
        
        } else {
            alert('Erro ao buscar exercícios, músculos ou equipamentos');
        }
    } catch (error) {
        alert('Erro ao buscar exercícios, músculos ou equipamentos');
        console.error('Erro ao buscar dados:', error);
    }
}

function renderExercisesGrouped(exercisesByGroup, musclesByGroup, equipmentsByGroup) {
    const row = document.querySelector('.row.g-4');
    row.innerHTML = '';
    Object.entries(exercisesByGroup).forEach(([groupName, exercises]) => {
        // LOG: Veja todos os nomes de grupo dos equipamentos agrupados
        console.log('Grupo atual:', groupName);
        console.log('Grupos disponíveis em equipmentsByGroup:', Object.keys(equipmentsByGroup));

        let itemsHtml = exercises.map(ex => {
            // LOG: Veja o group_name do exercício
            console.log('Exercício:', ex.exercise_name, 'group_name:', ex.group_name);

            const exerciseMuscles = (musclesByGroup[groupName] || []).map(m => m.muscle_name || m.name);

            // LOG: Veja todos os equipamentos desse grupo
            const normalizedGroupName = (groupName || '').trim().toLowerCase();
            const foundGroup = Object.entries(equipmentsByGroup)
                .find(([g]) => (g || '').trim().toLowerCase() === normalizedGroupName);
            console.log('Equipamentos encontrados para o grupo:', foundGroup);

            const exerciseEquipments = (foundGroup?.[1] || []).map(e => e.equipament_name).filter(Boolean);

            // LOG: Veja o resultado final dos equipamentos para o exercício
            console.log('Equipamentos do exercício:', exerciseEquipments);
            
            return `
                <div class=\"card exercise-card mb-3\">
                    <div class=\"card-body\">
                        <div class=\"d-flex justify-content-between align-items-start mb-2\">
                            <h5 class=\"card-title mb-0\">${ex.exercise_name}</h5>
                            <div class=\"dropdown\">
                                <button class=\"btn btn-outline-custom btn-sm\" type=\"button\" data-bs-toggle=\"dropdown\">⋯</button>
                                <ul class=\"dropdown-menu\">
                                    <li><a class=\"dropdown-item btn-edit\" data-id=\"${ex.exercise_id}\" href=\"#\">Editar</a></li>
                                    <li><a class=\"dropdown-item btn-delete\" data-id=\"${ex.exercise_id}\" href=\"#\">Excluir</a></li>
                                </ul>
                            </div>
                        </div>
                        <p class=\"text-muted-custom mb-2\">${ex.description || ''}</p>
                        <div class=\"mb-2\">
                            ${exerciseMuscles.map(m => `<span class=\"badge badge-custom\">${m}</span>`).join('')}
                        </div>
                        <div class=\"mb-2\">
                            <p class=\"text-muted-custom mb-2\">Equipamentos:</p>
                            <span class=\"text-white\">${exerciseEquipments.join(', ') || '-'}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        const cardHtml = `
            <div class=\"equipment-card\">
                <div class=\"equipment-header\">
                    <h3>${groupName}</h3>
                </div>
                <div class=\"equipment-list\">
                    ${itemsHtml}
                </div>
            </div>
        `;
        row.insertAdjacentHTML('beforeend', cardHtml);
    });
    // Eventos de delete
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            if (confirm('Deseja excluir este exercício?')) {
                await deleteExercise(btn.dataset.id);
            }
        });
    });
}


// Ajuste no trecho que renderiza os equipamentos corretamente com base no group_name
function renderExercises(exercises, muscles, equipments) {
    const row = document.querySelector('.row.g-4');
    const activeExercises = exercises.filter(ex => ex.active);
    activeExercises.forEach(ex => {
        // Musculatura por grupo
        const exerciseMuscles = muscles
            .filter(m => m.group_name === ex.group_name)
            .map(m => m.muscle_name || m.name);

        // Equipamentos por grupo
        const exerciseEquipments = equipments.filter(e => e.group_name === ex.group_name);
        console.log("Equipamentos do exercício:", exerciseEquipments);
        console.log("Nome do exercício:", ex.exercise_name);
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
                        ${exerciseMuscles.map(m => `<span class="badge badge-custom">${m}</span>`).join('')}
                    </div>
                    <div class="mb-2">
                        <p class="text-muted-custom mb-2">Equipamentos:</p>
                        ${exerciseEquipments.map(e => `<span class="badge bg-secondary">${e.equipament_name}</span>`).join('')}
                    </div>
                </div>
            </div>
        </div>`;
    });

    // Eventos de delete
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
        console.error('Erro ao criar exercício:', error);
        alert('Erro ao criar exercício');
    }
    let muscle_name = "";
    if (data.muscle == "Superior") {
        muscle_name = "Peitoral,Tríceps,Bíceps,Ombros,Costas,Trapézio,Deltóides,Antebraço";
    }
    else if (data.muscle == "Inferior") {
        muscle_name = "Quadríceps,Posterior da Coxa,Glúteos,Panturrilha,Adutores,Abdutores,Flexores do Quadril";
    }

    try {
        const response = await authApiClient.post('/api/data/muscle/new', {
            muscle_group: data.name,
            muscle_name: muscle_name
        });

        if (!response.ok) {
            return alert('Erro ao criar músculos');
        }
        alert("Músculos criado com sucesso");
    } catch (error) {
        console.error('Erro ao associar músculos ao exercício:', error);
    }
    try {
        await MuscleGroup.create(data.name);
    }
    catch (error) {
        console.error('Erro ao criar grupamento de músculos:', error);
    }

    try {
        const response = await authApiClient.post('/api/data/equipment/new', {
            group_name: data.name,
            equipment_name: data.equipments
        });
        if (!response.ok) {
            return alert('Erro ao criar equipamentos');
        }
        alert("Equipamento criado com sucesso");
    } catch (error) {
        console.error('Erro ao criar equipamentos:', error);
    }

}

// Função para deletar exercício
async function deleteExercise(id) {
    try {
        const response = await authApiClient.delete(`/api/data/exericse/inactivate/${id}`);
        if (response.ok) {
            alert("exercicio excluido com sucesso ");
        } else {
            alert('Erro ao excluir exercício');
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
    const muscle = document.querySelector('input[name="parteCorpo"]:checked')?.value || null;
    // Coleta todos os equipamentos selecionados (checkbox)
    const equipmentEls = document.querySelectorAll('input[name="equipamento"]:checked');
    const equipmentsArr = Array.from(equipmentEls).map(el => el.value);
    const equipments = equipmentsArr.join(',');

    console.log("Músculo selecionado:", muscle);
    console.log("Equipamentos selecionados:", equipments);

    if (!name || muscle === null || equipments.length === 0) {
        alert('Preencha o nome do exercício');
        return;
    } else {
        await createExercise({ name, description, muscle, equipments });
    }
});

fetchExercises();