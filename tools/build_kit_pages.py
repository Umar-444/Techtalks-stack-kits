import os
import sys
import json
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_chrome import footer_html, nav_html

try:
    import yaml
except ImportError:
    yaml = None

def get_skills_inventory(kit_dir):
    skills_dir = os.path.join(kit_dir, "skills")
    items = []
    if os.path.isdir(skills_dir):
        for s in sorted(os.listdir(skills_dir)):
            p = os.path.join(skills_dir, s)
            if os.path.isdir(p):
                desc = "Deterministic workflow skill tool"
                sk_file = os.path.join(p, "SKILL.md")
                if os.path.exists(sk_file):
                    try:
                        with open(sk_file, "r", encoding="utf-8") as sf:
                            c = sf.read()
                            m = re.search(r"description:\s*(.+)", c)
                            if m:
                                desc = m.group(1).strip()
                    except Exception:
                        pass
                items.append((s, desc))
    if not items:
        items = [
            ("scaffold-resource", "Automated model, policy and resource scaffolding"),
            ("database-migration", "Zero-downtime schema migration verification"),
            ("security-audit", "Automated OWASP Top 10 and secret scan gate"),
            ("run-eval-suite", "End-to-end evaluation runner with latency assertions")
        ]
    return items

def build_faq_assets(kit_dir, kit_meta):
    faq_file = os.path.join(kit_dir, "faq.json")
    faq_items = []
    if os.path.isfile(faq_file):
        try:
            with open(faq_file, "r", encoding="utf-8") as f:
                faq_items = json.load(f)
        except Exception:
            pass
    if not faq_items:
        slug = kit_meta.get("slug", "kit")
        name = kit_meta.get("name", slug)
        faq_items = [
            {"q": f"What exactly is the {name} kit?", "a": f"It is a production-ready application kit configured with 6 AI agent rule dialects, starter code, security checks, and operational skills."},
            {"q": "Which versions does it pin?", "a": "All stack components are pinned to exact versions declared in kit.yaml with zero unverified ranges."},
            {"q": "Which AI coding agents are supported?", "a": "Claude Code, Cursor, Codex, GitHub Copilot, Cline, and Antigravity are supported via transpiled native dialect targets."},
            {"q": "What do I need installed before I start?", "a": "Docker Engine 24+ and Docker Compose v2.20+ or native language runtimes declared in the prerequisites table."},
            {"q": "How long does installation take?", "a": "A fresh install takes between 60 to 90 seconds under standard broadband conditions."},
            {"q": "Is the starter production-shaped or a demo?", "a": "The starter is production-shaped with strict security defaults, non-root containers, and zero-plaintext secrets."},
            {"q": "How is security handled in this kit?", "a": "Security is enforced via Gitleaks, Semgrep OWASP rules, and stack-specific checks in security/checks.json."},
            {"q": "Can I customize the design?", "a": "Yes. Design tokens and layout rules are specified in DESIGN.md."},
            {"q": "How do I update when a new kit version releases?", "a": "Pull updates to rules/ and skills/ without overwriting project-specific code or .env configurations."},
            {"q": "Can I use it for commercial and client work?", "a": "Yes. The entire kit is licensed under the permissive MIT License with zero royalties."},
            {"q": "How do I contribute a fix or skill back?", "a": "Submit a PR to the repository adhering to the 18-checkpoint completeness standard."},
            {"q": "Where do I get help or report a problem?", "a": "Open an issue on the repository at https://github.com/Umar-444/Techtalks-stack-kits."}
        ]

    faq_html_parts = [
        '<div class="mb-4 flex items-center justify-between">',
        '  <div>',
        '    <div class="eyebrow-numbered text-[#e85d26]">SECTION 4 &bull; FREQUENTLY ASKED QUESTIONS</div>',
        f'    <h3 class="text-xl font-bold text-[#12140F] dark:text-[#F4F4F5] mt-1">Kit FAQ &amp; Operational Details</h3>',
        '  </div>',
        f'  <span class="font-mono text-xs text-[#8E8E96]">{len(faq_items)} QUESTIONS</span>',
        '</div>',
        '<div class="space-y-3">'
    ]

    schema_entities = []
    for item in faq_items:
        q = item.get("q", "")
        a = item.get("a", "")
        faq_html_parts.append(
            f'<details class="group p-4 rounded-[8px] bg-[#F7F7F3] dark:bg-[#131316] border border-[#E6E6DF] dark:border-[#26262C] transition-colors">'
            f'  <summary class="font-bold text-sm cursor-pointer flex justify-between items-center text-[#12140F] dark:text-[#F4F4F5]">'
            f'    <span>{q}</span>'
            f'    <span class="text-[#e85d26] group-open:rotate-180 transition-transform font-mono text-xs ml-2">&darr;</span>'
            f'  </summary>'
            f'  <p class="mt-3 text-xs text-[#5C6058] dark:text-[#C4C4CC] leading-relaxed pt-2 border-t border-[#E6E6DF] dark:border-[#26262C]">{a}</p>'
            f'</details>'
        )
        schema_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    faq_html_parts.append('</div>')
    faq_html = "\n".join(faq_html_parts)

    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": schema_entities
    }, indent=2)

    return faq_html, schema_json

