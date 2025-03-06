import { calcRemainingBodySpace } from "./utils.js"
import { Exercise, Muscle, Equipment } from "./classes.js"

function mountCreatingButton(type) {

    let currentButton = document.getElementById(`add-${type}-button`)

    if (currentButton) {
        null
    } else {
        const button = document.createElement("button");
        button.id = `add-${type}-button`;

        button.style.width = calcRemainingBodySpace() * 0.5 + "px";

        button.innerText = `Criar novo`

        document.body.appendChild(button);

        button.style.left = ((calcRemainingBodySpace() * 0.5) - (button.offsetWidth / 2) + "px")
    }
}

function displayAllEquipments(data) {
    let musclesArray = []
    let shownMusclesArray = []


    document.querySelectorAll('[id^="muscle-"]').forEach(item => {
        shownMusclesArray.push(item.id.split("-")[1])
    } )

    data.forEach(instance => {
        let equipmentArray = []
        let shownEquipmentsArray = []


        document.querySelectorAll('[id^="equipment-"]').forEach(item => {
            shownEquipmentsArray.push(item.id.split("-")[1])
        } )

        if (!shownEquipmentsArray.includes(String(instance.id_aparelho))) {
            equipmentArray.push(new Equipment(
                instance.id_aparelho, instance.nome_grupamento, instance.nome_aparelho
            ).mountView())
        }
    })

}

function displayAllMuscles(data) {
    let musclesArray = []
    let shownMusclesArray = []


    document.querySelectorAll('[id^="muscle-"]').forEach(item => {
        shownMusclesArray.push(item.id.split("-")[1])
    } )

    data.forEach(instance => {
        console.log(instance.id_musculo)

        if (!shownMusclesArray.includes(String(instance.id_musculo))) {
            musclesArray.push(new Muscle(
                instance.id_musculo, instance.nome_grupamento, instance.nome_musculo
            ).mountView())
        }
    })
}

document.getElementById("display-equipments").addEventListener("click", () => {
    fetch("/data/equipment/get", {credentials: "same-origin"})
    .then(response => response.json())
    .then(data => {mountCreatingButton(); displayAllEquipments(data);      
    })
})


fetch("/data/workout/division/add_exercise", {
    method: "POST",
    credentials: "same-origin",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify([
        {
            "divisao": "B",
            "id_ficha_treino": 1,
            "id_exercicio": 1,
            "ordem_execucao": 1,
            "series": 4,
            "repeticoes": "até a falha",
            "tecnica_avancada": "drop set",
            "descanso": 1800
        },
        {
            "divisao": "B",
            "id_ficha_treino": 1,
            "id_exercicio": 1,
            "ordem_execucao": 2,
            "series": 4,
            "repeticoes": "até a falha",
            "tecnica_avancada": "drop set",
            "descanso": 1800
        },
    ])
})