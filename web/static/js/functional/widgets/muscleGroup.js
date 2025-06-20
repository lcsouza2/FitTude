import { MuscleGroup } from '../../core/mapping/muscleGroupMapping.js';
import { tokenManager } from '../../core/auth.js';

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
        const groups = await MuscleGroup.getAll();
        console.log('Grupamentos carregados:', groups);
        renderMuscleGroups(groups);
    } catch (error) {
        console.error('Erro ao carregar grupamentos:', error);
    }
}

function renderMuscleGroups(groups) {
    const existingCards = mainContent.querySelectorAll('.group-card');
    existingCards.forEach(card => card.remove());
    groups.forEach(group => {
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
    card.innerHTML = `
        <div class="group-header">
            <h3>${group.group_name}</h3>
            <div>
                <button class="btn btn-outline-light btn-sm btn-edit">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-outline-danger btn-sm ms-2 btn-delete">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </div>
        <div class="muscle-list">
            ${group.muscles ? group.muscles.map(muscle => `
                <div class="muscle-item">
                    <span>${muscle.name}</span>
                    <span class="equipment-tag">${muscle.equipment_count || 0} aparelhos</span>
                </div>
            `).join('') : ''}
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