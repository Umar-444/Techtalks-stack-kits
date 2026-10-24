#!/usr/bin/env python3
"""Publish an honest maturity board for every kit.

    python tools/build_status_board.py           # write JSON + HTML
    python tools/build_status_board.py --check   # fail if outputs are stale

Maturity is DERIVED from evals/results/*_metrics.json, never self-declared in
kit.yaml. A kit cannot claim to be verified; it earns the label by having
verification commands that actually ran and passed on a machine with the
toolchain installed.

    verified   every eval task has a verify command, all executed ones passed,
               and the starter ships enough source to be a real application
    partial    some tasks executed and passed, others are still undefined
    pending    every task defines a real command, but the toolchain needed to
               run it is absent on this machine (Go, Rust, Bun, Elixir, Ruby).
               CI with that toolchain installed will execute them.
    scaffold   no task defines a verify command, so nothing can be executed
    failing    a structural gate or an executed task failed

Run `python evals/runner.py` first; this reads what that run recorded.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import sys
from pathlib import Path

from build_chrome import footer_html, nav_html  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "evals" / "results"
JSON_OUT = REPO_ROOT / "status.json"
HTML_OUT = REPO_ROOT / "status" / "index.html"
README = REPO_ROOT / "README.md"

README_BEGIN = "<!-- BEGIN GENERATED: kit-status -->"
README_END = "<!-- END GENERATED: kit-status -->"

SITE = "https://techtalks.itsumarfarooq.com"

#: A starter below this many lines of source is a scaffold, not an application.
REAL_STARTER_LOC = 250

LABELS = {
    "verified": ("Verified", "bg-[#1F7A4D] text-white"),
    "partial": ("Partially verified", "bg-[#E85D26] text-white"),
    "pending": ("Pending toolchain", "bg-[#FFF1E8] dark:bg-[#2A2E2A] text-[#8A4A28] dark:text-[#C9A68E]"),
    "scaffold": ("Scaffold", "bg-[#FDE3D2] dark:bg-[#4A2A18] text-[#A3450F] dark:text-[#F5BE9B]"),
    "failing": ("Failing", "bg-[#FBEAE4] dark:bg-[#3A201A] text-[#B23B12] dark:text-[#F0A389]"),
}


def classify(metrics: dict) -> str:
    gates = metrics.get("gates", {})
    tasks = metrics.get("task_verification", {})
    starter = metrics.get("starter", {})

    gates_ok = all(
        gates.get(k, False)
        for k in ("manifest_valid", "transpiler_zero_drift", "dialects_complete", "secret_leak_free")
    )
    if not gates_ok or tasks.get("failed", 0) > 0:
        return "failing"

    passed = tasks.get("passed", 0)
    total = tasks.get("total", 0)
    undefined = tasks.get("not_executed", 0)
    skipped = tasks.get("skipped", 0)

    if passed and undefined == 0 and starter.get("source_loc", 0) >= REAL_STARTER_LOC:
        return "verified"
    if passed:
        return "partial"
    # Every task has a real command; none could run here for lack of a
    # toolchain. That is materially better than having no commands at all.
    if total and skipped == total:
        return "pending"
    return "scaffold"


def collect() -> dict:
    kits = []
    for path in sorted(RESULTS_DIR.glob("*_metrics.json")):
        metrics = json.loads(path.read_text(encoding="utf-8"))
        tasks = metrics.get("task_verification", {})
        kits.append({
            "slug": metrics["kit_slug"],
            "maturity": classify(metrics),
            "context_tokens": metrics.get("context_cost", {}).get("context_tokens", 0),
            "tier": metrics.get("context_cost", {}).get("efficiency_tier", "?"),
            "starter_files": metrics.get("starter", {}).get("files", 0),
            "starter_loc": metrics.get("starter", {}).get("source_loc", 0),
            "tasks_total": tasks.get("total", 0),
            "tasks_passed": tasks.get("passed", 0),
            "tasks_failed": tasks.get("failed", 0),
            "tasks_skipped": tasks.get("skipped", 0),
            "tasks_undefined": tasks.get("not_executed", 0),
            "gates": metrics.get("gates", {}),
        })

    order = {"verified": 0, "partial": 1, "pending": 2, "scaffold": 3, "failing": 4}
    kits.sort(key=lambda k: (order[k["maturity"]], -k["tasks_passed"], k["slug"]))

    counts = {level: sum(1 for k in kits if k["maturity"] == level) for level in LABELS}
    return {
        "generated_at": dt.date.today().isoformat(),
        "kit_count": len(kits),
        "counts": counts,
        "tasks": {
            "total": sum(k["tasks_total"] for k in kits),
            "passed": sum(k["tasks_passed"] for k in kits),
            "failed": sum(k["tasks_failed"] for k in kits),
            "skipped": sum(k["tasks_skipped"] for k in kits),
            "undefined": sum(k["tasks_undefined"] for k in kits),
        },
        "thresholds": {
            "real_starter_loc": REAL_STARTER_LOC,
            "note": "Maturity is derived from executed eval results, not declared in kit.yaml.",
        },
        "kits": kits,
    }


def render_html(data: dict) -> str:
    e = html.escape
    counts, tasks = data["counts"], data["tasks"]

    rows = []
    for kit in data["kits"]:
        label, tone = LABELS[kit["maturity"]]
        if kit["tasks_total"]:
            task_cell = (
                f'{kit["tasks_passed"]}/{kit["tasks_total"]} passed'
                + (f', {kit["tasks_undefined"]} undefined' if kit["tasks_undefined"] else "")
            )
        else:
            task_cell = "&mdash;"
        rows.append(
            '<tr class="border-t border-[#E6E6DF] dark:border-[#2A2E2A] hover:bg-[#FAFAF7] dark:hover:bg-[#161918] transition-colors">'
            f'<th scope="row" class="px-3 py-2 text-left font-medium whitespace-nowrap">'
            f'<a href="{SITE}/kits/{e(kit["slug"])}/" class="hover:text-[#E85D26] transition-colors">{e(kit["slug"])}</a></th>'
            f'<td class="px-3 py-2"><span class="inline-flex rounded-[5px] px-2 py-0.5 font-mono text-[11px] {tone}">{label}</span></td>'
            f'<td class="px-3 py-2 text-center font-mono text-[12px]">{kit["context_tokens"]:,}</td>'
            f'<td class="px-3 py-2 text-center font-mono text-[12px]">{e(kit["tier"])}</td>'
            f'<td class="px-3 py-2 text-center font-mono text-[12px]">{kit["starter_loc"]:,}</td>'
            f'<td class="px-3 py-2 text-center font-mono text-[12px] text-[#5C6058] dark:text-[#A8ACA0]">{task_cell}</td>'
            "</tr>"
        )

    def stat(value, caption, accent=""):
        return (
            '<div class="rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#141716] px-4 py-3">'
            f'<div class="font-mono text-[22px] font-bold {accent}">{value}</div>'
            f'<div class="mt-0.5 font-mono text-[11px] uppercase tracking-wider text-[#5C6058] dark:text-[#A8ACA0]">{caption}</div></div>'
        )

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kit Status Board &bull; TechTalks Stack Kits</title>
  <meta name="description"
    content="Honest maturity status for all {data['kit_count']} TechTalks Stack Kits, derived from executed verification runs rather than self-declared.">
  <link rel="canonical" href="{SITE}/status/">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/status/">
  <meta property="og:title" content="Kit Status Board &bull; TechTalks Stack Kits">
  <meta property="og:description"
    content="Which kits are actually verified, which are scaffolds. Derived from executed eval runs.">
  <link rel="icon" type="image/svg+xml"
    href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23E85D26'><path d='M13 2L3 14h9l-1 8 10-12h-9l1-8z'/></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css">
</head>

<body class="bg-white dark:bg-[#0F1110] text-[#12140F] dark:text-[#F2F2EC] selection:bg-[#FFF1E8] selection:text-[#E85D26] min-h-screen flex flex-col font-sans transition-colors">

  {nav_html('status')}

  <main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">

    <h1 class="text-[34px] sm:text-[42px] font-extrabold tracking-[-0.03em] leading-[1.1]">Kit status board</h1>
    <p class="mt-4 max-w-3xl text-[16.5px] leading-relaxed text-[#5C6058] dark:text-[#A8ACA0]">
      What each kit has actually been proven to do. Maturity here is derived from executed verification
      runs recorded in <code class="font-mono text-[14px] text-[#E85D26]">evals/results/</code> &mdash;
      a kit cannot declare itself verified in its own manifest.
    </p>

    <div class="mt-8 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
      {stat(counts['verified'], 'verified', 'text-[#1F7A4D] dark:text-[#6EE7A8]')}
      {stat(counts['partial'], 'partial')}
      {stat(counts['pending'], 'pending toolchain')}
      {stat(counts['scaffold'], 'scaffold')}
      {stat(f"{tasks['passed']}/{tasks['total']}", 'tasks executed &amp; passed')}
    </div>

    <section class="mt-10 rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-[#FAFAF7] dark:bg-[#141716] p-5">
      <h2 class="text-[15px] font-semibold">How to read this</h2>
      <ul class="mt-3 space-y-2 text-[14px] leading-relaxed text-[#5C6058] dark:text-[#A8ACA0]">
        <li><strong class="text-[#12140F] dark:text-[#F2F2EC]">Verified</strong> &mdash; every eval task defines a real command, the executed ones passed, and the starter ships at least {data['thresholds']['real_starter_loc']} lines of source.</li>
        <li><strong class="text-[#12140F] dark:text-[#F2F2EC]">Partial</strong> &mdash; some tasks ran and passed; others have no verify command yet.</li>
        <li><strong class="text-[#12140F] dark:text-[#F2F2EC]">Pending toolchain</strong> &mdash; every task defines a real verify command, but the language toolchain (Go, Rust, Bun, Elixir, Ruby) is not installed on the machine that produced this board. CI with it installed executes them.</li>
        <li><strong class="text-[#12140F] dark:text-[#F2F2EC]">Scaffold</strong> &mdash; rules, security manifest and structure are complete and drift-checked, but nothing has been executed. Useful as an agent context pack; not yet a runnable application.</li>
        <li><strong class="text-[#12140F] dark:text-[#F2F2EC]">Context tokens</strong> &mdash; measured with tiktoken <code class="font-mono text-[12.5px]">cl100k_base</code>: what an agent must read before writing code. Tokens to <em>complete</em> a build are not measured, because that needs a live agent run.</li>
      </ul>
    </section>

    <div class="mt-8 overflow-x-auto rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A]">
      <table class="w-full text-[13px] border-collapse">
        <caption class="sr-only">Per-kit maturity, context cost and verification status</caption>
        <thead class="bg-[#FAFAF7] dark:bg-[#161918]">
          <tr>
            <th scope="col" class="px-3 py-3 text-left font-mono text-[11px] font-semibold text-[#5C6058] dark:text-[#A8ACA0]">Kit</th>
            <th scope="col" class="px-3 py-3 text-left font-mono text-[11px] font-semibold text-[#5C6058] dark:text-[#A8ACA0]">Maturity</th>
            <th scope="col" class="px-3 py-3 text-center font-mono text-[11px] font-semibold text-[#5C6058] dark:text-[#A8ACA0]">Context</th>
            <th scope="col" class="px-3 py-3 text-center font-mono text-[11px] font-semibold text-[#5C6058] dark:text-[#A8ACA0]">Tier</th>
            <th scope="col" class="px-3 py-3 text-center font-mono text-[11px] font-semibold text-[#5C6058] dark:text-[#A8ACA0]">Starter LOC</th>
            <th scope="col" class="px-3 py-3 text-center font-mono text-[11px] font-semibold text-[#5C6058] dark:text-[#A8ACA0]">Verification</th>
          </tr>
        </thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </div>

    <section class="mt-10 rounded-[10px] border border-[#E6E6DF] dark:border-[#2A2E2A] bg-white dark:bg-[#141716] p-6">
      <h2 class="text-[18px] font-bold tracking-[-0.02em]">Reproduce this</h2>
      <pre class="mt-4 overflow-x-auto rounded-[8px] bg-[#12140F] dark:bg-[#0B0D0C] p-4 font-mono text-[12.5px] text-[#E6E6DF]"><code>pip install -r requirements.txt
python evals/runner.py              # executes every task that defines a verify command
python tools/build_status_board.py  # regenerates this page from those results</code></pre>
      <p class="mt-3 text-[13.5px] text-[#5C6058] dark:text-[#A8ACA0]">
        Machine-readable: <a href="{SITE}/status.json" class="text-[#E85D26] hover:underline">status.json</a>
      </p>
    </section>

  </main>

  {footer_html()}

  <script src="/assets/js/main.js"></script>
</body>

</html>
"""


