import argparse
from pathlib import Path
import re
import shutil
import gzip
from webpage import *
from resources import *

try:
    import brotli

    BROTLI_AVAILABLE = True
except ImportError:
    BROTLI_AVAILABLE = False
    print("Warning: brotli module not installed. Brotli compression will be skipped.")
    print("Install with: pip install brotli")

try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Image scaling will be skipped.")
    print("Install with: pip install Pillow")


class WebsiteGenerator:
    """Generate optimized and unoptimized versions of a website"""

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.optimized_dir = self.output_dir / "optimized"
        self.unoptimized_dir = self.output_dir / "unoptimized"

    def setup_directories(self):
        """Create output directories"""
        for dir_path in [self.optimized_dir, self.unoptimized_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def minify_html(self, html):
        """Remove unnecessary whitespace and comments from HTML"""
        # Remove HTML comments
        html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
        # Remove extra whitespace
        html = re.sub(r"\s+", " ", html)
        html = re.sub(r">\s+<", "><", html)
        return html.strip()

    def minify_css(self, css):
        """Remove unnecessary whitespace and comments from CSS"""
        # Remove CSS comments
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
        # Remove extra whitespace
        css = re.sub(r"\s+", " ", css)
        css = re.sub(r"\s*([{}:;,])\s*", r"\1", css)
        return css.strip()

    def minify_js(self, js):
        """Basic JavaScript minification"""
        # Remove single-line comments
        js = re.sub(r"//.*?$", "", js, flags=re.MULTILINE)
        # Remove multi-line comments
        js = re.sub(r"/\*.*?\*/", "", js, flags=re.DOTALL)
        # Remove extra whitespace
        js = re.sub(r"\s+", " ", js)
        return js.strip()

    def get_base_html(self, optimized=False, options=None):
        """Generate base HTML structure"""
        if options is None:
            options = {}

        css_content = get_css(optimized, options)
        js_content = get_javascript(optimized, options)

        # Decide on CSS inclusion method
        if optimized and options.get("inline_css", False):
            css_include = f"<style>{css_content}</style>"
        else:
            css_include = '<link rel="stylesheet" href="styles.css">'

        # Decide on JS inclusion method
        if optimized and options.get("inline_js", False):
            js_include = f"<script>{js_content}</script>"
        else:
            defer_attr = " defer" if optimized and options.get("defer_js", True) else ""
            js_include = f'<script src="script.js"{defer_attr}></script>'

        # Image handling
        if optimized and options.get("lazy_loading", True):
            img_attrs = ' loading="lazy"'
        else:
            img_attrs = ""

        # Fetch priority for images (optimized only)
        if optimized and options.get("fetch_priority", True):
            img_attrs += ' fetchpriority="high"'

        # Preconnect hints for optimized version
        preconnect = ""
        if optimized and options.get("preconnect", True):
            preconnect = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="dns-prefetch" href="https://fonts.googleapis.com">"""

        # Resource hints
        resource_hints = ""
        if optimized and options.get("prefetch", True):
            resource_hints = '<link rel="prefetch" href="page2.html">'

        return get_html_page(
            optimized, css_include, js_include, resource_hints, preconnect, img_attrs
        )

    def generate(self, options):
        """Generate both optimized and unoptimized versions"""
        print("Setting up directories...")
        self.setup_directories()

        print("\nGenerating OPTIMIZED version...")
        self.generate_version(self.optimized_dir, optimized=True, options=options)

        print("\nGenerating UNOPTIMIZED version...")
        self.generate_version(self.unoptimized_dir, optimized=False, options=options)

        print(f"\nGeneration complete!")
        print(f" Optimized version: {self.optimized_dir}")
        print(f" Unoptimized version: {self.unoptimized_dir}")

    def generate_version(self, output_dir, optimized=False, options=None):
        """Generate a single version of the website"""
        if options is None:
            options = {}

        # Generate HTML
        html_content = self.get_base_html(optimized, options)
        page2_content = get_second_page_html(optimized, options)

        # Apply minification if enabled
        if optimized and options.get("minify", False):
            html_content = self.minify_html(html_content)
            page2_content = self.minify_html(page2_content)

        # Write HTML files
        (output_dir / "index.html").write_text(html_content)
        (output_dir / "page2.html").write_text(page2_content)
        print(f"  ✓ Generated HTML files")

        # Compress HTML files for optimized version
        if optimized:
            for html_file in ["index.html", "page2.html"]:
                html_path = output_dir / html_file
                with open(html_path, "rb") as f_in:
                    # Create gzip compressed version
                    with gzip.open(
                        str(html_path) + ".gz", "wb", compresslevel=9
                    ) as f_out:
                        shutil.copyfileobj(f_in, f_out)

                    # Create brotli compressed version
                    f_in.seek(0)
                    compressed_data = brotli.compress(f_in.read(), quality=11)
                    with open(str(html_path) + ".br", "wb") as f_out:
                        f_out.write(compressed_data)
            print(f"  ✓ Compressed HTML files (gzip + brotli)")

        # Generate CSS (if not inlined)
        if not (optimized and options.get("inline_css", False)):
            css_content = get_css(optimized, options)
            if optimized and options.get("minify", False):
                css_content = self.minify_css(css_content)
            (output_dir / "styles.css").write_text(css_content)
            print(f"  ✓ Generated CSS file")

        # Generate JavaScript (if not inlined)
        if not (optimized and options.get("inline_js", False)):
            js_content = get_javascript(optimized, options)
            if optimized and options.get("minify", False):
                js_content = self.minify_js(js_content)
            js_path = output_dir / "script.js"
            js_path.write_text(js_content)
            print(f"  ✓ Generated JavaScript file")

            # Compress JavaScript file for optimized version
            if optimized:
                with open(js_path, "rb") as f_in:
                    # Create gzip compressed version
                    with gzip.open(
                        str(js_path) + ".gz", "wb", compresslevel=9
                    ) as f_out:
                        shutil.copyfileobj(f_in, f_out)

                    # Create brotli compressed version
                    f_in.seek(0)
                    compressed_data = brotli.compress(f_in.read(), quality=11)
                    with open(str(js_path) + ".br", "wb") as f_out:
                        f_out.write(compressed_data)
                print(f"  ✓ Compressed JavaScript file (gzip + brotli)")

        # Copy images from images folder
        copy_images(output_dir, optimized)
        if optimized:
            print(f"  ✓ Copied and compressed images (gzip + brotli)")
        else:
            print(f"  ✓ Copied images")

        # Generate favicon
        generate_favicon(output_dir, optimized)
        print(f"  ✓ Generated favicon")


def main():
    parser = argparse.ArgumentParser(
        description="Generate optimized and unoptimized website versions for performance comparison",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all                          Enable all optimizations
  %(prog)s --minify --inline-css          Enable minification and CSS inlining
  %(prog)s --lazy-loading --defer-js      Enable lazy loading and deferred JS
  %(prog)s                                Generate with default settings
        """,
    )

    parser.add_argument(
        "--all", action="store_true", default=True, help="Enable all optimizations"
    )

    parser.add_argument(
        "--minify", action="store_true", help="Minify HTML, CSS, and JavaScript"
    )

    parser.add_argument(
        "--inline-css",
        action="store_true",
        help="Inline CSS in HTML (reduces render-blocking)",
    )

    parser.add_argument(
        "--inline-js", action="store_true", help="Inline JavaScript in HTML"
    )

    parser.add_argument(
        "--defer-js", action="store_true", help="Add defer attribute to script tags"
    )

    parser.add_argument(
        "--lazy-loading", action="store_true", help="Enable lazy loading for images"
    )

    parser.add_argument(
        "--fetch-priority",
        action="store_true",
        help="Add fetchpriority=high attribute to images",
    )

    parser.add_argument(
        "--preconnect",
        action="store_true",
        help="Add preconnect and DNS-prefetch hints",
    )

    parser.add_argument(
        "--prefetch", action="store_true", help="Add prefetch hints for next page"
    )

    parser.add_argument(
        "--remove-unused-css", action="store_true", help="Remove unused CSS rules"
    )

    parser.add_argument(
        "--remove-unused-js", action="store_true", help="Remove unused JavaScript code"
    )

    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory for generated websites (default: output)",
    )

    args = parser.parse_args()

    # Build options dictionary
    if args.all:
        options = {
            "minify": True,
            "inline_css": True,
            "inline_js": False,  # Usually keep JS external
            "defer_js": True,
            "lazy_loading": True,
            "fetch_priority": True,
            "preconnect": True,
            "prefetch": True,
            "remove_unused_css": True,
            "remove_unused_js": True,
        }
    else:
        options = {
            "minify": args.minify,
            "inline_css": args.inline_css,
            "inline_js": args.inline_js,
            "defer_js": args.defer_js,
            "lazy_loading": args.lazy_loading,
            "fetch_priority": args.fetch_priority,
            "preconnect": args.preconnect,
            "prefetch": args.prefetch,
            "remove_unused_css": args.remove_unused_css,
            "remove_unused_js": args.remove_unused_js,
        }

    print("Web Performance Comparison Generator")
    print("=" * 50)
    print("\nEnabled optimizations:")
    for key, value in options.items():
        if value:
            print(f"  ✓ {key.replace('_', ' ').title()}")

    if not any(options.values()):
        print("  (None - using default unoptimized settings)")

    # Generate websites
    generator = WebsiteGenerator(output_dir=args.output_dir)
    generator.generate(options)


if __name__ == "__main__":
    main()
