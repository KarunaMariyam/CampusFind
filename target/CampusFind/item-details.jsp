<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    String idParam = request.getParameter("id");
    if(idParam == null) { response.sendRedirect("items.jsp"); return; }
    int itemId = Integer.parseInt(idParam);
%>
<!DOCTYPE html>
<html>
<head>
    <title>Item Details - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=2">
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="items.jsp">Back to Items</a></nav>
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
