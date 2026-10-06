import os
import glob

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"
css_path = os.path.join(base_dir, r"src\main\webapp\css\style.css")

# 1. Write the Perfect Butter Yellow + Pinterest CSS
css_content = """@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:opsz,wght@9..144,300..700&display=swap');

:root {
    --bg: #FFFDE7; /* Beautiful Butter Yellow */
    --card-bg: #FFFFFF;
    --primary: #C56B46; /* Terracotta Accent */
    --primary-hover: #AD5A38;
    --text: #333333; /* Soft Black */
    --text-light: #666666;
    --border: #F2E8CC; /* Slightly darker warm border */
    --radius: 24px;
    --font-heading: 'Fraunces', serif; /* Aesthetic Serif Font */
    --font-body: 'DM Sans', sans-serif; /* Clean Body Font */
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

/* ---- NAVIGATION ---- */
nav {
    background: var(--card-bg);
    padding: 16px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

nav h2 {
    font-family: var(--font-heading);
    font-weight: 700;
    color: var(--primary);
    font-size: 26px;
    letter-spacing: -0.5px;
}

nav div { display: flex; align-items: center; gap: 10px; }

nav a {
    color: var(--text);
    text-decoration: none;
    font-weight: 600;
    font-size: 15px;
    padding: 10px 16px;
    border-radius: 24px;
    transition: all 0.2s;
}

nav a:hover { background: #FFFDE7; color: var(--primary); }
.nav-btn { background: var(--primary); color: #fff; }
.nav-btn:hover { background: var(--primary-hover); color: #fff; }

/* ---- LAYOUT & TYPOGRAPHY ---- */
.container { max-width: 1200px; margin: 40px auto; padding: 0 24px; }
h1 { font-family: var(--font-heading); font-size: 42px; font-weight: 700; margin-bottom: 15px; color: #222; }
h2 { font-family: var(--font-heading); font-size: 30px; font-weight: 600; margin-bottom: 20px; color: #333; }
h3 { font-family: var(--font-heading); font-size: 22px; font-weight: 600; margin-bottom: 12px; }

/* ---- CARDS ---- */
.card {
    background: var(--card-bg);
    padding: 35px;
    border-radius: var(--radius);
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
    margin-bottom: 24px;
    border: 1px solid var(--border);
}

/* ---- BUTTONS & PILLS ---- */
.btn {
    display: inline-block;
    padding: 14px 28px;
    background: var(--primary);
    color: #fff;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    text-decoration: none;
    font-weight: 600;
    font-size: 15px;
    font-family: var(--font-body);
    transition: all 0.2s ease;
    text-align: center;
}
.btn:hover { background: var(--primary-hover); transform: translateY(-2px); box-shadow: 0 4px 15px rgba(197, 107, 70, 0.2); }

.category-pills {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    overflow-x: auto;
    padding-bottom: 8px;
}
.pill {
    padding: 12px 24px;
    border-radius: 30px;
    background: #FFFFFF;
    border: 2px solid var(--border);
    font-weight: 600;
    font-family: var(--font-body);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    color: var(--text);
    white-space: nowrap;
}
.pill:hover { border-color: var(--primary); color: var(--primary); }
.pill.active { background: var(--primary); color: #fff; border-color: var(--primary); }

/* ---- FORMS ---- */
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 600; font-size: 15px; }
.form-group input, .form-group select, .form-group textarea {
    width: 100%;
    padding: 16px;
    border: 2px solid var(--border);
    border-radius: 16px;
    font-family: var(--font-body);
    font-size: 15px;
    transition: all 0.2s;
    background: #FAFAFA;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
    outline: none;
    border-color: var(--primary);
    background: #FFFFFF;
    box-shadow: 0 0 0 4px rgba(197, 107, 70, 0.1);
}

/* ---- PINTEREST MASONRY GRID ---- */
#searchResults {
    column-count: 3;
    column-gap: 24px;
}
@media (max-width: 900px) { #searchResults { column-count: 2; } }
@media (max-width: 600px) { #searchResults { column-count: 1; } }

.item-card {
    background: var(--card-bg);
    padding: 24px;
    border-radius: var(--radius);
    transition: all 0.2s ease;
    break-inside: avoid;
    margin-bottom: 24px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}
.item-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); }

.item-card-emoji {
    font-size: 48px;
    margin-bottom: 15px;
    display: block;
    text-align: center;
    background: var(--bg);
    padding: 30px;
    border-radius: 16px;
}

.item-card h4 { font-family: var(--font-heading); font-size: 20px; margin-bottom: 8px; font-weight: 600; }
.item-card p { color: var(--text-light); font-size: 14px; margin-bottom: 8px; }

.badge-lost { background: #FFE8E8; color: #C92A2A; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; }
.badge-found { background: #EBFBEE; color: #2B8A3E; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; }

.action-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; }
.share-btn { background: var(--bg); color: var(--text); padding: 10px 18px; border-radius: 20px; font-weight: 600; font-size: 13px; font-family: var(--font-body); cursor: pointer; border: none; transition: 0.2s; }
.share-btn:hover { background: #F0EAD6; color: var(--primary); }

/* ---- TABLES ---- */
table { width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 16px; border: 1px solid var(--border); border-radius: 16px; overflow: hidden; }
th { background: #FAFAFA; padding: 16px; text-align: left; font-weight: 600; font-family: var(--font-body); }
td { padding: 16px; border-top: 1px solid var(--border); background: #FFFFFF; }
tr:hover td { background: var(--bg); }
"""

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

# 2. Add Cache Buster ?v=5 to all JSPs so the browser updates instantly
jsp_files = glob.glob(os.path.join(base_dir, "src/main/webapp/*.jsp"))
for jsp in jsp_files:
    with open(jsp, "r", encoding="utf-8") as f:
        content = f.read()
    
    import re
    # Find style.css references and replace them with ?v=5
    content = re.sub(r'href="css/style\.css(\?v=\d+)?"', 'href="css/style.css?v=5"', content)
    
    with open(jsp, "w", encoding="utf-8") as f:
        f.write(content)

print("Butter Yellow Aesthetic CSS combined with Pinterest Masonry applied!")
