document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch("/auth/login", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Login failed");
    return;
  }

  localStorage.setItem("token", data.access_token);

  if (data.role === "admin") {
    window.location.href = "/ui/admin.html";
  } else {
    window.location.href = "/ui/user.html";
  }
});
