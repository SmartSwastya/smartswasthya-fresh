// Location Permission and Geolocation
if (localStorage.getItem('location_permission') === 'granted') {
  navigator.geolocation.getCurrentPosition(success, error, {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  });
} else {
  if (confirm("We need access to your location. Grant permission?")) {
    localStorage.setItem('location_permission', 'granted');
    window.location.reload();
  }
}

function success(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  console.log("Location fetched successfully:", { latitude, longitude });
  fetch('/track-location', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ latitude, longitude })
  })
  .then(response => {
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    return response.json();
  })
  .then(data => console.log('Data successfully sent to backend:', data))
  .catch(err => console.error('Error while sending location data to backend:', err));
}

function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`);
  alert("Failed to retrieve location. Please ensure location services are enabled and try again.");
  getLocationUsingGoogleAPI();
}

function getLocationUsingGoogleAPI() {
  const apiKey = "{{ google_maps_api_key }}";
  fetch(`https://www.googleapis.com/geolocation/v1/geolocate?key=${apiKey}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ "homeMobileCountryCode": 310, "homeMobileNetworkCode": 260 })
  })
  .then(response => response.json())
  .then(data => {
    const latitude = data.location.lat;
    const longitude = data.location.lng;
    console.log('Google Maps Geolocation API Response:', { latitude, longitude });
    fetch('/track-location', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ latitude, longitude })
    })
    .then(response => response.json())
    .then(data => console.log('Data successfully sent to backend:', data))
    .catch(err => console.error('Error while sending location data to backend:', err));
  })
  .catch(err => console.error('Error in Google Maps Geolocation API:', err));
}

// Desktop Slider
let currentIndexDesktop = 0;
const totalSlides = document.querySelectorAll('.desktop-slider .slider-item').length;
const sliderElement = document.querySelector('.desktop-slider .slider');

function changeDesktopSlide() {
  currentIndexDesktop = (currentIndexDesktop + 1) % totalSlides;
  sliderElement.style.transform = `translateX(-${currentIndexDesktop * 100}%)`;
}

setInterval(changeDesktopSlide, 4000);

// Mobile Slider
let currentIndexMobile = 0;
const mobileSlides = document.querySelectorAll('.mobile-slider .slider-item');
const totalMobileSlides = mobileSlides.length;

function changeMobileSlide() {
  currentIndexMobile = (currentIndexMobile + 1) % totalMobileSlides;
  const newTransformValue = -100 * currentIndexMobile + '%';
  document.querySelector('.mobile-slider .slider').style.transition = 'transform 1s ease-in-out';
  document.querySelector('.mobile-slider .slider').style.transform = `translateX(${newTransformValue})`;
}

setInterval(changeMobileSlide, 4000);

// Hamburger toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (toggleBtn && mobileMenu) {
    toggleBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }
});

// Search Functionality
document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.querySelector('.overlay-elements input[type="text"]');
  const resultBox = document.createElement('div');
  resultBox.className = 'absolute z-50 mt-2 bg-white text-gray-800 rounded-md shadow-lg w-full max-w-xl mx-auto';
  resultBox.style.display = 'none';
  searchInput.parentElement.appendChild(resultBox);

  let timeoutId;

  searchInput.addEventListener('input', function () {
    clearTimeout(timeoutId);
    const query = this.value.trim();
    if (query.length < 3) {
      resultBox.style.display = 'none';
      resultBox.innerHTML = '';
      return;
    }

    timeoutId = setTimeout(() => {
      fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          const results = data.results || [];
          if (results.length === 0) {
            resultBox.innerHTML = '<div class="px-4 py-2 text-sm text-gray-500">No results found</div>';
          } else {
            resultBox.innerHTML = results.map(item => `
              <div class="px-4 py-2 border-b hover:bg-blue-100 cursor-pointer">
                <strong>${item.title}</strong><br>
                ${item.location ? `<small>${item.location}</small>` : item.desc || ''}
              </div>
            `).join('');
          }
          resultBox.style.display = 'block';
        })
        .catch(err => console.error('Search error:', err));
    }, 300);
  });

  document.addEventListener('click', function (e) {
    if (!searchInput.contains(e.target)) {
      resultBox.style.display = 'none';
    }
  });
});