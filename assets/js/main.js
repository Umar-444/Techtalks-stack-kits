/**
 * UmarTechTalks - Core Interactive Functions
 * Lightweight vanilla JavaScript (Zero external dependencies)
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initMobileMenu();
  initCopyButtons();
  initPromptCopyButtons();
  initFaqAccordions();
  initReadingProgressBar();
  initChecklistPersistence();
});

/* ==========================================================================
   1. Theme Management (Dark Mode)
   ========================================================================== */
function initTheme() {
  const themeToggleButtons = document.querySelectorAll('[data-theme-toggle]');
  const html = document.documentElement;

  // Check saved preference or system preference
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    html.classList.add('dark');
  } else {
    html.classList.remove('dark');
  }

  themeToggleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const isDark = html.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
  });
}

/* ==========================================================================
   2. Mobile Navigation Menu
   ========================================================================== */
function initMobileMenu() {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (!menuBtn || !mobileMenu) return;

  menuBtn.addEventListener('click', () => {
    const isExpanded = menuBtn.getAttribute('aria-expanded') === 'true';
    menuBtn.setAttribute('aria-expanded', !isExpanded);
    mobileMenu.classList.toggle('hidden');
  });
}

/* ==========================================================================
   3. Code Block Copy Buttons
   ========================================================================== */
function initCopyButtons() {
  const copyButtons = document.querySelectorAll('.code-copy-btn');

  copyButtons.forEach(button => {
    button.addEventListener('click', async () => {
      const container = button.closest('.code-container');
      if (!container) return;

      const codeElement = container.querySelector('code');
      if (!codeElement) return;

      const textToCopy = codeElement.innerText;

      try {
        await navigator.clipboard.writeText(textToCopy);
        const originalHtml = button.innerHTML;
        button.innerHTML = `
          <svg class="w-3.5 h-3.5 text-emerald-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <span class="text-emerald-400 font-medium">Copied!</span>
        `;
        button.classList.add('bg-slate-700');

        setTimeout(() => {
          button.innerHTML = originalHtml;
          button.classList.remove('bg-slate-700');
        }, 2000);
      } catch (err) {
        console.error('Copy to clipboard failed:', err);
      }
    });
  });
}

/* ==========================================================================
   4. Prompt Template Copy Buttons
   ========================================================================== */
function initPromptCopyButtons() {
  const promptButtons = document.querySelectorAll('[data-copy-prompt]');

  promptButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const targetId = btn.getAttribute('data-copy-prompt');
      const targetElement = document.getElementById(targetId);
      if (!targetElement) return;

      const text = targetElement.innerText.trim();

      try {
        await navigator.clipboard.writeText(text);
        const originalText = btn.innerText;
        btn.innerText = 'Prompt Copied!';
        btn.classList.add('bg-emerald-600', 'text-white');

        setTimeout(() => {
          btn.innerText = originalText;
          btn.classList.remove('bg-emerald-600', 'text-white');
        }, 2000);
      } catch (e) {
        console.error('Prompt copy failed:', e);
      }
    });
  });
}

/* ==========================================================================
   5. FAQ Accordions
   ========================================================================== */
function initFaqAccordions() {
  const faqQuestions = document.querySelectorAll('.faq-question');

  faqQuestions.forEach(btn => {
    btn.addEventListener('click', () => {
      const isExpanded = btn.getAttribute('aria-expanded') === 'true';
      const answer = btn.nextElementSibling;
      const chevron = btn.querySelector('.faq-chevron');

      btn.setAttribute('aria-expanded', !isExpanded);

      if (isExpanded) {
        answer.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
      } else {
        answer.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
      }
    });
  });
}

/* ==========================================================================
   6. Reading Progress Bar (Lesson Pages)
   ========================================================================== */
function initReadingProgressBar() {
  const progressBar = document.getElementById('reading-progress-bar');
  if (!progressBar) return;

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (totalHeight <= 0) return;

    const progress = (window.scrollY / totalHeight) * 100;
    progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
  }, { passive: true });
}

/* ==========================================================================
   7. Checklist State Persistence (localStorage)
   ========================================================================== */
function initChecklistPersistence() {
  const checklistCheckboxes = document.querySelectorAll('.checklist-checkbox');
  if (checklistCheckboxes.length === 0) return;

  const pageKey = 'checklist_' + window.location.pathname;

  // Restore state
  try {
    const saved = JSON.parse(localStorage.getItem(pageKey) || '{}');
    checklistCheckboxes.forEach((cb, idx) => {
      if (saved[idx]) {
        cb.checked = true;
      }
      cb.addEventListener('change', () => {
        saved[idx] = cb.checked;
        localStorage.setItem(pageKey, JSON.stringify(saved));
      });
    });
  } catch (e) {
    console.warn('Checklist storage disabled:', e);
  }
}