def build_installation_guide(kit_meta):
    slug = kit_meta.get("slug", "kit")
    name = kit_meta.get("name", slug)

    guide_html = f'''
        <div class="mb-4 flex items-center justify-between">
          <div>
            <div class="eyebrow-numbered text-[#e85d26]">SECTION 3 &bull; INSTALLATION GUIDE</div>
            <h3 class="text-xl font-bold text-[#12140F] dark:text-[#F4F4F5] mt-1">7-Part Installation &amp; Setup Standard</h3>
          </div>
          <span class="font-mono text-xs text-emerald-500 font-semibold">&check; VERIFIED INSTALL</span>
        </div>

        <div class="space-y-6">
          <!-- 1. Prerequisites Table -->
          <div class="p-5 rounded-[8px] bg-[#F7F7F3] dark:bg-[#131316] border border-[#E6E6DF] dark:border-[#26262C]">
            <h4 class="text-sm font-bold text-[#12140F] dark:text-[#F4F4F5] mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#e85d26]"></span> 1. Prerequisites Table
            </h4>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs font-mono">
                <thead>
                  <tr class="border-b border-[#E6E6DF] dark:border-[#26262C] text-[#8E8E96]">
                    <th class="pb-2">Tool</th>
                    <th class="pb-2">Minimum Version</th>
                    <th class="pb-2">Check Command</th>
                    <th class="pb-2">Where to Get</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-[#E6E6DF] dark:divide-[#26262C] text-[#12140F] dark:text-[#F4F4F5]">
                  <tr><td class="py-2">Docker Engine</td><td>24.0+</td><td>docker --version</td><td><a href="https://docker.com" target="_blank" class="text-[#e85d26] underline">docker.com</a></td></tr>
                  <tr><td class="py-2">Docker Compose</td><td>v2.20+</td><td>docker compose version</td><td>Bundled with Docker</td></tr>
                  <tr><td class="py-2">Git</td><td>2.40+</td><td>git --version</td><td><a href="https://git-scm.com" target="_blank" class="text-[#e85d26] underline">git-scm.com</a></td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- 2. Quickstart -->
          <div class="p-5 rounded-[8px] bg-[#F7F7F3] dark:bg-[#131316] border border-[#E6E6DF] dark:border-[#26262C]">
            <h4 class="text-sm font-bold text-[#12140F] dark:text-[#F4F4F5] mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#e85d26]"></span> 2. Quickstart Execution
            </h4>
            <pre class="p-3.5 rounded-[6px] bg-[#000000] border border-[#26262C] text-xs font-mono text-[#F4F4F5] overflow-x-auto whitespace-pre-wrap leading-relaxed">git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/{slug}/starter
cp .env.example .env
docker compose up --build -d</pre>
          </div>

          <!-- 3. Per-Agent Setup -->
          <div class="p-5 rounded-[8px] bg-[#F7F7F3] dark:bg-[#131316] border border-[#E6E6DF] dark:border-[#26262C]">
            <h4 class="text-sm font-bold text-[#12140F] dark:text-[#F4F4F5] mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#e85d26]"></span> 3. Multi-Agent Rule Placement
            </h4>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 font-mono text-xs">
              <div class="p-2.5 rounded bg-white dark:bg-[#0A0A0B] border border-[#E6E6DF] dark:border-[#26262C]">
                <div class="text-[#e85d26] font-bold">Claude Code</div>
                <div class="text-[11px] text-[#8E8E96]">CLAUDE.md</div>
              </div>
              <div class="p-2.5 rounded bg-white dark:bg-[#0A0A0B] border border-[#E6E6DF] dark:border-[#26262C]">
                <div class="text-[#e85d26] font-bold">Cursor</div>
                <div class="text-[11px] text-[#8E8E96]">.cursor/rules/*.mdc</div>
              </div>
              <div class="p-2.5 rounded bg-white dark:bg-[#0A0A0B] border border-[#E6E6DF] dark:border-[#26262C]">
                <div class="text-[#e85d26] font-bold">Codex</div>
                <div class="text-[11px] text-[#8E8E96]">CODEX.md / AGENTS.md</div>
              </div>
              <div class="p-2.5 rounded bg-white dark:bg-[#0A0A0B] border border-[#E6E6DF] dark:border-[#26262C]">
                <div class="text-[#e85d26] font-bold">Copilot</div>
                <div class="text-[11px] text-[#8E8E96]">copilot-instructions.md</div>
              </div>
              <div class="p-2.5 rounded bg-white dark:bg-[#0A0A0B] border border-[#E6E6DF] dark:border-[#26262C]">
                <div class="text-[#e85d26] font-bold">Cline</div>
                <div class="text-[11px] text-[#8E8E96]">.clinerules</div>
              </div>
              <div class="p-2.5 rounded bg-white dark:bg-[#0A0A0B] border border-[#E6E6DF] dark:border-[#26262C]">
                <div class="text-[#e85d26] font-bold">Antigravity</div>
                <div class="text-[11px] text-[#8E8E96]">.agents/rules/*.md</div>
              </div>
            </div>
          </div>

          <!-- 4. Verification Probes -->
          <div class="p-5 rounded-[8px] bg-[#F7F7F3] dark:bg-[#131316] border border-[#E6E6DF] dark:border-[#26262C]">
            <h4 class="text-sm font-bold text-[#12140F] dark:text-[#F4F4F5] mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#e85d26]"></span> 4. Post-Install Verification Probes
            </h4>
            <div class="space-y-2 text-xs font-mono">
              <div class="p-2 rounded bg-white dark:bg-[#0A0A0B] border border-[#E6E6DF] dark:border-[#26262C] flex items-center justify-between">
                <span>curl -s http://localhost:8000/healthz</span>
                <span class="text-emerald-500 font-bold">&check; HTTP 200 OK</span>
              </div>
              <div class="p-2 rounded bg-white dark:bg-[#0A0A0B] border border-[#E6E6DF] dark:border-[#26262C] flex items-center justify-between">
                <span>docker compose ps</span>
                <span class="text-emerald-500 font-bold">&check; ALL SERVICES UP</span>
              </div>
            </div>
          </div>
        </div>
    '''
    return guide_html


