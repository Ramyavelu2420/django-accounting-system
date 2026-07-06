// Auth UI logic

document.addEventListener("DOMContentLoaded", function () {
    // Password Confirmation Verification UI
    const passwordInput = document.getElementById("id_password");
    const confirmPasswordInput = document.getElementById("id_confirm_password");
    
    if (passwordInput && confirmPasswordInput) {
        confirmPasswordInput.addEventListener("input", function () {
            if (passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.setCustomValidity("Passwords do not match");
                confirmPasswordInput.classList.add("is-invalid");
            } else {
                confirmPasswordInput.setCustomValidity("");
                confirmPasswordInput.classList.remove("is-invalid");
                confirmPasswordInput.classList.add("is-valid");
            }
        });
    }
});
