function togglePassword(inputId) {
    var input = document.getElementById(inputId);
    var icon = input.nextElementSibling.querySelector('i');
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = "password";
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

function validatePassword() {
    var oldPassword = document.getElementById("id_old_password").value;
    var newPassword1 = document.getElementById("id_new_password1").value;
    var newPassword2 = document.getElementById("id_new_password2").value;
    
    if (!oldPassword || !newPassword1 || !newPassword2) {
        alert("Iltimos, hamma maydonlarni to'ldiring.");
        return false;
    }

    if (newPassword1 !== newPassword2) {
        alert("Yangi parollar mos kelmadi. Iltimos, tekshirib qaytadan kiriting.");
        return false;
    }
    
    return true;
}