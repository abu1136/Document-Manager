async function loadHistory() {
    const token = getToken();
    const tbody = document.getElementById("historyBody");

    const params = new URLSearchParams();

    const docNo = document.getElementById("docNo").value;
    const createdBy = document.getElementById("createdBy").value;
    const dateFrom = document.getElementById("dateFrom").value;
    const dateTo = document.getElementById("dateTo").value;

    if (docNo) params.append("doc_no", docNo);
    if (createdBy) params.append("created_by", createdBy);
    if (dateFrom) params.append("date_from", dateFrom);
    if (dateTo) params.append("date_to", dateTo);

    const res = await fetch(`/documents/history?${params.toString()}`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    tbody.innerHTML = "";

    if (!res.ok) {
        tbody.innerHTML = "<tr><td colspan='5'>Failed to load data</td></tr>";
        return;
    }

    const docs = await res.json();

    if (docs.length === 0) {
        tbody.innerHTML = "<tr><td colspan='5'>No results found</td></tr>";
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

function clearFilters() {
    document.getElementById("docNo").value = "";
    document.getElementById("createdBy").value = "";
    document.getElementById("dateFrom").value = "";
    document.getElementById("dateTo").value = "";
    loadHistory();
}
