import { MuscleGroup } from '../../core/mapping/muscleGroupMapping.js';
import { tokenManager, authApiClient } from '../../core/auth.js';

if (!tokenManager.getSessionToken()) {
    tokenManager.redirectToLogin();
}

const mainContent = document.querySelector('.main-content');
const btnNovoGrupamento = document.getElementById('newgrup');
const novoGrupamentoModal = new bootstrap.Modal(document.getElementById('novoGrupamentoModal'));
const formNovoGrupamento = document.getElementById('formNovoGrupamento');
const modalMessage = document.getElementById('modalMessage');


async function loadMuscleGroups() {
    try {
        // Busca todos os grupamentos e músculos usando authApiClient
        const groupsResp = await authApiClient.get('/api/data/groups');
        const musclesResp = await authApiClient.get('/api/data/muscles');
        const equipmentsResp = await authApiClient.get('/api/data/equipment');
        if (!groupsResp.ok || !musclesResp.ok) throw new Error('Erro ao buscar dados');
        const groups = groupsResp.body;
        const muscles = musclesResp.body;
        const equipments = equipmentsResp.body;
        window.equipmentsGlobal = equipments; // Salva para uso na contagem
        groups.forEach(group => {
            group.muscles = muscles.filter(muscle => muscle.group_name === group.group_name);
        });
        renderMuscleGroups(groups);
    } catch (error) {
        console.error('Erro ao carregar grupamentos:', error);
    }
}

function renderMuscleGroups(groups) {
    // Filtra apenas os grupos ativos
    const activeGroups = groups.filter(group => group.active);
    const existingCards = mainContent.querySelectorAll('.group-card');
    //existingCards.forEach(card => card.remove());
    activeGroups.forEach(group => {
        const groupCard = createGroupCard(group);
        mainContent.appendChild(groupCard);
        const btnEdit = groupCard.querySelector('.btn-edit');
        const btnDelete = groupCard.querySelector('.btn-delete');
        btnEdit.addEventListener('click', () => editGroup(group));
        btnDelete.addEventListener('click', () => deleteGroup(group.group_name));
    });
}

function createGroupCard(group) {
    const card = document.createElement('div');
    card.className = 'group-card';
    card.dataset.groupName = group.group_name;
    let musclesHtml = '';
    if (group.muscles && typeof group.muscles === 'string') {
        const muscleArr = group.muscles.split(',').map(m => m.trim()).filter(Boolean);
        musclesHtml = muscleArr.map(muscleName => `
            <div class="muscle-item">
                <span>${muscleName}</span>
                <span class="equipment-tag">Grupo ${group.group_name}</span>
            </div>
        `).join('');
    } else if (Array.isArray(group.muscles) && group.muscles.length > 0) {
        musclesHtml = group.muscles.map(muscle => {
            let names = [];
            if (typeof muscle.muscle_name === 'string') {
                names = muscle.muscle_name.split(',').map(m => m.trim()).filter(Boolean);
            } else if (muscle.name) {
                names = [muscle.name];
            }
            return names.map(name => `
                <div class="muscle-item">
                    <span>${name}</span>
                    <span class="equipment-tag">Grupo ${group.group_name}</span>
                </div>
            `).join('');
        }).join('');
    }
    card.innerHTML = `
        <div class="group-header">
            <h3>${group.group_name}</h3>
            <div>
                <button class="btn btn-edit btn-sm-custom" onclick="editGroup('${group.group_name.replace(/'/g, "\\'")}')">
                    <i class="bi bi-pencil me-1"></i>Editar
                </button>
                <button class="btn btn-delete btn-sm-custom ms-2" onclick="confirmDeleteGroup('${group.group_name.replace(/'/g, "\\'")}')">
                    <i class="bi bi-trash me-1"></i>Excluir
                </button>
            </div>
        </div>
        <div class="muscle-list">
            ${musclesHtml}
        </div>
    `;
    return card;
}

btnNovoGrupamento.addEventListener('click', () => {
    novoGrupamentoModal.show();
});

formNovoGrupamento.addEventListener('submit', async (e) => {
    e.preventDefault();
    const groupName = document.getElementById('group_name').value;
    try {
        await MuscleGroup.create(groupName);
        showMessage(modalMessage, 'Grupamento criado com sucesso!', 'success');
        loadMuscleGroups();
        novoGrupamentoModal.hide();
        document.getElementById('group_name').value = '';
    } catch (error) {
        showMessage(modalMessage, 'Erro ao criar grupamento', 'danger');
    }
});

function editGroup(group) {
    const editModal = new bootstrap.Modal(document.getElementById('editarGrupamentoModal'));
    const editForm = document.getElementById('formEditarGrupamento');
    const editNameInput = document.getElementById('edit_group_name');
    const editModalMessage = document.getElementById('editModalMessage');
    editNameInput.value = group.group_name;
    editModal.show();

    // Remove listener anterior para evitar múltiplos submits
    editForm.onsubmit = null;
    editForm.onsubmit = async (e) => {
        e.preventDefault();
        try {
            await MuscleGroup.update(group.group_name, editNameInput.value);
            showMessage(editModalMessage, 'Grupamento atualizado com sucesso!', 'success');
            loadMuscleGroups();
            setTimeout(() => {
                editModal.hide();
            }, 5000);
            
        } catch (error) {
            showMessage(editModalMessage, 'Erro ao atualizar grupamento', 'danger');
        }
    };
}

function deleteGroup(groupName) {
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmarExclusaoModal'));
    const confirmButton = document.getElementById('btnConfirmarExclusao');
    confirmModal.show();

    // Remove listener anterior para evitar múltiplas execuções
    confirmButton.onclick = null;
    confirmButton.onclick = async () => {
        try {
            await MuscleGroup.delete(groupName);
            loadMuscleGroups();
            confirmModal.hide();
            showMessage(document.getElementById('modalMessage'), 'Grupamento excluído com sucesso!', 'success');
        } catch (error) {
            showMessage(document.getElementById('modalMessage'), 'Erro ao deletar grupamento', 'danger');
        }
    };
}

function showMessage(element, message, type) {
    element.className = `alert alert-${type}`;
    element.textContent = message;
    element.classList.remove('d-none');
    
    setTimeout(() => {
        element.classList.add('d-none');
    }, 3000);
}

loadMuscleGroups();