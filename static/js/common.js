// common.js
// Tailwind Config
tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: '#d8e850',
        secondary: '#99e3f9',
      }
    }
  }
};

// Suppress Tailwind CDN warnings
console.warn = new Proxy(console.warn, {
  apply(target, thisArg, args) {
    if (args[0]?.includes?.('cdn.tailwindcss.com should not be used')) return;
    if (args[0]?.includes?.('@tailwindcss/line-clamp')) return;
    return target.apply(thisArg, args);
  }
});

// Menu Toggle
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('menu-toggle');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;
  btn.addEventListener('click', () => {
    const isOpen = !menu.classList.toggle('hidden');
    btn.setAttribute('aria-expanded', String(isOpen));
  });
});

// Common Modal Close
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
  } else {
    console.error(`Modal with ID ${modalId} not found`);
  }
}