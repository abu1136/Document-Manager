const token = localStorage.getItem("token");
if (!token) location.href = "/ui/login.html";

const headers = { "Authorization": "Bearer " + token };

// Load users
async function loadUsers() {
  const res = await fetch("/admin/users", { headers });
  if (!res.ok) {
    userMsg.innerText = "Failed to load users";
    return;
  }

  const users = await res.json();
  const ul = document.getElementById("userList");
  ul.innerHTML = "";

  users.forEach(u => {
    const li = document.createElement("li");
    li.textContent = `${u.username} (${u.role})`;
    ul.appendChild(li);
  });
}

loadUsers();

// Create user
document.getElementById("userForm").onsubmit = async e => {
  e.preventDefault();

  const res = await fetch("/admin/users", {
    method: "POST",
    headers: headers,
    body: new URLSearchParams({
      username: u.value,
      password: p.value,
      role: r.value
    })
  });

  userMsg.innerText = res.ok ? "User created" : "Error creating user";
  loadUsers();
};

// Upload letterhead
document.getElementById("lhForm").onsubmit = async e => {
  e.preventDefault();

  const fd = new FormData();
  fd.append("file", lhFile.files[0]);

  const res = await fetch("/admin/letterhead", {
    method: "POST",
    headers: headers,
    body: fd
  });

  lhMsg.innerText = res.ok ? "Letterhead uploaded" : "Upload failed";
};
