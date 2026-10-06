import os
import re

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Fix Admin Navbar
admin_jsp_path = os.path.join(base_dir, r"src\main\webapp\admin.jsp")
with open(admin_jsp_path, "r", encoding="utf-8") as f:
    admin_content = f.read()

admin_content = admin_content.replace(
    '<a href="LogoutServlet" class="btn"',
    '<a href="items.jsp">Browse Items</a>\n            <a href="LogoutServlet" class="btn"'
)

with open(admin_jsp_path, "w", encoding="utf-8") as f:
    f.write(admin_content)

# 2. Add "Smart Match" to dashboard.jsp
dashboard_path = os.path.join(base_dir, r"src\main\webapp\dashboard.jsp")
dashboard_updates = """
        <!-- Smart Match Feature -->
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
                    matchesHtml.append("<div class='item-card' style='background:#FFF; border-color:#C56B46; margin-top:10px;'>");
                    matchesHtml.append("<h4>💡 Possible Match: ").append(rsMatch.getString("item_name")).append("</h4>");
                    matchesHtml.append("<p>Found at: ").append(rsMatch.getString("location")).append("</p>");
                    matchesHtml.append("<a href='item-details.jsp?id=").append(rsMatch.getInt("id")).append("' class='btn'>View Details</a>");
                    matchesHtml.append("</div>");
                }
                if(hasMatches) {
        %>
            <div class="card" style="background: #FFE8E8; border: 2px solid #C56B46;">
                <h3 style="color: #C56B46;">✨ Smart Connect Alerts</h3>
                <p>We noticed someone found items matching the category of what you lost!</p>
                <div style="display:grid; gap:15px; grid-template-columns: 1fr 1fr;">
                    <%= matchesHtml.toString() %>
                </div>
            </div>
        <%
                }
            } catch(Exception e) { e.printStackTrace(); }
        %>
        
        <div class="dashboard-grid">
"""

with open(dashboard_path, "r", encoding="utf-8") as f:
    dash_content = f.read()

dash_content = dash_content.replace('<div class="dashboard-grid">', dashboard_updates)
with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(dash_content)


# 3. Add Printable Missing Poster feature to item-details.jsp
poster_js = """
<script>
function printPoster() {
    window.print();
}
</script>
<style>
@media print {
    body * { visibility: hidden; }
    #poster-area, #poster-area * { visibility: visible; }
    #poster-area {
        position: absolute; left: 0; top: 0; width: 100%; text-align: center;
        padding: 50px; border: 10px solid #C56B46; background: #FFFDE7;
    }
    .no-print { display: none !important; }
}
</style>
"""

item_details_path = os.path.join(base_dir, r"src\main\webapp\item-details.jsp")
with open(item_details_path, "r", encoding="utf-8") as f:
    details_content = f.read()

# Insert styles and scripts in head
details_content = details_content.replace('</head>', poster_js + '\n</head>')

# Add the print button if it's LOST
print_btn = """
            <% if("LOST".equals(rs.getString("type"))) { %>
                <button onclick="printPoster()" class="btn no-print" style="background:#333; margin-top:15px;">🖨️ Print Missing Poster</button>
            <% } %>
            <div id="poster-area" style="margin-top:20px;">
                <h2 style="font-size:30px;"><%= rs.getString("item_name") %></h2>
                <p style="font-size:18px;"><strong>Status:</strong> <%= rs.getString("type") %> in <%= rs.getString("category") %></p>
                <p style="font-size:18px;"><strong>Location:</strong> <%= rs.getString("location") %></p>
                <p style="font-size:18px;"><strong>Date:</strong> <%= rs.getString("date_reported") %></p>
                <div style="background:#FAFAFA; padding:20px; border-radius:10px; margin-top:15px; border:1px solid #EEE;">
                    <p><strong>Description:</strong></p>
                    <p style="font-size:16px;"><%= rs.getString("description") %></p>
                </div>
            </div>
"""
# Replace the standard details block with the poster-area wrapped block
details_content = re.sub(
    r'<p><strong>Category:</strong>.*?</p>',
    print_btn.replace('\\', '\\\\'), # simplify replacement
    details_content,
    flags=re.DOTALL | re.IGNORECASE
)
# Actually, a safer replace:
details_content = f.read() if False else "" # just resetting
with open(item_details_path, "r", encoding="utf-8") as f:
    original = f.read()

