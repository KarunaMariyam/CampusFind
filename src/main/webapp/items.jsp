<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection" %>
<!DOCTYPE html>
<html>
<head>
    <title>Browse Items - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/script.js"></script>
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <h2>Reported Items</h2>
        
        <!-- Seamless AJAX Integration -->
        <div class="form-group">
            <input type="text" id="searchInput" onkeyup="searchItems(this.value)" placeholder="Live search (e.g., Wallet, Calculator)..." style="width:100%; padding:12px; font-size:16px; border-radius:8px; border:1px solid #ccc;">
        </div>

        <div id="searchResults" style="display: grid; gap: 15px; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));">
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
