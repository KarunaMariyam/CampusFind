import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Update CSS for Vintage Scrapbook Aesthetic
css_content = """@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:opsz,ital,wght@9..144,0,300..700;9..144,1,300..700&display=swap');

:root {
    --bg: #F1ECE1; /* Vintage paper beige */
    --card-bg: #FCFAF5;
    --primary: #943A29; /* Deep vintage terracotta */
    --primary-hover: #752C1E;
    --text: #41362D; /* Ink brown */
    --text-light: #7A6F66;
    --border: #D8D0C1; 
    --radius: 8px; /* Less rounded for polaroid/paper look */
    --font-heading: 'Fraunces', serif;
    --font-body: 'DM Sans', sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background-color: var(--bg);
    /* Subtle paper noise texture using SVG base64 */
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
    color: var(--text);
    font-family: var(--font-body);
    line-height: 1.6;
}

/* ---- NAVIGATION ---- */
nav {
    background: var(--card-bg);
    padding: 20px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}
nav h2 { font-family: var(--font-heading); font-style: italic; color: var(--primary); font-size: 28px; }
nav div { display: flex; align-items: center; gap: 15px; }
nav a { color: var(--text); text-decoration: none; font-family: var(--font-heading); font-weight: 600; font-size: 16px; transition: 0.2s; }
nav a:hover { color: var(--primary); }

/* ---- LAYOUT ---- */
.container { max-width: 1200px; margin: 50px auto; padding: 0 24px; }
h1, h2, h3, h4 { font-family: var(--font-heading); color: var(--text); }
h1 { font-size: 46px; font-weight: 700; margin-bottom: 15px; letter-spacing: -1px; }
h2 { font-size: 32px; font-weight: 600; margin-bottom: 20px; font-style: italic; }

/* ---- SCRAPBOOK CARDS ---- */
.card {
    background: var(--card-bg);
    padding: 35px;
    border-radius: var(--radius);
    box-shadow: 2px 4px 12px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.08);
    margin-bottom: 24px;
    border: 1px solid #FFF;
    position: relative;
}

/* Tape effect for top of cards */
.card::before {
    content: '';
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%) rotate(-2deg);
    width: 80px;
    height: 25px;
    background: rgba(255,255,255,0.4);
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-radius: 2px;
}

/* ---- DASHBOARD FIX ---- */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    margin-top: 30px;
}
.dash-card {
    background: var(--card-bg);
    padding: 40px 30px;
    border-radius: var(--radius);
    text-align: center;
    text-decoration: none;
    color: var(--text);
    box-shadow: 2px 4px 12px rgba(0,0,0,0.06);
    border: 10px solid #FFF; /* Polaroid look */
    transition: 0.3s;
}
.dash-card:hover { transform: rotate(2deg) scale(1.02); z-index: 10; box-shadow: 5px 10px 20px rgba(0,0,0,0.1); }
.dash-icon { font-size: 50px; margin-bottom: 15px; }

/* ---- BUTTONS & PILLS ---- */
.btn {
    display: inline-block;
    padding: 12px 24px;
    background: var(--primary);
    color: #FFFDE7;
    border: 1px solid #66271B;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none;
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 16px;
    transition: all 0.2s;
}
.btn:hover { background: var(--primary-hover); transform: translateY(-2px); box-shadow: 2px 4px 8px rgba(0,0,0,0.15); }

.category-pills { display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 24px; }
.pill { padding: 10px 20px; border-radius: 4px; background: transparent; border: 2px solid var(--text); font-family: var(--font-heading); font-weight: 600; font-size: 15px; cursor: pointer; color: var(--text); }
.pill:hover, .pill.active { background: var(--text); color: var(--card-bg); }

/* ---- FORMS & TABLES ---- */
input, select, textarea {
    width: 100%; padding: 15px; border: 2px solid var(--border); border-radius: 4px;
    font-family: var(--font-body); font-size: 15px; background: transparent;
}
input:focus, select:focus, textarea:focus { outline: none; border-color: var(--primary); background: #FFF; }
table { width: 100%; border-collapse: collapse; margin-top: 16px; background: var(--card-bg); border-radius: var(--radius); }
th { border-bottom: 2px solid var(--border); padding: 16px; text-align: left; font-family: var(--font-heading); }
td { border-bottom: 1px solid var(--border); padding: 16px; }

/* ---- PINTEREST MASONRY ---- */
#searchResults { column-count: 3; column-gap: 30px; }
@media (max-width: 900px) { #searchResults { column-count: 2; } }
@media (max-width: 600px) { #searchResults { column-count: 1; } }

.item-card {
    background: #FFF;
    padding: 20px;
    border-radius: 4px;
    break-inside: avoid;
    margin-bottom: 30px;
    box-shadow: 2px 4px 15px rgba(0,0,0,0.06);
    border: 12px solid #FFF; /* Polaroid frame */
    border-bottom: 40px solid #FFF; /* Classic polaroid bottom */
    position: relative;
    transition: 0.3s;
}
.item-card:hover { transform: rotate(-1deg) scale(1.02); }
.item-card h4 { font-family: var(--font-heading); font-size: 22px; margin-bottom: 8px; font-style: italic; }

.badge-lost { background: transparent; color: #943A29; border: 1px solid #943A29; padding: 4px 10px; border-radius: 2px; font-size: 11px; font-family: var(--font-heading); }
.badge-found { background: transparent; color: #2B8A3E; border: 1px solid #2B8A3E; padding: 4px 10px; border-radius: 2px; font-size: 11px; font-family: var(--font-heading); }
"""
with open(os.path.join(base_dir, r"src\main\webapp\css\style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)

# 2. Fix dashboard.jsp missing classes and encoding issues
dashboard_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null) { response.sendRedirect("login.jsp"); return; }
    if("ADMIN".equals(user.getRole())) { response.sendRedirect("admin.jsp"); return; }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=6">
</head>
<body>
    <nav><h2>CIT CampusFind</h2><div><a href="report.jsp">Report Item</a><a href="items.jsp">Browse Items</a><a href="LogoutServlet">Logout</a></div></nav>
    <div class="container">
        <h2>Welcome, <%= user.getName() %>!</h2>
        
        <%
            boolean hasMatches = false;
            try (java.sql.Connection conn = com.campusfind.util.DBConnection.getConnection()) {
                String matchSql = "SELECT DISTINCT f.* FROM items f JOIN items l ON f.category = l.category AND l.type = 'LOST' AND l.user_id = ? WHERE f.type = 'FOUND' AND f.status = 'ACTIVE' LIMIT 2";
                java.sql.PreparedStatement psMatch = conn.prepareStatement(matchSql);
                psMatch.setInt(1, user.getId());
                java.sql.ResultSet rsMatch = psMatch.executeQuery();
                
                StringBuilder matchesHtml = new StringBuilder();
                while(rsMatch.next()) {
                    hasMatches = true;
                    matchesHtml.append("<div class='item-card' style='border: 1px solid #943A29; padding:15px; border-bottom:15px solid #FFF;'>");
                    matchesHtml.append("<h4>💡 Match: ").append(rsMatch.getString("item_name")).append("</h4>");
                    matchesHtml.append("<p>Found at: ").append(rsMatch.getString("location")).append("</p>");
                    matchesHtml.append("<a href='item-details.jsp?id=").append(rsMatch.getInt("id")).append("' class='btn' style='font-size:12px; padding:6px 12px;'>View Details</a>");
                    matchesHtml.append("</div>");
                }
                if(hasMatches) {
        %>
            <div class="card" style="background: #FDF9F2; border: 2px dashed #943A29;">
                <h3 style="color: #943A29;">✨ Smart Connect Alert</h3>
                <p>We found items matching the category of what you lost!</p>
                <div style="display:flex; gap:20px; margin-top:15px;">
                    <%= matchesHtml.toString() %>
                </div>
            </div>
        <% } } catch(Exception e) { e.printStackTrace(); } %>
        
        <div class="dashboard-grid">
            <a href="report.jsp" class="dash-card">
                <div class="dash-icon">📝</div>
                <h4>Report Item</h4>
                <p>Pin up a new report</p>
            </a>
            <a href="items.jsp" class="dash-card">
                <div class="dash-icon">🔍</div>
                <h4>Browse Items</h4>
                <p>Search the archive</p>
            </a>
            <a href="my-reports.jsp" class="dash-card">
                <div class="dash-icon">📋</div>
                <h4>My Reports & Codes</h4>
                <p>View your items & handover codes</p>
            </a>
        </div>
    </div>
</body>
</html>
"""
with open(os.path.join(base_dir, r"src\main\webapp\dashboard.jsp"), "w", encoding="utf-8") as f:
    f.write(dashboard_jsp)

# 3. Handover Code & Resolution System
resolve_servlet = """package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;

@WebServlet("/ResolveItemServlet")
public class ResolveItemServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        int itemId = Integer.parseInt(request.getParameter("itemId"));
        String inputCode = request.getParameter("code");
        
        // Generate the secret code hash expected
        String expectedCode = String.format("%04d", (itemId * 9876) % 10000);
        
        if(expectedCode.equals(inputCode)) {
            try (Connection conn = DBConnection.getConnection()) {
                String sql = "UPDATE items SET status='RETURNED' WHERE id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, itemId);
                ps.executeUpdate();
                response.sendRedirect("item-details.jsp?id=" + itemId + "&success=paired");
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            response.sendRedirect("item-details.jsp?id=" + itemId + "&error=invalidcode");
        }
    }
}
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\ResolveItemServlet.java"), "w", encoding="utf-8") as f:
    f.write(resolve_servlet)

