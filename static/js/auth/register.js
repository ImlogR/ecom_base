const form = document.getElementById("registration-form");

form.addEventListener("submit", function(event) {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const errorElement = document.getElementById("error-message");

    if (password !== confirmPassword) {
        event.preventDefault();
        errorElement.innerHTML = "Passwords do not match";
    }
});