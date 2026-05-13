/* Daydream marketing site — frontend behavior.
   Time tick, chip toggles, reveal-on-scroll, and the contact form
   POSTing to /api/contact with an inline success/error state. */

(function () {
  /* ---------------- live Monterrey time ---------------- */
  function updateTime() {
    const fmt = new Intl.DateTimeFormat('en-GB', {
      timeZone: 'America/Monterrey',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    });
    const [hh, mm] = fmt.format(new Date()).split(':');
    const heroEl = document.getElementById('local-time');
    if (heroEl) heroEl.textContent = `${hh}:${mm} · MTY`;
    const footEl = document.getElementById('footer-time');
    if (footEl) footEl.textContent = `MTY ${hh}:${mm}`;
  }
  updateTime();
  setInterval(updateTime, 30000);

  /* ---------------- chip toggles ---------------- */
  const chips = document.getElementById('form-chips');
  if (chips) {
    chips.addEventListener('click', (e) => {
      const c = e.target.closest('[data-chip]');
      if (!c) return;
      c.dataset.active = c.dataset.active === 'true' ? 'false' : 'true';
    });
  }

  /* ---------------- reveal-on-scroll ---------------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.classList.add('in');
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.15 });

  document
    .querySelectorAll('.section-head, .process-step, .about-block, .service, .client, .form')
    .forEach((el) => {
      el.classList.add('reveal');
      io.observe(el);
    });

  /* ---------------- contact form ---------------- */
  const form = document.getElementById('contact-form');
  if (!form) return;

  const btn = document.getElementById('form-submit-btn');
  const btnLabel = btn.querySelector('.form-submit-label');
  const errorEl = document.getElementById('form-error');
  const successEl = document.getElementById('form-success');

  function setError(msg) {
    if (!msg) {
      errorEl.hidden = true;
      errorEl.textContent = '';
      return;
    }
    errorEl.hidden = false;
    errorEl.textContent = msg;
  }

  function selectedNeeds() {
    return Array.from(document.querySelectorAll('#form-chips [data-chip][data-active="true"]'))
      .map((el) => el.textContent.trim())
      .filter(Boolean);
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    setError(null);

    const data = {
      name: form.elements['name'].value.trim(),
      email: form.elements['email'].value.trim(),
      company: form.elements['company'].value.trim(),
      message: form.elements['message'].value.trim(),
      needs: selectedNeeds(),
      // Honeypot — should stay empty.
      website: form.elements['website'].value,
    };

    if (!data.name) return setError('Tell us your name.');
    if (!data.email || !/.+@.+\..+/.test(data.email)) return setError('A real email helps us reply.');

    btn.disabled = true;
    btnLabel.textContent = 'Sending…';

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (res.status === 429) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || 'A little too quick — try again in a moment.');
      }
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || 'Something went wrong. Email hola@letsdaydream.ai directly.');
      }

      // success: swap form for success card
      form.hidden = true;
      successEl.hidden = false;
      successEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (err) {
      setError(err.message || 'Network hiccup. Try again, or email hola@letsdaydream.ai.');
      btn.disabled = false;
      btnLabel.textContent = 'Send inquiry';
    }
  });
})();
