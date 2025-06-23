import { authApiClient, tokenManager } from '../core/auth.js';
import { populateUsername } from '../visual/dashboardVisuals.js';

const token = tokenManager.getSessionToken()? undefined : tokenManager.refreshSessionToken();
const user_fullname = window.sessionStorage.getItem('user_fullname') || 'Usuário';
populateUsername(user_fullname)
console.log("carregano")

const logoffButton = document.getElementById('logoff');
logoffButton.addEventListener('click', function() {
    tokenManager.logout();
});

