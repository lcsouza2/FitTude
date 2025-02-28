import { getSessionToken } from "./utils"; 
import { Exercise, Muscle, Equipment } from "./classes";

let currentTab = "Main"

function displayAllExercises() {
    const addExerciseBtn = document.createElement("button")
    addExerciseBtn.id = "add-exercise-button" 
    document.appendChild(addExerciseBtn)
}

document.getElementById("display-exercises").addEventListener("click", () => {
    displayAllExercises()
})