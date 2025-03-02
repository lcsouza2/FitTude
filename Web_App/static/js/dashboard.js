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

document.getElementById("display-muscles").addEventListener("click", () => {
    fetch("/data/muscle/get", {credentials: "same-origin"})
    .then(response => response.json())
    .then(data => {mountCreatingButton(); displayAllMuscles(data);      
    })
})


