const token = localStorage.getItem("token");
if (!token) location.href = "/ui/login.html";

const headers = { Authorization: "Bearer " + token };

function logout() {
  localStorage.removeItem("token");
  location.href = "/ui/login.html";
}

document.getElementById("pwdForm").onsubmit = async e => {
  e.preventDefault();

  const res = await fetch("/profile/change-password", {
    method: "POST",
    headers,
    body: new URLSearchParams({
      old_password: oldp.value,
      new_password: newp.value
    })
  });

  const data = await res.json();
  msg.innerText = res.ok ? "Password updated" : data.detail;
};
