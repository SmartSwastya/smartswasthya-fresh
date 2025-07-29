// smartuser_dashboard.js
let failedAccuracyCount = 0;

function dropPin() {
  const previewDiv = document.getElementById("mapPreview");
  previewDiv.classList.remove("hidden");
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const accuracy = position.coords.accuracy;
      document.getElementById("latitude").value = lat;
      document.getElementById("longitude").value = lng;
      document.getElementById("accuracy").value = accuracy;

      map = new google.maps.Map(previewDiv, { center: { lat, lng }, zoom: 15 });
      marker = new google.maps.Marker({ position: { lat, lng }, map, draggable: true, title: "Drag to adjust location" });
      google.maps.event.addListener(marker, 'dragend', e => {
        document.getElementById("latitude").value = e.latLng.lat();
        document.getElementById("longitude").value = e.latLng.lng();
      });

      if (accuracy > 50) {
        failedAccuracyCount++;
        if (failedAccuracyCount >= 2) {
          document.getElementById("fallback-address-options").classList.remove("hidden");
        }
      } else {
        failedAccuracyCount = 0;
        document.getElementById("fallback-address-options").classList.add("hidden");
      }
    }, () => alert("❌ Location access failed."), { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 });
  } else {
    alert("❌ Geolocation not supported.");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const flatFields = document.getElementById("flat-fields");
  const houseFields = document.getElementById("house-fields");
  document.querySelectorAll('input[name="fallback_option"]').forEach(radio => {
    radio.addEventListener("change", function () {
      flatFields.style.display = this.value === "flat" ? "block" : "none";
      houseFields.style.display = this.value === "house" ? "block" : "none";
    });
  });
});

function setupAgeCalculation() {
  const dobField = document.getElementById("updateDob");
  dobField.addEventListener("change", function () {
    const dob = new Date(this.value);
    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) age--;
    const blocks = document.querySelectorAll(".text-gray-600.block");
    blocks.forEach(el => {
      if (el.innerText.includes("Age:")) {
        const parts = el.innerText.split("|");
        if (parts.length >= 1) {
          parts[0] = `Age: ${age} yrs `;
          el.innerText = parts.join("|");
        }
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", setupAgeCalculation);

function openProfilePopup() {
  const modal = document.getElementById("profileModal");
  if (modal) modal.style.display = "flex";
  else console.error("Profile modal not found");
}

function setupImagePreview() {
  const input = document.getElementById("updateImage");
  const preview = document.getElementById("previewImage");
  input.addEventListener("change", function () {
    const reader = new FileReader();
    reader.onload = e => preview.src = e.target.result;
    if (this.files[0]) reader.readAsDataURL(this.files[0]);
  });
}

document.addEventListener("DOMContentLoaded", setupImagePreview);

function saveProfileChanges() {
  const form = document.getElementById("profileForm");
  const dob = document.getElementById("updateDob").value.trim();
  const userLocation = document.getElementById("userLocation").value.trim();
  if (!dob || !userLocation) {
    alert("⚠️ Date of Birth and Location are required!");
    return;
  }

  const formData = new FormData(form);
  formData.set("dob", dob);
  formData.set("location", userLocation);
  formData.set("doctor_name", document.getElementById("updateDoctor").value);
  formData.set("contact_number", document.getElementById("connectMobile").value);
  formData.set("recent_appointment", document.getElementById("lastVisit").value);
  formData.set("gender", document.getElementById("updateGender").value);
  formData.set("latitude", document.getElementById("latitude").value);
  formData.set("longitude", document.getElementById("longitude").value);

  const imageInput = document.getElementById("updateImage");
  if (imageInput && imageInput.files.length > 0) {
    formData.set("profile_image", imageInput.files[0]);
  }

  fetch("/profile/update-profile", {
    method: "POST",
    body: formData
  })
  .then(res => res.text())
  .then(() => {
    alert("✅ Profile updated successfully!");
    location.reload();
  })
  .catch(err => {
    console.error("Profile update error:", err);
    alert("❌ Something went wrong.");
  });
}

const sortable = new Sortable(document.getElementById('sortable'), {
  animation: 150,
  onStart(evt) { localStorage.removeItem('cardOrder'); },
  onEnd(evt) {
    const newOrder = Array.from(document.querySelectorAll('#sortable .card')).map(card => card.innerHTML);
    localStorage.setItem('cardOrder', JSON.stringify(newOrder));
  },
});

let isSortingEnabled = false;

document.getElementById('toggleSort').addEventListener('click', function() {
  isSortingEnabled = !isSortingEnabled;
  sortable.option('disabled', !isSortingEnabled);
  document.body.style.overflow = isSortingEnabled ? 'hidden' : 'auto';
  this.innerText = isSortingEnabled ? 'Switch to Scroll' : 'Switch to Sort';
});

window.onload = function() {
  const savedOrder = localStorage.getItem('cardOrder');
  if (savedOrder) {
    const order = JSON.parse(savedOrder);
    const cards = document.querySelectorAll('#sortable .card');
    if (order.length === cards.length) {
      order.forEach((cardHtml, index) => { cards[index].innerHTML = cardHtml; });
    }
  }
  document.getElementById('toggleSort').innerText = 'Switch to Sort';
  document.body.style.overflow = 'auto';
  sortable.option('disabled', true);
};

let otpTimerInterval;

function sendEmailOTP() {
  const emailValue = document.getElementById('updateEmail').value.trim();
  fetch('/profile/send-otp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: emailValue })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.status === 'success' ? 'OTP sent successfully.' : data.message);
    if (data.status === 'success') {
      document.getElementById('sendOTPButton').style.display = 'none';
      document.getElementById('otpSection').style.display = 'flex';
      startOTPTimer(60, 'otpTimer', 'sendOTPButton', () => {
        document.getElementById('sendOTPButton').style.display = 'inline-block';
      });
    }
  })
  .catch(() => alert('Error sending OTP.'));
}

function verifyEmailOTP() {
  const otp = document.getElementById('otpInput').value;
  fetch('/profile/verify-otp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ otp })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message);
    if (data.status === 'success') {
      clearInterval(otpTimerInterval);
      document.getElementById('otpSection').style.display = 'none';
      document.getElementById('emailBadge').textContent = '✅';
    }
  })
  .catch(() => alert('Error verifying OTP.'));
}

document.addEventListener('DOMContentLoaded', function() {
  const emailInput = document.getElementById('updateEmail');
  const sendBtn = document.getElementById('sendOTPButton');
  if (!emailInput.value) {
    emailInput.readOnly = false;
    emailInput.addEventListener('input', function() {
      sendBtn.style.display = emailInput.value.includes('@') ? 'inline-block' : 'none';
    });
  }
});