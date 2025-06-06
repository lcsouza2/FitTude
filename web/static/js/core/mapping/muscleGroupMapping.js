import { BASE_URL } from 'utils.js';

export async function getAllMuscleGroups() {
    try {
        const response = await fetch(BASE_URL + '/api/data/groups');
        if (response.status === 401) {
            throw new Error('Unauthorized access. Please log in.');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching muscle groups:', error);
    }
}

export class MuscleGroup {
    constructor(groupName) {
        this.groupName = groupName;
    }

    create(groupName) {
        fetch(BASE_URL + '/api/data/groups/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Credentials: 'include',
            },
            body: JSON.stringify({
                group_name: groupName,
            }),
        });
    }

    delete(groupName) {
        fetch(BASE_URL + '/api/data/groups/inactivate/' + groupName, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                Credentials: 'include',
            },
        });
    }

    update(groupName, newGroupName) {
        fetch(BASE_URL + '/api/data/groups/update/' + groupName, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Credentials: 'include',
            },
            body: JSON.stringify({
                group_name: newGroupName,
            }),
        });
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