# 4. Update my-reports.jsp to show Handover Code
my_reports = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null) { response.sendRedirect("login.jsp"); return; }
%>
<!DOCTYPE html>
<html>
<head>
    <title>My Reports - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=6">
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="dashboard.jsp">Back to Dashboard</a></nav>
    <div class="container">
        <h2>My Submitted Reports</h2>
        <table>
            <tr><th>Item</th><th>Type</th><th>Status</th><th>Handover Code (Secret)</th></tr>
            <%
                try (Connection conn = DBConnection.getConnection()) {
                    PreparedStatement ps = conn.prepareStatement("SELECT * FROM items WHERE user_id=? ORDER BY id DESC");
                    ps.setInt(1, user.getId());
                    ResultSet rs = ps.executeQuery();
                    while(rs.next()) {
                        int itemId = rs.getInt("id");
                        String secretCode = String.format("%04d", (itemId * 9876) % 10000);
            %>
            <tr>
                <td><strong><%= rs.getString("item_name") %></strong></td>
                <td><%= rs.getString("type") %></td>
                <td><%= rs.getString("status") %></td>
                <td>
                    <% if("ACTIVE".equals(rs.getString("status"))) { %>
                        <span style="background:#333; color:#FFF; padding:4px 8px; border-radius:4px; font-family:monospace; font-size:18px;"><%= secretCode %></span>
                        <br><small>Give this code to the person claiming.</small>
                    <% } else { %>
                        <span style="color:#2B8A3E;">Resolved</span>
                    <% } %>
                </td>
            </tr>
            <% } } catch(Exception e) { e.printStackTrace(); } %>
        </table>
    </div>
