---
title: "Livewire 4, Volt & Folio Conventions"
description: "Single-file component patterns, reactive properties, and Folio routing."
globs: ["resources/views/**/*.blade.php", "app/Livewire/**/*.php"]
---

# Livewire 4, Volt & Folio Conventions

1. **Volt Single-File Components:**
   - Use Volt functional or class-based syntax inside `resources/views/livewire/`.
   - Keep state properties strictly typed (`public string $query = '';`).

2. **Folio Page Routing:**
   - Organize URL routes as `.blade.php` pages under `resources/views/pages/`.
   - Apply middleware in Volt components using `middleware(['auth', 'verified'])`.
