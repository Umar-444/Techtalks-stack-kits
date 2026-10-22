# Design System: AI Chat & Semantic Search Interface

## 1. Principles
- **Clarity & Transparency**: Clearly distinguish user messages, streaming AI responses, thinking steps, and tool execution status.
- **Citation Chips**: Document sources are rendered as clickable badge chips linking directly to ground-truth passages.
- **Theme Support**: Slate dark theme (`#090d16` background) and crisp light theme (`#ffffff`).
- **WCAG AA Compliance**: High-contrast ratios (> 4.5:1 on text, > 3:1 on citations and status badges).

## 2. Color Palette
- **Primary / AI Accent**: Indigo 600 (`#4f46e5` light, `#6366f1` dark)
- **Neutral Dark**: Slate 950 (`#090d16`), Slate 900 (`#0f172a`), Slate 800 (`#1e293b`)
- **Neutral Light**: Slate 50 (`#f8fafc`), Slate 100 (`#f1f5f9`), Slate 200 (`#e2e8f0`)
- **Success / Grounded**: Emerald 500 (`#10b981`)
- **Warning / Injection Detected**: Amber 500 (`#f59e0b`) / Rose 500 (`#f43f5e`)

## 3. UI Component Hierarchy
- **Chat Feed**: Threaded conversation history with smooth auto-scroll on SSE token delivery.
- **Input Bar**: Auto-expanding textarea with keyboard shortcuts (`Cmd+Enter` / `Ctrl+Enter` to send).
- **Source Drawer**: Slide-over panel displaying retrieved chunks with cosine similarity score badges.
