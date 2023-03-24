const form = document.getElementById("login-form");

form.addEventListener("submit", function(event) {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorElement = document.getElementById("error-message");

    if (username !== "example_user" || password !== "example_password") {
        event.preventDefault();
        errorElement.innerHTML = "Invalid username or password";
    }
});