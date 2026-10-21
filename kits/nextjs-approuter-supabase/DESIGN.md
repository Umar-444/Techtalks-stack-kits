# DESIGN.md — Next.js + shadcn/ui Design System

## 1. Tokens
```yaml
colors:
  primary:
    DEFAULT: "#E85D26" # TechTalks Orange
  teal:
    DEFAULT: "#0E7C6B"
  neutral:
    bg_light: "#FFFFFF"
    bg_canvas: "#F4F4F0"
    bg_dark: "#0F1110"
    bg_dark_card: "#171A18"
```

## 2. Component Guidelines
- Use Radix UI primitives styled with Tailwind CSS via shadcn/ui.
- Maintain CSS variables for `--background`, `--foreground`, and `--primary`.
- Full dark mode support using `next-themes` and `.dark` class.
