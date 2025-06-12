import {MuscleGroup, MuscleGroupWidget, getAllMuscleGroups} from '../../core/mapping/muscleGroupMapping.js';
import { tokenManager } from '../../core/auth.js';

tokenManager.getSessionToken()?null:tokenManager.refreshSessionToken()

let currentMuscleGroups = await getAllMuscleGroups()

console.log(currentMuscleGroups)

let muscleGroupArray = [];
let muscleGroupWidgetArray = [];

currentMuscleGroups.array.forEach(element => {
   muscleGroupArray.push(new MuscleGroup(element.group_name));
   muscleGroupWidgetArray.push(new MuscleGroupWidget(element.id, element.group_name))
   document.body.appendChild(muscleGroupWidget.render());
});