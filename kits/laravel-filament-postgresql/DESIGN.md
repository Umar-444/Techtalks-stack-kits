# DESIGN.md — Laravel 12/13 + Filament 4/3 Design System
# Open Design Specification (Tokens first, then Filament components and layout)

## 1. Design Tokens (Source of Truth)

### Color Palette
```yaml
colors:
  primary:
    DEFAULT: "#E85D26" # TechTalks Orange
    hover: "#CF4D1B"
    tint: "#FFF1E8"
    dark_tint: "#2A1E16"
  teal:
    DEFAULT: "#0E7C6B" # Security Teal
    tint: "#E6F4F1"
    dark_tint: "#122A26"
  gold:
    DEFAULT: "#B7791F" # Ecosystem Gold
    tint: "#FEF6D8"
    dark_tint: "#2A2410"
  neutral:
    bg_light: "#FFFFFF"
    bg_canvas: "#F4F4F0"
    bg_dark: "#0F1110"
    bg_dark_card: "#171A18"
    text_light: "#12140F"
    text_dark: "#F2F2EC"
    muted_light: "#5C6058"
    muted_dark: "#A8ACA0"
    border_light: "#E6E6DF"
    border_dark: "#2A2E2A"
```

### Typography Scale
- **Headings Font:** Inter, -apple-system, sans-serif (Weights: 600, 700, 800)
- **Body Font:** Inter, system-ui, sans-serif (Weights: 400, 500)
- **Code/Mono Font:** JetBrains Mono, monospace (Weight: 400, 500)

---

## 2. Filament Dashboard Architecture

1. **SPA Mode Enabled:**
   The admin panel runs in Single-Page Application (SPA) mode using Livewire navigation for rapid page transitions without full browser reloads.

2. **Navigation Grouping:**
   - Group resources by user mental model, not raw Eloquent models (e.g., `Billing & Invoicing`, `Access Control`, `System Health`).
   - Every navigation item includes an explicit Heroicon or Lucide icon.

3. **Tables:**
   - Striped alternate rows using `bg-neutral-bg_canvas` in light mode and `bg-neutral-bg_dark_card` in dark mode.
   - Default pagination set to 25 items per page.
   - Bulk actions require an explicit confirmation modal with an explanation.

4. **Forms:**
   - Two-column responsive layout (`lg:grid-cols-2`).
   - Sticky form action bar at the bottom with explicit `Save Changes` and `Cancel` buttons.
   - Unsaved changes alert active on all edit pages.

5. **Accessibility & Contrast:**
   - All interactive elements must maintain a minimum 4.5:1 contrast ratio against their background (WCAG AA).
   - Form inputs must include accessible labels and visible focus rings.