</body>
</html>
"""
with open(os.path.join(base_dir, r"src\main\webapp\my-reports.jsp"), "w", encoding="utf-8") as f:
    f.write(my_reports)

# 5. Update item-details.jsp to allow Entering Handover Code + Meetup Pinpoint
item_details_path = os.path.join(base_dir, r"src\main\webapp\item-details.jsp")
with open(item_details_path, "r", encoding="utf-8") as f:
    details_content = f.read()

bluetooth_html = """
        <% if("paired".equals(request.getParameter("success"))) { %>
            <div style="background:#EBFBEE; color:#2B8A3E; padding:15px; border-radius:4px; margin-bottom:20px; font-family:var(--font-heading);">✅ Bluetooth Connection Paired Successfully! Item marked as RETURNED.</div>
        <% } else if("invalidcode".equals(request.getParameter("error"))) { %>
            <div style="background:#FFE8E8; color:#C92A2A; padding:15px; border-radius:4px; margin-bottom:20px; font-family:var(--font-heading);">❌ Pairing Failed. Invalid Handover Code.</div>
        <% } %>
        
        <div class="card" id="poster-area">
"""
details_content = details_content.replace('<div class="card" id="poster-area">', bluetooth_html)

meetup_html = """
            <div style="background:#FFF; padding:25px; border-radius:4px; border:1px solid #D8D0C1; margin-top:20px; text-align:left;">
                <p style="font-size: 18px; color:#666;"><strong>Description:</strong></p>
                <p style="font-size: 20px; margin-top:10px;"><%= rs.getString("description") %></p>
                <hr style="border:0; border-top:1px solid #EEE; margin: 15px 0;">
                <a href="https://www.google.com/maps/search/?api=1&query=Coimbatore+Institute+of+Technology+<%= rs.getString("location").replace(" ", "+") %>" target="_blank" class="btn" style="background:#FFF; color:#943A29; font-size:14px; padding:8px 16px;">📍 Pinpoint Location on Map</a>
            </div>
"""
details_content = details_content.replace('<div style="background:#FFF; padding:25px; border-radius:16px; border:1px solid #F2E8CC; margin-top:20px; text-align:left;">\n                <p style="font-size: 18px; color:#666;"><strong>Description:</strong></p>\n                <p style="font-size: 20px; margin-top:10px;"><%= rs.getString("description") %></p>\n            </div>', meetup_html)

pairing_html = """
            <% if(isLost) { %>
                <button onclick="window.print()" class="btn" style="background:#333;">🖨️ Print Missing Poster</button>
            <% } %>
            
            <% if("ACTIVE".equals(rs.getString("status")) && user != null) { %>
                <form action="ResolveItemServlet" method="POST" style="margin-left:auto; display:flex; gap:10px; align-items:center; background:#FAFAFA; padding:10px; border-radius:4px; border:1px solid #D8D0C1;">
                    <span style="font-size:24px;">📳</span>
                    <div>
                        <p style="margin:0; font-size:12px; font-weight:bold;">Pairing Connection</p>
                        <input type="hidden" name="itemId" value="<%= rs.getInt("id") %>">
                        <input type="text" name="code" placeholder="4-Digit Handover Code" required pattern="\\d{4}" style="padding:8px; width:180px; text-align:center; letter-spacing:3px; font-weight:bold;">
                    </div>
                    <button type="submit" class="btn" style="background:#2B8A3E;">Pair & Resolve</button>
                </form>
            <% } %>
"""
details_content = details_content.replace('<% if(isLost) { %>\n                <button onclick="window.print()" class="btn" style="background:#333;">🖨️ Print Missing Poster</button>\n            <% } %>', pairing_html)

with open(item_details_path, "w", encoding="utf-8") as f:
    f.write(details_content)

print("Scrapbook vintage aesthetic applied. Pinpoint location and Bluetooth Pairing Handover Code system created.")
