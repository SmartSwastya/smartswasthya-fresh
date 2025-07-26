// login.js
function isDigitOnly(e) {
  const ch = String.fromCharCode(e.which);
  return /^[0-9]$/.test(ch);
}

function filterToDigitsOnly(e) {
  const el = e.target;
  el.value = el.value.replace(/\D/g, '');
  document.getElementById('mobileErrorMsg').classList.toggle('hidden', el.value.length === 10);
}

function handlePaste(e) {
  const clip = (e.clipboardData || window.clipboardData).getData('text');
  if (!/^\d+$/.test(clip)) e.preventDefault();
}

function togglePassword() {
  const pw = document.getElementById('password');
  const eye = document.getElementById('eyeIcon');
  if (pw.type === 'password') {
    pw.type = 'text';
    eye.innerHTML = `
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M13.875 18.825A10.05 10.05 0 0112 19
           c-4.478 0-8.269-2.943-9.543-7
           a9.955 9.955 0 012.42-3.568
           M6.21 6.21A9.953 9.953 0 0112 5
           c4.478 0 8.269 2.943 9.543 7
           a9.96 9.96 0 01-4.196 5.255
           M3 3l18 18"/>`;
  } else {
    pw.type = 'password';
    eye.innerHTML = `
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M2.458 12C3.732 7.943 7.523 5 12 5
           c4.477 0 8.268 2.943 9.542 7
           -1.274 4.057-5.065 7-9.542 7
           -4.477 0-8.268-2.943-9.542-7z"/>`;
  }
}

const form = document.getElementById('loginForm');
const identity = document.getElementById('identity');
const password = document.getElementById('password');
const errorMsg = document.getElementById('errorMsg');
const roleSelector = document.getElementById('roleSelector');
const roleInputs = roleSelector ? roleSelector.querySelectorAll('input[type=radio]') : [];
let isLegacy = false;

identity.addEventListener('blur', async () => {
  const mobile = identity.value.trim();
  if (!mobile || mobile.length !== 10) return;
  try {
    const res = await fetch('/check-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identity: mobile })
    });
    const data = await res.json();
    if (data.status === 'create') {
      password.placeholder = '🔐 Create your new password';
      isLegacy = true;
    } else if (data.status === 'existing') {
      password.placeholder = '🔑 Enter your password';
      isLegacy = false;
    } else {
      errorMsg.textContent = '⚠️ User not found. Please sign up.';
      errorMsg.classList.remove('hidden');
      return;
    }
    errorMsg.classList.add('hidden');
    if (data.roles && Array.isArray(data.roles) && roleSelector) {
      roleSelector.classList.remove('hidden');
      roleInputs.forEach(input => {
        const show = data.roles.includes(input.value);
        input.parentElement.style.display = show ? 'block' : 'none';
        if (show) input.checked = true;
      });
    }
  } catch (err) {
    console.error('Check-user failed:', err);
    errorMsg.textContent = '⚠️ Server error.';
    errorMsg.classList.remove('hidden');
  }
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const mobile = identity.value.trim();
  const pass = password.value.trim();
  const role = document.querySelector('input[name="role"]:checked')?.value || 'smartuser';
  const endpoint = isLegacy ? '/set-password' : '/login';
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identity: mobile, password: pass, role })
    });
    const result = await res.json();
    if (result.status === 'success') {
      if (result.token) {
        localStorage.setItem("authToken", result.token);
        document.cookie = `Authorization=Bearer ${result.token}; path=/`;
      }
      if (result.redirect === "/awareness") {
        sessionStorage.setItem("fromSignup", "true");
      }
      window.location.href = result.redirect || "/smart_user";
    } else {
      errorMsg.textContent = result.message || "❌ Login failed.";
      errorMsg.classList.remove("hidden");
    }
  } catch (err) {
    console.error('Login error:', err);
    errorMsg.textContent = '⚠️ Internal server error.';
    errorMsg.classList.remove('hidden');
  }
});