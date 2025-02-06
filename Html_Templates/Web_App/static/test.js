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
                "group_name": document.getElementById("nome-grupamento").value,
                "equipment_name": document.getElementById("nome-aparelho").value
            })
        }
    )
})

document.getElementById("login").addEventListener("submit", (event) => {
    event.preventDefault();
    fetch(
        "http://localhost:8000/main/login", {
            headers: {
                "Content-type": "application/json",
            },
            method: "POST",
            body: JSON.stringify(
                {
                "login_key": document.getElementById("username-email").value,
                "password": document.getElementById("senha-login").value,
                "keep_login": false
            })
        }
    )
})

document.getElementById("registro").addEventListener("submit", (event) => {
    event.preventDefault();
    fetch(
        "http://localhost:8000/main/register", {
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
