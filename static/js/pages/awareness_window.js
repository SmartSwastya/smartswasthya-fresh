// awareness_window.js
window.onload = function () {
  const skip = localStorage.getItem("hideAwarenessWindow");
  const justSignedUp = sessionStorage.getItem("fromSignup");
  if (skip === "true" && !justSignedUp) {
    redirectWithToken();
  }
};

function skipAndRedirect() {
  const checkbox = document.getElementById("dontShowAgain");
  if (checkbox.checked) {
    localStorage.setItem("hideAwarenessWindow", "true");
  }
  sessionStorage.removeItem("fromSignup");
  redirectWithToken();
}

function redirectWithToken() {
  const token = localStorage.getItem("authToken");
  if (!token) {
    alert("❌ Missing token. Please login again.");
    return;
  }
  document.cookie = `Authorization=Bearer ${token}; path=/`;
  setTimeout(() => {
    window.location.href = "/smart";
  }, 200);
}