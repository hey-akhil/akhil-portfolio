/**
 * AutomateX - Client Application Script
 * Handles real-time search, category filtering, live API test ping,
 * contact submissions, and ambient particle network.
 */

document.addEventListener('DOMContentLoaded', () => {
  initParticleCanvas();
  bindFilterAndSearch();
  bindContactForm();
  bindMobileNav();
  initScrollSpy();
});

/* Dynamic ScrollSpy for Navbar Active States */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links .nav-link');

  if (sections.length === 0 || navLinks.length === 0) return;

  const onScroll = () => {
    const scrollPos = window.scrollY + 140;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(link => {
          const href = link.getAttribute('href');
          if (href === `/#${id}` || href === `#${id}`) {
            link.classList.add('active');
          } else if (href.includes('#') || href === '/' || href === '/#hero') {
            link.classList.remove('active');
          }
        });
      }
    });
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  setTimeout(onScroll, 150);
}

/* Real-Time Search & Category Filters */
function bindFilterAndSearch() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');
  const searchInput = document.getElementById('project-search-input');

  let currentFilter = 'all';

  function applyFilters() {
    const query = searchInput ? searchInput.value.trim().toLowerCase() : '';

    projectCards.forEach(card => {
      const category = card.dataset.category || '';
      const hasRender = card.dataset.render === 'true';
      const searchText = card.dataset.search || '';

      // Check category filter
      let matchesFilter = false;
      if (currentFilter === 'all') matchesFilter = true;
      else if (currentFilter === 'render') matchesFilter = hasRender;
      else if (currentFilter === 'backend') matchesFilter = (category === 'backend');
      else if (currentFilter === 'automation') matchesFilter = (category === 'automation');

      // Check search query
      const matchesSearch = !query || searchText.includes(query);

      if (matchesFilter && matchesSearch) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.filter || 'all';
      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }
}

/* Live API Test Ping Feature (Interactive WOW element) */
window.testLiveApiPing = async function () {
  const btn = document.getElementById('hub-ping-btn');
  if (!btn) return;

  const originalText = btn.textContent;
  btn.textContent = 'Pinging /api/projects... ⏳';
  btn.style.opacity = '0.7';

  const startTime = performance.now();
  try {
    const res = await fetch('/api/projects');
    const elapsed = Math.round(performance.now() - startTime);

    if (res.ok) {
      btn.textContent = `● 200 OK (${elapsed}ms) ⚡`;
      btn.style.background = 'rgba(16, 185, 129, 0.3)';
      btn.style.color = '#34d399';
      showToast(`Live FastAPI ping succeeded! Returned HTTP 200 in ${elapsed}ms.`);
    } else {
      btn.textContent = '● Error';
    }
  } catch (err) {
    btn.textContent = '● Offline';
  }

  setTimeout(() => {
    btn.textContent = originalText;
    btn.style.opacity = '1';
    btn.style.background = 'rgba(16, 185, 129, 0.15)';
    btn.style.color = 'var(--emerald-light)';
  }, 3500);
};

/* Contact Form Submission to FastAPI Backend */
function bindContactForm() {
  const form = document.getElementById('fastapi-contact-form');
  const submitBtn = document.getElementById('contact-submit-btn');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('contact-name').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const subject = document.getElementById('contact-subject').value.trim();
    const message = document.getElementById('contact-message').value.trim();

    if (!name || !email || !message) {
      showToast('Please fill in all required fields.', 'error');
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span>Sending... ⏳</span>';
    }

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, subject, message })
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showToast(`Thank you, ${name}! Your inquiry has been sent to Akhil. 🚀`);
        form.reset();
      } else {
        showToast(result.detail || 'Could not send message. Please try again.', 'error');
      }
    } catch (err) {
      showToast('Network error while sending inquiry. Please try again.', 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>🚀 Send Inquiry</span>';
      }
    }
  });
}

/* Mobile Nav Toggle */
function bindMobileNav() {
  const toggle = document.getElementById('mobile-nav-toggle');
  const links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => links.classList.toggle('mobile-open'));
    links.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => links.classList.remove('mobile-open'));
    });
  }
}

/* Toast Alerts */
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.style.borderColor = type === 'error' ? '#ef4444' : '#10b981';
  toast.innerHTML = `<span>${type === 'error' ? '⚠️' : '⚡'}</span><span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

/* Ambient Canvas Particle Network */
function initParticleCanvas() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particles = [];
  const particleCount = Math.min(Math.floor(width / 24), 45);

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      radius: Math.random() * 1.5 + 0.8,
      alpha: Math.random() * 0.35 + 0.15
    });
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > width) p.vx *= -1;
      if (p.y < 0 || p.y > height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(99, 102, 241, ${p.alpha})`;
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 100) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(99, 102, 241, ${0.1 * (1 - dist / 100)})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(animate);
  }
  animate();
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
