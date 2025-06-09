import {MuscleGroup, MuscleGroupWidget, getAllMuscleGroups} from '../mapping/muscleGroupMapping.js';

let currentMuscleGroups = await getAllMuscleGroups()

currentMuscleGroups.array.forEach(element => {
   const muscleGroupWidget = new MuscleGroupWidget(element.id, element.name);
   document.body.appendChild(muscleGroupWidget.render());
});