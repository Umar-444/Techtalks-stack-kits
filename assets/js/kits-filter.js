/**
 * TechTalks Stack Kits - Interactive Filter & Explorer
 * Handles live client-side filtering, search, badge toggles, and copy-to-clipboard interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
  initKitsExplorer();
});

function initKitsExplorer() {
  const searchInput = document.getElementById('kit-search-input');
  const ecosystemPills = document.querySelectorAll('[data-filter-eco]');
  const statusPills = document.querySelectorAll('[data-filter-status]');
  const kitCards = document.querySelectorAll('[data-kit-item]');
  const countBadge = document.getElementById('kit-count-badge');
  const emptyState = document.getElementById('kit-empty-state');
  const clearFiltersBtn = document.getElementById('kit-clear-filters');

  if (!kitCards.length) return;

  let activeEcosystem = 'all';
  let activeStatus = 'all';
  let searchQuery = '';

  // Focus search with '/' key
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== searchInput) {
      if (!['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        if (searchInput) searchInput.focus();
      }
    }
  });

  function applyFilters() {
    let visibleCount = 0;
    const query = searchQuery.trim().toLowerCase();

    kitCards.forEach(card => {
      const cardEco = card.getAttribute('data-eco') || '';
      const cardStatus = card.getAttribute('data-status') || '';
      const cardText = (card.textContent || '').toLowerCase();
      const cardTags = (card.getAttribute('data-tags') || '').toLowerCase();

      const matchesEco = (activeEcosystem === 'all' || cardEco.split(' ').includes(activeEcosystem));
      const matchesStatus = (activeStatus === 'all' || cardStatus === activeStatus);
      const matchesSearch = (!query || cardText.includes(query) || cardTags.includes(query));

      if (matchesEco && matchesStatus && matchesSearch) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (countBadge) {
      countBadge.textContent = `Showing ${visibleCount} of ${kitCards.length} kits`;
    }

    if (emptyState) {
      emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  // Search input handler
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value;
      applyFilters();
    });
  }

  // Ecosystem filter pills
  ecosystemPills.forEach(pill => {
    pill.addEventListener('click', () => {
      ecosystemPills.forEach(p => {
        p.classList.remove('bg-[#E85D26]', 'text-white', 'border-[#E85D26]');
        p.classList.add('bg-[#F4F4F0]', 'dark:bg-[#171A18]', 'text-[#5C6058]', 'dark:text-[#A8ACA0]', 'border-[#E6E6DF]', 'dark:border-[#2A2E2A]');
      });
      pill.classList.remove('bg-[#F4F4F0]', 'dark:bg-[#171A18]', 'text-[#5C6058]', 'dark:text-[#A8ACA0]', 'border-[#E6E6DF]', 'dark:border-[#2A2E2A]');
      pill.classList.add('bg-[#E85D26]', 'text-white', 'border-[#E85D26]');
      activeEcosystem = pill.getAttribute('data-filter-eco') || 'all';
      applyFilters();
    });
  });

  // Status filter pills
  statusPills.forEach(pill => {
    pill.addEventListener('click', () => {
      statusPills.forEach(p => {
        p.classList.remove('bg-[#0E7C6B]', 'text-white', 'border-[#0E7C6B]');
        p.classList.add('bg-[#F4F4F0]', 'dark:bg-[#171A18]', 'text-[#5C6058]', 'dark:text-[#A8ACA0]', 'border-[#E6E6DF]', 'dark:border-[#2A2E2A]');
      });
      pill.classList.remove('bg-[#F4F4F0]', 'dark:bg-[#171A18]', 'text-[#5C6058]', 'dark:text-[#A8ACA0]', 'border-[#E6E6DF]', 'dark:border-[#2A2E2A]');
      pill.classList.add('bg-[#0E7C6B]', 'text-white', 'border-[#0E7C6B]');
      activeStatus = pill.getAttribute('data-filter-status') || 'all';
      applyFilters();
    });
  });

  // Reset button
  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      searchQuery = '';
      activeEcosystem = 'all';
      activeStatus = 'all';

      // Reset pill styles
      ecosystemPills.forEach((p, idx) => {
        if (idx === 0) {
          p.classList.add('bg-[#E85D26]', 'text-white', 'border-[#E85D26]');
          p.classList.remove('bg-[#F4F4F0]', 'dark:bg-[#171A18]', 'text-[#5C6058]', 'dark:text-[#A8ACA0]', 'border-[#E6E6DF]', 'dark:border-[#2A2E2A]');
        } else {
          p.classList.remove('bg-[#E85D26]', 'text-white', 'border-[#E85D26]');
          p.classList.add('bg-[#F4F4F0]', 'dark:bg-[#171A18]', 'text-[#5C6058]', 'dark:text-[#A8ACA0]', 'border-[#E6E6DF]', 'dark:border-[#2A2E2A]');
        }
      });

      statusPills.forEach((p, idx) => {
        if (idx === 0) {
          p.classList.add('bg-[#0E7C6B]', 'text-white', 'border-[#0E7C6B]');
          p.classList.remove('bg-[#F4F4F0]', 'dark:bg-[#171A18]', 'text-[#5C6058]', 'dark:text-[#A8ACA0]', 'border-[#E6E6DF]', 'dark:border-[#2A2E2A]');
        } else {
          p.classList.remove('bg-[#0E7C6B]', 'text-white', 'border-[#0E7C6B]');
          p.classList.add('bg-[#F4F4F0]', 'dark:bg-[#171A18]', 'text-[#5C6058]', 'dark:text-[#A8ACA0]', 'border-[#E6E6DF]', 'dark:border-[#2A2E2A]');
        }
      });

      applyFilters();
    });
  }

  // Copy Clone command button
  document.querySelectorAll('[data-copy-cmd]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const cmd = btn.getAttribute('data-copy-cmd');
      if (!cmd) return;

      navigator.clipboard.writeText(cmd).then(() => {
        showToast('Copied clone command to clipboard!');
        const origText = btn.innerHTML;
        btn.innerHTML = `<svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> Copied!`;
        setTimeout(() => {
          btn.innerHTML = origText;
        }, 2000);
      });
    });
  });

  // Copy Agent Prompt button
  document.querySelectorAll('[data-copy-prompt]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const promptText = btn.getAttribute('data-copy-prompt');
      if (!promptText) return;

      navigator.clipboard.writeText(promptText).then(() => {
        showToast('Copied agent prompt header!');
        const origText = btn.innerHTML;
        btn.innerHTML = `<svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> Copied!`;
        setTimeout(() => {
          btn.innerHTML = origText;
        }, 2000);
      });
    });
  });
}

function showToast(message) {
  let toast = document.getElementById('kit-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'kit-toast';
    toast.className = 'fixed bottom-6 right-6 z-50 flex items-center gap-2.5 px-4 py-3 bg-[#12140F] dark:bg-[#F2F2EC] text-white dark:text-[#12140F] text-sm font-medium rounded-md shadow-xl transition-all duration-300 transform translate-y-8 opacity-0 pointer-events-none';
    document.body.appendChild(toast);
  }

  toast.innerHTML = `<svg class="w-4 h-4 text-[#E85D26]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> <span>${message}</span>`;
  
  // Animate in
  setTimeout(() => {
    toast.classList.remove('translate-y-8', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');
  }, 10);

  // Animate out
  setTimeout(() => {
    toast.classList.remove('translate-y-0', 'opacity-100');
    toast.classList.add('translate-y-8', 'opacity-0');
  }, 2500);
}
