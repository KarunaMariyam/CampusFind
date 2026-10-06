<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
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
    <link rel="stylesheet" type="text/css" href="css/style.css?v=8">
</head>
<body>
    <nav><h2>CIT CampusFind</h2><div><a href="report.jsp">Report Item</a><a href="items.jsp">Browse Items</a><a href="LogoutServlet">Logout</a></div></nav>
    <div class="container">
        
        <!-- Massive Aesthetic Welcome Banner -->
        <div style="background: linear-gradient(135deg, #E05D3A, #F28C6D); padding: 60px 40px; border-radius: 24px; color: #FFF; margin-bottom: 40px; text-align: center; box-shadow: 0 15px 40px rgba(224, 93, 58, 0.25); position: relative; overflow: hidden;">
            <div style="position:absolute; top:-50px; right:-20px; font-size:200px; opacity:0.1; line-height:1;">✨</div>
            <h1 style="font-size: 56px; color: #FFF; margin: 0; letter-spacing: -2px; font-weight:800;">Welcome, <%= user.getName() %>! 👋</h1>
            <p style="font-size: 20px; opacity: 0.95; margin-top: 15px; font-weight:500;">Ready to connect your lost and found items on campus.</p>
        </div>

        
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