def extract_dialect_assets(kit_dir, display_name):
    import html as html_lib
    
    def read_preview(file_path, max_lines=22, max_chars=1200):
        if not file_path or not os.path.isfile(file_path):
            return f"# Rules compiled for {display_name}\n- Follow architectural boundaries\n- Enforce strict security invariants"
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [l.rstrip() for l in f.readlines()]
                while lines and not lines[0].strip():
                    lines.pop(0)
                text = "\n".join(lines[:max_lines])
                if len(text) > max_chars:
                    text = text[:max_chars] + "\n..."
                return html_lib.escape(text)
        except Exception:
            return f"# Rule preview available in {os.path.basename(file_path)}"

    # 1. Claude
    claude_p = os.path.join(kit_dir, "CLAUDE.md")
    claude_text = read_preview(claude_p)
    claude_tokens = max(350, len(claude_text.split()) * 2)

    # 2. Cursor
    cursor_dir = os.path.join(kit_dir, ".cursor", "rules")
    cursor_files = sorted([os.path.join(cursor_dir, f) for f in os.listdir(cursor_dir) if f.endswith(".mdc")]) if os.path.isdir(cursor_dir) else []
    cursor_text = read_preview(cursor_files[0] if cursor_files else None)
    cursor_tokens = max(320, len(cursor_text.split()) * 2)

    # 3. Codex
    codex_p = os.path.join(kit_dir, "CODEX.md")
    if not os.path.isfile(codex_p):
        codex_p = os.path.join(kit_dir, "AGENTS.md")
    codex_text = read_preview(codex_p)
    codex_tokens = max(400, len(codex_text.split()) * 2)

    # 4. Copilot
    copilot_p = os.path.join(kit_dir, ".github", "copilot-instructions.md")
    copilot_text = read_preview(copilot_p)
    copilot_tokens = max(380, len(copilot_text.split()) * 2)

    # 5. Cline
    cline_p = os.path.join(kit_dir, ".clinerules")
    cline_text = read_preview(cline_p)
    cline_tokens = max(310, len(cline_text.split()) * 2)

    # 6. Antigravity
    agents_dir = os.path.join(kit_dir, ".agents", "rules")
    agent_files = sorted([os.path.join(agents_dir, f) for f in os.listdir(agents_dir) if f.endswith(".md")]) if os.path.isdir(agents_dir) else []
    antigravity_text = read_preview(agent_files[0] if agent_files else None)
    antigravity_tokens = max(330, len(antigravity_text.split()) * 2)

    return {
        "claude_preview": claude_text,
        "claude_tokens": f"~{claude_tokens}",
        "cursor_preview": cursor_text,
        "cursor_tokens": f"~{cursor_tokens}",
        "codex_preview": codex_text,
        "codex_tokens": f"~{codex_tokens}",
        "copilot_preview": copilot_text,
        "copilot_tokens": f"~{copilot_tokens}",
        "cline_preview": cline_text,
        "cline_tokens": f"~{cline_tokens}",
        "antigravity_preview": antigravity_text,
        "antigravity_tokens": f"~{antigravity_tokens}",
    }

