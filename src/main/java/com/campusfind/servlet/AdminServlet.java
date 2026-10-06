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
        int itemId = Integer.parseInt(request.getParameter("itemId"));
        
        try (Connection conn = DBConnection.getConnection()) {
            if ("return".equals(action)) {
                String sql = "UPDATE items SET status='RETURNED' WHERE id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, itemId);
                ps.executeUpdate();
            } else if ("delete".equals(action)) {
                String sql = "DELETE FROM items WHERE id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, itemId);
                ps.executeUpdate();
            }
            response.sendRedirect("admin.jsp?msg=success");
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("admin.jsp?error=true");
        }
    }
}
