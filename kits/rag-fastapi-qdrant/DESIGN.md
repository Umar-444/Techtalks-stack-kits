# System & Interface Design Specification: RAG FastAPI + Qdrant

## 1. Design Overview
This specification details the interface tokens, vector search visualization standards, and latency budgets for the RAG FastAPI + Qdrant vector retrieval service.

---

## 2. Latency & Resource Budgets

| Operation | Target (p50) | Upper Bound (p95) | Constraints |
|---|:---:|:---:|---|
| **Query Embedding** (FastEmbed BGE-small) | 4 ms | 12 ms | Runs locally on CPU via ONNX Runtime |
| **Qdrant Vector Search** (HNSW Graph) | 2 ms | 8 ms | In-memory index, `m=16`, `ef_construct=100` |
| **Payload Filtering** (Tenant ID Match) | 0.5 ms | 2 ms | Evaluated via Qdrant keyword index |
| **Context Assembly & Formatting** | 1 ms | 3 ms | Token budget capped at 3,000 tokens |
| **End-to-End Retrieval Endpoint** | **8 ms** | **25 ms** | Sub-30ms total p95 response time |

---

## 3. Semantic Color Palette & Score Badging

Semantic score badges communicate relevance confidence:

```css
:root {
  /* High Confidence Match (Score >= 0.80) */
  --score-high-bg: #ecfdf5;      /* emerald-50 */
  --score-high-border: #a7f3d0;  /* emerald-200 */
  --score-high-text: #065f46;    /* emerald-800 */

  /* Moderate Confidence Match (Score 0.60 - 0.79) */
  --score-med-bg: #fffbeb;       /* amber-50 */
  --score-med-border: #fde68a;   /* amber-200 */
  --score-med-text: #92400e;     /* amber-800 */

  /* Low / Below Threshold (Score < 0.60) */
  --score-low-bg: #fff1f2;       /* rose-50 */
  --score-low-border: #fecdd3;   /* rose-200 */
  --score-low-text: #9f1239;     /* rose-800 */

  /* Surface & Base */
  --bg-primary: #090d16;        /* Dark slate 950 */
  --bg-card: #131b2e;           /* Dark slate 900 */
  --accent-qdrant: #dc2626;     /* Qdrant red 600 */
  --accent-fastapi: #059669;    /* FastAPI teal 600 */
}
```

---

## 4. Source Citation Card Component Specifications
Every retrieved context chunk must render with provenance cards displaying:
1. **Document Identifier & Title**: Truncated with ellipsis if > 40 chars.
2. **Chunk Index & Character Range**: Explicit provenance coordinates (`start_char`, `end_char`).
3. **Similarity Score Badge**: Color-coded pill badge displaying four decimal precision (e.g. `Score: 0.8412`).
4. **Tenant Metadata Tag**: Subtle badge indicating tenant isolation boundary.
5. **Highlighted Match Excerpt**: Clean typography with 1.5 line height and WCAG AA contrast (minimum 4.5:1 ratio).