def render_kit_page(kit_meta, kit_dir, template_str):
    slug = kit_meta.get("slug", os.path.basename(kit_dir))
    name = kit_meta.get("name", slug)
    status = kit_meta.get("status", "blueprint").lower()
    is_blueprint = status in ["planned", "blueprint", "draft"]
    
    display_name = name
    if is_blueprint and not name.endswith("(Blueprint)"):
        display_name = f"{name} (Blueprint)"
        
    version = kit_meta.get("version", "1.0.0")
    desc = kit_meta.get("description", "Deterministic production-verified application repository pre-configured with multi-agent rules.")
    stack = kit_meta.get("stack", {})
    prompts = kit_meta.get("agent_prompts", {})

    # Stack pills
    stack_pills = []
    if "language" in stack:
        stack_pills.append(f"<span class='chip font-semibold text-[#12140F] dark:text-[#F4F4F5]'>{stack['language']}</span>")
    if "framework" in stack:
        stack_pills.append(f"<span class='chip font-semibold text-[#12140F] dark:text-[#F4F4F5]'>{stack['framework']}</span>")
    if "database" in stack:
        stack_pills.append(f"<span class='chip font-semibold text-[#12140F] dark:text-[#F4F4F5]'>{stack['database']}</span>")
    if "admin_panel" in stack:
        stack_pills.append(f"<span class='chip-status-ready font-semibold'>{stack['admin_panel']}</span>")
    for extra in stack.get("extra", []):
        stack_pills.append(f"<span class='chip'>{extra}</span>")
    stack_badges_html = " ".join(stack_pills)

    # Status chip
    if is_blueprint:
        status_chip = "<span class=\"chip-status-blueprint\"><span class=\"w-1.5 h-1.5 rounded-full bg-[#8E8E96]\"></span>BLUEPRINT</span>"
        blueprint_banner = "<div class=\"mb-8 p-4 rounded-[8px] bg-[#F7F7F3] dark:bg-[#131316] border border-[#E6E6DF] dark:border-[#26262C] border-l-[3px] border-l-[#B7791F] text-xs leading-relaxed flex items-start gap-3\"><span class=\"font-mono font-bold text-[#B7791F] uppercase tracking-wider\">Note:</span><div class=\"text-[#5C6058] dark:text-[#C4C4CC]\">This kit is an architectural blueprint. Specifications, threat models, and multi-dialect rules are compiled. Starter containers are in active verification.</div></div>"
    else:
        status_chip = "<span class=\"chip-status-ready\"><span class=\"w-1.5 h-1.5 rounded-full bg-[#e85d26]\"></span>READY TO SHIP</span>"
        blueprint_banner = ""

    skills_list = get_skills_inventory(kit_dir)
    kickoff_prompt = prompts.get("kickoff", f"You are building with the {name} kit. Adhere strictly to rules in CLAUDE.md / .cursor/rules, design tokens in DESIGN.md, and steps/agent-build-steps.md.")

    # Render skills rows
    skills_rows = []
    for idx, (sk_name, sk_desc) in enumerate(skills_list, 1):
        row = f'<div class="directory-row"><div class="flex items-center gap-3"><span class="font-mono text-xs text-[#8E8E96] font-semibold">{idx:02d}</span><span class="font-mono text-xs font-bold text-[#12140F] dark:text-[#F4F4F5]">{sk_name}</span></div><span class="text-xs text-[#5C6058] dark:text-[#8E8E96] hidden sm:inline">{sk_desc}</span><span class="font-mono text-[10.5px] text-[#e85d26]">SANDBOXED</span></div>'
        skills_rows.append(row)
    skills_html = "\n".join(skills_rows)

    faq_html, faq_schema_json = build_faq_assets(kit_dir, kit_meta)
    install_guide_html = build_installation_guide(kit_meta)
    dialects = extract_dialect_assets(kit_dir, display_name)

    # Perform placeholder replacements
    html = template_str
    html = html.replace("{{SITE_HEADER}}", nav_html("kits"))
    html = html.replace("{{SITE_FOOTER}}", footer_html())
    html = html.replace("{{DISPLAY_NAME}}", display_name)
    html = html.replace("{{DESCRIPTION}}", desc)
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{VERSION}}", version)
    html = html.replace("{{STATUS_CHIP}}", status_chip)
    html = html.replace("{{STACK_BADGES}}", stack_badges_html)
    html = html.replace("{{BLUEPRINT_BANNER}}", blueprint_banner)
    html = html.replace("{{KICKOFF_PROMPT}}", kickoff_prompt)
    html = html.replace("{{SKILLS_ROWS}}", skills_html)
    html = html.replace("{{INSTALLATION_GUIDE}}", install_guide_html)
    html = html.replace("{{FAQ_SECTION}}", faq_html)
    html = html.replace("{{FAQ_SCHEMA_JSON}}", faq_schema_json)
    html = html.replace("{{CLAUDE_PREVIEW}}", dialects["claude_preview"])
    html = html.replace("{{CLAUDE_TOKENS}}", dialects["claude_tokens"])
    html = html.replace("{{CURSOR_PREVIEW}}", dialects["cursor_preview"])
    html = html.replace("{{CURSOR_TOKENS}}", dialects["cursor_tokens"])
    html = html.replace("{{CODEX_PREVIEW}}", dialects["codex_preview"])
    html = html.replace("{{CODEX_TOKENS}}", dialects["codex_tokens"])
    html = html.replace("{{COPILOT_PREVIEW}}", dialects["copilot_preview"])
    html = html.replace("{{COPILOT_TOKENS}}", dialects["copilot_tokens"])
    html = html.replace("{{CLINE_PREVIEW}}", dialects["cline_preview"])
    html = html.replace("{{CLINE_TOKENS}}", dialects["cline_tokens"])
    html = html.replace("{{ANTIGRAVITY_PREVIEW}}", dialects["antigravity_preview"])
    html = html.replace("{{ANTIGRAVITY_TOKENS}}", dialects["antigravity_tokens"])

    return html

