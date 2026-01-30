const token = localStorage.getItem("token");
if (!token) window.location = "/ui/login.html";

async function loadUsers() {
    const res = await fetch("/admin/users", {
        headers: { Authorization: token }
    });

    const users = await res.json();
    const list = document.getElementById("users");
    list.innerHTML = "";

    users.forEach(u => {
        const li = document.createElement("li");
        li.innerText = `${u.username} (${u.role})`;
        list.appendChild(li);
    });
}

document.getElementById("createUserForm").onsubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("/admin/create-user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: token
        },
        body: JSON.stringify({
            username: newUsername.value,
            password: newPassword.value,
            role: role.value
        })
    });

    const data = await res.json();
    alert(data.message || data.detail);
    loadUsers();
};

document.getElementById("logout").onclick = () => {
    localStorage.clear();
    window.location = "/ui/login.html";
};

loadUsers();
