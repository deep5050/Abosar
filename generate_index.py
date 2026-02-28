import os
import re
import json
import markdown

readme_path = "/home/deep/code/Abosar/README.md"
html_path = "/home/deep/code/Abosar/index.html"
base_dir = "/home/deep/code/Abosar"

def parse_readme(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    story_pattern = re.compile(r'\|\s*\d+\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*(?:\[([^\]]+)\]\(([^)]+)\))?\s*\|')
    
    rabibasariya = []
    onnoalo = []
    
    for match in story_pattern.finditer(content):
        # Rabibasariya
        t_a_1 = match.group(1).strip()
        l_1 = match.group(2).strip()
        if t_a_1 and l_1:
            parts = [x.strip() for x in t_a_1.split('-', 1)]
            t = parts[0]
            a = parts[1] if len(parts) > 1 else "Unknown"
            
            # Generate the HTML link
            md_path = l_1.replace('./', '')
            html_link = md_path.replace('stories/', 'html_stories/').replace('.md', '.html')
            
            rabibasariya.append({
                'title': t, 
                'author': a, 
                'link': html_link,
                'md_path': md_path
            })
            
        # Onnoalo
        t_a_2 = match.group(3)
        l_2 = match.group(4)
        if t_a_2 and l_2:
            t_a_2 = t_a_2.strip()
            l_2 = l_2.strip()
            parts = [x.strip() for x in t_a_2.split('-', 1)]
            t = parts[0]
            a = parts[1] if len(parts) > 1 else "Unknown"
            
            # Generate the HTML link
            md_path = l_2.replace('./', '')
            html_link = md_path.replace('stories/', 'html_stories/').replace('.md', '.html')
            
            onnoalo.append({
                'title': t, 
                'author': a, 
                'link': html_link,
                'md_path': md_path
            })
            
    return rabibasariya, onnoalo

r_stories, o_stories = parse_readme(readme_path)

# --------------------------------------------------------------------------------------
# 1. Generate Individual HTML Story Pages
# --------------------------------------------------------------------------------------

story_template = """<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {author}</title>
    <link href="https://fonts.googleapis.com/css2?family=Tiro+Bangla:ital@0;1&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #fdfbf7;
            --text-color: #2c1810;
            --accent: #8b4513;
            --accent-light: #d2b48c;
            --paper-shadow: rgba(0,0,0,0.1);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: #e2e8f0;
            background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
            background-size: 20px 20px;
            font-family: 'Tiro Bangla', serif;
            color: var(--text-color);
            line-height: 1.8;
            padding: 2rem 1rem;
            display: flex;
            justify-content: center;
        }}

        .paper-container {{
            background-color: var(--bg-color);
            max-width: 800px;
            width: 100%;
            padding: 4rem 3rem 6rem;
            border-radius: 4px;
            box-shadow: 
                0 10px 30px rgba(0,0,0,0.1),
                inset 0 0 50px rgba(200, 180, 160, 0.2);
            position: relative;
        }}
        
        .paper-container::before {{
            content: '';
            position: absolute;
            top: 0;
            bottom: 0;
            left: 2rem;
            width: 2px;
            background-color: rgba(139, 69, 19, 0.2);
        }}

        .back-nav {{
            position: absolute;
            top: 2rem;
            left: -5rem;
        }}

        .back-btn {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: white;
            border-radius: 50%;
            color: var(--accent);
            text-decoration: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .back-btn:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}

        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            position: relative;
        }}
        
        header::after {{
            content: '❦';
            position: absolute;
            bottom: -15px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--bg-color);
            padding: 0 10px;
            color: var(--accent);
            font-size: 1.5rem;
        }}

        h1 {{
            font-size: 2.5rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
            line-height: 1.3;
        }}

        .author {{
            font-size: 1.2rem;
            color: #555;
            font-style: italic;
        }}

        .story-content {{
            font-size: 1.25rem;
            text-align: justify;
        }}

        .story-content p {{
            margin-bottom: 1.5rem;
            text-indent: 2rem;
        }}
        
        .story-content img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 2rem auto;
            border-radius: 4px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}

        .story-content hr {{
            border: none;
            text-align: center;
            margin: 3rem 0;
        }}
        
        .story-content hr::after {{
            content: '***';
            font-size: 1.5rem;
            letter-spacing: 0.5rem;
            color: rgba(0,0,0,0.3);
        }}

        @media (max-width: 768px) {{
            .paper-container {{
                padding: 3rem 1.5rem;
            }}
            .back-nav {{
                position: relative;
                top: 0;
                left: 0;
                margin-bottom: 2rem;
            }}
            .paper-container::before {{
                left: 0.5rem;
            }}
            h1 {{
                font-size: 2rem;
            }}
            .story-content {{
                font-size: 1.1rem;
            }}
        }}
    </style>
</head>
<body>

    <div class="paper-container">
        <div class="back-nav">
            <a href="../../index.html" class="back-btn" title="Back to Library">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="19" y1="12" x2="5" y2="12"></line>
                    <polyline points="12 19 5 12 12 5"></polyline>
                </svg>
            </a>
        </div>

        <header>
            <h1>{title}</h1>
            <div class="author">{author}</div>
        </header>

        <div class="story-content">
            {html_content}
        </div>
    </div>

</body>
</html>
"""

def generate_html_files(stories, category):
    os.makedirs(os.path.join(base_dir, f'html_stories/{category}'), exist_ok=True)
    
    for story in stories:
        md_file = os.path.join(base_dir, story['md_path'])
        
        # Determine the depth to construct relative back link accurately.
        # usually it's "html_stories/rabibasariya/filename.html" -> backlink="../../index.html"
        # However, we hardcoded "../../index.html" in the template which handles this standard depth.
        
        if os.path.exists(md_file):
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
                
            # Convert Markdown to HTML
            html_content = markdown.markdown(md_content)
            
            # Format template
            final_html = story_template.format(
                title=story['title'],
                author=story['author'],
                html_content=html_content
            )
            
            out_file = os.path.join(base_dir, story['link'])
            
            # Be mindful of subdirectories if there are any inside stories/category/
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(final_html)

print("Generating individual HTML story pages...")
generate_html_files(r_stories, 'rabibasariya')
generate_html_files(o_stories, 'onnoalo')
print("Done generating individual pages.")

# --------------------------------------------------------------------------------------
# 2. Generate Main index.html
# --------------------------------------------------------------------------------------

html_template = """<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>অবসর (ABOSAR) - Short Bengali Stories</title>
    <link href="https://fonts.googleapis.com/css2?family=Tiro+Bangla:ital@0;1&family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f4ecce;
            --text-main: #332211;
            --text-muted: #5a4b3c;
            --accent: #8b4513;
            --accent-hover: #5c2e0e;
            --card-bg: rgba(139, 69, 19, 0.05);
            --book-spine: rgba(0,0,0,0.15);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            background-image: radial-gradient(rgba(139, 69, 19, 0.1) 1px, transparent 1px);
            background-size: 20px 20px;
            color: var(--text-main);
            line-height: 1.6;
            overflow-x: hidden;
            scroll-behavior: smooth;
        }
        
        /* Adds a subtle paper texture over everything */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100" preserveAspectRatio="none"><filter id="noiseFilter"><feTurbulence type="fractalNoise" baseFrequency="1" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100" height="100" filter="url(%23noiseFilter)" opacity="0.05"/></svg>');
            pointer-events: none;
            z-index: 9999;
        }

        /* Hero Section */
        .hero {
            min-height: 70vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 2rem;
            position: relative;
            background: radial-gradient(circle at center, rgba(255,255,255,0.4) 0%, transparent 70%);
        }
        
        .hero::before {
            content: '❦';
            font-size: 3rem;
            color: var(--accent);
            opacity: 0.6;
            margin-bottom: 1rem;
        }

        .hero h1 {
            font-family: 'Tiro Bangla', serif;
            font-size: 6rem;
            margin-bottom: 1rem;
            color: var(--accent);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            animation: fadeInDown 1s ease-out;
        }

        .hero p.tagline {
            font-size: 1.5rem;
            color: var(--text-muted);
            max-width: 600px;
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease-out 0.3s both;
            font-family: 'Tiro Bangla', serif;
        }

        .features-grid {
            display: flex;
            gap: 2rem;
            margin-top: 3rem;
            flex-wrap: wrap;
            justify-content: center;
            animation: fadeInUp 1s ease-out 0.6s both;
            z-index: 10;
        }

        .feature-card {
            background: var(--card-bg);
            padding: 1.5rem 2rem;
            border-radius: 4px;
            border: 1px solid rgba(139, 69, 19, 0.2);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            max-width: 250px;
            box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 4px 8px 15px rgba(139, 69, 19, 0.15);
        }

        .feature-card h3 {
            font-size: 1.2rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
            font-family: 'Tiro Bangla', serif;
        }

        .feature-card p {
            color: var(--text-muted);
            font-size: 1rem;
        }

        .cta-buttons {
            margin-top: 2rem;
            z-index: 10;
        }

        .cta-button {
            display: inline-block;
            padding: 1rem 2.5rem;
            background: var(--accent);
            color: #f4ecce;
            text-decoration: none;
            border-radius: 2px;
            font-weight: 600;
            font-family: 'Tiro Bangla', serif;
            font-size: 1.2rem;
            transition: background 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 10px rgba(139, 69, 19, 0.3);
            border: 1px solid var(--accent-hover);
        }

        .cta-button:hover {
            background: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(139, 69, 19, 0.4);
        }

        /* Stories Section */
        .section-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }

        .section-title {
            font-family: 'Tiro Bangla', serif;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 3rem;
            color: var(--accent);
            position: relative;
        }

        .section-title::after {
            content: '❧';
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            color: var(--accent);
            font-size: 1.5rem;
            opacity: 0.5;
        }

        .tabs {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
            margin-top: 2rem;
            flex-wrap: wrap;
        }

        .tab-btn {
            background: transparent;
            border: 1px solid rgba(139, 69, 19, 0.3);
            color: var(--text-main);
            padding: 0.75rem 2.5rem;
            border-radius: 2px;
            font-size: 1.2rem;
            font-family: 'Tiro Bangla', serif;
            cursor: pointer;
            transition: all 0.3s ease;
            outline: none;
        }

        .tab-btn.active {
            background: var(--accent);
            color: #f4ecce;
            border-color: var(--accent);
            box-shadow: 0 4px 10px rgba(139, 69, 19, 0.2);
        }

        .tab-btn:hover:not(.active) {
            background: var(--card-bg);
        }

        /* Search Section */
        .search-container {
            text-align: center;
            margin-bottom: 3rem;
        }

        .search-input {
            width: 100%;
            max-width: 600px;
            padding: 1rem 1.5rem;
            border-radius: 2px;
            border: 1px solid rgba(139, 69, 19, 0.4);
            background: rgba(255,255,255,0.5);
            color: var(--text-main);
            font-size: 1.1rem;
            outline: none;
            transition: all 0.3s ease;
            font-family: 'Tiro Bangla', serif;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        }

        .search-input:focus {
            border-color: var(--accent);
            background: rgba(255,255,255,0.8);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05), 0 0 0 3px rgba(139, 69, 19, 0.2);
        }

        .search-input::placeholder {
            color: rgba(139, 69, 19, 0.5);
        }

        .books-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 4rem 2.5rem;
            justify-content: center;
            padding: 2rem 0;
            min-height: 400px;
            perspective: 1000px;
        }

        /* Book CSS - Restyled to look like older books */
        .book {
            position: relative;
            width: 100%;
            aspect-ratio: 2 / 3.1;
            background: #e6d5b8;
            border-radius: 2px 6px 6px 2px;
            box-shadow: 
                inset 5px 0 15px var(--book-spine), 
                inset -2px 0 5px rgba(255,255,255,0.4), 
                5px 10px 15px rgba(0,0,0,0.3);
            text-decoration: none;
            color: #2c1810;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 1.5rem;
            text-align: center;
            transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.5s ease;
            transform-style: preserve-3d;
            cursor: pointer;
            border: 1px solid rgba(139, 69, 19, 0.2);
        }

        .book::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            width: 12px;
            background: linear-gradient(to right, rgba(0,0,0,0.2) 0%, rgba(255,255,255,0.1) 30%, rgba(0,0,0,0.1) 100%);
            border-radius: 2px 0 0 2px;
            z-index: 2;
        }

        /* Page edges - aged paper color */
        .book::after {
            content: '';
            position: absolute;
            top: 2px;
            bottom: 2px;
            right: -4px;
            width: 4px;
            background: repeating-linear-gradient(
                to bottom,
                #d4c4a8 0,
                #d4c4a8 1px,
                #ebdcc0 1px,
                #ebdcc0 3px
            );
            border-radius: 0 2px 2px 0;
            transform: translateZ(-1px);
            box-shadow: inset 1px 0 2px rgba(0,0,0,0.2);
        }

        /* Vintage book cover colors */
        .book:nth-child(5n+1) { background: #8b4513; color: #f4ecce; } /* Saddle Brown */
        .book:nth-child(5n+2) { background: #556b2f; color: #f4ecce; } /* Dark Olive Green */
        .book:nth-child(5n+3) { background: #800000; color: #f4ecce; } /* Maroon */
        .book:nth-child(5n+4) { background: #2f4f4f; color: #f4ecce; } /* Dark Slate Gray */
        .book:nth-child(5n+5) { background: #b8860b; color: #f4ecce; } /* Dark Goldenrod */

        .book:nth-child(5n+1) .book-title,
        .book:nth-child(5n+2) .book-title,
        .book:nth-child(5n+3) .book-title,
        .book:nth-child(5n+4) .book-title,
        .book:nth-child(5n+5) .book-title {
            color: #fceec4;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        .book:nth-child(5n+1) .book-author,
        .book:nth-child(5n+2) .book-author,
        .book:nth-child(5n+3) .book-author,
        .book:nth-child(5n+4) .book-author,
        .book:nth-child(5n+5) .book-author {
            color: #dcb87d;
        }
        
        .book:nth-child(5n+1) .book-decoration,
        .book:nth-child(5n+2) .book-decoration,
        .book:nth-child(5n+3) .book-decoration,
        .book:nth-child(5n+4) .book-decoration,
        .book:nth-child(5n+5) .book-decoration {
            background: rgba(255,255,255,0.3);
        }
        
        .book:nth-child(5n+1) .book-decoration::after,
        .book:nth-child(5n+2) .book-decoration::after,
        .book:nth-child(5n+3) .book-decoration::after,
        .book:nth-child(5n+4) .book-decoration::after,
        .book:nth-child(5n+5) .book-decoration::after {
            border-color: rgba(255,255,255,0.3);
        }

        .book:hover {
            transform: translateY(-15px) rotateY(-12deg) rotateX(5deg) scale(1.03);
            box-shadow: 
                inset 5px 0 15px var(--book-spine), 
                inset -2px 0 5px rgba(255,255,255,0.2), 
                15px 25px 30px rgba(0,0,0,0.5);
            z-index: 10;
        }

        .book-title {
            font-family: 'Tiro Bangla', serif;
            font-size: 1.15rem;
            font-weight: bold;
            margin-bottom: 1rem;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
            z-index: 3;
            border-top: 2px double rgba(255,255,255,0.2);
            border-bottom: 1px solid rgba(255,255,255,0.2);
            padding: 10px 0;
            width: 80%;
        }

        .book-author {
            font-size: 0.9rem;
            font-style: italic;
            z-index: 3;
            font-family: 'Tiro Bangla', serif;
            margin-top: 10px;
        }
        
        .book-decoration {
            position: absolute;
            bottom: 20px;
            width: 40px;
            height: 2px;
            z-index: 3;
        }

        .book-decoration::after {
            content: '';
            position: absolute;
            top: -4px;
            left: 50%;
            transform: translateX(-50%);
            width: 10px;
            height: 10px;
            border: 2px solid;
            border-radius: 50%;
            background: transparent;
        }

        /* Pagination */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-top: 3rem;
            flex-wrap: wrap;
        }

        .page-btn {
            background: rgba(139, 69, 19, 0.1);
            border: 1px solid rgba(139, 69, 19, 0.3);
            color: var(--accent);
            padding: 10px 20px;
            border-radius: 2px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Tiro Bangla', serif;
            font-weight: 600;
            font-size: 1.1rem;
        }

        .page-btn:hover:not(:disabled) {
            background: var(--accent);
            color: #f4ecce;
            border-color: var(--accent);
            transform: translateY(-2px);
        }
        
        .page-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            background: transparent;
        }

        .page-info {
            color: var(--text-muted);
            font-size: 1rem;
            font-family: 'Tiro Bangla', serif;
        }

        /* Empty state */
        .no-results {
            grid-column: 1 / -1;
            text-align: center;
            padding: 3rem;
            color: var(--text-muted);
            font-size: 1.5rem;
            font-family: 'Tiro Bangla', serif;
            border: 1px dashed rgba(139, 69, 19, 0.3);
            border-radius: 4px;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 4rem 2rem;
            border-top: 1px solid rgba(139, 69, 19, 0.2);
            margin-top: 4rem;
            color: var(--text-muted);
            background: var(--card-bg);
            font-family: 'Tiro Bangla', serif;
        }
        
        footer p {
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }

        footer a {
            color: var(--accent);
            text-decoration: none;
            transition: color 0.3s ease;
            border-bottom: 1px dotted var(--accent);
        }

        footer a:hover {
            color: var(--accent-hover);
            border-bottom-style: solid;
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 4rem;
            }
            .books-grid {
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
                gap: 2.5rem 1.5rem;
            }
            .book-title {
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>

    <header class="hero">
        <h1>অবসর</h1>
        <p class="tagline">A beautifully curated collection of short Bengali stories, preserved like old pages in a timeless library.</p>
        
        <div class="features-grid">
            <div class="feature-card">
                <h3 style="font-size: 1.5rem; margin-bottom: 10px; opacity: 0.8;">🕰️</h3>
                <h3>Weekly Updates</h3>
                <p>New stories added dynamically every Sunday at 1:30 PM</p>
            </div>
            <div class="feature-card">
                <h3 style="font-size: 1.5rem; margin-bottom: 10px; opacity: 0.8;">📚</h3>
                <h3>Massive Library</h3>
                <p>Over 700+ hand-picked stories from verified sources</p>
            </div>
            <div class="feature-card">
                <h3 style="font-size: 1.5rem; margin-bottom: 10px; opacity: 0.8;">✨</h3>
                <h3>Immersive Reading</h3>
                <p>Distraction-free, vintage paper-styled readable view</p>
            </div>
        </div>

        <div class="cta-buttons">
            <a href="#library" class="cta-button" onclick="document.getElementById('library').scrollIntoView({ behavior: 'smooth' })">Open the Archives</a>
        </div>
    </header>

    <main class="section-container" id="library">
        <h2 class="section-title">Story Archives</h2>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab(event, 'rabibasariya')">রবিবাসরীয়</button>
            <button class="tab-btn" onclick="switchTab(event, 'onnoalo')">অন্য আলো</button>
        </div>

        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="Search stories by title or author..." oninput="handleSearch()">
        </div>

        <div id="booksContainer" class="books-grid">
            <!-- Books injected by JS -->
        </div>

        <div class="pagination" id="paginationControls">
            <button class="page-btn" id="prevBtn" onclick="prevPage()">← Previous</button>
            <span class="page-info" id="pageInfo">Page 1 of 1</span>
            <button class="page-btn" id="nextBtn" onclick="nextPage()">Next →</button>
        </div>

    </main>

    <footer>
        <p>Created automatically for open-source project <a href="https://github.com/deep5050/Abosar" target="_blank">Abosar</a>.</p>
        <p>Source & Copyright: <a href="https://www.anandabazar.com/rabibashoriyo/" target="_blank">Anandabazar Rabibashoriyo</a> & <a href="https://www.prothomalo.com/onnoalo" target="_blank">Prothom Alo - Onnoalo</a></p>
    </footer>

    <script>
        const rabibasariya = __RABI__;
        const onnoalo = __ONNO__;

        let currentTab = 'rabibasariya';
        let currentPage = 1;
        const itemsPerPage = 30;
        let pagedData = [];
        let filteredData = [];

        const booksContainer = document.getElementById('booksContainer');
        const searchInput = document.getElementById('searchInput');
        const pageInfo = document.getElementById('pageInfo');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');

        function switchTab(event, tab) {
            currentTab = tab;
            
            // Update buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            // Reset
            searchInput.value = '';
            currentPage = 1;
            applyData();
        }

        function handleSearch() {
            currentPage = 1;
            applyData();
        }

        function applyData() {
            const currentData = currentTab === 'rabibasariya' ? rabibasariya : onnoalo;
            const query = searchInput.value.toLowerCase().trim();

            if (query) {
                filteredData = currentData.filter(s => 
                    s.title.toLowerCase().includes(query) || 
                    s.author.toLowerCase().includes(query)
                );
            } else {
                filteredData = currentData;
            }

            renderBooks();
        }

        function renderBooks() {
            booksContainer.innerHTML = '';

            if (filteredData.length === 0) {
                booksContainer.innerHTML = '<div class="no-results">No stories found. Try a different search term.</div>';
                updatePagination(0);
                return;
            }

            const totalPages = Math.ceil(filteredData.length / itemsPerPage);
            if (currentPage > totalPages && totalPages > 0) currentPage = totalPages;

            const startIndex = (currentPage - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;
            const currentItems = filteredData.slice(startIndex, endIndex);

            currentItems.forEach(story => {
                const bookHtml = `
                    <a href="${story.link}" class="book" target="_self">
                        <div class="book-texture"></div>
                        <div class="book-title">${story.title}</div>
                        <div class="book-author">${story.author}</div>
                        <div class="book-decoration"></div>
                    </a>
                `;
                booksContainer.innerHTML += bookHtml;
            });

            updatePagination(totalPages);
        }

        function updatePagination(totalPages) {
            if (totalPages === 0) {
                prevBtn.disabled = true;
                nextBtn.disabled = true;
                pageInfo.textContent = `Page 0 of 0`;
                return;
            }

            pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
            prevBtn.disabled = currentPage === 1;
            nextBtn.disabled = currentPage === totalPages;
        }

        function prevPage() {
            if (currentPage > 1) {
                currentPage--;
                renderBooks();
                document.getElementById('library').scrollIntoView({ behavior: 'smooth' });
            }
        }

        function nextPage() {
            const totalPages = Math.ceil(filteredData.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                renderBooks();
                document.getElementById('library').scrollIntoView({ behavior: 'smooth' });
            }
        }

        // Initialize
        applyData();
    </script>
</body>
</html>
"""

html_final = html_template.replace('__RABI__', json.dumps(r_stories)).replace('__ONNO__', json.dumps(o_stories))

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_final)
    
print("Updated index.html to point to generated HTML story files.")
