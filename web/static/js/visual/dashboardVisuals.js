export function populateUsername(username) {
    const elements = document.querySelectorAll('#username');
    elements.forEach(element => {
        element.textContent = element.textContent.replace("@username", username);
        element.textContent = element.textContent.replace("@U", username[0]);
        element.value = username;
    });
}

export function populateFirstStats(visuals) {
    document.getElementById('registeredWorkouts').textContent = visuals.registeredWorkouts;
    document.getElementById('RegisteredPlans').textContent = visuals.RegisteredPlans;
    document.getElementById('RegisteredExercises').textContent = visuals.RegisteredExercises;
    document.getElementById('TotalSets').textContent = visuals.TotalSets;
}   

export function populatePLans(plans) {
    const plansContainer = document.getElementsByClassName('training-plans')[0];

    plans.forEach(plan => {
        `
        <div class="plan-card">
            <div class="plan-title">${plan.name}</div>
                <div class="plan-details">
                <div><strong>Objetivo:</strong>${plan.objective}</div>
                <div><strong>Divisões:</strong></div>
            </div>
            <button class="button-style" style="width: 100%">Ver Ficha</button>
        </div>
        `
    })
    
}