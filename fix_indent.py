"""Fix indentation in dashboard.py"""

# Read the file
with open(r'c:\Users\mdash\OneDrive\Documents\Data-analytics\climate-change-analytics\dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix indentation from line 726 to 1054 (0-indexed: 725 to 1053)
# These lines have 12 spaces when they should have 8 (remove 4 spaces)
fixed_lines = []
for i, line in enumerate(lines):
    line_num = i + 1
    if 726 <= line_num <= 1054:
        # Check if line starts with exactly 12 spaces
        if line.startswith('            ') and not line.startswith('             '):
            # Remove 4 spaces
            fixed_lines.append(line[4:])
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# Write back
with open(r'c:\Users\mdash\OneDrive\Documents\Data-analytics\climate-change-analytics\dashboard.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("✅ Fixed indentation in dashboard.py")
