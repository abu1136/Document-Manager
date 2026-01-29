async function loadHistory() {
    const token = getToken();
    const tbody = document.getElementById("historyBody");

    const res = await fetch("/documents/history", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (!res.ok) {
        tbody.innerHTML = "<tr><td colspan='5'>Failed to load history</td></tr>";
        return;
    }

    const docs = await res.json();
    tbody.innerHTML = "";

    if (docs.length === 0) {
        tbody.innerHTML = "<tr><td colspan='5'>No documents found</td></tr>";
        return;
    }

    docs.forEach(d => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${d.document_number}</td>
            <td>${d.title}</td>
            <td>${d.created_by}</td>
            <td>${new Date(d.created_at).toLocaleString()}</td>
            <td>
                ${d.pdf_url ? `<a href="${d.pdf_url}" target="_blank">Download</a>` : "N/A"}
            </td>
        `;

        tbody.appendChild(tr);
    });
}
