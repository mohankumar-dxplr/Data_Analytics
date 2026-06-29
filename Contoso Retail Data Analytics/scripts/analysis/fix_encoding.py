"""Replace all non-ASCII Unicode characters in run_all_analyses.py with ASCII safe equivalents."""
path = r"C:\Users\Mohan\Downloads\sample\scripts\analysis\run_all_analyses.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Full character mapping
replacements = {
    # Box drawing
    "\u2550": "=",  # ═
    "\u2551": "|",  # ║
    "\u2554": "+",  # ╔ 
    "\u2557": "+",  # ╗
    "\u255A": "+",  # ╚
    "\u255D": "+",  # ╝
    "\u2500": "-",  # ─
    "\u2502": "|",  # │
    # Arrows
    "\u2192": "->", # →
    # Dashes
    "\u2014": "--", # —
    "\u2013": "-",  # –
    # Quotes
    "\u2018": "'",  # '
    "\u2019": "'",  # '
    "\u201c": '"',  # "
    "\u201d": '"',  # "
    # Other
    "\u2022": "*",  # •
    "\u2026": "...", # …
}

for old, new in replacements.items():
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"  U+{ord(old):04X} x{count} -> {repr(new)}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone. All non-ASCII characters replaced.")
