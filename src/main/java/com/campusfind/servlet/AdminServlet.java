package com.campusfind.servlet;
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
