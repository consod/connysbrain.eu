import re
from pathlib import Path

from bs4 import BeautifulSoup

BASE_URL = "https://ik.imagekit.io/vu0zmaqce/"
SIZES = [(360, 75), (640, 80), (768, 80), (1024, 85)]


def generate_client_hints_meta():
    """Generate Client Hints meta tag for HTML head"""
    return '<meta http-equiv="Accept-CH" content="DPR, Width, Viewport-Width">'


def update_figure_with_srcset(content):
    """Update figure/img tags with srcset if not already present"""
    soup = BeautifulSoup(content, 'html.parser')

    for img in soup.find_all('img'):
        # Skip if srcset already exists
        if img.get('srcset'):
            continue

        src = img.get('src')
        if not src or not src.startswith('http'):
            continue

        # Extract filename
        filename = src.split('/')[-1].split('?')[0]

        # Generate srcset
        srcset_parts = [
            f"{BASE_URL}{filename}?tr=w-{w},q-{q} {w}w"
            for w, q in SIZES
        ]
        img['srcset'] = ', '.join(srcset_parts)
        img['sizes'] = "(max-width: 480px) 100vw, (max-width: 768px) 90vw, 1024px"
        img['loading'] = 'lazy'

    return str(soup)


def process_markdown_files(root_dir="../docs"):
    """Recursively process all .md files in docs directory"""
    docs_dir = Path(__file__).parent / root_dir

    if not docs_dir.exists():
        print(f"Directory {docs_dir} does not exist.")
        return

    md_files = docs_dir.rglob("*.md")

    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find HTML blocks containing <figure> or <img>
        html_blocks = re.finditer(r'<(figure|img)[^>]*>.*?</\1>', content, re.DOTALL)

        if html_blocks:
            updated_content = update_figure_with_srcset(content)

            # Save only if changes were made
            if updated_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"Updated: {file_path}")

# Run the script
process_markdown_files()
