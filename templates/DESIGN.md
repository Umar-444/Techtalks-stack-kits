# DESIGN.md — {{ KIT_NAME }} Design System
# Open Design Specification (Tokens first, then 8 implementation sections)
# Reference: 05-Design-Standard.md & 11-Design-Deep-Dive.md

## 1. Design Tokens (The Source of Truth)

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
    bg_dark: "#0F1110"
    surface_warm_light: "#F4F4F0"
    surface_warm_dark: "#171A18"
    card_light: "#FFFFFF"
    card_dark: "#171A18"
    line_light: "#E6E6DF"
    line_dark: "#2A2E2A"
    ink_light: "#12140F"
    ink_dark: "#F2F2EC"
    muted_light: "#5C6058"
    muted_dark: "#A8ACA0"
```

### Typography Tokens
- **Display Headings:** Inter / System UI, font-weight 700, letter-spacing: -0.035em.
- **Section Headings:** Inter / System UI, font-weight 600, letter-spacing: -0.02em.
- **Body Text:** Inter, font-size 15px-16px, line-height 1.6, normal tracking.
- **Editorial Callouts:** Lyon Text / Georgia / serif, italic.
- **Code & Monospace:** JetBrains Mono / SFMono-Regular, font-size 13px.

### Geometry & Elevation
- **Border Radius:** `xs: 4px` (small badges), `sm: 8px` (buttons, inputs), `md: 12px` (cards, panels).
- **Shadows:** Soft whisper-light layered elevation. Never harsh single-drop shadows.

---

## 2. Visual Identity & Brand Persona
Calm, editorial, and engineering-focused. Interfaces must feel fast, responsive, and uncluttered. Interaction is carried primarily by brand accents while maintaining high contrast.

## 3. Layout Architecture
- Standard grid system with responsive 1-column (mobile), 2-column (tablet), and 3-column / 4-column (desktop).
- Header: Sticky 64px bar with subtle hairline under-rule.
- Content Containers: Max-width 1152px (`max-w-6xl`) with 24px (`px-6`) side padding.

## 4. Component Recipes
- **Primary Buttons:** 38px height, 8px radius, primary accent fill, white text, 2px focus ring.
- **Secondary Buttons:** 38px height, 8px radius, tinted accent fill, pressed text.
- **Cards:** 12px radius, 1px solid hairline border, 24px internal padding, subtle hover lift.
- **Data Tables:** Clear column hierarchy, right-aligned numbers, monospaced dates, clean row borders.

## 5. Motion & Micro-Interactions
- Transitions: 150ms ease-out on hovers and color shifts.
- Progress bars: Smooth width transitions with zero layout jank.

## 6. Accessibility & WCAG AA Compliance
- Strict contrast compliance: All body and headline text must achieve >= 4.5:1 against canvas.
- Keyboard navigation: Explicit `outline: 2px solid` with `2px offset` on all interactive elements.

## 7. Responsive Behavior
- Multi-column cards collapse to 1-column on viewports under 768px.
- Horizontal scroll overflow on wide data tables with visual scroll indicators.

## 8. Pre-Flight Design Review (5 Questions)
1. Does every button have an active, hover, and 2px focus outline state?
2. Does dark mode maintain exact visual parity without washed-out text?
3. Are all borders hairline (`1px solid var(--line)`) rather than heavy rules?
4. Is negative tracking strictly limited to display headings >= 24px?
5. Do tables and empty states feel designed rather than default framework scaffolding?
