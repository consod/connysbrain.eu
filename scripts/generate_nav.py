import re
from pathlib import Path


def extract_title_from_frontmatter(file_path):
    """Extract title from frontmatter if present, otherwise return None"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for YAML frontmatter (between --- lines)
        frontmatter_match = re.search(r'^---\s*\n(.*?)^---\s*\n', content, re.DOTALL | re.MULTILINE)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            # Look for title in frontmatter
            title_match = re.search(r'^\s*title:\s*"?(.*?)"?\s*$|\s*title:\s*"(.*?)"', frontmatter, re.MULTILINE)
            if title_match:
                # Return first non-empty group
                return title_match.group(1) or title_match.group(2)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return None

def generate_nav_text(docs_dir="docs"):
    """Generate well-formatted navigation structure with proper spacing and alignment."""
    docs_path = Path(docs_dir)
    nav_lines = ["nav = ["]

    category_names = {
        "eat_and_drink": "Eat & Drink",
        "entertainment": "Entertainment",
        "guides": "Guides",
        "programming": "Programming"
    }

    for category_dir in docs_path.iterdir():
        if category_dir.is_dir():
            category_key = category_dir.name
            category_name = category_names.get(category_key, category_key.replace('_', ' ').title())

            # Process directory structure
            content = process_directory_text(category_dir, docs_path)
            if content:
                nav_lines.append(f'  {{"{category_name}" = [{content}  ]}},')

    # Remove trailing comma from last item
    if nav_lines[-1].endswith(','):
        nav_lines[-1] = nav_lines[-1][:-1]

    nav_lines.append("]")
    return "\n".join(nav_lines)


def process_directory_text(dir_path, docs_path, indent=4):
    """Process a directory and return its navigation structure as formatted text."""
    lines = []

    # Add markdown files in this directory
    md_files = sorted([f for f in dir_path.iterdir() if f.is_file() and f.suffix == '.md'])
    for file_path in md_files:
        # Extract title from frontmatter
        title = extract_title_from_frontmatter(file_path)

        # Fall back to filename if no frontmatter title
        if not title:
            if file_path.stem == "index":
                title = "Index"
            else:
                title = file_path.stem.replace('_', ' ').title()

        rel_path = file_path.relative_to(docs_path).as_posix()
        lines.append(f"{' ' * indent}{{\"{title}\" = \"{rel_path}\"}},")

    # Process subdirectories
    subdirs = sorted([d for d in dir_path.iterdir() if d.is_dir()])
    for subdir in subdirs:
        subdir_name = subdir.name.replace('_', ' ').title()
        subdir_content = process_directory_text(subdir, docs_path, indent + 2)

        if subdir_content:
            lines.append(f"{' ' * indent}{{\"{subdir_name}\" = [")
            lines.append(subdir_content)
            lines.append(f"{' ' * indent}  ]}},")

    # Remove trailing comma from last item
    if lines and lines[-1].endswith(','):
        lines[-1] = lines[-1][:-1]

    return "\n".join(lines) + ("\n" if lines else "")

# Read the entire file
with open('zensical.toml', 'r') as f:
    content = f.read()

# Generate new navigation
new_nav = generate_nav_text()

# Find and replace existing nav block
nav_start = content.find('nav = [')
if nav_start != -1:
    # Find the opening bracket
    bracket_start = content.find('[', nav_start)
    if bracket_start != -1:
        # Count brackets to find the matching closing bracket
        bracket_count = 1
        pos = bracket_start + 1
        while pos < len(content) and bracket_count > 0:
            if content[pos] == '[':
                bracket_count += 1
            elif content[pos] == ']':
                bracket_count -= 1
            pos += 1

        if bracket_count == 0:
            # Replace the entire nav block
            content = content[:nav_start] + new_nav + content[pos:]
else:
    # Find the position after the complete copyright field
    copyright_start = content.find('copyright =')
    if copyright_start != -1:
        # Handle both single-line and multi-line copyright
        if content[content.find('=', copyright_start)+1:].strip().startswith('"""'):
            # Find the closing triple quotes
            copyright_end = content.find('"""', content.find('"""', copyright_start) + 3)
            if copyright_end != -1:
                copyright_end = content.find('\n', copyright_end) + 1
        else:
            # Single line - find the next newline
            copyright_end = content.find('\n', copyright_start)

        if copyright_end != -1:
            # Insert nav after copyright with proper spacing
            content = content[:copyright_end] + '\n' + new_nav + '\n' + content[copyright_end:]

# Write back to file
with open('zensical.toml', 'w') as f:
    f.write(content)
