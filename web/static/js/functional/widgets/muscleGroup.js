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
        renderMuscleGroups(groups);
    } catch (error) {
        console.error('Erro ao carregar grupamentos:', error);
    }
}

function renderMuscleGroups(groups) {
    const existingCards = mainContent.querySelectorAll('.group-card:not(:first-child)');
    existingCards.forEach(card => card.remove());
    
    groups.forEach(group => {
        const groupCard = createGroupCard(group);
        groupCard.querySelector('.btn-edit').addEventListener('click', () => editGroup(group.name));
        groupCard.querySelector('.btn-delete').addEventListener('click', () => deleteGroup(group.name));
        mainContent.appendChild(groupCard);
    });
}

function createGroupCard(group) {
    const card = document.createElement('div');
    card.className = 'group-card';
    card.dataset.groupId = group.id;
    
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
        loadMuscleGroups(); // Recarrega a lista
        novoGrupamentoModal.hide();
        document.getElementById('group_name').value = ''; // Limpa o campo
    } catch (error) {
        showMessage(modalMessage, 'Erro ao criar grupamento', 'danger');
    }
});

async function editGroup(group) {
    const editModal = new bootstrap.Modal(document.getElementById('editarGrupamentoModal'));
    const editForm = document.getElementById('formEditarGrupamento');
    const editNameInput = document.getElementById('edit_group_name');
    const editIdInput = document.getElementById('edit_group_id');
    
    editNameInput.value = group.group_name;
    editIdInput.value = group.id;
    
    editModal.show();
    
    editForm.onsubmit = async (e) => {
        e.preventDefault();
        try {
            await MuscleGroup.update(group.id, editNameInput.value);
            showMessage(document.getElementById('editModalMessage'), 'Grupamento atualizado com sucesso!', 'success');
            loadMuscleGroups();
            editModal.hide();
        } catch (error) {
            showMessage(document.getElementById('editModalMessage'), 'Erro ao atualizar grupamento', 'danger');
        }
    };
}

async function deleteGroup(group_name) {
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmarExclusaoModal'));
    const confirmButton = document.getElementById('btnConfirmarExclusao');
    
    confirmModal.show();
    
    confirmButton.onclick = async () => {
        try {
            await MuscleGroup.delete(group_name);
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