export function calcRemainingBodySpace() {
    return window.innerWidth - document.getElementById("options-sidebar").offsetWidth
}

export function redirectToLogin() {
    window.href = "/"
}