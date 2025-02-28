
export function getRefreshToken() {
    const token = localStorage.getItem("refresh_token")

    if (!token) {
        alert("Sessão expirada, faça login novamente")
        window.location.href = "/user/login"
    } else {
        return token
    }
}

export function renewSessionToken() {
    fetch("/user/renew_token", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "refresh_token": getRefreshToken()
        })
    }).then(response => response.json())
    .then(data => {
        if (data.status == 401) {
            alert("Sessão expirada, faça login novamente")
            window.location.href = "/user/login"
        } else if (data.status == 400 ) {
            alert("Token inválido enviado, tente novamente")
        } else {   
            sessionStorage.setItem("session_token", data.token )
        }
        
    })
}

export function getSessionToken() {
    const token = sessionStorage.getItem("session_token")

    if (!token) {
        renewSessionToken()
    }
}