def render_readme_table(data: dict) -> str:
    """Markdown kit table for the generated README section."""
    badge = {"verified": "**Verified**", "partial": "Partial",
             "pending": "Pending toolchain", "scaffold": "Scaffold", "failing": "FAILING"}
    rows = [
        "| Kit | Maturity | Context tokens | Tier | Starter LOC | Verification |",
        "|---|---|---:|:---:|---:|---|",
    ]
    for kit in data["kits"]:
        verification = (
            f'{kit["tasks_passed"]}/{kit["tasks_total"]} passed'
            if kit["tasks_passed"] else
            (f'{kit["tasks_undefined"]} tasks undefined' if kit["tasks_total"] else "—")
        )
        rows.append(
            f'| [`{kit["slug"]}`](kits/{kit["slug"]}/) | {badge[kit["maturity"]]} '
            f'| {kit["context_tokens"]:,} | {kit["tier"]} | {kit["starter_loc"]:,} | {verification} |'
        )
    c, t = data["counts"], data["tasks"]
    return (
        f"<!-- Generated by tools/build_status_board.py on {data['generated_at']}. Do not edit by hand. -->\n\n"
        f"**{data['kit_count']} kits** — {c['verified']} verified, {c['partial']} partial, "
        f"{c['pending']} pending toolchain, {c['scaffold']} scaffold, {c['failing']} failing. "
        f"**{t['passed']}/{t['total']}** eval tasks execute and pass.\n\n"
        "Context tokens are what an agent must read before writing code, measured with tiktoken\n"
        "`cl100k_base`. Tiers derive from that number. Starter LOC excludes installed dependencies.\n\n"
        + "\n".join(rows)
    )


