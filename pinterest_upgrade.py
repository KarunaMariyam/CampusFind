import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Ultra-Minimalist Pinterest CSS
css_content = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #FCFBF9; /* Ultra-light warm off-white */
    --card-bg: #FFFFFF;
    --primary: #E60023; /* Pinterest Red */
    --primary-hover: #AD081B;
    --text: #111111;
    --text-light: #767676;
    --border: #EFEFEF;
    --radius: 24px;
    --font-body: 'Inter', sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    line-height: 1.5;
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
}

nav h2 {
    font-weight: 700;
    color: var(--primary);
    font-size: 20px;
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
    transition: background 0.2s;
}

nav a:hover { background: #F0F0F0; }
.nav-btn { background: var(--text); color: #fff; }
.nav-btn:hover { background: #000; color: #fff; }

/* ---- LAYOUT ---- */
.container { max-width: 1200px; margin: 40px auto; padding: 0 24px; }
h1 { font-size: 40px; font-weight: 700; letter-spacing: -1px; margin-bottom: 15px; }
h2 { font-size: 28px; font-weight: 600; margin-bottom: 20px; letter-spacing: -0.5px; }
h3 { font-size: 20px; font-weight: 600; margin-bottom: 12px; }

/* ---- CARDS ---- */
.card {
    background: var(--card-bg);
    padding: 32px;
    border-radius: var(--radius);
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    margin-bottom: 24px;
}

/* ---- BUTTONS & PILLS ---- */
.btn {
    display: inline-block;
    padding: 12px 24px;
    background: var(--primary);
    color: #fff;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    text-decoration: none;
    font-weight: 600;
    font-size: 15px;
    transition: all 0.2s ease;
    text-align: center;
}
.btn:hover { background: var(--primary-hover); }

.category-pills {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    overflow-x: auto;
    padding-bottom: 8px;
}
.pill {
    padding: 12px 20px;
    border-radius: 30px;
    background: #E9E9E9;
    border: none;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    color: var(--text);
    white-space: nowrap;
}
.pill:hover { background: #D0D0D0; }
.pill.active { background: var(--text); color: #fff; }

/* ---- FORMS ---- */
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 600; font-size: 14px; }
.form-group input, .form-group select, .form-group textarea {
    width: 100%;
    padding: 16px;
    border: 2px solid var(--border);
    border-radius: 16px;
    font-family: var(--font-body);
    font-size: 15px;
    transition: all 0.2s;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
    outline: none;
    border-color: #999;
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
    position: relative;
    overflow: hidden;
}
.item-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); }

.item-card-emoji {
    font-size: 48px;
    margin-bottom: 15px;
    display: block;
    text-align: center;
    background: #F8F8F8;
    padding: 30px;
    border-radius: 16px;
}

.item-card h4 { font-size: 18px; margin-bottom: 8px; font-weight: 600; }
.item-card p { color: var(--text-light); font-size: 14px; margin-bottom: 8px; }

.badge-lost { background: #FFE8E8; color: #C92A2A; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.badge-found { background: #EBFBEE; color: #2B8A3E; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }

.action-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; }
.share-btn { background: #F1F1F1; color: var(--text); padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 13px; text-decoration: none; cursor: pointer; border: none; }
.share-btn:hover { background: #E0E0E0; }

table { width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 16px; }
th { background: #F8F8F8; padding: 16px; text-align: left; font-weight: 600; }
td { padding: 16px; border-top: 1px solid var(--border); }
tr:hover td { background: #FAFAFA; }
"""
with open(os.path.join(base_dir, r"src\main\webapp\css\style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)


# 2. Update Items Page (AJAX Categories + Share Feature)
items_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>Browse Items - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=3">
    <script src="js/script.js"></script>
</head>
<body onload="searchItems('')">
    <nav><h2>CIT CampusFind</h2><div><a href="index.jsp">Home</a></div></nav>
    <div class="container">
        <h2>Explore Reports</h2>
        
        <!-- Category Filters -->
        <div class="category-pills">
            <button class="pill active" onclick="setCategory(this, '')">All</button>
            <button class="pill" onclick="setCategory(this, 'Electronics')">💻 Electronics</button>
            <button class="pill" onclick="setCategory(this, 'Personal')">🎒 Personal</button>
            <button class="pill" onclick="setCategory(this, 'Documents')">📚 Documents</button>
            <button class="pill" onclick="setCategory(this, 'Other')">✨ Other</button>
        </div>

        <div class="form-group">
            <input type="text" id="searchInput" onkeyup="triggerSearch()" placeholder="Search items (e.g., Wallet, Calculator)...">
        </div>

        <!-- Pinterest Masonry Grid -->
        <div id="searchResults">
            <!-- Filled via AJAX -->
        </div>
    </div>
</body>
</html>
"""
with open(os.path.join(base_dir, r"src\main\webapp\items.jsp"), "w", encoding="utf-8") as f:
    f.write(items_jsp)


# 3. Update JavaScript for Smart Emojis, Categories, and Sharing
script_js = """
let currentCategory = "";

function setCategory(btn, category) {
    // Update active pill styling
    document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    
    currentCategory = category;
    triggerSearch();
}

function triggerSearch() {
    let query = document.getElementById("searchInput").value;
    searchItems(query);
}

function getEmojiForCategory(category) {
    if (category === 'Electronics') return '💻';
    if (category === 'Personal') return '🎒';
    if (category === 'Documents') return '📚';
    return '✨';
}

function copyShareLink(id) {
    const url = window.location.origin + '/CampusFind/item-details.jsp?id=' + id;
    navigator.clipboard.writeText(url).then(() => {
        alert("Link copied! Share it with your friends.");
    });
}

function searchItems(query) {
    let url = 'SearchItemServlet?q=' + encodeURIComponent(query) + '&cat=' + encodeURIComponent(currentCategory);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let html = "";
            if(data.length === 0) {
                html = "<p style='grid-column: 1/-1; text-align:center; color:#999;'>No items found.</p>";
            } else {
                data.forEach(item => {
                    let typeClass = item.type === 'LOST' ? 'badge-lost' : 'badge-found';
                    let emoji = getEmojiForCategory(item.category);
                    
                    html += `<div class="item-card">
                        <div class="item-card-emoji">${emoji}</div>
                        <h4>${item.item_name} <span class="${typeClass}">${item.type}</span></h4>
                        <p><strong>📍</strong> ${item.location}</p>
                        <p><strong>🕒</strong> ${item.date_reported}</p>
                        <div class="action-bar">
                            <a href="item-details.jsp?id=${item.id}" class="btn" style="padding: 8px 16px;">View</a>
                            <button onclick="copyShareLink(${item.id})" class="share-btn">🔗 Share</button>
                        </div>
                    </div>`;
                });
            }
            document.getElementById("searchResults").innerHTML = html;
        });
}

function loadGuidelines() {
    fetch('GuidelinesServlet')
        .then(response => response.text())
        .then(html => {
            document.getElementById('guidelines-list').innerHTML = html;
        });
}
"""
with open(os.path.join(base_dir, r"src\main\webapp\js\script.js"), "w", encoding="utf-8") as f:
    f.write(script_js)


# 4. Update SearchItemServlet to support Category Filtering
search_servlet = """package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import org.json.JSONArray;
import org.json.JSONObject;

@WebServlet("/SearchItemServlet")
public class SearchItemServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String query = request.getParameter("q");
        String category = request.getParameter("cat");
        if (query == null) query = "";
        if (category == null) category = "";
        
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        JSONArray itemsArray = new JSONArray();
        
        try (Connection conn = DBConnection.getConnection()) {
            String sql = "SELECT * FROM items WHERE item_name LIKE ? AND status='ACTIVE'";
            if (!category.isEmpty()) {
                sql += " AND category = ?";
            }
            sql += " ORDER BY date_reported DESC";
            
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, "%" + query + "%");
            if (!category.isEmpty()) {
                ps.setString(2, category);
            }
            
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                JSONObject obj = new JSONObject();
                obj.put("id", rs.getInt("id"));
                obj.put("item_name", rs.getString("item_name"));
                obj.put("type", rs.getString("type"));
                obj.put("category", rs.getString("category"));
                obj.put("location", rs.getString("location"));
                obj.put("date_reported", rs.getString("date_reported"));
                itemsArray.put(obj);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        out.print(itemsArray.toString());
        out.flush();
    }
}
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\SearchItemServlet.java"), "w") as f:
    f.write(search_servlet)


print("Pinterest aesthetic upgrade applied!")
