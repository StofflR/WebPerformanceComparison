from pathlib import Path


def get_srcset_attr(optimized, img_name):
    if optimized:
        # Extract filename and extension
        img_path = Path(img_name)
        stem = img_path.stem
        suffix = img_path.suffix
        return f' srcset="{stem}-200w{suffix} 200w, {stem}-400w{suffix} 400w, {stem}-800w{suffix} 800w, {stem}-1600w{suffix} 1600w" sizes="auto, (max-width: 30em) 100vw, (max-width: 50em) 50vw, calc(33vw - 100px)"'
    return ""


def get_javascript(optimized, options=None):
    """Generate JavaScript content"""
    if options is None:
        options = {}

    # Add unnecessary JavaScript for unoptimized version
    extra_js = ""
    if not optimized or not options.get("remove_unused_js", True):
        extra_js = """
// Unused functions that bloat the JavaScript
function unusedFunction1() {
    console.log("This function is never called");
    return Math.random() * 100;
}

function unusedFunction2(a, b, c) {
    return a + b + c + unusedFunction1();
}

const unusedArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const unusedObject = {
    key1: "value1",
    key2: "value2",
    key3: "value3"
};
"""

    js = f"""
// Web Performance Comparison - JavaScript
(function() {{
    'use strict';
    
    // Log page load time
    window.addEventListener('load', function() {{
        if (window.performance && window.performance.timing) {{
            const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
            console.log('Page Load Time:', loadTime + 'ms');
        }}
    }});
    
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
        anchor.addEventListener('click', function(e) {{
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {{
                e.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth'
                    }});
                }}
            }}
        }});
    }});
    
    // Add animation on scroll
    const observerOptions = {{
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    }};
    
    const observer = new IntersectionObserver(function(entries) {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }}
        }});
    }}, observerOptions);
    
    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {{
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    }});
    
{extra_js}
}})();
"""

    return js


def get_css(optimized, options=None):
    """Generate CSS content"""
    if options is None:
        options = {}

    # Add unnecessary CSS for unoptimized version
    extra_css = ""
    if not optimized or not options.get("remove_unused_css", True):
        extra_css = """
/* Unused styles that bloat the CSS */
.unused-class-1 { color: red; background: blue; }
.unused-class-2 { margin: 50px; padding: 50px; }
.unused-class-3 { font-size: 72px; line-height: 2; }
.unused-class-4 { border: 10px solid black; }
.unused-class-5 { display: flex; justify-content: center; }
"""

    css = f"""
/* Reset and Base Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Navigation */
.navbar {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

.navbar .container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: bold;
}}

.nav-links {{
    display: flex;
    list-style: none;
    gap: 2rem;
}}

.nav-links a {{
    color: white;
    text-decoration: none;
    transition: opacity 0.3s;
}}

.nav-links a:hover {{
    opacity: 0.8;
}}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 0;
    text-align: center;
}}

.hero h2 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.subtitle {{
    font-size: 1.5rem;
    opacity: 0.9;
    margin-bottom: 2rem;
}}

.hero-content {{
    max-width: 600px;
    margin: 0 auto;
}}

.cta-button {{
    background: white;
    color: #667eea;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    margin-top: 1rem;
}}

.cta-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}}

/* Features Section */
.features {{
    padding: 4rem 0;
    background: white;
}}

.features h2 {{
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: #333;
}}

.feature-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}}

.feature-card {{
    background: #f9f9f9;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
}}

.feature-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}}

.feature-icon {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.feature-card h3 {{
    margin-bottom: 1rem;
    color: #667eea;
}}

/* Gallery Section */
.gallery {{
    padding: 4rem 0;
    background: #f5f5f5;
}}

.gallery h2 {{
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}}

.image-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}}

.image-item {{
    overflow: hidden;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}}

.image-item img {{
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.3s;
}}

.image-item:hover img {{
    transform: scale(1.05);
}}

/* Content Section */
.content {{
    padding: 4rem 0;
    background: white;
}}

.content h2 {{
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}}

.content-columns {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}}

.column h3 {{
    color: #667eea;
    margin-bottom: 1rem;
}}

.column p {{
    margin-bottom: 1rem;
}}

.optimization-list {{
    list-style-position: inside;
    max-width: 800px;
    margin: 0 auto;
}}

.optimization-list li {{
    margin-bottom: 1rem;
    padding-left: 1rem;
}}

/* Footer */
footer {{
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem 0;
}}

/* Responsive */
@media (max-width: 768px) {{
    .nav-links {{
        gap: 1rem;
    }}
    
    .hero h2 {{
        font-size: 2rem;
    }}
    
    .subtitle {{
        font-size: 1.2rem;
    }}
}}
{extra_css}
"""

    return css