def update_readme(data: dict) -> bool:
    """Replace the generated block in README.md. Returns True if it changed."""
    if not README.exists():
        return False
    text = README.read_text(encoding="utf-8")
    if README_BEGIN not in text or README_END not in text:
        return False
    head, rest = text.split(README_BEGIN, 1)
    _old, tail = rest.split(README_END, 1)
    updated = f"{head}{README_BEGIN}\n{render_readme_table(data)}\n{README_END}{tail}"
    if updated == text:
        return False
    README.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if outputs are stale")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="print a GitHub Actions step summary to stdout and write nothing",
    )
    args = parser.parse_args()

    if not RESULTS_DIR.exists() or not any(RESULTS_DIR.glob("*_metrics.json")):
        print("no eval results found — run: python evals/runner.py")
        return 1

    data = collect()

    if args.summary:
        c, t = data["counts"], data["tasks"]
        print("## Kit verification\n")
        print(f"**{data['kit_count']} kits** — {c['verified']} verified, "
              f"{c['partial']} partial, {c['pending']} pending toolchain, "
              f"{c['scaffold']} scaffold, {c['failing']} failing\n")
        print(f"**{t['passed']}/{t['total']}** eval tasks executed and passed"
              f" · {t['skipped']} skipped · {t['undefined']} undefined\n")
        print("| Kit | Maturity | Context | Tasks |")
        print("|---|---|---:|---|")
        for kit in data["kits"]:
            print(f"| `{kit['slug']}` | {kit['maturity']} | {kit['context_tokens']:,} "
                  f"| {kit['tasks_passed']}/{kit['tasks_total']} |")
        return 0

    json_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    html_text = render_html(data)

    if args.check:
        stale = [
            str(p.relative_to(REPO_ROOT))
            for p, expected in ((JSON_OUT, json_text), (HTML_OUT, html_text))
            if not p.exists() or p.read_text(encoding="utf-8") != expected
        ]
        readme_text = README.read_text(encoding="utf-8") if README.exists() else ""
        if README_BEGIN in readme_text:
            expected_block = README_BEGIN + "\n" + render_readme_table(data) + "\n" + README_END
            _head, rest = readme_text.split(README_BEGIN, 1)
            body, _tail = rest.split(README_END, 1)
            if README_BEGIN + body + README_END != expected_block:
                stale.append("README.md (kit-status section)")
        if stale:
            print("FAIL — status board out of date: " + ", ".join(stale))
            print("Regenerate with: python tools/build_status_board.py")
            return 1
        print("PASS — status board is current")
        return 0

    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json_text, encoding="utf-8")
    HTML_OUT.write_text(html_text, encoding="utf-8")
    if update_readme(data):
        print("updated README.md kit-status section")

    c = data["counts"]
    print(f"wrote status.json and status/index.html")
    print(f"\n{data['kit_count']} kits: {c['verified']} verified, {c['partial']} partial, "
          f"{c['pending']} pending toolchain, {c['scaffold']} scaffold, {c['failing']} failing")
    print(f"tasks: {data['tasks']['passed']}/{data['tasks']['total']} executed and passed, "
          f"{data['tasks']['undefined']} still undefined")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
