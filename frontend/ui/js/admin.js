function goAdminHome() {
    window.location.href = "/ui/admin.html";
}

function goUsers() {
    window.location.href = "/ui/users.html";
}

function goLetterhead() {
    window.location.href = "/ui/letterhead.html";
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
