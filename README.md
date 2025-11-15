# Web Performance Comparison

A Python script that generates two versions of a website - one optimized for performance and one unoptimized - to demonstrate the impact of various web performance optimization techniques.

## Features

The script generates websites with the following configurable optimizations:

- **HTML/CSS/JS Minification**: Removes whitespace and comments to reduce file sizes
- **Inline CSS**: Embeds critical CSS directly in HTML to eliminate render-blocking requests
- **Inline JavaScript**: Embeds JS in HTML (optional)
- **Deferred JavaScript**: Delays script execution until page is parsed
- **Lazy Loading Images**: Loads images only when they enter the viewport
- **Fetch Priority**: Adds `fetchpriority="high"` attribute to important images for faster LCP
- **Resource Hints**: Adds preconnect and DNS-prefetch hints for faster resource loading
- **Prefetch Hints**: Adds prefetch hints for next page navigation
- **Unused Code Removal**: Removes unused CSS and JavaScript
- **Image Compression**: Generates Gzip and Brotli compressed versions of images (optimized only)
- **Responsive Images**: Creates multiple image sizes with `srcset` for optimal bandwidth usage

## Installation

### Requirements

- Python 3
- Required Python packages (install with pip):

```bash
git clone <your-repo-url>
cd WebPerformanceComparison

# Install Python dependencies
pip install -r requirements.txt
```

The following packages are required:
- **brotli** (1.2.0+): For Brotli compression of optimized assets
- **Pillow** (12.0.0+): For image scaling and optimization

## Usage

### Basic Usage

Generate websites with all optimizations enabled (default behavior):

```bash
python generate_websites.py
```

This is equivalent to:

```bash
python generate_websites.py --all
```

### Enable Specific Optimizations

To disable all optimizations and enable only specific ones, you need to explicitly specify them:

```bash
# Minification only (you need to specify it explicitly)
python generate_websites.py --minify

# Minification + CSS inlining + lazy loading
python generate_websites.py --minify --inline-css --lazy-loading

# Full optimization suite (same as default --all)
python generate_websites.py --minify --inline-css --defer-js --lazy-loading --fetch-priority --preconnect --prefetch --remove-unused-css --remove-unused-js
```

**Note**: When you specify individual flags, you override the default `--all` behavior.

### Available Options

| Option | Description |
|--------|-------------|
| `--all` | Enable all optimizations (default: enabled) |
| `--minify` | Minify HTML, CSS, and JavaScript |
| `--inline-css` | Inline CSS in HTML (reduces render-blocking) |
| `--inline-js` | Inline JavaScript in HTML |
| `--defer-js` | Add defer attribute to script tags |
| `--lazy-loading` | Enable lazy loading for images |
| `--fetch-priority` | Add fetchpriority=high attribute to images |
| `--preconnect` | Add preconnect and DNS-prefetch hints |
| `--prefetch` | Add prefetch hints for next page |
| `--remove-unused-css` | Remove unused CSS rules |
| `--remove-unused-js` | Remove unused JavaScript code |
| `--output-dir DIR` | Specify output directory (default: output) |

### Help

```bash
python generate_websites.py --help
```

## Output Structure

After running the script, you'll get:

```
output/
├── optimized/
│   ├── index.html
│   ├── page2.html
│   ├── styles.css (if not inlined)
│   ├── script.js (if not inlined)
│   ├── favicon.svg
│   ├── image1.PNG (+ .gz and .br compressed versions)
│   ├── image2.WebP (+ .gz and .br compressed versions)
│   ├── image3.AVIF (+ .gz and .br compressed versions)
│   ├── image4.JPEG (+ .gz and .br compressed versions)
│   ├── image1-200w.PNG (responsive image variants)
│   ├── image1-400w.PNG
│   ├── image1-800w.PNG
│   ├── image1-1600w.PNG
│   └── ... (similar variants for other images)
└── unoptimized/
    ├── index.html
    ├── page2.html
    ├── styles.css
    ├── script.js
    ├── favicon.svg
    ├── image1.PNG
    ├── image2.WebP
    ├── image3.AVIF
    └── image4.JPEG
```

**Note**: The optimized version includes:
- Gzip (.gz) and Brotli (.br) compressed versions of all assets
- Multiple responsive image sizes (200w, 400w, 800w, 1600w) when Pillow is installed

## Testing Performance

### Running a Local Server (Recommended)

For accurate performance testing, serve the files with HTTP server. A convenience script is provided:

```bash
# Install http-server globally (one time only)
npm install -g http-server

# Run both servers with optimal settings
./serve.sh
```

This will start:
- **Optimized version**: http://localhost:8080 (with gzip/brotli compression)
- **Unoptimized version**: http://localhost:8081 (no cache for accurate testing)

Press `Ctrl+C` to stop both servers.

**Manual alternative using Python:**

```bash
# Python 3 - Terminal 1
cd output/optimized
python -m http.server 8000

# Python 3 - Terminal 2 (new terminal)
cd output/unoptimized
python -m http.server 8001
```

### Method 1: Browser DevTools

1. Open http://localhost:8080 in your browser (optimized version)
2. Open DevTools (F12)
3. Go to the Network tab and reload the page
4. Note the total load time and transferred size
5. Repeat for http://localhost:8081 (unoptimized version)
6. Compare the results

### Method 2: Lighthouse

1. Open Chrome DevTools (F12)
2. Go to the Lighthouse tab
3. Run an audit on both versions
4. Compare the Performance scores
