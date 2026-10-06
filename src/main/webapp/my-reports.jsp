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
    <link rel="stylesheet" type="text/css" href="css/style.css?v=2">
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="dashboard.jsp">Dashboard</a></nav>
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
