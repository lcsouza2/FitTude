const loginForm = document.getElementById("login-form");
const loginData = loginForm.querySelectorAll("input");

const registerForm = document.getElementById("register-form");
const registerData = registerForm.querySelectorAll("input");
const registerToCheck = document.querySelectorAll(".to-check-available");

registerToCheck.forEach(item => item.addEventListener("focusout", (event) => {
    let timeOut;
    clearTimeout(timeOut);

    timeOut = setTimeout( () => {
    const values = Array.from(registerToCheck).map(input => input.value.trim());

    if (values.every(value => value.length > 3)) { 

        
            event.preventDefault();
            fetch("/user/find_user", {
                method: "POST",
                headers: {"Content-type": "application/json"},
                body: JSON.stringify({"credentials": item.value})
            }).then(response => response.json())
            .then(data =>{
                if (data.status !== "available") {
                    alert(data.detail)
            }
        })
    }}, 500)
    }
))

registerForm.addEventListener("submit", (event) => {
    event.preventDefault();
    fetch("/user/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            "username": registerData[0].value,
            "email": registerData[1].value,
            "password": registerData[2].value
        })
    }).then(response => {if (response.ok) {alert("Verifique sua caixa de email")}})
})



loginForm.addEventListener("submit", (event) => {

    event.preventDefault();

    fetch("/user/login", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "login_key": loginData[0].value,
            "password": loginData[1].value,
            "keep_login": loginData[2].checked
        })
    }).then(response => {if (!response.ok) {alert(response.detail)} else {window.href = "/dashboard"}})
})