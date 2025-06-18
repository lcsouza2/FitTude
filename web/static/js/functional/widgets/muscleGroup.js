import { MuscleGroup } from '../../core/mapping/muscleGroupMapping.js';
import { tokenManager } from '../../core/auth.js';

// Verifica autenticação
if (!tokenManager.getSessionToken()) {
    tokenManager.redirectToLogin();
}

// Elementos do DOM
const mainContent = document.querySelector('.main-content');
const btnNovoGrupamento = document.getElementById('newgrup');
const novoGrupamentoModal = new bootstrap.Modal(document.getElementById('novoGrupamentoModal'));
const formNovoGrupamento = document.getElementById('formNovoGrupamento');
const modalMessage = document.getElementById('modalMessage');

// Carrega todos os grupamentos ao iniciar
async function loadMuscleGroups() {
    try {
        const groups = await MuscleGroup.getAll();
        renderMuscleGroups(groups);
    } catch (error) {
        console.error('Erro ao carregar grupamentos:', error);
    }
}

// Renderiza os grupamentos na tela
function renderMuscleGroups(groups) {
    // Limpa todos os group-cards existentes
    const existingCards = mainContent.querySelectorAll('.group-card:not(:first-child)');
    existingCards.forEach(card => card.remove());
    
    groups.forEach(group => {
        const groupCard = createGroupCard(group);
        mainContent.appendChild(groupCard);
    });
}

// Cria um novo card de grupamento
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
    
    // Adiciona eventos aos botões
    card.querySelector('.btn-edit').addEventListener('click', () => editGroup(group));
    card.querySelector('.btn-delete').addEventListener('click', () => deleteGroup(group.id));
    
    return card;
}

// Abre o modal de novo grupamento
btnNovoGrupamento.addEventListener('click', () => {
    novoGrupamentoModal.show();
});

// Criar novo grupamento
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

// Editar grupamento
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

// Deletar grupamento
async function deleteGroup(groupId) {
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmarExclusaoModal'));
    const confirmButton = document.getElementById('btnConfirmarExclusao');
    
    confirmModal.show();
    
    confirmButton.onclick = async () => {
        try {
            await MuscleGroup.delete(groupId);
            loadMuscleGroups();
            confirmModal.hide();
            showMessage(document.getElementById('modalMessage'), 'Grupamento excluído com sucesso!', 'success');
        } catch (error) {
            showMessage(document.getElementById('modalMessage'), 'Erro ao deletar grupamento', 'danger');
        }
    };
}

// Função auxiliar para mostrar mensagens
function showMessage(element, message, type) {
    element.className = `alert alert-${type}`;
    element.textContent = message;
    element.classList.remove('d-none');
    
    setTimeout(() => {
        element.classList.add('d-none');
    }, 3000);
}

// Inicia o carregamento dos grupamentos
loadMuscleGroups();