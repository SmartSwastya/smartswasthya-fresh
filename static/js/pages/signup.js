// signup.js
async function sendOTP() {
  const mobile = document.getElementById("mobile").value.trim();
  const name = document.getElementById("name").value.trim();
  const gender = document.getElementById("gender").value;
  if (!mobile || mobile.length !== 10) {
    alert("Please Enter Valid 10-digit Mobile Number ");
    return;
  }

  try {
    const response = await fetch(`/otp?mobile=${mobile}&name=${encodeURIComponent(name)}&gender=${gender}`);
    const text = await response.text();
    const data = JSON.parse(text);
    if (data.status === "sent") {
      alert("✅ OTP sent successfully!");
      document.getElementById("otpSection").classList.remove("hidden");
      document.getElementById("passwordSection").classList.remove("hidden");
      document.getElementById("submitSection").classList.remove("hidden");
      startOTPTimer(60, 'timer', 'sendBtn');
    } else {
      alert("❌ " + data.message);
    }
  } catch (error) {
    console.error("❌ Fetch Failed:", error);
    alert("❌ Could not send OTP due to server error.");
  }
}

async function verifyOTP() {
  const name = document.getElementById("name").value.trim();
  const mobile = document.getElementById("mobile").value.trim();
  const emailField = document.getElementById("email");
  const email = emailField ? emailField.value.trim() : "";
  const password = document.getElementById("passwordInput").value.trim();
  const otp = document.getElementById("otpInput").value.trim();
  const gender = document.getElementById("gender").value;

  if (!otp || otp.length !== 6 || !password) {
    return alert("❌ Please enter OTP and Password.");
  }

  const res = await fetch('/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, mobile, email, otp, password, gender })
  });

  const data = await res.json();
  console.log("✅ Response from /verify:", data);

  if (data.success) {
    alert("🎉 Signup Successful! Redirecting...");
    sessionStorage.setItem("fromSignup", "true");
    window.location.href = data.redirect || "/awareness";
  } else {
    alert("❌ " + (data.message || "Something went wrong"));
  }
}

function isAlpha(e) {
  const char = String.fromCharCode(e.which);
  return /^[a-zA-Z\s]$/.test(char);
}

function filterNameInput() {
  const input = document.getElementById("name");
  const error = document.getElementById("nameError");
  const value = input.value;
  const cleaned = value.replace(/[^a-zA-Z\s]/g, '');
  input.value = cleaned;
  error.classList.toggle("hidden", value === cleaned);
}

function isNumber(e) {
  const char = String.fromCharCode(e.which);
  return /^[0-9]$/.test(char);
}

function validateMobile() {
  const input = document.getElementById("mobile");
  const error = document.getElementById("mobileError");
  input.value = input.value.replace(/[^0-9]/g, '');
  error.classList.toggle("hidden", input.value.length === 10);
}

function validateEmail() {
  const emailInput = document.getElementById("email");
  const emailError = document.getElementById("emailError");
  const value = emailInput.value.trim();
  if (value === "") {
    emailError.classList.add("hidden");
    return;
  }
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  emailError.classList.toggle("hidden", emailPattern.test(value));
}

function togglePassword() {
  const passwordInput = document.getElementById("passwordInput");
  const icon = event.currentTarget;
  passwordInput.type = passwordInput.type === "password" ? "text" : "password";
  icon.textContent = passwordInput.type === "text" ? "🙈" : "👁️";
}

document.getElementById("mobile").addEventListener("blur", async () => {
  const mobile = document.getElementById("mobile").value.trim();
  const sendBtn = document.getElementById("sendBtn");
  if (mobile.length !== 10) return;
  try {
    const res = await fetch(`/check-mobile-exists?mobile=${mobile}`);
    const data = await res.json();
    if (data.exists) {
      sendBtn.disabled = true;
      alert("❌ This mobile number is already registered. Please login.");
    } else {
      sendBtn.disabled = false;
    }
  } catch (err) {
    console.error("Error checking mobile existence:", err);
    alert("⚠️ Could not validate mobile number. Please try again.");
  }
});