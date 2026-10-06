import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Update AdminServlet.java to add "Delete User" powers securely via JDBC
admin_servlet = """package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;

@WebServlet("/AdminServlet")
public class AdminServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String action = request.getParameter("action");
        
        try (Connection conn = DBConnection.getConnection()) {
            if ("return".equals(action)) {
                int itemId = Integer.parseInt(request.getParameter("itemId"));
                String sql = "UPDATE items SET status='RETURNED' WHERE id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, itemId);
                ps.executeUpdate();
                
            } else if ("delete".equals(action)) {
                int itemId = Integer.parseInt(request.getParameter("itemId"));
                // Delete claims for this item first to avoid foreign key issues
                PreparedStatement psClaims = conn.prepareStatement("DELETE FROM claims WHERE item_id=?");
                psClaims.setInt(1, itemId);
                psClaims.executeUpdate();
                
                // Then delete item
                String sql = "DELETE FROM items WHERE id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, itemId);
                ps.executeUpdate();
                
            } else if ("deleteUser".equals(action)) {
                int userId = Integer.parseInt(request.getParameter("userId"));
                // 1. Delete user's claims
                PreparedStatement psClaims = conn.prepareStatement("DELETE FROM claims WHERE user_id=?");
                psClaims.setInt(1, userId);
                psClaims.executeUpdate();
                
                // 2. Delete user's items
                PreparedStatement psItems = conn.prepareStatement("DELETE FROM items WHERE user_id=?");
                psItems.setInt(1, userId);
                psItems.executeUpdate();
                
                // 3. Delete the user
                PreparedStatement psUser = conn.prepareStatement("DELETE FROM users WHERE id=?");
                psUser.setInt(1, userId);
                psUser.executeUpdate();
            }
            response.sendRedirect("admin.jsp?msg=success");
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("admin.jsp?error=true");
        }
    }
}
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\AdminServlet.java"), "w", encoding="utf-8") as f:
    f.write(admin_servlet)


# 2. Update admin.jsp to clearly show powers: Managing Users and Deleting Spam
admin_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null || !"ADMIN".equals(user.getRole())) {
        response.sendRedirect("login.jsp");
        return;
    }
    
    int totalItems = 0, lostCount = 0, foundCount = 0, returnedCount = 0, userCount = 0;
    try (Connection conn = DBConnection.getConnection()) {
        ResultSet rs1 = conn.prepareStatement("SELECT COUNT(*) FROM items").executeQuery();
        if(rs1.next()) totalItems = rs1.getInt(1);
        
        ResultSet rs2 = conn.prepareStatement("SELECT COUNT(*) FROM items WHERE type='LOST' AND status='ACTIVE'").executeQuery();
        if(rs2.next()) lostCount = rs2.getInt(1);
        
        ResultSet rs3 = conn.prepareStatement("SELECT COUNT(*) FROM items WHERE type='FOUND' AND status='ACTIVE'").executeQuery();
        if(rs3.next()) foundCount = rs3.getInt(1);
        
        ResultSet rs4 = conn.prepareStatement("SELECT COUNT(*) FROM items WHERE status='RETURNED'").executeQuery();
        if(rs4.next()) returnedCount = rs4.getInt(1);
        
        ResultSet rs5 = conn.prepareStatement("SELECT COUNT(*) FROM users WHERE role='STUDENT'").executeQuery();
        if(rs5.next()) userCount = rs5.getInt(1);
    } catch(Exception e) { e.printStackTrace(); }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=4">
</head>
<body>
    <nav>
        <h2>CIT CampusFind</h2>
        <div>
            <a href="admin.jsp" class="active">Admin Dashboard</a>
            <a href="LogoutServlet" class="btn" style="background:#111;">Logout</a>
        </div>
    </nav>
    <div class="container">
        <h1>Admin Control Panel</h1>
        
        <% if("success".equals(request.getParameter("msg"))) { %>
            <div style="background:#EBFBEE; color:#2B8A3E; padding:15px; border-radius:12px; margin-bottom:20px; font-weight:600;">
                Action completed successfully!
            </div>
        <% } %>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin-bottom: 30px;">
            <div class="card" style="text-align:center; padding:20px;">
                <h2 style="font-size:36px; margin:0; color:#E60023;"><%= totalItems %></h2>
                <p>Total Items</p>
            </div>
            <div class="card" style="text-align:center; padding:20px;">
                <h2 style="font-size:36px; margin:0;"><%= returnedCount %></h2>
                <p>Resolved</p>
            </div>
            <div class="card" style="text-align:center; padding:20px;">
                <h2 style="font-size:36px; margin:0;"><%= userCount %></h2>
                <p>Students</p>
            </div>
        </div>
        
        <div class="card">
            <h2>1. Manage Students</h2>
            <p style="color:#666; margin-bottom:15px;">Remove students who create fake reports.</p>
            <table>
                <tr><th>ID</th><th>Name</th><th>Email</th><th>Action</th></tr>
                <%
                    try (Connection conn = DBConnection.getConnection()) {
                        PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE role='STUDENT' ORDER BY id DESC");
                        ResultSet rs = ps.executeQuery();
                        while(rs.next()) {
                %>
                <tr>
                    <td><%= rs.getInt("id") %></td>
                    <td><strong><%= rs.getString("name") %></strong></td>
                    <td><%= rs.getString("email") %></td>
                    <td>
                        <form action="AdminServlet" method="POST" style="margin:0;">
                            <input type="hidden" name="action" value="deleteUser">
                            <input type="hidden" name="userId" value="<%= rs.getInt("id") %>">
                            <button type="submit" class="btn" style="background:#E60023; padding:8px 16px; font-size:13px;" onclick="return confirm('WARNING: This will permanently delete the user AND all their lost/found reports. Proceed?');">Ban & Delete User</button>
                        </form>
                    </td>
                </tr>
                <% } } catch(Exception e) { e.printStackTrace(); } %>
            </table>
        </div>

        <div class="card">
            <h2>2. Manage All Reports</h2>
            <p style="color:#666; margin-bottom:15px;">Mark items as returned or force-delete spam posts.</p>
            <table>
                <tr><th>Report ID</th><th>Item</th><th>Type</th><th>Status</th><th>Actions</th></tr>
                <%
                    try (Connection conn = DBConnection.getConnection()) {
                        PreparedStatement ps = conn.prepareStatement("SELECT * FROM items ORDER BY id DESC");
                        ResultSet rs = ps.executeQuery();
                        while(rs.next()) {
                %>
                <tr>
                    <td>#<%= rs.getInt("id") %></td>
                    <td><strong><%= rs.getString("item_name") %></strong></td>
                    <td><span class="<%= "LOST".equals(rs.getString("type")) ? "badge-lost" : "badge-found" %>"><%= rs.getString("type") %></span></td>
                    <td><%= rs.getString("status") %></td>
                    <td>
                        <form action="AdminServlet" method="POST" style="margin:0; display:flex; gap:10px;">
                            <input type="hidden" name="itemId" value="<%= rs.getInt("id") %>">
                            <% if(!"RETURNED".equals(rs.getString("status"))) { %>
                                <button type="submit" name="action" value="return" class="btn" style="background:#111; padding:8px 16px; font-size:13px;">Mark Returned</button>
                            <% } %>
                            <button type="submit" name="action" value="delete" class="btn" style="background:#E60023; padding:8px 16px; font-size:13px;" onclick="return confirm('Permanently delete this report?');">Delete Post</button>
                        </form>
                    </td>
                </tr>
                <% } } catch(Exception e) { e.printStackTrace(); } %>
            </table>
        </div>
    </div>
</body>
</html>
"""
with open(os.path.join(base_dir, r"src\main\webapp\admin.jsp"), "w", encoding="utf-8") as f:
    f.write(admin_jsp)

print("Admin dashboard heavily upgraded with Manage Users and spam deletion capabilities.")
