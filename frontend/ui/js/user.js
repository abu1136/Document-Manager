const token = localStorage.getItem("token");
if (!token) location.href = "/ui/login.html";

const headers = { "Authorization": "Bearer " + token };

function logout() {
  localStorage.removeItem("token");
  location.href = "/ui/login.html";
}

document.getElementById("docForm").onsubmit = async e => {
  e.preventDefault();
  msg.innerText = "Generating document...";

  const res = await fetch("/documents", {
    method: "POST",
    headers,
    body: new URLSearchParams({
      title: title.value,
      content: content.value
    })
  });

  let data;
  try {
    data = await res.json();
  } catch {
    msg.innerText = "Server error while generating document";
    return;
  }

  if (!res.ok) {
    msg.innerText = data.detail || "Document generation failed";
    return;
  }

  msg.innerText = "Document created successfully";
  downloads.style.display = "block";

  pdfLink.href = "/" + data.pdf;

  if (data.docx) {
    docxLink.href = "/" + data.docx;
    docxLink.style.display = "block";
  }
};
