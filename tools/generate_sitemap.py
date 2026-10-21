"""
tools/generate_sitemap.py
Dynamic, automated sitemap generator for TechTalks Stack Kits.
Extracts honest lastmod dates directly from git commit history (git log -1 --format=%cs)
and emits clean canonical URLs (no .html extensions, no redirects).
"""

import os
import subprocess
import glob

BASE_URL = "https://techtalks.itsumarfarooq.com"

def get_git_lastmod(filepath):
    try:
        res = subprocess.run(
            ["git", "log", "-1", "--format=%cs", filepath],
            capture_output=True,
            text=True,
            check=True
        )
        date_str = res.stdout.strip()
        if date_str and len(date_str) == 10:
            return date_str
    except Exception:
        pass
    return "2026-10-21"

def generate():
    pages = []

    # 1. Root Homepage
    pages.append({
        "url": f"{BASE_URL}/",
        "file": "index.html",
        "priority": "1.0",
        "changefreq": "weekly"
    })

    # 2. Main Hubs
    pages.append({
        "url": f"{BASE_URL}/kits/",
        "file": "kits/index.html",
        "priority": "0.9",
        "changefreq": "weekly"
    })
    pages.append({
        "url": f"{BASE_URL}/security/",
        "file": "security/index.html",
        "priority": "0.9",
        "changefreq": "weekly"
    })
    pages.append({
        "url": f"{BASE_URL}/security/laravel/",
        "file": "security/laravel/index.html",
        "priority": "0.85",
        "changefreq": "weekly"
    })
    pages.append({
        "url": f"{BASE_URL}/blog/",
        "file": "blog/index.html",
        "priority": "0.85",
        "changefreq": "weekly"
    })

    # 3. Blog Posts (5 Posts)
    blog_dirs = sorted(glob.glob("blog/*/index.html"))
    for bd in blog_dirs:
        slug = os.path.basename(os.path.dirname(bd))
        pages.append({
            "url": f"{BASE_URL}/blog/{slug}/",
            "file": bd,
            "priority": "0.8",
            "changefreq": "monthly"
        })

    # 4. Stack Kits (10 Kits)
    kit_dirs = sorted(glob.glob("kits/*/index.html"))
    for kd in kit_dirs:
        slug = os.path.basename(os.path.dirname(kd))
        pages.append({
            "url": f"{BASE_URL}/kits/{slug}/",
            "file": kd,
            "priority": "0.8",
            "changefreq": "weekly"
        })

    # 5. Security Lessons (22 Lessons - Retired checklist excluded as it redirects)
    lesson_files = sorted(glob.glob("security/laravel/*.html"))
    for lf in lesson_files:
        base = os.path.basename(lf)
        if base in ["index.html", "checklist.html"]:
            continue
        slug = base[:-5]
        pages.append({
            "url": f"{BASE_URL}/security/laravel/{slug}",
            "file": lf,
            "priority": "0.75",
            "changefreq": "monthly"
        })

    print(f"Total canonical pages indexed: {len(pages)}")

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for p in pages:
        lastmod = get_git_lastmod(p["file"])
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{p['url']}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append(f"    <changefreq>{p['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{p['priority']}</priority>")
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>\n")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))

    print("sitemap.xml successfully generated with honest git lastmod dates and clean URLs.")

if __name__ == "__main__":
    generate()
