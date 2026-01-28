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

  const data = await res.json();

  if (!res.ok) {
    msg.innerText = "Failed to generate document";
    return;
  }

  msg.innerText = "Document created successfully";
  document.getElementById("downloads").style.display = "block";

  pdfLink.href = "/" + data.pdf;

  if (data.docx) {
    docxLink.href = "/" + data.docx;
    docxLink.style.display = "block";
  }
};
