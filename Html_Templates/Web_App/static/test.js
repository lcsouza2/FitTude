function sendNewTokenRequest() {
    fetch("http://localhost:8000/user/renew_token", 
        {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({"refresh_token": localStorage.getItem("refresh_token")}
        )
    }).then(response => response.json())
    .then(sessionStorage.setItem("session_token", response.session_token))
}


document.getElementById("aparelho").addEventListener("submit", (event) => {
    event.preventDefault();
    fetch(
        "http://localhost:8000/equipment/new", {
            headers: {
                "Content-type": "application/json",
                "Authorization": `Bearer ${sessionStorage.getItem("session_token")}`
            },
            method: "POST",
            body: JSON.stringify(
                {
                "nome_grupamento": document.getElementById("nome-grupamento").value,
                "nome_aparelho": document.getElementById("nome-aparelho").value
            })
        }
    ).then(response => response.json())
    .then(response => {
        if (response.detail.includes("Token expirado")) {
            sendNewTokenRequest()
        }
    }
)})

document.getElementById("login").addEventListener("submit", (event) => {
    event.preventDefault();
    fetch(
        "http://localhost:8000/user/login", {
            headers: {
                "Content-type": "application/json",
            },
            method: "POST",
            body: JSON.stringify(
                {
                "login_key": document.getElementById("username-email").value,
                "password": document.getElementById("senha-login").value,
                "keep_login": document.getElementById("keep-login").checked
            })
        }
    )
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem("session_token", data.session_token)

        if (data.refresh_token) {
            localStorage.setItem("refresh_token", data.refresh_token)
        }
    })
})

document.getElementById("registro").addEventListener("submit", (event) => {
    event.preventDefault();
    fetch(
        "http://localhost:8000/teste/register", {
            headers: {
                "Content-type": "application/json",
            },
            method: "POST",
            body: JSON.stringify(
                {
                "username": document.getElementById("username").value,
                "email": document.getElementById("email").value,
                "password": document.getElementById("senha-registro").value
            })
        }
    )
})