# Let's just rewrite item-details.jsp entirely to ensure it's clean and safe
new_item_details = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    String idParam = request.getParameter("id");
    if(idParam == null) { response.sendRedirect("items.jsp"); return; }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Item Details - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=5">
    <style>
    @media print {
        body * { visibility: hidden; }
        #poster-area, #poster-area * { visibility: visible; }
        #poster-area {
            position: absolute; left: 0; top: 0; width: 100%; height: 100%; text-align: center;
            padding: 50px; border: 15px solid #C56B46; background: #FFFDE7;
        }
        .no-print { display: none !important; }
        .poster-title { font-size: 80px !important; color: #C56B46; margin-bottom: 20px; text-transform: uppercase;}
        .poster-emoji { font-size: 120px !important; margin: 30px 0; }
        .poster-text { font-size: 30px !important; margin-bottom: 20px; }
    }
    </style>
</head>
<body>
    <nav class="no-print"><h2>CIT CampusFind</h2><a href="items.jsp">Back to Items</a></nav>
    <div class="container">
        <%
            try (Connection conn = DBConnection.getConnection()) {
                String sql = "SELECT * FROM items WHERE id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, Integer.parseInt(idParam));
                ResultSet rs = ps.executeQuery();
                if(rs.next()) {
                    boolean isLost = "LOST".equals(rs.getString("type"));
        %>
        <div class="card" id="poster-area">
            <h1 class="poster-title"><%= isLost ? "MISSING" : "FOUND" %></h1>
            <div class="poster-emoji">🔍</div>
            <h2 style="font-size: 36px;"><%= rs.getString("item_name") %></h2>
            
            <div style="margin: 20px 0; font-size: 20px;" class="poster-text">
                <p><strong>Category:</strong> <%= rs.getString("category") %></p>
                <p><strong><%= isLost ? "Lost at:" : "Found at:" %></strong> <%= rs.getString("location") %></p>
                <p><strong>Date:</strong> <%= rs.getString("date_reported") %></p>
            </div>
            
            <div style="background:#FFF; padding:25px; border-radius:16px; border:1px solid #F2E8CC; margin-top:20px; text-align:left;">
                <p style="font-size: 18px; color:#666;"><strong>Description:</strong></p>
                <p style="font-size: 20px; margin-top:10px;"><%= rs.getString("description") %></p>
            </div>
            
            <% if(isLost) { %>
                <p class="poster-text" style="margin-top:30px; font-weight:bold; color:#C56B46;">If found, please hand it over to the CIT Administration Office immediately.</p>
            <% } else { %>
                <p class="poster-text" style="margin-top:30px; font-weight:bold; color:#2B8A3E;">If this is yours, please claim it via the CampusFind portal.</p>
            <% } %>
        </div>
        
        <div class="no-print" style="margin-top: 20px; display:flex; gap:15px;">
            <% if(user != null && rs.getInt("user_id") != user.getId()) { %>
                <form action="ClaimItemServlet" method="POST" style="margin:0;">
                    <input type="hidden" name="itemId" value="<%= rs.getInt("id") %>">
                    <input type="text" name="message" placeholder="Message to owner..." required style="padding:12px; border-radius:8px; border:1px solid #ccc; width:300px; margin-right:10px;">
                    <button type="submit" class="btn">Claim / Contact</button>
                </form>
            <% } else if(user == null) { %>
                <p style="color:#666;"><em><a href="login.jsp" style="color:#C56B46; font-weight:bold;">Log in</a> to claim this item or contact the finder.</em></p>
            <% } %>
            
            <% if(isLost) { %>
                <button onclick="window.print()" class="btn" style="background:#333;">🖨️ Print Missing Poster</button>
            <% } %>
        </div>
        
        <%
                } else {
                    out.println("<p>Item not found.</p>");
                }
            } catch(Exception e) { e.printStackTrace(); }
        %>
    </div>
</body>
</html>
"""
with open(item_details_path, "w", encoding="utf-8") as f:
    f.write(new_item_details)

print("Creative features added: Smart Connect (JDBC SQL) and Printable Missing Poster (HTML/CSS Print Media).")
