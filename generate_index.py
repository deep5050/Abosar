import re
import json

readme_path = "/home/deep/code/Abosar/README.md"
html_path = "/home/deep/code/Abosar/index.html"

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
            rabibasariya.append({'title': t, 'author': a, 'link': l_1.replace('./', '')})
            
        # Onnoalo
        t_a_2 = match.group(3)
        l_2 = match.group(4)
        if t_a_2 and l_2:
            t_a_2 = t_a_2.strip()
            l_2 = l_2.strip()
            parts = [x.strip() for x in t_a_2.split('-', 1)]
            t = parts[0]
            a = parts[1] if len(parts) > 1 else "Unknown"
            onnoalo.append({'title': t, 'author': a, 'link': l_2.replace('./', '')})
            
    return rabibasariya, onnoalo

r_stories, o_stories = parse_readme(readme_path)

html_template = """<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>অবসর (ABOSAR) - Short Bengali Stories</title>
    <link href="https://fonts.googleapis.com/css2?family=Tiro+Bangla:ital@0;1&family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --card-bg: #e2e8f0;
            --book-spine: rgba(0,0,0,0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            overflow-x: hidden;
            scroll-behavior: smooth;
        }

        /* Hero Section */
        .hero {
            min-height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 2rem;
            background: radial-gradient(circle at top, #1e293b, var(--bg-color) 70%);
            position: relative;
        }

        .hero::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 100px;
            background: linear-gradient(to bottom, transparent, var(--bg-color));
        }

        .hero h1 {
            font-family: 'Tiro Bangla', serif;
            font-size: 5rem;
            margin-bottom: 1rem;
            background: linear-gradient(to right, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeInDown 1s ease-out;
        }

        .hero p.tagline {
            font-size: 1.5rem;
            color: var(--text-muted);
            max-width: 600px;
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease-out 0.3s both;
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
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            padding: 1.5rem 2rem;
            border-radius: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            transition: transform 0.3s ease, border-color 0.3s ease;
            max-width: 250px;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            border-color: rgba(255, 255, 255, 0.3);
        }

        .feature-card h3 {
            font-size: 1.2rem;
            color: #fff;
            margin-bottom: 0.5rem;
        }

        .feature-card p {
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        .cta-buttons {
            margin-top: 2rem;
            z-index: 10;
        }

        .cta-button {
            display: inline-block;
            padding: 1rem 2.5rem;
            background: var(--accent);
            color: white;
            text-decoration: none;
            border-radius: 2rem;
            font-weight: 600;
            transition: background 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }

        .cta-button:hover {
            background: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
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
            color: #fff;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 3px;
            background: var(--accent);
            border-radius: 2px;
        }

        .tabs {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }

        .tab-btn {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.2);
            color: var(--text-main);
            padding: 0.75rem 2.5rem;
            border-radius: 2rem;
            font-size: 1.1rem;
            font-family: 'Tiro Bangla', serif;
            cursor: pointer;
            transition: all 0.3s ease;
            outline: none;
        }

        .tab-btn.active {
            background: var(--accent);
            border-color: var(--accent);
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }

        .tab-btn:hover:not(.active) {
            background: rgba(255,255,255,0.1);
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
            border-radius: 2rem;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.05);
            color: white;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .search-input:focus {
            border-color: var(--accent);
            background: rgba(255,255,255,0.1);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
        }

        .search-input::placeholder {
            color: rgba(255,255,255,0.4);
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

        /* Book CSS */
        .book {
            position: relative;
            width: 100%;
            aspect-ratio: 2 / 3.1;
            background: #fdfbf7;
            border-radius: 4px 12px 12px 4px;
            box-shadow: 
                inset 5px 0 15px var(--book-spine), 
                inset -2px 0 5px rgba(255,255,255,0.8), 
                5px 10px 15px rgba(0,0,0,0.5);
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
        }

        .book::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            width: 16px;
            background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.4) 30%, rgba(0,0,0,0.15) 100%);
            border-radius: 4px 0 0 4px;
            z-index: 2;
        }

        /* Page edges */
        .book::after {
            content: '';
            position: absolute;
            top: 4px;
            bottom: 4px;
            right: -6px;
            width: 6px;
            background: repeating-linear-gradient(
                to bottom,
                #dfdacd 0,
                #dfdacd 1px,
                #fdfbf7 1px,
                #fdfbf7 3px
            );
            border-radius: 0 4px 4px 0;
            transform: translateZ(-1px);
            box-shadow: inset 1px 0 2px rgba(0,0,0,0.1);
        }

        /* Different book colors to make it look dynamic */
        .book:nth-child(5n+1) { background: #fdfbf7; } /* Cream */
        .book:nth-child(5n+2) { background: #e2e8f0; } /* Light Grayish Blue */
        .book:nth-child(5n+3) { background: #fef3c7; } /* Warm Yellow */
        .book:nth-child(5n+4) { background: #fce7f3; } /* Light Pink */
        .book:nth-child(5n+5) { background: #e0f2fe; } /* Light Blue */

        /* Optional texture overlay */
        .book-texture {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100" preserveAspectRatio="none"><filter id="noiseFilter"><feTurbulence type="fractalNoise" baseFrequency="1" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100" height="100" filter="url(%23noiseFilter)" opacity="0.05"/></svg>');
            mix-blend-mode: multiply;
            z-index: 1;
            border-radius: 4px 12px 12px 4px;
            pointer-events: none;
        }

        .book:hover {
            transform: translateY(-15px) rotateY(-12deg) rotateX(5deg) scale(1.03);
            box-shadow: 
                inset 5px 0 15px var(--book-spine), 
                inset -2px 0 5px rgba(255,255,255,0.8), 
                15px 25px 30px rgba(0,0,0,0.6);
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
            color: #1e293b;
            text-shadow: 0 1px 1px rgba(255,255,255,0.5);
        }

        .book-author {
            font-size: 0.85rem;
            color: #475569;
            font-style: italic;
            z-index: 3;
            font-family: 'Tiro Bangla', serif;
        }
        
        .book-decoration {
            position: absolute;
            bottom: 20px;
            width: 40px;
            height: 2px;
            background: rgba(0,0,0,0.2);
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
            border: 2px solid rgba(0,0,0,0.2);
            border-radius: 50%;
            background: inherit;
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
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }

        .page-btn:hover:not(:disabled) {
            background: var(--accent);
            border-color: var(--accent);
            transform: translateY(-2px);
        }
        
        .page-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .page-info {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        /* Empty state */
        .no-results {
            grid-column: 1 / -1;
            text-align: center;
            padding: 3rem;
            color: var(--text-muted);
            font-size: 1.2rem;
            font-family: 'Tiro Bangla', serif;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 4rem 2rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 4rem;
            color: var(--text-muted);
            background: rgba(0,0,0,0.2);
        }
        
        footer p {
            margin-bottom: 0.5rem;
        }

        footer a {
            color: var(--accent);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        footer a:hover {
            color: var(--accent-hover);
            text-decoration: underline;
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
                font-size: 3.5rem;
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
        <p class="tagline">A beautifully curated collection of short Bengali stories scraped weekly from leading eMagazines.</p>
        
        <div class="features-grid">
            <div class="feature-card">
                <h3 style="font-size: 1.5rem; margin-bottom: 10px;">🕰️</h3>
                <h3>Weekly Updates</h3>
                <p>New stories added dynamically every Sunday at 1:30 PM</p>
            </div>
            <div class="feature-card">
                <h3 style="font-size: 1.5rem; margin-bottom: 10px;">📚</h3>
                <h3>Massive Library</h3>
                <p>Over 700+ hand-picked stories from verified sources</p>
            </div>
            <div class="feature-card">
                <h3 style="font-size: 1.5rem; margin-bottom: 10px;">✨</h3>
                <h3>Immersive Reading</h3>
                <p>Distraction-free, minimal and paper-styled readable view</p>
            </div>
        </div>

        <div class="cta-buttons">
            <a href="#library" class="cta-button" onclick="document.getElementById('library').scrollIntoView({ behavior: 'smooth' })">Open the Library</a>
        </div>
    </header>

    <main class="section-container" id="library">
        <h2 class="section-title">Story Library</h2>
        
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
    
print(f"Generated successfully with {len(r_stories)} Rabibasariya and {len(o_stories)} Onno Alo stories.")
