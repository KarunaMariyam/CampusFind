import os
import re

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Update CSS for Modern, Clean "Aesthetic Cool" (No Cursive)
css_content = """@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #FFFDF4; /* Very light aesthetic Butter Yellow */
    --card-bg: #FFFFFF;
    --primary: #E05D3A; /* Vibrant aesthetic terracotta */
    --primary-hover: #C24828;
    --text: #1A1A1A; /* Crisp almost-black */
    --text-light: #737373;
    --border: #F0EAD6; 
    --radius: 20px; /* Smooth modern curves */
    --font-main: 'Plus Jakarta Sans', sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background-color: var(--bg);
    color: var(--text);
    font-family: var(--font-main);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

/* ---- NAVIGATION ---- */
nav {
    background: var(--card-bg);
    padding: 18px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}
nav h2 { font-weight: 800; color: var(--primary); font-size: 24px; letter-spacing: -0.5px; }
nav div { display: flex; align-items: center; gap: 20px; }
nav a { color: var(--text); text-decoration: none; font-weight: 600; font-size: 15px; transition: 0.2s; }
nav a:hover { color: var(--primary); }

/* ---- LAYOUT ---- */
.container { max-width: 1200px; margin: 40px auto; padding: 0 24px; }
h1, h2, h3, h4 { color: var(--text); font-weight: 800; letter-spacing: -0.5px; }
h1 { font-size: 42px; margin-bottom: 15px; letter-spacing: -1.5px; }
h2 { font-size: 28px; margin-bottom: 20px; }

/* ---- CARDS ---- */
.card {
    background: var(--card-bg);
    padding: 35px;
    border-radius: var(--radius);
    box-shadow: 0 8px 30px rgba(0,0,0,0.04);
    margin-bottom: 24px;
    border: 1px solid #FFF;
}

/* ---- DASHBOARD GRID ---- */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    margin-top: 30px;
}
.dash-card {
    background: var(--card-bg);
    padding: 35px 30px;
    border-radius: var(--radius);
    text-align: center;
    text-decoration: none;
    color: var(--text);
    box-shadow: 0 8px 30px rgba(0,0,0,0.04);
    border: 1px solid var(--border);
    transition: 0.3s;
}
.dash-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.08); border-color: var(--primary); }
.dash-icon { font-size: 46px; margin-bottom: 15px; }

/* ---- BUTTONS & PILLS ---- */
.btn {
    display: inline-block;
    padding: 14px 28px;
    background: var(--primary);
    color: #FFF;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    text-decoration: none;
    font-weight: 700;
    font-size: 15px;
    transition: all 0.2s;
    text-align: center;
}
.btn:hover { background: var(--primary-hover); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(224, 93, 58, 0.25); }

.category-pills { display: flex; gap: 12px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 24px; }
.pill { padding: 12px 24px; border-radius: 30px; background: #FFF; border: 2px solid var(--border); font-weight: 700; font-size: 14px; cursor: pointer; color: var(--text); transition: 0.2s; }
.pill:hover, .pill.active { background: var(--text); border-color: var(--text); color: #FFF; }

/* ---- FORMS & TABLES ---- */
input, select, textarea {
    width: 100%; padding: 16px; border: 2px solid var(--border); border-radius: 12px;
    font-family: var(--font-main); font-size: 15px; background: #FAFAFA; transition: 0.2s;
}
input:focus, select:focus, textarea:focus { outline: none; border-color: var(--primary); background: #FFF; box-shadow: 0 0 0 4px rgba(224, 93, 58, 0.1); }
table { width: 100%; border-collapse: collapse; margin-top: 16px; background: var(--card-bg); border-radius: var(--radius); overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }
th { background: #FAFAFA; border-bottom: 2px solid var(--border); padding: 16px; text-align: left; }
td { border-bottom: 1px solid var(--border); padding: 16px; }

/* ---- PINTEREST MASONRY ---- */
#searchResults { column-count: 3; column-gap: 24px; }
@media (max-width: 900px) { #searchResults { column-count: 2; } }
@media (max-width: 600px) { #searchResults { column-count: 1; } }

.item-card {
    background: var(--card-bg);
    padding: 24px;
    border-radius: var(--radius);
    break-inside: avoid;
    margin-bottom: 24px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.04);
    border: 1px solid var(--border);
    transition: 0.3s;
}
.item-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.08); }
.item-card h4 { font-size: 20px; margin-bottom: 8px; font-weight: 800; }

.badge-lost { background: #FFF0F0; color: #D9534F; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 800; }
.badge-found { background: #EBFBEE; color: #2B8A3E; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 800; }
"""
with open(os.path.join(base_dir, r"src\main\webapp\css\style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)


# 2. Update dashboard.jsp to add a MASSIVE Aesthetic Welcome Banner
dashboard_path = os.path.join(base_dir, r"src\main\webapp\dashboard.jsp")
with open(dashboard_path, "r", encoding="utf-8") as f:
    dash_content = f.read()

# Replace the old <h2>Welcome...</h2> with the new massive banner
banner_html = """
        <!-- Massive Aesthetic Welcome Banner -->
        <div style="background: linear-gradient(135deg, #E05D3A, #F28C6D); padding: 60px 40px; border-radius: 24px; color: #FFF; margin-bottom: 40px; text-align: center; box-shadow: 0 15px 40px rgba(224, 93, 58, 0.25); position: relative; overflow: hidden;">
            <div style="position:absolute; top:-50px; right:-20px; font-size:200px; opacity:0.1; line-height:1;">✨</div>
            <h1 style="font-size: 56px; color: #FFF; margin: 0; letter-spacing: -2px; font-weight:800;">Welcome, <%= user.getName() %>! 👋</h1>
            <p style="font-size: 20px; opacity: 0.95; margin-top: 15px; font-weight:500;">Ready to connect your lost and found items on campus.</p>
        </div>
"""
# Use regex to replace <h2>Welcome, <%= user.getName() %>!</h2>
dash_content = re.sub(r'<h2>Welcome, <%= user\.getName\(\) %>!</h2>', banner_html, dash_content)

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(dash_content)


# 3. Cache buster update
import glob
jsp_files = glob.glob(os.path.join(base_dir, "src/main/webapp/*.jsp"))
for jsp in jsp_files:
    with open(jsp, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'href="css/style\.css(\?v=\d+)?"', 'href="css/style.css?v=8"', content)
    with open(jsp, "w", encoding="utf-8") as f:
        f.write(content)

print("Cursive removed. Modern cool Plus Jakarta Sans applied. Massive dashboard welcome banner added.")
