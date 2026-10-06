package com.campusfind.servlet;
import com.campusfind.model.User;
import com.campusfind.util.DBConnection;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.time.LocalDate;

@WebServlet("/ReportItemServlet")
public class ReportItemServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession();
        User user = (User) session.getAttribute("user");
        if(user == null) { response.sendRedirect("login.jsp"); return; }
        
        String itemName = request.getParameter("itemName");
        String category = request.getParameter("category");
        String type = request.getParameter("type");
        String location = request.getParameter("location");
        String description = request.getParameter("description");
        String reward = request.getParameter("reward");
        String imageBase64 = request.getParameter("imageBase64");
        
        if("FOUND".equals(type)) reward = null; // Found items don't have rewards

        try (Connection conn = DBConnection.getConnection()) {
            String sql = "INSERT INTO items (user_id, item_name, category, type, location, date_reported, description, status, reward, image_base64) VALUES (?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?)";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setInt(1, user.getId());
            ps.setString(2, itemName);
            ps.setString(3, category);
            ps.setString(4, type);
            ps.setString(5, location);
            ps.setDate(6, java.sql.Date.valueOf(LocalDate.now()));
            ps.setString(7, description);
            ps.setString(8, reward == null || reward.trim().isEmpty() ? null : reward);
            ps.setString(9, imageBase64 == null || imageBase64.trim().isEmpty() ? null : imageBase64);
            
            ps.executeUpdate();
            response.sendRedirect("dashboard.jsp");
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("report.jsp?error=true");
        }
    }
}
