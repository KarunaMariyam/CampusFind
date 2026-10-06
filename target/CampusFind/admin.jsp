<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
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
    <title>Admin Dashboard - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CIT CampusFind Admin</h2><a href="LogoutServlet">Logout</a></nav>
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
