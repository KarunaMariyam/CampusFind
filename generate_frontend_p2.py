import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

web_files = {
    r"src\main\webapp\items.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection" %>
<!DOCTYPE html>
<html>
<head>
    <title>Browse Items - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <h2>Reported Items</h2>
        <div id="searchResults">
        <%
            try (Connection conn = DBConnection.getConnection()) {
                String sql = "SELECT * FROM items WHERE status='ACTIVE' ORDER BY date_reported DESC";
                PreparedStatement ps = conn.prepareStatement(sql);
                ResultSet rs = ps.executeQuery();
                while(rs.next()) {
                    String badgeClass = "LOST".equals(rs.getString("type")) ? "badge-lost" : "badge-found";
        %>
            <div class="item-card card">
                <h4><%= rs.getString("item_name") %> <span class="<%= badgeClass %>"><%= rs.getString("type") %></span></h4>
                <p><strong>Category:</strong> <%= rs.getString("category") %></p>
                <p><strong>Location:</strong> <%= rs.getString("location") %></p>
                <p><strong>Date:</strong> <%= rs.getString("date_reported") %></p>
                <a href="item-details.jsp?id=<%= rs.getInt("id") %>" class="btn">View Details</a>
            </div>
        <%
                }
            } catch(Exception e) { e.printStackTrace(); }
        %>
        </div>
    </div>
</body>
</html>
""",
    r"src\main\webapp\ajax-demo.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>AJAX Demo - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/script.js"></script>
</head>
<body>
    <nav><h2>CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <div class="card">
            <h2>AJAX Live Search Demonstration</h2>
            <p>Type to search items without refreshing the page.</p>
            <input type="text" onkeyup="searchItems(this.value)" placeholder="Search e.g. Calculator..." style="width:100%; padding:10px; font-size:16px;">
        </div>
        <div id="searchResults">
            <!-- Results will be injected here via AJAX -->
        </div>
    </div>
</body>
</html>
""",
    r"src\main\webapp\item-details.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    String idParam = request.getParameter("id");
    if(idParam == null) { response.sendRedirect("items.jsp"); return; }
    int itemId = Integer.parseInt(idParam);
%>
<!DOCTYPE html>
<html>
<head>
    <title>Item Details - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CampusFind</h2><a href="items.jsp">Back to Items</a></nav>
    <div class="container">
        <div class="card">
        <%
            try (Connection conn = DBConnection.getConnection()) {
                String sql = "SELECT items.*, users.name as reporter_name FROM items JOIN users ON items.user_id = users.id WHERE items.id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, itemId);
                ResultSet rs = ps.executeQuery();
                if(rs.next()) {
        %>
            <h2><%= rs.getString("item_name") %> (<%= rs.getString("type") %>)</h2>
            <p><strong>Category:</strong> <%= rs.getString("category") %></p>
            <p><strong>Location:</strong> <%= rs.getString("location") %></p>
            <p><strong>Date Reported:</strong> <%= rs.getString("date_reported") %></p>
            <p><strong>Status:</strong> <%= rs.getString("status") %></p>
            <p><strong>Reported By:</strong> <%= rs.getString("reporter_name") %></p>
            <hr>
            <p><strong>Description:</strong></p>
            <p><%= rs.getString("description") %></p>
            
            <% 
                User user = (User) session.getAttribute("user");
                if(user != null && user.getId() != rs.getInt("user_id")) { 
            %>
                <hr>
                <h3>Claim / Contact</h3>
                <form action="ClaimItemServlet" method="POST">
                    <input type="hidden" name="itemId" value="<%= itemId %>">
                    <div class="form-group">
                        <label>Message (Provide details to prove ownership or arrange meetup):</label>
                        <textarea name="message" rows="3" required></textarea>
                    </div>
                    <button type="submit" class="btn">Submit Claim</button>
                </form>
            <%  } else if (user == null) { %>
                <hr>
                <p><a href="login.jsp">Login to claim or contact regarding this item.</a></p>
            <%  } %>
            
        <%
                }
            } catch(Exception e) { e.printStackTrace(); }
        %>
        </div>
    </div>
</body>
</html>
""",
    r"src\main\webapp\my-reports.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null) { response.sendRedirect("login.jsp"); return; }
%>
<!DOCTYPE html>
<html>
<head>
    <title>My Reports - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CampusFind</h2><a href="dashboard.jsp">Dashboard</a></nav>
    <div class="container">
        <h2>My Reported Items</h2>
        <table>
            <tr><th>Item</th><th>Type</th><th>Date</th><th>Status</th></tr>
            <%
                try (Connection conn = DBConnection.getConnection()) {
                    String sql = "SELECT * FROM items WHERE user_id=? ORDER BY date_reported DESC";
                    PreparedStatement ps = conn.prepareStatement(sql);
                    ps.setInt(1, user.getId());
                    ResultSet rs = ps.executeQuery();
                    while(rs.next()) {
            %>
            <tr>
                <td><%= rs.getString("item_name") %></td>
                <td><%= rs.getString("type") %></td>
                <td><%= rs.getString("date_reported") %></td>
                <td><%= rs.getString("status") %></td>
            </tr>
            <%
                    }
                } catch(Exception e) { e.printStackTrace(); }
            %>
        </table>
    </div>
</body>
</html>
""",
    r"src\main\webapp\admin.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null || !"ADMIN".equals(user.getRole())) {
        response.sendRedirect("login.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CampusFind Admin</h2><a href="LogoutServlet">Logout</a></nav>
    <div class="container">
        <h2>Manage Reports</h2>
        <table>
            <tr><th>ID</th><th>Item</th><th>Type</th><th>Status</th><th>Action</th></tr>
            <%
                try (Connection conn = DBConnection.getConnection()) {
                    String sql = "SELECT * FROM items ORDER BY id DESC";
                    PreparedStatement ps = conn.prepareStatement(sql);
                    ResultSet rs = ps.executeQuery();
                    while(rs.next()) {
            %>
            <tr>
                <td><%= rs.getInt("id") %></td>
                <td><%= rs.getString("item_name") %></td>
                <td><%= rs.getString("type") %></td>
                <td><%= rs.getString("status") %></td>
                <td>
                    <form action="AdminServlet" method="POST" style="display:inline;">
                        <input type="hidden" name="itemId" value="<%= rs.getInt("id") %>">
                        <% if(!"RETURNED".equals(rs.getString("status"))) { %>
                            <button type="submit" name="action" value="return" class="btn">Mark Returned</button>
                        <% } %>
                        <button type="submit" name="action" value="delete" class="btn btn-danger">Delete</button>
                    </form>
                </td>
            </tr>
            <%
                    }
                } catch(Exception e) { e.printStackTrace(); }
            %>
        </table>
    </div>
</body>
</html>
""",
    r"src\main\webapp\xml-demo.html": """<!DOCTYPE html>
<html>
<head>
    <title>XML Demo - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/script.js"></script>
</head>
<body onload="loadXMLData()">
    <nav><h2>CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <div class="card">
            <h2>XML Processing Demonstration</h2>
            <p>This table is populated by JavaScript reading an XML file (<code>data/items.xml</code>).</p>
            <div id="xmlTableContainer"></div>
        </div>
    </div>
</body>
</html>
""",
    r"src\main\webapp\php-demo.php": """<?php
// PHP Demonstration for Web Technology Lab Syllabus
$sampleData = [
    ["id" => 1, "name" => "Scientific Calculator", "type" => "Lost", "location" => "Maths Dept"],
    ["id" => 2, "name" => "Lab Coat", "type" => "Found", "location" => "Chemistry Lab"],
    ["id" => 3, "name" => "USB Drive", "type" => "Lost", "location" => "Computer Lab"]
];
?>
<!DOCTYPE html>
<html>
<head>
    <title>PHP Demo - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <div class="card">
            <h2>PHP Array Demonstration</h2>
            <p>This page demonstrates basic PHP integration by iterating through a PHP array.</p>
            <table>
                <tr><th>ID</th><th>Name</th><th>Type</th><th>Location</th></tr>
                <?php foreach($sampleData as $item): ?>
                <tr>
                    <td><?php echo $item['id']; ?></td>
                    <td><?php echo $item['name']; ?></td>
                    <td><?php echo $item['type']; ?></td>
                    <td><?php echo $item['location']; ?></td>
                </tr>
                <?php endforeach; ?>
            </table>
        </div>
    </div>
</body>
</html>
""",
    r"src\main\webapp\ecommerce.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    // Simple E-commerce demonstration using session
    if(request.getParameter("action") != null && request.getParameter("action").equals("buy")) {
        session.setAttribute("cart_msg", "Order placed successfully for " + request.getParameter("item"));
        response.sendRedirect("ecommerce.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Campus Essentials - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <h2>Campus Essentials (E-commerce Demo)</h2>
        <% if(session.getAttribute("cart_msg") != null) { %>
            <div class="card" style="background:#d4edda; color:#155724;">
                <%= session.getAttribute("cart_msg") %>
                <% session.removeAttribute("cart_msg"); %>
            </div>
        <% } %>
        <div id="searchResults">
            <div class="item-card">
                <h4>Scientific Calculator</h4>
                <p>Casio fx-991EX</p>
                <p><strong>$20.00</strong></p>
                <form method="POST">
                    <input type="hidden" name="action" value="buy">
                    <input type="hidden" name="item" value="Scientific Calculator">
                    <button type="submit" class="btn">Buy Now</button>
                </form>
            </div>
            <div class="item-card">
                <h4>Lab Coat</h4>
                <p>Standard white cotton lab coat.</p>
                <p><strong>$15.00</strong></p>
                <form method="POST">
                    <input type="hidden" name="action" value="buy">
                    <input type="hidden" name="item" value="Lab Coat">
                    <button type="submit" class="btn">Buy Now</button>
                </form>
            </div>
            <div class="item-card">
                <h4>Notebook</h4>
                <p>A4 size, 200 pages.</p>
                <p><strong>$3.00</strong></p>
                <form method="POST">
                    <input type="hidden" name="action" value="buy">
                    <input type="hidden" name="item" value="Notebook">
                    <button type="submit" class="btn">Buy Now</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
"""
}

for rel_path, content in web_files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend Files Part 2 written successfully.")
