import { calcRemainingBodySpace } from "./utils.js";

export class Exercise {
    constructor(exerciseId, exerciseName, exerciseDesc, equipmentId, muscleId) {
        this.exerciseId = exerciseId;
        this.exerciseName = exerciseName;
        this.exerciseDesc = exerciseDesc;
        this.equipmentId = equipmentId;
        this.muscleId = muscleId;
    }
    requestCreation() {
        fetch("/data/exercise/new", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                "nome_exercicio": this.exerciseName,
                "id_aparelho": this.equipmentId,
                "descricao": this.exerciseDesc
            })
        });
    }
}
export class Muscle {
    constructor(muscleId, groupName, muscleName) {
        this.muscleId = muscleId;
        this.groupName = groupName;
        this.muscleName = muscleName;
    }

    requestCreation(event) {
        event.preventDefault();
        fetch("/data/muscle/new", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                "nome_grupamento": this.groupName,
                "nome_musculo": this.muscleName
            })
        });
    }

    mountView() {
        const view = document.createElement("div")
        view.id = `muscle-${this.muscleId}`
        view.className = "view-muscle"

        view.style.width = calcRemainingBodySpace() * 0.35 + "px"
        view.style.height = calcRemainingBodySpace() * 0.2 + "px"

        view.innerHTML = `
            <h1>${this.muscleName}</h1>
            <h2>${this.groupName}</h2>
        `

        document.getElementById("display-data").appendChild(view)
    }
}
export class Equipment {
    constructor(equipmentId, groupName, equipmentName) {
        this.equipmentId = equipmentId;
        this.groupName = groupName;
        this.equipmentName = equipmentName;
    }
    requestCreation() {
        fetch("/data/equipment/new", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                "nome_grupamento": this.groupName,
                "nome_aparelho": this.equipmentName
            })
        });
    }
}
