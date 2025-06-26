import { authApiClient, tokenManager } from '../core/auth.js';
import { populateUsername } from '../visual/dashboardVisuals.js';

console.log("carregano")
const token = tokenManager.getSessionToken()? undefined : tokenManager.refreshSessionToken();
const user_fullname = window.sessionStorage.getItem('user_fullname');
if (user_fullname ) {
    populateUsername(user_fullname)
} 

const logoffButton = document.getElementById('logoff');
logoffButton.addEventListener('click', function() {
    tokenManager.logout();
});

document.getElementById('menuToggle').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    sidebar.classList.toggle('show');
    overlay.classList.toggle('show');
});

document.getElementById('sidebarOverlay').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    sidebar.classList.remove('show');
    overlay.classList.remove('show');
});

const sidebarItems = document.querySelectorAll('.sidebar-menu li');
sidebarItems.forEach(item => {
    item.addEventListener('click', function() {
        if (window.innerWidth <= 991.98) {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebarOverlay');
            
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        }
    });
});

window.addEventListener('resize', function() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    if (window.innerWidth > 991.98) {
        sidebar.classList.remove('show');
        overlay.classList.remove('show');
    }
});

