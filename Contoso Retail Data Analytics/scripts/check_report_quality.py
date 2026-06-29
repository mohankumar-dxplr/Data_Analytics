import re

with open(r'C:\Users\Mohan\Downloads\sample\CLIENT-EXECUTIVE-REPORT.md', 'r') as f:
    text = f.read()

print('=== Leftover Placeholder Markers ===')
for p in ['DOLLAR_SIGN', 'BOLD_START']:
    count = text.count(p)
    print(f'  {p}: {count}')

print('\n=== Image References ===')
imgs = re.findall(r'!\[.*?\]\((.*?)\)', text)
print(f'  Total: {len(imgs)}')
for img in imgs:
    print(f'  {img}')

print('\n=== Section Headers ===')
sections = re.findall(r'^## (.*?)$', text, re.MULTILINE)
for s in sections:
    print(f'  ## {s}')

print('\n=== Table Integrity ===')
# Count table rows (lines starting with |)
lines = text.split('\n')
table_rows = [l for l in lines if l.strip().startswith('|')]
print(f'  Total table rows: {len(table_rows)}')

# Check for empty cells in tables
empty_issues = 0
for i, line in enumerate(lines):
    if line.strip().startswith('|') and '|  |' in line:
        print(f'  EMPTY CELL at L{i+1}: {line.strip()[:80]}')
        empty_issues += 1

print(f'\n  Empty cell issues: {empty_issues}')

# Verify dollar signs on known money columns
# Check Revenue by Category table
print('\n=== Dollar Sign Spot Checks ===')
checks = [
    ('Revenue by Category (Computers)', '$19,301,595'),
    ('Top Products (WWI Desktop)', '$505,450'),
    ('RFM Champions Avg Spend', '$9,525'),
    ('Italy COVID change', '-94.2%'),
    ('Home Appliances COVID change', '-93.9%'),
    ('Year 2019 (no $)', '2019'),
]
for label, expected in checks:
    found = expected in text
    print(f'  {label}: \"{expected}\" {"FOUND" if found else "MISSING!"}')

print('\n=== File Sizes ===')
import os
root_size = os.path.getsize(r'C:\Users\Mohan\Downloads\sample\CLIENT-EXECUTIVE-REPORT.md')
reports_size = os.path.getsize(r'C:\Users\Mohan\Downloads\sample\reports\CLIENT-EXECUTIVE-REPORT.md')
print(f'  Root copy:   {root_size:,} bytes')
print(f'  Reports copy: {reports_size:,} bytes')

print('\nDone.')
