import { authApiClient, tokenManager } from '../core/auth.js';

const mainContent = document.querySelector('.main-content');
const dashboardHeader = document.querySelector('.dashboard-header');

function groupEquipmentsByGroup(equipments) {
    const groups = {};
    equipments.forEach(eq => {
        const group = eq.group_name || 'Outros';
        if (!groups[group]) groups[group] = [];
        groups[group].push(eq);
    });
    return groups;
}

// Função para buscar aparelhos
async function fetchEquipments() {
    try {
        const response = await authApiClient.get('/api/data/equipment');
        if (response.ok) {
            renderEquipments(response.body);
        } else {
            alert('Erro ao buscar aparelhos');
        }
    } catch (error) {
        alert('Erro ao buscar aparelhos');
    }
}

// Renderiza os cards de aparelhos
function renderEquipments(equipments) {
    // Remove todos os cards antigos, mas mantém o header
    const oldCards = mainContent.querySelectorAll('.equipment-card, .text-center.text-muted');
    oldCards.forEach(card => card.remove());
    if (!equipments || equipments.length === 0) {
        mainContent.insertAdjacentHTML('beforeend', '<p class="text-center text-muted">Nenhum aparelho cadastrado.</p>');
        return;
    }
    const groups = groupEquipmentsByGroup(equipments);
    Object.entries(groups).forEach(([groupName, items]) => {
        let itemsHtml = items.map(eq => `
            <div class="equipment-item">
                <span>${eq.equipment_name || eq.name || 'Aparelho'}</span>
                <div class="equipment-actions">
                    <button class="btn btn-outline-light btn-sm btn-edit" data-group="${groupName}" data-name="${eq.equipment_name}"><i class="bi bi-pencil"></i></button>
                    <button class="btn btn-outline-danger btn-sm btn-delete" data-group="${groupName}" data-name="${eq.equipment_name}"><i class="bi bi-trash"></i></button>
                </div>
            </div>
        `).join('');
        const cardHtml = `
            <div class="equipment-card">
                <div class="equipment-header">
                    <h3>${groupName}</h3>
                </div>
                <div class="equipment-list">
                    ${itemsHtml}
                </div>
            </div>
        `;
        mainContent.insertAdjacentHTML('beforeend', cardHtml);
    });
    // Adiciona eventos de editar e deletar
    mainContent.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', () => openEditModal(btn.dataset.group, btn.dataset.name));
    });
    mainContent.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', () => deleteEquipment(btn.dataset.group, btn.dataset.name));
    });
}

// Modal dinâmico para adicionar/editar
function ensureModal() {
    let modal = document.getElementById('equipmentModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'equipmentModal';
        modal.tabIndex = -1;
        modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content bg-dark">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title" id="equipmentModalLabel">Novo Aparelho</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="formEquipment">
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="equipment_group" class="form-label">Grupamento</label>
                            <input type="text" class="form-control bg-dark text-white" id="equipment_group" name="equipment_group" required>
                        </div>
                        <div class="mb-3">
                            <label for="equipment_name" class="form-label">Nome do Aparelho</label>
                            <input type="text" class="form-control bg-dark text-white" id="equipment_name" name="equipment_name" required>
                        </div>
                        <div id="equipmentModalMessage" class="alert d-none" role="alert"></div>
                    </div>
                    <div class="modal-footer border-secondary">
                        <button type="button" class="button btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="button-style">Salvar</button>
                    </div>
                </form>
            </div>
        </div>`;
        document.body.appendChild(modal);
    }
    return modal;
}

// Adicionar novo aparelho
function openAddModal() {
    const modal = ensureModal();
    const modalInstance = new bootstrap.Modal(modal);
    document.getElementById('equipmentModalLabel').textContent = 'Novo Aparelho';
    document.getElementById('equipment_group').value = '';
    document.getElementById('equipment_name').value = '';
    document.getElementById('equipmentModalMessage').classList.add('d-none');
    modalInstance.show();
    const form = document.getElementById('formEquipment');
    form.onsubmit = async (e) => {
        e.preventDefault();
        await createEquipment();
    };
}

// Editar aparelho
function openEditModal(group_name, equipment_name) {
    const modal = ensureModal();
    const modalInstance = new bootstrap.Modal(modal);
    document.getElementById('equipmentModalLabel').textContent = 'Editar Aparelho';
    document.getElementById('equipment_group').value = group_name;
    document.getElementById('equipment_name').value = equipment_name;
    document.getElementById('equipmentModalMessage').classList.add('d-none');
    modalInstance.show();
    const form = document.getElementById('formEquipment');
    form.onsubmit = async (e) => {
        e.preventDefault();
        await updateEquipment(group_name, equipment_name);
    };
}

// Criação
async function createEquipment() {
    const group_name = document.getElementById('equipment_group').value;
    const equipment_name = document.getElementById('equipment_name').value;
    const msg = document.getElementById('equipmentModalMessage');
    try {
        const response = await authApiClient.post('/api/data/equipment/new', { group_name, equipment_name });
        if (response.ok) {
            msg.className = 'alert alert-success';
            msg.textContent = 'Aparelho cadastrado com sucesso!';
            msg.classList.remove('d-none');
            fetchEquipments();
            setTimeout(() => bootstrap.Modal.getInstance(document.getElementById('equipmentModal')).hide(), 1000);
        } else {
            msg.className = 'alert alert-danger';
            msg.textContent = 'Erro ao cadastrar aparelho.';
            msg.classList.remove('d-none');
        }
    } catch (error) {
        msg.className = 'alert alert-danger';
        msg.textContent = 'Erro ao cadastrar aparelho.';
        msg.classList.remove('d-none');
    }
}

// Edição
async function updateEquipment(oldGroup, oldName) {
    const group_name = document.getElementById('equipment_group').value;
    const equipment_name = document.getElementById('equipment_name').value;
    const msg = document.getElementById('equipmentModalMessage');
    try {
        const response = await authApiClient.put(`/api/data/equipment/update/${oldGroup}/${oldName}`, { group_name, equipment_name });
        if (response.ok) {
            msg.className = 'alert alert-success';
            msg.textContent = 'Aparelho atualizado com sucesso!';
            msg.classList.remove('d-none');
            fetchEquipments();
            setTimeout(() => bootstrap.Modal.getInstance(document.getElementById('equipmentModal')).hide(), 1000);
        } else {
            msg.className = 'alert alert-danger';
            msg.textContent = 'Erro ao atualizar aparelho.';
            msg.classList.remove('d-none');
        }
    } catch (error) {
        msg.className = 'alert alert-danger';
        msg.textContent = 'Erro ao atualizar aparelho.';
        msg.classList.remove('d-none');
    }
}

// Exclusão
async function deleteEquipment(group_name, equipment_name) {
    if (!confirm('Deseja realmente excluir este aparelho?')) return;
    try {
        const response = await authApiClient.delete(`/api/data/equipment/delete/${group_name}/${equipment_name}`);
        if (response.ok) {
            fetchEquipments();
        } else {
            alert('Erro ao excluir aparelho.');
        }
    } catch (error) {
        alert('Erro ao excluir aparelho.');
    }
}

// Botão de adicionar
if (dashboardHeader) {
    const addBtn = dashboardHeader.querySelector('.button-style');
    if (addBtn) addBtn.addEventListener('click', openAddModal);
}

// Logout
const logoffBtn = document.getElementById('logoff');
if (logoffBtn) {
    logoffBtn.addEventListener('click', () => {
        tokenManager.logout();
    });
}

// Carrega os aparelhos ao abrir a página
fetchEquipments();