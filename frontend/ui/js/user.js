function goCreate() {
    window.location.href = "/ui/user_create.html";
}

function goHistory() {
    window.location.href = "/ui/history.html";
}

function goProfile() {
    window.location.href = "/ui/profile.html";
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/ui/login.html";
}
