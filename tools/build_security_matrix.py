#!/usr/bin/env python3
"""Aggregate every kit's security manifest into one OWASP Top 10:2025 matrix.

    python tools/build_security_matrix.py            # write JSON + HTML
    python tools/build_security_matrix.py --check    # fail if outputs are stale

Outputs:
    security/coverage.json          machine-readable aggregate
    security/coverage/index.html    the published coverage matrix

The JSON is the interesting artifact: it lets an agent answer "which kit
already solves tenant isolation?" without reading 35 manifests.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import owasp  # noqa: E402
from lib import security_checks as sc  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
KITS_DIR = REPO_ROOT / "kits"
JSON_OUT = REPO_ROOT / "security" / "coverage.json"
HTML_OUT = REPO_ROOT / "security" / "coverage" / "index.html"

SITE = "https://techtalks.itsumarfarooq.com"

SEVERITY_ORDER = ("critical", "high", "medium", "low")


def collect() -> dict:
    kits = []
    for kit_dir in sorted(p for p in KITS_DIR.iterdir() if (p / "kit.yaml").exists()):
        manifest_path = kit_dir / "security" / "checks.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        per_category: dict[str, int] = {}
        per_severity: dict[str, int] = {}
        for check in manifest["checks"]:
            for cat in check["owasp"]:
                per_category[cat] = per_category.get(cat, 0) + 1
            per_severity[check["severity"]] = per_severity.get(check["severity"], 0) + 1
        kits.append({
            "slug": kit_dir.name,
            "total": len(manifest["checks"]),
            "owasp": per_category,
            "severity": per_severity,
            "updated_at": manifest.get("updated_at"),
        })

    totals: dict[str, int] = {c.id: 0 for c in owasp.CATEGORIES}
    severities: dict[str, int] = {s: 0 for s in SEVERITY_ORDER}
    for kit in kits:
        for cat, n in kit["owasp"].items():
            totals[cat] = totals.get(cat, 0) + n
        for sev, n in kit["severity"].items():
            severities[sev] = severities.get(sev, 0) + n

    gaps = {
        c.id: sorted(k["slug"] for k in kits if c.id not in k["owasp"])
        for c in owasp.CATEGORIES
    }

    return {
        "generated_at": dt.date.today().isoformat(),
        "owasp_edition": owasp.EDITION,
        "schema_version": sc.SCHEMA_VERSION,
        "kit_count": len(kits),
        "control_count": sum(k["total"] for k in kits),
        "categories": [
            {
                "id": c.id,
                "rank": c.rank,
                "name": c.name,
                "summary": c.summary,
                "url": c.url,
                "control_count": totals[c.id],
                "kits_covering": len(kits) - len(gaps[c.id]),
                "kits_missing": gaps[c.id],
            }
            for c in owasp.CATEGORIES
        ],
        "severity_totals": severities,
        "kits": kits,
    }


def _coverage_tone(count: int) -> str:
    """Tailwind classes for a matrix cell, scaled by control count."""
    if count == 0:
        return "bg-[#FBEAE4] dark:bg-[#3A201A] text-[#B23B12] dark:text-[#F0A389]"
    if count == 1:
        return "bg-[#FFF1E8] dark:bg-[#2A2E2A] text-[#8A4A28] dark:text-[#C9A68E]"
    if count <= 3:
        return "bg-[#FDE3D2] dark:bg-[#4A2A18] text-[#A3450F] dark:text-[#F5BE9B]"
    return "bg-[#E85D26] text-white dark:bg-[#E85D26] dark:text-white font-semibold"


def render_html(data: dict) -> str:
    cats = data["categories"]
    e = html.escape

    head_cells = "".join(
        f'<th scope="col" class="px-2 py-3 text-center font-mono text-[11px] '
        f'font-semibold text-[#5C6058] dark:text-[#A8ACA0] whitespace-nowrap" '
        f'title="{e(c["name"])}">{e(c["id"].split(":")[0])}</th>'
        for c in cats
    )

    body_rows = []
    for kit in data["kits"]:
        cells = []
        for c in cats:
            n = kit["owasp"].get(c["id"], 0)
            cells.append(
                f'<td class="px-2 py-1.5 text-center"><span class="inline-flex min-w-[26px] '
                f'justify-center rounded-[5px] px-1.5 py-0.5 font-mono text-[11px] '
                f'{_coverage_tone(n)}" title="{e(kit["slug"])} &middot; {e(c["name"])}: '
                f'{n} control(s)">{n or "&mdash;"}</span></td>'
            )
        body_rows.append(
            '<tr class="border-t border-[#E6E6DF] dark:border-[#2A2E2A] '
            'hover:bg-[#FAFAF7] dark:hover:bg-[#161918] transition-colors">'
            f'<th scope="row" class="px-3 py-1.5 text-left font-medium whitespace-nowrap">'
            f'<a href="{SITE}/kits/{e(kit["slug"])}/" '
            f'class="hover:text-[#E85D26] transition-colors">{e(kit["slug"])}</a></th>'
            f'<td class="px-3 py-1.5 text-center font-mono text-[12px] '
            f'text-[#5C6058] dark:text-[#A8ACA0]">{kit["total"]}</td>'
            + "".join(cells) + "</tr>"
        )

    category_cards = []
    for c in cats:
        missing = c["kits_missing"]
        if missing:
            gap_html = (
                f'<p class="mt-3 text-[13px] text-[#5C6058] dark:text-[#A8ACA0]">'
                f'<span class="font-semibold text-[#B23B12] dark:text-[#F0A389]">'
                f'{len(missing)} kit(s) without a mapped control:</span> '
                f'<span class="font-mono text-[11.5px]">{e(", ".join(missing[:8]))}'
                f'{" &hellip;" if len(missing) > 8 else ""}</span></p>'
            )
        else:
            gap_html = (
                '<p class="mt-3 text-[13px] font-medium text-[#1F7A4D] dark:text-[#6EE7A8]">'
                'Covered by every kit in the catalogue.</p>'
            )
        category_cards.append(f"""
        <article class="rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#141716] p-5">
          <div class="flex items-baseline justify-between gap-3">
            <h3 class="font-semibold text-[15px]">
              <a href="{e(c['url'])}" target="_blank" rel="noopener noreferrer"
                 class="hover:text-[#E85D26] transition-colors">
                <span class="font-mono text-[12px] text-[#E85D26]">{e(c['id'])}</span>
                &nbsp;{e(c['name'])}
              </a>
            </h3>
            <span class="shrink-0 font-mono text-[12px] text-[#5C6058] dark:text-[#A8ACA0]">
              {c['control_count']} controls
            </span>
          </div>
          <p class="mt-2 text-[13.5px] leading-relaxed text-[#5C6058] dark:text-[#A8ACA0]">{e(c['summary'])}</p>
          <div class="mt-3 h-1.5 w-full rounded-full bg-[#EFEFE9] dark:bg-[#242825] overflow-hidden">
            <div class="h-full rounded-full bg-[#E85D26]"
                 style="width: {round(100 * c['kits_covering'] / max(data['kit_count'], 1))}%"></div>
          </div>
          <p class="mt-1.5 font-mono text-[11px] text-[#5C6058] dark:text-[#A8ACA0]">
            {c['kits_covering']} / {data['kit_count']} kits
          </p>
          {gap_html}
        </article>""")

    sev = data["severity_totals"]
    sev_cells = "".join(
        f'<div class="rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] '
        f'bg-white dark:bg-[#141716] px-4 py-3">'
        f'<div class="font-mono text-[22px] font-bold text-[#12140F] dark:text-[#F2F2EC]">{sev.get(s, 0)}</div>'
        f'<div class="mt-0.5 font-mono text-[11px] uppercase tracking-wider '
        f'text-[#5C6058] dark:text-[#A8ACA0]">{s}</div></div>'
        for s in SEVERITY_ORDER
    )

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OWASP Top 10:2025 Coverage Matrix &bull; TechTalks Stack Kits</title>
  <meta name="description"
    content="Every security control across all {data['kit_count']} TechTalks Stack Kits, mapped to the OWASP Top 10:2025. {data['control_count']} controls, with per-kit coverage and gap analysis.">
  <link rel="canonical" href="{SITE}/security/coverage/">

  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/security/coverage/">
  <meta property="og:title" content="OWASP Top 10:2025 Coverage Matrix &bull; TechTalks Stack Kits">
  <meta property="og:description"
    content="{data['control_count']} security controls across {data['kit_count']} stack kits, mapped to OWASP Top 10:2025.">
  <meta property="og:image" content="{SITE}/assets/img/Techtalks%20Stack%20Kits.jpg">

  <link rel="icon" type="image/svg+xml"
    href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23E85D26'><path d='M13 2L3 14h9l-1 8 10-12h-9l1-8z'/></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap"
    rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css">
</head>

<body
  class="bg-white dark:bg-[#0F1110] text-[#12140F] dark:text-[#F2F2EC] selection:bg-[#FFF1E8] selection:text-[#E85D26] min-h-screen flex flex-col font-sans transition-colors">

  <header
    class="sticky top-0 z-50 h-[60px] bg-white/90 dark:bg-[#0F1110]/90 backdrop-blur-md border-b border-[#E6E6DF] dark:border-[#2A2E2A] transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      <a href="/" class="flex items-center gap-2.5 group select-none" aria-label="TechTalks Stack Kits Home">
        <div class="w-[30px] h-[30px] rounded-[6px] bg-[#E85D26] flex items-center justify-center text-white font-bold text-xs">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" /></svg>
        </div>
        <div class="flex items-baseline">
          <span class="font-bold text-[17px] tracking-[-0.02em] group-hover:text-[#E85D26] transition-colors">TechTalks</span>
          <span class="font-mono text-[10px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0] font-semibold ml-2">STACK KITS</span>
        </div>
      </a>
      <nav class="hidden md:flex items-center gap-6 text-[15px]" aria-label="Main Navigation">
        <a href="/kits/" class="text-[#5C6058] dark:text-[#8E8E96] hover:text-[#12140F] dark:hover:text-[#F4F4F5] font-medium transition-colors">Kits</a>
        <a href="/security/" class="text-[#5C6058] dark:text-[#8E8E96] hover:text-[#12140F] dark:hover:text-[#F4F4F5] font-medium transition-colors">Standards</a>
        <a href="/security/coverage/" class="text-[#E85D26] font-semibold transition-colors" aria-current="page">Coverage</a>
        <a href="/status/" class="text-[#5C6058] dark:text-[#8E8E96] hover:text-[#12140F] dark:hover:text-[#F4F4F5] font-medium transition-colors">Status</a>
        <a href="https://github.com/Umar-444/Techtalks-stack-kits" target="_blank" rel="noopener noreferrer"
           class="text-[#5C6058] dark:text-[#8E8E96] hover:text-[#12140F] dark:hover:text-[#F4F4F5] font-medium transition-colors">GitHub</a>
      </nav>
      <button id="theme-toggle" type="button" aria-label="Toggle theme"
        class="w-[36px] h-[36px] rounded-[6px] flex items-center justify-center text-[#5C6058] dark:text-[#A8ACA0] hover:text-[#12140F] dark:hover:text-white hover:bg-[#F7F7F3] dark:hover:bg-[#171A18] transition-colors focus:outline-none focus:ring-2 focus:ring-[#E85D26]">
        <svg class="w-4 h-4 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg class="w-4 h-4 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </button>
    </div>
  </header>

  <main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">

    <nav class="font-mono text-[11.5px] text-[#5C6058] dark:text-[#A8ACA0] mb-6" aria-label="Breadcrumb">
      <a href="/security/" class="hover:text-[#E85D26] transition-colors">Standards</a>
      <span class="mx-1.5">/</span><span class="text-[#12140F] dark:text-[#F2F2EC]">OWASP Coverage</span>
    </nav>

    <h1 class="text-[34px] sm:text-[42px] font-extrabold tracking-[-0.03em] leading-[1.1]">
      OWASP Top&nbsp;10:2025 coverage matrix
    </h1>
    <p class="mt-4 max-w-3xl text-[16.5px] leading-relaxed text-[#5C6058] dark:text-[#A8ACA0]">
      Every security control shipped across the catalogue, mapped to the current OWASP Top&nbsp;10.
      Generated directly from each kit's <code class="font-mono text-[14px] text-[#E85D26]">security/checks.json</code>,
      so this page cannot drift from what the kits actually enforce.
    </p>

    <div class="mt-8 grid grid-cols-2 sm:grid-cols-4 gap-3">
      <div class="rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#141716] px-4 py-3">
        <div class="font-mono text-[22px] font-bold">{data['control_count']}</div>
        <div class="mt-0.5 font-mono text-[11px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0]">controls</div>
      </div>
      <div class="rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#141716] px-4 py-3">
        <div class="font-mono text-[22px] font-bold">{data['kit_count']}</div>
        <div class="mt-0.5 font-mono text-[11px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0]">kits</div>
      </div>
      <div class="rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#141716] px-4 py-3">
        <div class="font-mono text-[22px] font-bold">10 / 10</div>
        <div class="mt-0.5 font-mono text-[11px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0]">categories</div>
      </div>
      <div class="rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#141716] px-4 py-3">
        <div class="font-mono text-[22px] font-bold">{data['generated_at']}</div>
        <div class="mt-0.5 font-mono text-[11px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0]">generated</div>
      </div>
    </div>

    <section class="mt-12">
      <h2 class="text-[22px] font-bold tracking-[-0.02em]">Controls by severity</h2>
      <div class="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3">{sev_cells}</div>
    </section>

    <section class="mt-12">
      <h2 class="text-[22px] font-bold tracking-[-0.02em]">Kit &times; category matrix</h2>
      <p class="mt-2 text-[14.5px] text-[#5C6058] dark:text-[#A8ACA0]">
        Each cell counts controls in that kit mapped to that category. A dash means no control in this
        kit maps there &mdash; which is often correct: a static analysis pack has no session layer to harden.
      </p>
      <div class="mt-5 overflow-x-auto rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A]">
        <table class="w-full text-[13px] border-collapse">
          <caption class="sr-only">Security control counts per kit, by OWASP Top 10:2025 category</caption>
          <thead class="bg-[#FAFAF7] dark:bg-[#161918]">
            <tr>
              <th scope="col" class="px-3 py-3 text-left font-mono text-[11px] font-semibold text-[#5C6058] dark:text-[#A8ACA0]">Kit</th>
              <th scope="col" class="px-3 py-3 text-center font-mono text-[11px] font-semibold text-[#5C6058] dark:text-[#A8ACA0]">All</th>
              {head_cells}
            </tr>
          </thead>
          <tbody>{"".join(body_rows)}</tbody>
        </table>
      </div>
    </section>

    <section class="mt-14">
      <h2 class="text-[22px] font-bold tracking-[-0.02em]">Category breakdown</h2>
      <div class="mt-5 grid gap-4 md:grid-cols-2">{"".join(category_cards)}</div>
    </section>

    <section class="mt-14 rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-[#FAFAF7] dark:bg-[#141716] p-6">
      <h2 class="text-[18px] font-bold tracking-[-0.02em]">Machine-readable</h2>
      <p class="mt-2 text-[14.5px] leading-relaxed text-[#5C6058] dark:text-[#A8ACA0]">
        The same data as JSON, for agents and dashboards. Each kit manifest validates against
        <a href="{SITE}/schemas/kit-security-checks.schema.json" class="text-[#E85D26] hover:underline">kit-security-checks.schema.json</a>.
      </p>
      <pre class="mt-4 overflow-x-auto rounded-[8px] bg-[#12140F] dark:bg-[#0B0D0C] p-4 font-mono text-[12.5px] text-[#E6E6DF]"><code>curl -s {SITE}/security/coverage.json | jq '.categories[] | select(.id=="A01:2025")'

# Verify locally
python tools/validate_checks.py
python tools/build_security_matrix.py --check</code></pre>
    </section>

  </main>

  <footer class="border-t border-[#E6E6DF] dark:border-[#2A2E2A] py-8 mt-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3">
      <p class="text-[13px] text-[#5C6058] dark:text-[#A8ACA0]">
        &copy; 2026 Umar Farooq &middot; MIT licensed &middot; Not affiliated with OWASP.
      </p>
      <p class="font-mono text-[11.5px] text-[#5C6058] dark:text-[#A8ACA0]">
        Generated by <span class="text-[#E85D26]">tools/build_security_matrix.py</span>
      </p>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
</body>

</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if outputs are stale")
    args = parser.parse_args()

    data = collect()
    json_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    html_text = render_html(data)

    if args.check:
        stale = []
        for path, expected in ((JSON_OUT, json_text), (HTML_OUT, html_text)):
            if not path.exists():
                stale.append(f"missing {path.relative_to(REPO_ROOT)}")
            elif path.read_text(encoding="utf-8") != expected:
                stale.append(f"stale {path.relative_to(REPO_ROOT)}")
        if stale:
            print("FAIL — security matrix out of date:")
            for line in stale:
                print(f"  - {line}")
            print("\nRegenerate with: python tools/build_security_matrix.py")
            return 1
        print("PASS — security matrix is current")
        return 0

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json_text, encoding="utf-8")
    HTML_OUT.write_text(html_text, encoding="utf-8")

    print(f"wrote {JSON_OUT.relative_to(REPO_ROOT)}")
    print(f"wrote {HTML_OUT.relative_to(REPO_ROOT)}")
    print(
        f"\n{data['control_count']} controls across {data['kit_count']} kits, "
        f"OWASP Top 10:{data['owasp_edition']}"
    )
    for c in data["categories"]:
        bar = "#" * round(20 * c["kits_covering"] / max(data["kit_count"], 1))
        print(
            f"  {c['id']}  {c['control_count']:>4} controls  "
            f"{c['kits_covering']:>2}/{data['kit_count']} kits  {bar}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
