# Design System: Filament 4 Admin Interface

## 1. Principles
- **Density & Clarity**: High-density data tables designed for operational efficiency.
- **Theme Support**: Flawless dark mode (`#0f172a` slate background) and light mode (`#f8fafc`).
- **WCAG AA Compliance**: High-contrast ratios (minimum 4.5:1 on text and 3:1 on UI elements).

## 2. Color Palette
- **Primary / Brand**: Amber / Goldenrod (`#d97706` dark, `#b45309` light)
- **Neutral Dark**: Slate 900 (`#0f172a`), Slate 800 (`#1e293b`), Slate 700 (`#334155`)
- **Neutral Light**: Slate 50 (`#f8fafc`), Slate 100 (`#f1f5f9`), Slate 200 (`#e2e8f0`)
- **Success**: Emerald 600 (`#059669`)
- **Danger / Warning**: Rose 600 (`#e11d48`) / Amber 500 (`#f59e0b`)

## 3. Component Hierarchy
- **Top Navigation**: Search bar with global keyboard shortcut (`Cmd+K` / `Ctrl+K`), Tenant switcher, User menu with Passkey status.
- **Data Table**: Server-side pagination, sticky header, multi-column sorting, MySQL full-text search input with debounce.
- **Form Modal**: Two-column responsive grid, validation error callouts, audit timestamp badges.
