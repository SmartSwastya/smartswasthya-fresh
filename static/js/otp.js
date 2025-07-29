// otp.js
function startOTPTimer(seconds, timerId, buttonId, callback) {
  let remaining = seconds;
  const timerEl = document.getElementById(timerId);
  const btn = document.getElementById(buttonId);
  btn.disabled = true;
  timerEl.textContent = `⏳ Resend in ${remaining}s`;

  const interval = setInterval(() => {
    remaining--;
    timerEl.textContent = `⏳ Resend in ${remaining}s`;
    if (remaining <= 0) {
      clearInterval(interval);
      timerEl.textContent = '';
      btn.disabled = false;
      btn.innerText = '🔁 Resend OTP';
      if (callback) callback();
    }
  }, 1000);
  return interval;
}