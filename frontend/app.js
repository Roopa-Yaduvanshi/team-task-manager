/**
 * Team Task Manager — shared frontend logic
 * Uses fetch API and stores JWT in localStorage.
 */

// Change this to your deployed API URL (Railway) in production
https://team-task-manager-production-0245.up.railway.app  
// ---------- Token & user helpers ----------

function getToken() {
  return localStorage.getItem("token");
}

function getUser() {
  const raw = localStorage.getItem("user");
  return raw ? JSON.parse(raw) : null;
}

function saveAuth(token, user) {
  localStorage.setItem("token", token);
  localStorage.setItem("user", JSON.stringify(user));
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = "login.html";
}

function isLoggedIn() {
  return !!getToken();
}

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "login.html";
    return false;
  }
  return true;
}

function isAdmin() {
  const user = getUser();
  return user && user.role === "admin";
}

// ---------- API calls ----------

async function apiRequest(endpoint, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });
  } catch (err) {
    throw new Error(
      "Cannot reach API at " +
        API_BASE_URL +
        ". Start backend (uvicorn) and open frontend at http://127.0.0.1:5500 (not 0.0.0.0)."
    );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    let message = data.detail || data.message || "Something went wrong";
    if (Array.isArray(message)) {
      message = message.map((e) => e.msg || JSON.stringify(e)).join(", ");
    }
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }

  return data;
}

// ---------- Navbar setup (call on protected pages) ----------

function setupNavbar() {
  const user = getUser();
  const userNameEl = document.getElementById("navUserName");
  const roleBadge = document.getElementById("navUserRole");
  const adminLinks = document.querySelectorAll(".admin-only");

  if (userNameEl && user) {
    userNameEl.textContent = user.name;
  }
  if (roleBadge && user) {
    roleBadge.textContent = user.role;
    roleBadge.className =
      user.role === "admin" ? "badge bg-danger" : "badge bg-secondary";
  }

  adminLinks.forEach((el) => {
    el.style.display = isAdmin() ? "" : "none";
  });

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
  }
}

// ---------- Status badge helper ----------

function statusBadgeClass(status) {
  if (status === "Completed") return "badge-completed";
  if (status === "In Progress") return "badge-progress";
  return "badge-pending";
}

function formatDate(dateStr) {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString();
}

function showAlert(containerId, message, type = "danger") {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `;
}
