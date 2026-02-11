/* =====================================================
   SMART ATTENDANCE – COMMON UI UTILITIES
   File: static/js/common.js
===================================================== */

/* ---------------- TOAST NOTIFICATIONS ---------------- */
function showToast(message, type = "success", duration = 3000) {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerText = message;

  document.body.appendChild(toast);

  setTimeout(() => toast.classList.add("show"), 50);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

/* ---------------- LOADING SPINNER ---------------- */
function showLoader() {
  let loader = document.getElementById("globalLoader");
  if (!loader) {
    loader = document.createElement("div");
    loader.id = "globalLoader";
    loader.innerHTML = `<div class="spinner"></div>`;
    document.body.appendChild(loader);
  }
}

function hideLoader() {
  const loader = document.getElementById("globalLoader");
  if (loader) loader.remove();
}

/* ---------------- MODAL HELPER ---------------- */
function openModal(id) {
  document.getElementById(id).classList.add("show");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("show");
}

/* ---------------- API FETCH WRAPPER ---------------- */
async function apiFetch(url, options = {}) {
  try {
    showLoader();
    const res = await fetch(url, options);
    const data = await res.json();
    hideLoader();
    return data;
  } catch (err) {
    hideLoader();
    showToast("Network error", "error");
    throw err;
  }
}

/* ---------------- DATE FORMAT ---------------- */
function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleString();
}

/* ---------------- LOCAL STORAGE ---------------- */
const storage = {
  set(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  },
  get(key) {
    const val = localStorage.getItem(key);
    return val ? JSON.parse(val) : null;
  },
  remove(key) {
    localStorage.removeItem(key);
  }
};

/* ---------------- ANIMATION UTILS ---------------- */
function animateCounter(el, target, duration = 800) {
  let start = 0;
  const step = Math.ceil(target / (duration / 16));

  const interval = setInterval(() => {
    start += step;
    if (start >= target) {
      el.innerText = target;
      clearInterval(interval);
    } else {
      el.innerText = start;
    }
  }, 16);
}
