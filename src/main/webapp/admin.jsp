<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null || !"ADMIN".equals(user.getRole())) {
        response.sendRedirect("login.jsp");
        return;
    }
    
    // Fetch stats for dashboard
    int totalItems = 0, lostCount = 0, foundCount = 0, returnedCount = 0, claimCount = 0;
    try (Connection conn = DBConnection.getConnection()) {
        ResultSet rs1 = conn.prepareStatement("SELECT COUNT(*) FROM items").executeQuery();
        if(rs1.next()) totalItems = rs1.getInt(1);
        
        ResultSet rs2 = conn.prepareStatement("SELECT COUNT(*) FROM items WHERE type='LOST' AND status='ACTIVE'").executeQuery();
        if(rs2.next()) lostCount = rs2.getInt(1);
        
        ResultSet rs3 = conn.prepareStatement("SELECT COUNT(*) FROM items WHERE type='FOUND' AND status='ACTIVE'").executeQuery();
        if(rs3.next()) foundCount = rs3.getInt(1);
        
        ResultSet rs4 = conn.prepareStatement("SELECT COUNT(*) FROM items WHERE status='RETURNED'").executeQuery();
        if(rs4.next()) returnedCount = rs4.getInt(1);
        
        ResultSet rs5 = conn.prepareStatement("SELECT COUNT(*) FROM claims").executeQuery();
        if(rs5.next()) claimCount = rs5.getInt(1);
    } catch(Exception e) { e.printStackTrace(); }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=2">
</head>
<body>
    <nav>
        <h2>CIT CampusFind</h2>
        <div>
            <a href="admin.jsp">Dashboard</a>
            <a href="items.jsp">Browse Items</a>
            <a href="LogoutServlet">Logout</a>
        </div>
    </nav>
    <div class="container">
        <h2>Welcome, Admin!</h2>
        
        <!-- Stats Cards -->
        <div class="dashboard-grid">
            <div class="dash-card">
                <div class="dash-icon">📦</div>
                <h4><%= totalItems %></h4>
                <p>Total Reports</p>
            </div>
            <div class="dash-card">
                <div class="dash-icon">🔴</div>
                <h4><%= lostCount %></h4>
                <p>Active Lost</p>
            </div>
            <div class="dash-card">
                <div class="dash-icon">🟢</div>
                <h4><%= foundCount %></h4>
                <p>Active Found</p>
            </div>
            <div class="dash-card">
                <div class="dash-icon">✅</div>
                <h4><%= returnedCount %></h4>
                <p>Returned</p>
            </div>
            <div class="dash-card">
                <div class="dash-icon">📩</div>
                <h4><%= claimCount %></h4>
                <p>Claims</p>
            </div>
        </div>
        
        <!-- Manage Reports Table -->
        <div class="card" style="margin-top: 30px;">
            <h3>Manage All Reports</h3>
            <table>
                <tr><th>ID</th><th>Item</th><th>Type</th><th>Location</th><th>Date</th><th>Status</th><th>Action</th></tr>
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
                    <td><span class="<%= "LOST".equals(rs.getString("type")) ? "badge-lost" : "badge-found" %>"><%= rs.getString("type") %></span></td>
                    <td><%= rs.getString("location") %></td>
                    <td><%= rs.getString("date_reported") %></td>
                    <td><%= rs.getString("status") %></td>
                    <td>
                        <form action="AdminServlet" method="POST" style="display:inline;">
                            <input type="hidden" name="itemId" value="<%= rs.getInt("id") %>">
                            <% if(!"RETURNED".equals(rs.getString("status"))) { %>
                                <button type="submit" name="action" value="return" class="btn" style="padding:8px 14px; font-size:13px;">Mark Returned</button>
                            <% } %>
                            <button type="submit" name="action" value="delete" class="btn btn-danger" style="padding:8px 14px; font-size:13px;" onclick="return confirm('Are you sure you want to delete this report?');">Delete</button>
                        </form>
                    </td>
                </tr>
                <%
                        }
                    } catch(Exception e) { e.printStackTrace(); }
                %>
            </table>
        </div>
        
        <!-- Claims Section -->
        <div class="card">
            <h3>Recent Claims</h3>
            <table>
                <tr><th>Claim ID</th><th>Item</th><th>Claimed By</th><th>Message</th><th>Date</th></tr>
                <%
                    try (Connection conn = DBConnection.getConnection()) {
                        String sql = "SELECT c.id, i.item_name, u.name, c.message, c.claim_date FROM claims c JOIN items i ON c.item_id = i.id JOIN users u ON c.user_id = u.id ORDER BY c.claim_date DESC";
                        PreparedStatement ps = conn.prepareStatement(sql);
                        ResultSet rs = ps.executeQuery();
                        boolean hasClaims = false;
                        while(rs.next()) {
                            hasClaims = true;
                %>
                <tr>
                    <td><%= rs.getInt("id") %></td>
                    <td><%= rs.getString("item_name") %></td>
                    <td><%= rs.getString("name") %></td>
                    <td><%= rs.getString("message") %></td>
                    <td><%= rs.getString("claim_date") %></td>
                </tr>
                <%
                        }
                        if(!hasClaims) {
                %>
                <tr><td colspan="5" style="text-align:center; color:#999;">No claims yet.</td></tr>
                <%
                        }
                    } catch(Exception e) { e.printStackTrace(); }
                %>
            </table>
        </div>
    </div>
</body>
</html>
