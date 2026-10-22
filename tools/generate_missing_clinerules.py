import os

base = "kits"
kits = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]

for kit in kits:
    kit_dir = os.path.join(base, kit)
    clinerules_p = os.path.join(kit_dir, ".clinerules")
    if not os.path.exists(clinerules_p):
        agents_p = os.path.join(kit_dir, "AGENTS.md")
        overview = f"# Assistant Guidelines for {kit.replace('-', ' ').title()} Stack Kit\n\n"
        if os.path.exists(agents_p):
            with open(agents_p, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # Extract first 30 lines of useful instructions
            overview += "".join(lines[:35])
        else:
            overview += f"Follow all repository rules in rules/source/*.md.\n"
            
        with open(clinerules_p, "w", encoding="utf-8") as f:
            f.write(overview)
        print(f"Generated missing .clinerules for {kit}")

print("All kits verified for .clinerules!")
