<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null) { response.sendRedirect("login.jsp"); return; }
%>
<!DOCTYPE html>
<html>
<head>
    <title>My Reports - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=8">
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