def get_second_page_html(optimized=False, options=None):
    """Generate second page HTML"""
    if options is None:
        options = {}

    css_content = get_css(optimized, options)
    js_content = get_javascript(optimized, options)

    if optimized and options.get("inline_css", False):
        css_include = f"<style>{css_content}</style>"
    else:
        css_include = '<link rel="stylesheet" href="styles.css">'

    if optimized and options.get("inline_js", False):
        js_include = f"<script>{js_content}</script>"
    else:
        defer_attr = " defer" if optimized and options.get("defer_js", True) else ""
        js_include = f'<script src="script.js"{defer_attr}></script>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - {'Optimized' if optimized else 'Unoptimized'}</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    {css_include}
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="container">
                <h1 class="logo">Performance {'⚡' if optimized else '🐌'}</h1>
                <ul class="nav-links">
                    <li><a href="index.html">Home</a></li>
                    <li><a href="page2.html">About</a></li>
                    <li><a href="index.html#features">Features</a></li>
                </ul>
            </div>
        </nav>
    </header>
    
    <main>
        <section class="hero">
            <div class="container">
                <h2>About This Project</h2>
                <p class="subtitle">Understanding Web Performance</p>
            </div>
        </section>
        
        <section class="content">
            <div class="container">
                <h2>Optimization Techniques</h2>
                <ul class="optimization-list">
                    <li><strong>HTML/CSS/JS Minification:</strong> Removes unnecessary whitespace and comments</li>
                    <li><strong>Inline Critical CSS:</strong> Embeds CSS directly in HTML to reduce render-blocking</li>
                    <li><strong>Deferred JavaScript:</strong> Delays script execution until page is parsed</li>
                    <li><strong>Lazy Loading Images:</strong> Loads images only when they enter the viewport</li>
                    <li><strong>Resource Hints:</strong> Preconnect, DNS-prefetch, and prefetch for faster resource loading</li>
                    <li><strong>Image Optimization:</strong> Uses appropriate formats and compression</li>
                </ul>
                <p><a href="index.html">← Back to Home</a></p>
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; 2025 Web Performance Comparison. Version: {'Optimized' if optimized else 'Unoptimized'}</p>
        </div>
    </footer>
    
    {js_include}
</body>
</html>"""

    return html


def get_html_page(
    optimized, css_include, js_include, resource_hints, preconnect, img_attrs
):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Web Performance Comparison - {'Optimized' if optimized else 'Unoptimized'} Version">
    <title>Performance Test - {'Optimized' if optimized else 'Unoptimized'}</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">{preconnect}{resource_hints}
    {css_include}
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="container">
                <h1 class="logo">Performance {'⚡' if optimized else '🐌'}</h1>
                <ul class="nav-links">
                    <li><a href="index.html">Home</a></li>
                    <li><a href="page2.html">About</a></li>
                    <li><a href="index.html#features">Features</a></li>
                </ul>
            </div>
        </nav>
    </header>
    
    <main>
        <section class="hero">
            <div class="container">
                <h2>Web Performance Comparison</h2>
                <p class="subtitle">{'Optimized' if optimized else 'Unoptimized'} Version</p>
                <div class="hero-content">
                    <p>This website demonstrates the impact of various web performance optimizations.</p>
                    <button class="cta-button" onclick="alert('Button clicked!')">Get Started</button>
                </div>
            </div>
        </section>
        
        <section class="gallery">
            <div class="container">
                <h2>Gallery</h2>
                <div class="image-grid">
                    <div class="image-item">
                        <img src="image1.PNG" alt="Image 1"{img_attrs}{get_srcset_attr(optimized, 'image1.PNG')} width="40vw" height="30vw">
                    </div>
                    <div class="image-item">
                        <img src="image2.WebP" alt="Image 2"{img_attrs}{get_srcset_attr(optimized, 'image2.WebP')} width="40vw" height="30vw">
                    </div>
                    <div class="image-item">
                        <img src="image3.AVIF" alt="Image 3"{img_attrs}{get_srcset_attr(optimized, 'image3.AVIF')} width="40vw" height="30vw">
                    </div>
                    <div class="image-item">
                        <img src="image4.JPEG" alt="Image 4"{img_attrs}{get_srcset_attr(optimized, 'image4.JPEG')} width="40vw" height="30vw">
                    </div>
                </div>
            </div>
        </section>

        <section id="features" class="features">
            <div class="container">
                <h2>Features</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <div class="feature-icon">🎨</div>
                        <h3>Beautiful Design</h3>
                        <p>Modern and responsive design that looks great on all devices.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">⚡</div>
                        <h3>Fast Loading</h3>
                        <p>{'Optimized for lightning-fast loading times.' if optimized else 'Standard loading performance.'}</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📱</div>
                        <h3>Mobile First</h3>
                        <p>Designed with mobile users in mind from the ground up.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🔒</div>
                        <h3>Secure</h3>
                        <p>Built with security best practices in mind.</p>
                    </div>
                </div>
            </div>
        </section>
        
        <section class="content">
            <div class="container">
                <h2>Why Performance Matters</h2>
                <div class="content-columns">
                    <div class="column">
                        <h3>User Experience</h3>
                        <p>Fast websites provide better user experience. Users expect pages to load quickly, and slow loading times lead to higher bounce rates.</p>
                        <p>Studies show that a 1-second delay in page load time can result in a 7% reduction in conversions.</p>
                    </div>
                    <div class="column">
                        <h3>SEO Benefits</h3>
                        <p>Search engines like Google consider page speed as a ranking factor. Faster websites tend to rank higher in search results.</p>
                        <p>Core Web Vitals are now essential metrics for SEO performance.</p>
                    </div>
                    <div class="column">
                        <h3>Resource Efficiency</h3>
                        <p>Optimized websites consume less bandwidth and resources, leading to lower hosting costs and reduced environmental impact.</p>
                        <p>Mobile users especially benefit from optimized content delivery.</p>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; 2025 Web Performance Comparison. Version: {'Optimized' if optimized else 'Unoptimized'}</p>
        </div>
    </footer>
    
    {js_include}
</body>
</html>"""
