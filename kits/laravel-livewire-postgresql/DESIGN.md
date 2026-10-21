# DESIGN.md — Laravel 12 + Livewire 3 + Flux UI Design System
# Open Design Specification for Autonomous Coding Agents (Doc 17 & 18 Conforming)

This document is the absolute design authority for autonomous coding agents (Claude Code, Cursor, Codex, Windsurf, Roo, Antigravity) building interfaces inside this repository. Every generated Blade component, Livewire component, and Flux UI element must strictly implement these tokens, geometries, and anti-slop rules.

---

## 1. Design Tokens (Source of Truth)

### Color Palette
```yaml
colors:
  brand:
    primary: "#E85D26"        # Signature Orange (Strictly <= 5% of screen)
    primary_hover: "#CF4D19"
    primary_tint: "#FFF1E8"
    primary_dark_tint: "#2A1E16"
  ink:
    DEFAULT: "#12140F"        # Deep ink black (light mode text & primary buttons)
    dark: "#F2F2EC"           # Crisp cream white (dark mode text)
    secondary: "#5C6058"      # Muted body text (light)
    secondary_dark: "#A8ACA0" # Muted body text (dark)
    line: "#E6E6DF"           # 1px hairline border (light)
    line_dark: "#2A2E2A"      # 1px hairline border (dark)
    canvas: "#FFFFFF"         # Pure paper background (light)
    canvas_dark: "#0F1110"    # Deep night background (dark)
    surface: "#FFFFFF"        # Card surface (light)
    surface_dark: "#171A18"   # Card surface (dark)
    tint: "#F7F7F3"           # Subtle alternate section tint
  semantic:
    teal: "#0E7C6B"           # Verified / Ready status
    teal_tint: "#E6F4F1"
    gold: "#B7791F"           # Blueprint / Warning status
    gold_tint: "#FEF6D8"
    danger: "#DC2626"         # High-risk / Destructive
    success: "#16A34A"        # Test passing / Confirmed
```

### Typography Scale
- **Headings Font:** `Inter`, -apple-system, sans-serif
  - H1: 44px–56px, weight 700, letter-spacing: -0.03em, line-height: 1.15
  - H2: 30px–36px, weight 700, letter-spacing: -0.02em, line-height: 1.2
  - H3: 18px–22px, weight 700, letter-spacing: -0.02em, line-height: 1.3
- **Body Font:** `Inter`, system-ui, sans-serif
  - Size: 16px (14px for UI cards), line-height: 1.75, weight 400 (medium 500 for UI items)
  - Column Width: Reading articles and documentation strictly capped at 760px (`max-w-[760px]`).
- **Code & Number Font:** `JetBrains Mono`, monospace
  - Figures, uppercase eyebrow labels (11px tracking-wider), status chips, and code snippets.
- **Fingerprint Accent:** `Newsreader` italic
  - Exactly one italic serif word permitted in hero headlines and pull quotes.

---

## 2. Geometry & Spacing (8pt Grid)

- **Spacing scale:** 4, 8, 12, 16, 24, 32, 48, 64, 96px. Never use arbitrary off-scale paddings.
- **Border Radius:**
  - Buttons: `6px` (`rounded-[6px]`)
  - Cards & Modals: `8px` (`rounded-[8px]`)
  - Meta Chips: `4px` (`rounded-[4px]`)
  - Status Pills: `9999px` (`rounded-full`)
- **Borders & Hairlines:**
  - 1px solid hairline (`#E6E6DF` light, `#2A2E2A` dark) everywhere separation is needed.
  - Zero drop shadows at rest. The only allowed elevation is `0 8px 24px rgba(18,20,15,0.06)` on card hover with a `translateY(-2px)` lift.

---

## 3. Livewire 3 & Flux UI Component Hierarchy

### Buttons (Strict 40px Height)
1. **Primary Button:** Height 40px, padding 0 18px, radius 6px, font 14px/600. Default background is ink black (`#12140F`) with white text. Brand orange is reserved for the single most important call-to-action per screen.
2. **Secondary Button:** Same 40px dimensions. Background white, 1px border `#E6E6DF`, text `#12140F`. Hover: border `#CFCFC4`, background `#F7F7F3`.
3. **Ghost / Action:** Transparent background, muted text, hover background `#F4F4F0`.

### Livewire Component State & Telemetry
- **Loading States:** Always attach `wire:loading` feedback (e.g. `wire:loading.attr="disabled"` and spinner transition).
- **Debounced Inputs:** Text inputs bound to Livewire must specify `wire:model.live.debounce.300ms` to prevent server request flooding.
- **Validation Errors:** Render inline beneath inputs using 13px danger text (`text-[#DC2626]`) with 1px hairline border focus.

---

## 4. The Anti-Slop Rules (Non-Negotiable)

1. **No Gradients:** No linear or radial gradients on surfaces, backgrounds, or text.
2. **No Glassmorphism:** No backdrop blur except on the sticky header bar.
3. **No Decorative Drop Shadows:** Shadows are banned at rest.
4. **No Emojis as UI Icons:** Use Lucide or stroke SVGs (1.5px stroke, 18px size) only.
5. **Orange Budget:** Brand orange (`#E85D26`) must remain under 5% of total screen real estate.
