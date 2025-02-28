import {getRefreshToken, getSessionToken, renewSessionToken} from "./utils"

export class Exercise {
    exerciseId: number | null
    exerciseName: string
    exerciseDesc: string | null
    equipmentId: number | null
    muscleId: number

    constructor(
        exerciseId: number | null, 
        exerciseName: string,
        exerciseDesc: string | null,
        equipmentId: number | null,
        muscleId: number
    ) {
        this.exerciseId = exerciseId
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
        })
    }
}

export class Muscle {
    muscleId: number | null
    groupName: string
    muscleName: string

    constructor(
        muscleId: number | null,
        groupName: string,
        muscleName: string,
    ) {
        this.muscleId = muscleId
        this.groupName = groupName
        this.muscleName = muscleName
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
        })
    }
}

export class Equipment {
    equipmentId: number | null
    groupName: string
    equipmentName: string

    constructor(
        equipmentId: number | null,
        groupName: string,
        equipmentName: string,
    ) {
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
        })
    }
}