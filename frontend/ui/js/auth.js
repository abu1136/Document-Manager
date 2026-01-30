document.getElementById("loginForm").onsubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: username.value,
            password: password.value
        })
    });

    const data = await res.json();

    if (!res.ok) {
        document.getElementById("error").innerText = data.detail;
        return;
    }

    localStorage.setItem("token", data.token);

    if (data.role === "admin") {
        window.location = "/ui/admin.html";
    } else {
        window.location = "/ui/user.html";
    }
};
