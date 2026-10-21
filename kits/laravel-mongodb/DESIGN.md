# DESIGN.md — Laravel 12 + MongoDB NoSQL Design System
# Open Design Specification for Autonomous Coding Agents (Doc 17 & 18 Conforming)

This document is the absolute design authority for autonomous coding agents (Claude Code, Cursor, Codex, Windsurf, Roo, Antigravity) building interfaces and data views inside this repository. Every generated Blade template, admin view, and analytics dashboard component must strictly adhere to these tokens, geometry rules, and anti-slop guidelines.

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
    danger: "#DC2626"         # Destructive action / Error
    success: "#16A34A"        # Verified safe / Success
```

### Typography Scale
- **Headings Font:** `Inter`, -apple-system, sans-serif
  - H1: 44px–56px, weight 700, letter-spacing: -0.03em, line-height: 1.15
  - H2: 30px–36px, weight 700, letter-spacing: -0.02em, line-height: 1.2
  - H3: 18px–22px, weight 700, letter-spacing: -0.02em, line-height: 1.3
- **Body Font:** `Inter`, system-ui, sans-serif
  - Size: 16px (14px for data cards and tables), line-height: 1.75, weight 400
  - Column Width: Content columns never wider than 760px (`max-w-[760px]`).
- **Code & Number Font:** `JetBrains Mono`, monospace
  - MongoDB ObjectIDs, collection metrics, JSON payloads, figures, and status chips.
- **Fingerprint Accent:** `Newsreader` italic
  - Exactly one italic serif word permitted in hero headlines and pull quotes.

---

## 2. Geometry & Spacing (8pt Grid)

- **Spacing scale:** 4, 8, 12, 16, 24, 32, 48, 64, 96px. Never use ad-hoc off-scale margins.
- **Border Radius:**
  - Buttons: `6px` (`rounded-[6px]`)
  - Cards & Document Panels: `8px` (`rounded-[8px]`)
  - Meta Chips: `4px` (`rounded-[4px]`)
  - Status Pills: `9999px` (`rounded-full`)
- **Borders & Hairlines:**
  - 1px solid hairline (`#E6E6DF` light, `#2A2E2A` dark) everywhere.
  - Zero shadows at rest. Cards elevate with `0 8px 24px rgba(18,20,15,0.06)` on hover with `translateY(-2px)`.

---

## 3. Data Tables & Document Inspection Views

### Document Tables (Strict Hairline Grid)
- **Header Row:** Mono 11px uppercase muted text (`#5C6058`), hairline border bottom, zero zebra striping.
- **Data Rows:** Height 44px, 14px regular text, hairline border between rows, subtle `#F7F7F3` tint on row hover.
- **IDs & Numbers:** Right-aligned or displayed in mono font (`JetBrains Mono`).

### JSON Document Previews (Dark Blocks)
- Even on light mode pages, document inspection code blocks stay dark (`#0F1110`), with JetBrains Mono 13.5px/1.7, 8px radius, and hairline `#2A2E2A` border.

---

## 4. The Anti-Slop Rules (Non-Negotiable)

1. **No Gradients:** No gradients on cards, backgrounds, or text.
2. **No Glassmorphism:** No backdrop blur except on the sticky header.
3. **No Decorative Shadows:** Zero shadows at rest.
4. **No Emojis as UI Icons:** Use Lucide stroke icons only (1.5px stroke, 18px size).
5. **Strict Orange Budget:** Brand orange (`#E85D26`) is spent only on the primary CTA and active status tags (strictly <= 5% of screen).
