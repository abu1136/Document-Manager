async function loadProfile() {
    const token = getToken();

    const res = await fetch("/profile/me", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (!res.ok) {
        document.getElementById("status").innerText = "Failed to load profile";
        return;
    }

    const data = await res.json();
    document.getElementById("username").innerText = data.username;
    document.getElementById("role").innerText = data.role;
}


async function changePassword(event) {
    event.preventDefault();

    const token = getToken();
    const currentPassword = document.getElementById("currentPassword").value;
    const newPassword = document.getElementById("newPassword").value;

    const res = await fetch("/profile/change-password", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword
        })
    });

    const status = document.getElementById("status");

    if (res.ok) {
        status.innerText = "Password updated successfully";
        status.style.color = "green";
        document.getElementById("currentPassword").value = "";
        document.getElementById("newPassword").value = "";
    } else {
        const err = await res.json();
        status.innerText = err.detail || "Failed to update password";
        status.style.color = "red";
    }
}
