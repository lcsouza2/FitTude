import { authApiClient } from '../auth.js';

export async function getAllMuscleGroups() {
    try {
        const response = authApiClient.get("/api/data/groups")
        return response.body
    } catch (error) {
        console.error('Error fetching muscle groups:', error);
    }
}

export class MuscleGroup {
    constructor(groupName) {
        this.groupName = groupName;
    }

    create(groupName) {
        response = authApiClient.post("/api/data/groups", {"group_name":groupName})
        return response.body
    }

    delete(groupName) {
        authApiClient.delete(BASE_URL + '/api/data/groups/inactivate/' + groupName);
    }

    update(groupName, newGroupName) {
        authApiClient.put(BASE_URL + '/api/data/groups/update/' + groupName, {"group_name": newGroupName})
    };
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
