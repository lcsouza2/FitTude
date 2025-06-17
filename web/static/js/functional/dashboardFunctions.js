import { authApiClient, tokenManager } from '../core/auth.js';
import { populateUsername } from '../visual/dashboardVisuals.js';

const token = tokenManager.getSessionToken()? undefined : tokenManager.refreshSessionToken();
populateUsername("Joao")

const logoffButton = document.getElementById('logoff');
logoffButton.addEventListener('click', function() {
    tokenManager.logout();
});

