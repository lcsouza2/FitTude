import { authApiClient } from '../auth.js';

export async function getAllMuscleGroups() {
    try {
        const response = authApiClient.get("/api/data/groups")
        console.log(response)
        return response.body
    } catch (error) {
        console.error('Error fetching muscle groups:', error);
    }
}

export class MuscleGroup {
    constructor(groupName) {
        this.groupName = groupName;
        
    }

    // Criar novo grupamento muscular
    static async create(groupName) {
        try {
            const response = await authApiClient.post("/api/data/groups/new", {
                "group_name": groupName,
            });
            return response.body;
        } catch (error) {
            console.error("Erro ao criar grupamento:", error);
            throw error;
        }
    }

    // Deletar um grupamento muscular
    static async delete(groupId) {
        try {
            const response = await authApiClient.delete(`/api/data/groups/inactivate/${groupId}`);
            return response.body;
        } catch (error) {
            console.error("Erro ao deletar grupamento:", error);
            throw error;
        }
    }

    // Atualizar nome do grupamento muscular
    static async update(groupId, newGroupName) {
        try {
            const response = await authApiClient.put(`/api/data/groups/update/${groupId}`, {
                "group_name": newGroupName
            });
            return response.body;
        } catch (error) {
            console.error("Erro ao atualizar grupamento:", error);
            throw error;
        }
    }

    // Buscar todos os grupamentos
    static async getAll() {
        try {
            const response = await authApiClient.get("/api/data/groups");
            return response.body;
        } catch (error) {
            console.error("Erro ao buscar grupamentos:", error);
            throw error;
        }
    }

    // Buscar um grupamento específico
    static async getById(groupId) {
        try {
            const response = await authApiClient.get(`/api/data/groups/${groupId}`);
            return response.body;
        } catch (error) {
            console.error("Erro ao buscar grupamento:", error);
            throw error;
        }
    }
}


export class MuscleGroupWidget extends MuscleGroup {
    constructor(muscleGroupId, muscleGroupName) {
        this.muscleGroupId = muscleGroupId;
        this.muscleGroupName = muscleGroupName;
    }

    render() {
        const widget = document.createElement('div');
        widget.classList.add('muscle-group-widget');
        widget.innerHTML = `
            <h3>${this.muscleGroupName}</h3>
            <button class="delete-btn">Delete</button>
        `;
        widget.querySelector('.delete-btn').addEventListener('click', () => {
            this.muscleGroup.delete(this.muscleGroupName);
        });
        widget.id = "muscle-group-" + this.muscleGroupId;
        return widget;

    }
}
