requireAuth();

async function loadUsers() {
    const token = getToken();
    const res = await fetch("/admin/users", {
        headers: { 
            "Authorization": "Bearer " + token
        }
    });

    if (!res.ok) {
        alert("Failed to load users");
        return;
    }

    const users = await res.json();
    const tbody = document.getElementById("userTableBody");
    tbody.innerHTML = "";

    users.forEach(u => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${u.id}</td>
            <td>${u.username}</td>
            <td>${u.role}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function createUser(e) {
    e.preventDefault();

    const token = getToken();
    const username = document.getElementById("newUsername").value;
    const password = document.getElementById("newPassword").value;
    const role = document.getElementById("newRole").value;
    const msg = document.getElementById("createUserMsg");

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    formData.append("role", role);

    const res = await fetch("/admin/create-user", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        },
        body: formData
    });

    const data = await res.json();
    msg.innerText = res.ok ? data.message : data.detail;

    if (res.ok) {
        document.getElementById("newUsername").value = "";
        document.getElementById("newPassword").value = "";
        loadUsers();
    }
}

async function resetUserPassword() {
    const token = getToken();
    const userId = document.getElementById("resetUserId").value;
    const newPassword = document.getElementById("resetPassword").value;
    const msg = document.getElementById("resetMsg");

    if (!userId || !newPassword) {
        msg.innerText = "Please enter both User ID and new password";
        return;
    }

    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("new_password", newPassword);

    const res = await fetch("/admin/reset-password", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        },
        body: formData
    });

    const data = await res.json();
    msg.innerText = res.ok ? data.message : data.detail;

    if (res.ok) {
        document.getElementById("resetUserId").value = "";
        document.getElementById("resetPassword").value = "";
    }
}
