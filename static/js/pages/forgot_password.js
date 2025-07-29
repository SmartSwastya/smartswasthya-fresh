// forgot_password.js
async function sendOTP() {
  const mobile = document.getElementById("mobile").value.trim();
  if (!mobile || mobile.length !== 10) {
    return alert("❌ Please enter a valid 10-digit mobile number");
  }
  const response = await fetch(`/send-forgot-otp?mobile=${mobile}`);
  const data = await response.json();
  if (data.status === "sent") {
    alert("✅ OTP sent successfully!");
    document.getElementById("otpSection").classList.remove("hidden");
    document.getElementById("passwordSection").classList.remove("hidden");
    document.getElementById("submitSection").classList.remove("hidden");
    startOTPTimer(60, 'timer', 'sendBtn');
  } else {
    alert("❌ " + (data.message || "Failed to send OTP"));
  }
}

async function resetPassword() {
  const mobile = document.getElementById("mobile").value.trim();
  const otp = document.getElementById("otpInput").value.trim();
  const password = document.getElementById("passwordInput").value.trim();
  if (!mobile || !otp || !password) {
    return alert("❌ All fields are required!");
  }
  const response = await fetch(`/reset-password?mobile=${mobile}&otp=${otp}&password=${encodeURIComponent(password)}`);
  const data = await response.json();
  if (data.success) {
    alert("🎉 Password reset successful! Redirecting...");
    window.location.href = "/login";
  } else {
    alert("❌ " + (data.message || "Reset failed"));
  }
}