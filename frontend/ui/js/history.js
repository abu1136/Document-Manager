const token = localStorage.getItem("token");
if (!token) location.href = "/ui/login.html";

const headers = { Authorization: "Bearer " + token };

function logout() {
  localStorage.removeItem("token");
  location.href = "/ui/login.html";
}

async function load() {
  const q = document.getElementById("q").value;
  const res = await fetch(`/documents/history?q=${q}`, { headers });
  const data = await res.json();

  rows.innerHTML = "";
  data.forEach(d => {
    rows.innerHTML += `
      <tr>
        <td>${d.document_number}</td>
        <td>${d.title}</td>
        <td>${new Date(d.created_at).toLocaleString()}</td>
        <td><a href="/${d.pdf_path}" target="_blank">PDF</a></td>
        <td>${d.docx_path ? `<a href="/${d.docx_path}">DOCX</a>` : "-"}</td>
      </tr>`;
  });
}

load();
