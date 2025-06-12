import { authApiClient, tokenManager } from '../core/auth.js';

tokenManager.getSessionToken()? undefined : tokenManager.refreshSessionToken();








const logoffButton = document.getElementById('logoff');
logoffButton.addEventListener('click', function() {
    tokenManager.logout();
});

