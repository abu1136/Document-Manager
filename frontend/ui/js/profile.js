async function changePassword(e) {
    e.preventDefault();

    const token = getToken();
    const msg = document.getElementById("msg");

    const current = document.getElementById("currentPassword").value;
    const newer = document.getElementById("newPassword").value;

    const res = await fetch("/profile/change-password", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            current_password: current,
            new_password: newer
        })
    });

    const data = await res.json();

    msg.innerText = res.ok ? data.message : data.detail;
}
