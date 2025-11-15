from pathlib import Path
import shutil
import gzip

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


def generate_favicon(output_dir, optimized=False):
    """Generate an SVG favicon"""
    # Different favicons for optimized vs unoptimized
    if optimized:
        # Lightning bolt for optimized
        svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
    <rect width="32" height="32" fill="#667eea" rx="4"/>
    <path d="M18 2 L10 16 L14 16 L14 30 L22 16 L18 16 Z" fill="#ffd700" stroke="#fff" stroke-width="1"/>
</svg>"""
    else:
        # Snail for unoptimized
        svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
    <!-- Background -->
    <rect width="32" height="32" fill="#764ba2" rx="4"/>
    
    <!-- Snail shell - spiral design -->
    <circle cx="18" cy="14" r="7" fill="#8B7355" stroke="#6B5345" stroke-width="1"/>
    <circle cx="18" cy="14" r="5.5" fill="#A0826D" stroke="#8B7355" stroke-width="0.8"/>
    <circle cx="18" cy="14" r="4" fill="#B8956A" stroke="#A0826D" stroke-width="0.6"/>
    <circle cx="19" cy="13" r="2.5" fill="#D4B896" stroke="#B8956A" stroke-width="0.5"/>
    <circle cx="19.5" cy="12.5" r="1.2" fill="#E8D4B8"/>
    
    <!-- Snail body -->
    <ellipse cx="12" cy="20" rx="6" ry="3.5" fill="#C8B8A8" stroke="#A89888" stroke-width="0.8"/>
    <ellipse cx="11" cy="20" rx="5" ry="3" fill="#D8C8B8"/>
    
    <!-- Snail head/neck -->
    <ellipse cx="7" cy="18" rx="2.5" ry="3" fill="#D8C8B8" stroke="#C8B8A8" stroke-width="0.6"/>
    
    <!-- Left antenna -->
    <path d="M 6 17 Q 4 15 4 13" fill="none" stroke="#A89888" stroke-width="0.8" stroke-linecap="round"/>
    <circle cx="4" cy="13" r="0.8" fill="#8B7355"/>
    
    <!-- Right antenna -->
    <path d="M 8 17 Q 9 15 9 13" fill="none" stroke="#A89888" stroke-width="0.8" stroke-linecap="round"/>
    <circle cx="9" cy="13" r="0.8" fill="#8B7355"/>
</svg>"""

    filepath = output_dir / "favicon.svg"
    filepath.write_text(svg)


def copy_images(output_dir, optimized=False):
    """Copy images from images folder and optionally compress them"""
    images_source = Path("images")

    if not images_source.exists():
        print(f"  ⚠ Warning: images folder not found, skipping image copy")
        return self.generate_placeholder_images(output_dir)

    # Get all images from the source folder
    image_files = list(images_source.glob("*"))

    # Filter for common image formats
    valid_extensions = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg"}
    image_files = [f for f in image_files if f.suffix.lower() in valid_extensions]

    if not image_files:
        print(f"  ⚠ Warning: no images found in images folder")
        return

    for img_file in image_files:
        dest_path = output_dir / img_file.name

        # Scale images to 1920x1080 (preserving aspect ratio)
        if PIL_AVAILABLE and img_file.suffix.lower() in {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".avif",
        }:
            try:
                with Image.open(img_file) as img:
                    # Target size
                    target_width = 1920 * 2
                    target_height = 1080 * 2

                    # Calculate aspect ratios
                    img_ratio = img.width / img.height
                    target_ratio = target_width / target_height

                    # Determine scaling to fit within 1920x1080 while preserving aspect ratio
                    if img_ratio > target_ratio:
                        # Image is wider - scale by width
                        new_width = target_width
                        new_height = int(target_width / img_ratio)
                    else:
                        # Image is taller - scale by height
                        new_height = target_height
                        new_width = int(target_height * img_ratio)

                    # Only resize if image is larger than target
                    if img.width > target_width or img.height > target_height:
                        scaled_img = img.resize(
                            (new_width, new_height), Image.Resampling.LANCZOS
                        )
                        scaled_img.save(dest_path, quality=100, optimize=optimized)
                        print(
                            f"  ✓ Scaled {img_file.name} from {img.width}x{img.height} to {new_width}x{new_height}"
                        )
                    else:
                        # Image is already smaller, just copy
                        shutil.copy2(img_file, dest_path)
                        print(
                            f"  ✓ Copied {img_file.name} (already within bounds: {img.width}x{img.height})"
                        )

                    # For optimized version, create multiple responsive image sizes
                    if optimized:
                        # Generate 200w, 400w, 800w, 1600w versions
                        widths = [200, 400, 800, 1600]

                        for width in widths:
                            # Calculate height preserving aspect ratio
                            new_width = width
                            new_height = int(width / img_ratio)

                            # Resize and save
                            resized_img = img.resize(
                                (new_width, new_height), Image.Resampling.LANCZOS
                            )
                            resized_path = (
                                output_dir
                                / f"{img_file.stem}-{width}w{img_file.suffix}"
                            )
                            resized_img.save(resized_path, quality=85, optimize=True)
                            print(
                                f"  ✓ Created {img_file.stem}-{width}w{img_file.suffix} ({new_width}x{new_height})"
                            )

                            # Compress resized image
                            with open(resized_path, "rb") as f_in:
                                with gzip.open(
                                    str(resized_path) + ".gz", "wb", compresslevel=9
                                ) as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                            if BROTLI_AVAILABLE:
                                with open(resized_path, "rb") as f_in:
                                    compressed_data = brotli.compress(
                                        f_in.read(), quality=11
                                    )
                                    with open(str(resized_path) + ".br", "wb") as f_out:
                                        f_out.write(compressed_data)

            except Exception as e:
                print(f"  ⚠ Error scaling {img_file.name}: {e}, copying original")
                shutil.copy2(img_file, dest_path)
        else:
            # SVG or Pillow not available - just copy
            shutil.copy2(img_file, dest_path)

        # For optimized version, create gzip and brotli compressed versions
        if optimized:
            # Create gzip compressed version
            print(f"    Compressing {img_file.name} with gzip...")
            with open(dest_path, "rb") as f_in:
                with gzip.open(str(dest_path) + ".gz", "wb", compresslevel=9) as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Create brotli compressed version
            print(f"    Compressing {img_file.name} with brotli...")
            with open(dest_path, "rb") as f_in:
                compressed_data = brotli.compress(f_in.read(), quality=11)
                with open(str(dest_path) + ".br", "wb") as f_out:
                    f_out.write(compressed_data)
