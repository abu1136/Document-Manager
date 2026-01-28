async function checkSetupStatus() {
  const res = await fetch("/auth/setup/status");
  const data = await res.json();

  if (!data.setup_required) {
    location.href = "/ui/login.html";
  }
}

function getToken() {
  return localStorage.getItem("token");
}

function authHeader() {
  return {
    "Authorization": "Bearer " + getToken()
  };
}
