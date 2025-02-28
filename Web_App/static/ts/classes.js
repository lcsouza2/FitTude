import { getSessionToken } from "./utils";
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
            headers: {
                "Authorization": `Bearer ${getSessionToken()}`,
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
    requestCreation() {
        fetch("/data/muscle/new", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${getSessionToken()}`,
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                "nome_grupamento": this.groupName,
                "nome_musculo": this.muscleName
            })
        });
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
            headers: {
                "Authorization": `Bearer ${getSessionToken()}`,
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                "nome_grupamento": this.groupName,
                "nome_aparelho": this.equipmentName
            })
        });
    }
}
