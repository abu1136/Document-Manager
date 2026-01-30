// Ensure user is authenticated
requireAuth();

// ===============================
// LOAD USERS
// ===============================
async function loadUsers() {
    const token = getToken();
    const tbody = document.getElementById("userTableBody");

    const res = await fetch("/admin/users", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    tbody.innerHTML = "";

    if (!res.ok) {
        tbody.innerHTML = "<tr><td colspan='3'>Failed to load users</td></tr>";
        return;
    }

    const users = await res.json();

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


// ===============================
// CREATE USER
// ===============================
async function createUser(e) {
    e.preventDefault();

    const token = getToken();
    const msg = document.getElementById("createUserMsg");

    const username = document.getElementById("newUsername").value;
    const password = document.getElementById("newPassword").value;
    const role = document.getElementById("newRole").value;

    const res = await fetch("/admin/create-user", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            username,
            password,
            role
        })
    });

    const data = await res.json();
    msg.innerText = res.ok ? data.message : data.detail;

    if (res.ok) {
        loadUsers();
    }
}


// ===============================
// RESET USER PASSWORD
// ===============================
async function resetUserPassword() {
    const token = getToken();
    const msg = document.getElementById("resetMsg");

    const userId = document.getElementById("resetUserId").value;
    const newPassword = document.getElementById("resetPassword").value;

    const res = await fetch("/admin/reset-password", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            user_id: userId,
            new_password: newPassword
        })
    });

    const data = await res.json();
    msg.innerText = res.ok ? data.message : data.detail;
}


// ===============================
// UPLOAD LETTERHEAD
// ===============================
async function uploadLetterhead() {
    const token = getToken();
    const fileInput = document.getElementById("letterheadFile");
    const msg = document.getElementById("letterheadMsg");

    if (fileInput.files.length === 0) {
        msg.innerText = "Please select a file";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const res = await fetch("/admin/letterhead", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        },
        body: formData
    });

    const data = await res.json();
    msg.innerText = res.ok ? data.message : data.detail;
}


// ===============================
// NAVIGATION
// ===============================
function goHistory() {
    window.location.href = "/ui/history.html";
}

function goProfile() {
    window.location.href = "/ui/profile.html";
}


// ===============================
// INIT
// ===============================
loadUsers();