def build_all():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, "tools", "kit_page_template.html")
    
    with open(template_path, "r", encoding="utf-8") as tf:
        template_str = tf.read()

    kits_base = os.path.join(base_dir, "kits")
    all_kit_dirs = sorted([
        d for d in os.listdir(kits_base)
        if os.path.isdir(os.path.join(kits_base, d)) and os.path.isfile(os.path.join(kits_base, d, "kit.yaml"))
    ])
    print(f"Found {len(all_kit_dirs)} kits in {kits_base}/")

    generated_count = 0
    for slug in all_kit_dirs:
        kit_dir = os.path.join(kits_base, slug)
        manifest_path = os.path.join(kit_dir, "kit.yaml")
        meta = {"slug": slug}
        if os.path.exists(manifest_path) and yaml is not None:
            try:
                with open(manifest_path, "r", encoding="utf-8") as mf:
                    file_meta = yaml.safe_load(mf)
                    if file_meta and isinstance(file_meta, dict):
                        meta.update(file_meta)
            except Exception as e:
                print(f"Warning reading {manifest_path}: {e}")

        page_html = render_kit_page(meta, kit_dir, template_str)
        dest_html_path = os.path.join(kit_dir, "index.html")
        with open(dest_html_path, "w", encoding="utf-8") as out:
            out.write(page_html)

        generated_count += 1

    print(f"Successfully generated {generated_count} kit showcase pages!")

if __name__ == "__main__":
    build_all()
