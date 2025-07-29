let countdown;

function startTimer() {
  let seconds = 60;
  const timer = document.getElementById("timer");
  const btn = document.getElementById("sendBtn");
  btn.disabled = true;
  countdown = setInterval(() => {
    seconds--;
    timer.textContent = `⏳ Resend in ${seconds}s`;
    if (seconds <= 0) {
      clearInterval(countdown);
      timer.textContent = "";
      btn.disabled = false;
      btn.innerText = "🔁 Resend OTP";
    }
  }, 1000);
}

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
    try {
      const data = JSON.parse(text);
      if (data.status === "sent") {
        alert("✅ OTP sent successfully!");
        document.getElementById("otpSection").classList.remove("hidden");
        document.getElementById("passwordSection").classList.remove("hidden");
        document.getElementById("submitSection").classList.remove("hidden");
        startTimer();
      } else {
        alert("❌ " + data.message);
      }
    } catch (parseErr) {
      console.error("❌ JSON Parse Error:", text);
      alert("❌ Server response error. Check console.");
    }
  } catch (error) {
    console.error("❌ Fetch Failed:", error);
    alert("❌ Could not send OTP due to server error.");
  }
}

async function verifyOTP() {
  const name = document.getElementById("name").value.trim();
  const mobile = document.getElementById("mobile").value.trim();
  const email = document.getElementById("email").value.trim();
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

  if (data.status === "verified") {  // Fix: status चेक
    alert("🎉 Signup Successful! Redirecting...");
    sessionStorage.setItem("fromSignup", "true");
    window.location.href = data.redirect || "/awareness";
    return;
  }

  alert("❌ " + (data.reason || "Something went wrong"));  // Fix: reason चेक
}

document.getElementById("signup-form").addEventListener("submit", (e) => {
  e.preventDefault();
  verifyOTP();
});

// Block invalid characters while typing
function isAlpha(e) {
  const char = String.fromCharCode(e.which);
  if (!/^[a-zA-Z\s]$/.test(char)) {
    return false;
  }
  return true;
}

// Remove invalid characters if pasted
function filterNameInput() {
  const input = document.getElementById("name");
  const error = document.getElementById("nameError");
  const value = input.value;

  const cleaned = value.replace(/[^a-zA-Z\s]/g, '');
  input.value = cleaned;

  if (value !== cleaned) {
    error.classList.remove("hidden");
  } else {
    error.classList.add("hidden");
  }
}

// Block any non-numeric key press
function isNumber(e) {
  const char = String.fromCharCode(e.which);
  return /^[0-9]$/.test(char);
}

// Clean pasted input and validate length
function validateMobile() {
  const input = document.getElementById("mobile");
  const error = document.getElementById("mobileError");

  input.value = input.value.replace(/[^0-9]/g, '');

  if (input.value.length !== 10) {
    error.classList.remove("hidden");
  } else {
    error.classList.add("hidden");
  }
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

  if (emailPattern.test(value)) {
    emailError.classList.add("hidden");
  } else {
    emailError.classList.remove("hidden");
  }
}

function togglePassword() {
  const passwordInput = document.getElementById("passwordInput");
  const icon = event.currentTarget;

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    icon.textContent = "🙈";
  } else {
    passwordInput.type = "password";
    icon.textContent = "👁️";
  }
}

document.getElementById("mobile").addEventListener("blur", async () => {
  const mobileInput = document.getElementById("mobile");
  const mobile = mobileInput.value.trim();
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

// Attach event listeners
document.getElementById("name").addEventListener("input", filterNameInput);
document.getElementById("name").addEventListener("keypress", isAlpha);
document.getElementById("mobile").addEventListener("input", validateMobile);
document.getElementById("mobile").addEventListener("keypress", isNumber);
document.getElementById("email").addEventListener("input", validateEmail);
document.querySelector('.absolute.right-3.top-9').addEventListener("click", togglePassword);
document.getElementById("sendBtn").addEventListener("click", sendOTP);