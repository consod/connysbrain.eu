import re
from pathlib import Path

from bs4 import BeautifulSoup

BASE_URL = "https://ik.imagekit.io/vu0zmaqce/"
SIZES = [
    (320, 70),   # Small mobile devices
    (375, 70),   # iPhone SE/older Android
    (414, 75),   # iPhone 8 Plus/XR
    (480, 75),   # Android phones
    (640, 80),   # Larger phones/early tablets
    (688, 80),   # Larger phones/early tablets
    (768, 80),   # Tablets (iPad, Android) 【0】
    (960, 80),   # Larger tablets/landscape mode
    (1024, 80),  # Small laptops/tablet landscape
    (1280, 85),  # Standard desktop
    (1440, 85),  # Retina/MacBook Pro
    (1920, 90),  # Full HD displays
    (2560, 90),  # QHD/2K displays
    (3840, 95)   # 4K/UHD displays
]


def generate_client_hints_meta():
    """Generate Client Hints meta tag for HTML head"""
    return '<meta http-equiv="Accept-CH" content="DPR, Width, Viewport-Width">'


def update_figure_with_srcset(content):
    """Update figure/img tags with srcset and wrap with lightGallery links"""
    soup = BeautifulSoup(content, 'html.parser')

    for figure in soup.find_all('figure'):
        img = figure.find('img')
        if not img or img.get('srcset'):
            continue

        src = img.get('src')
        if not src or not isinstance(src, str) or not src.startswith('http'):
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

        # Create lightGallery link
        fig_caption = figure.find('figcaption')
        caption_text = fig_caption.get_text() if fig_caption else ""

        # Extract full size image URL (largest in SIZES)
        full_size_url = f"{BASE_URL}{filename}?tr=w-{SIZES[-1][0]},q-{SIZES[-1][1]}"

        # Create link element
        link = soup.new_tag('a',
                           attrs={
                             'href': full_size_url,
                             'data-lg-size': f'{SIZES[-1][0]}-{int(SIZES[-1][0]*0.8)}',
                             'data-sub-html': f"<figcaption>{caption_text}</figcaption>"
                           }
                         )

        # Wrap img with link
        img.wrap(link)

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

        updated_content = update_figure_with_srcset(content)

        # Save only if changes were made
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {file_path}")

# Run the script
process_markdown_files()
