function getToken() {
    return localStorage.getItem("token");
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/ui/login.html";
}

function requireAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = "/ui/login.html";
    }
}

function goHistory() {
    window.location.href = "/ui/history.html";
}

function goProfile() {
    window.location.href = "/ui/profile.html";
}
