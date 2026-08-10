/* =========================================================
   DecorAI — shared behaviour
   ========================================================= */

// Toggle a "favourite" heart on any element with [data-fav]
document.addEventListener('click', (e) => {
  const favBtn = e.target.closest('[data-fav]');
  if (favBtn) {
    favBtn.classList.toggle('is-fav');
    const svg = favBtn.querySelector('svg');
    if (svg) svg.setAttribute('fill', favBtn.classList.contains('is-fav') ? 'currentColor' : 'none');
  }

  // Generic chip / tab toggle within a shared chip-row
  const chip = e.target.closest('[data-chip-group]');
  if (chip) {
    const group = chip.parentElement;
    group.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
  }

  // Step-based "select" cards (style / room-type pickers etc.)
  const pick = e.target.closest('[data-pick-group]');
  if (pick) {
    const group = pick.closest('[data-pick-parent]') || pick.parentElement;
    group.querySelectorAll('[data-pick-group]').forEach(c => c.classList.remove('selected'));
    pick.classList.add('selected');
  }

  // Simple button "loading -> done" simulation for AI actions
  const aiBtn = e.target.closest('[data-ai-action]');
  if (aiBtn && !aiBtn.classList.contains('is-loading')) {
    simulateAIAction(aiBtn);
  }
});

function simulateAIAction(btn){
  const original = btn.innerHTML;
  btn.classList.add('is-loading');
  btn.innerHTML = 'Generating…';
  btn.style.opacity = '0.75';
  setTimeout(() => {
    btn.innerHTML = original;
    btn.style.opacity = '1';
    btn.classList.remove('is-loading');
    const target = document.querySelector(btn.getAttribute('data-ai-action'));
    if (target) target.classList.add('revealed');
  }, 900);
}

// Budget slider (AI Design Studio) - keep label synced
document.addEventListener('input', (e) => {
  if (e.target.matches('[data-budget-slider]')) {
    const labels = ['Low', 'Medium', 'High'];
    const out = document.querySelector('[data-budget-label]');
    if (out) out.textContent = labels[e.target.value];
  }
});
