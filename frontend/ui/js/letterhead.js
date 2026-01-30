async function uploadLetterhead() {
    const token = getToken();
    const fileInput = document.getElementById("letterheadFile");
    const msg = document.getElementById("letterheadMsg");

    if (fileInput.files.length === 0) {
        msg.innerText = "Please select a PDF file";
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
