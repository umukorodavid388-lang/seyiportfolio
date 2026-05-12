// Main site JS
// Toggle subservices under a category card
document.addEventListener('click', function (e) {
  // toggle when clicking a category card (has .category-card)
  const card = e.target.closest('.category-card');
  if (!card) return;
  const catId = card.dataset.catId;
  if (!catId) return;
  const panel = document.querySelector('.subservices-panel[data-parent="' + catId + '"]');
  if (!panel) return;
  panel.classList.toggle('open');
  // Animate simple height transition
  if (panel.classList.contains('open')) {
    panel.style.maxHeight = panel.scrollHeight + 'px';
  } else {
    panel.style.maxHeight = null;
  }
});
