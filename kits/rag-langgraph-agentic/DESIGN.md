# Design Tokens & System Standards: LangGraph + LangChain + Qdrant + Ragas Evals

Reference: Document 17 (Design System Spec) & Document 18 (Layout & Structure).

## 1. Typography & Hierarchy
- **Primary Font Family:** Inter (`font-sans`), weights 400 (regular), 500 (medium), 600 (semibold), 700 (bold).
- **Code & Numeric Labels:** JetBrains Mono (`font-mono`), weight 500.
- **Editorial Signature Accent:** Newsreader Italic (`font-serif italic`).

## 2. Palette Tokens
- **Background Light:** `#FDFDFC`
- **Background Dark:** `#0C0D0A`
- **Surface Cards Light:** `#FFFFFF` (Border: `#E6E6DF`)
- **Surface Cards Dark:** `#141712` (Border: `#2A2E2A`)
- **Brand Primary Accent:** `#E85D26`
- **Text Primary Light:** `#12140F`
- **Text Primary Dark:** `#F2F2EC`
- **Text Muted Light:** `#5C6058`
- **Text Muted Dark:** `#A8ACA0`

## 3. UI Invariants
- Zero floating gradients; strictly high-contrast borders and solid surfaces.
- Button height: strictly `40px` (`h-10 px-4 text-sm font-semibold rounded-md`).
- Focus rings: `focus:ring-2 focus:ring-[#E85D26]/20 focus:outline-none`.
