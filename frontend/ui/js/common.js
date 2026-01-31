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

function goDashboard() {
    const token = getToken();
    if (!token) {
        window.location.href = "/ui/login.html";
        return;
    }
    
    // Decode token to check role
    const payload = JSON.parse(atob(token.split(".")[1]));
    if (payload.role === "admin") {
        window.location.href = "/ui/admin.html";
    } else {
        window.location.href = "/ui/user.html";
    }
}

function goAdmin() {
    window.location.href = "/ui/admin.html";
}
