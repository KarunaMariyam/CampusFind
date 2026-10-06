package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import com.campusfind.model.User;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;

@WebServlet("/ReportItemServlet")
public class ReportItemServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect("login.jsp");
            return;
        }
        
        User user = (User) session.getAttribute("user");
        
        String itemName = request.getParameter("itemName");
        String category = request.getParameter("category");
        String type = request.getParameter("type");
        String location = request.getParameter("location");
        String date = request.getParameter("date");
        String desc = request.getParameter("description");
        
        try (Connection conn = DBConnection.getConnection()) {
            String sql = "INSERT INTO items (user_id, item_name, category, type, location, date_reported, description) VALUES (?, ?, ?, ?, ?, ?, ?)";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setInt(1, user.getId());
            ps.setString(2, itemName);
            ps.setString(3, category);
            ps.setString(4, type);
            ps.setString(5, location);
            ps.setString(6, date);
            ps.setString(7, desc);
            ps.executeUpdate();
            
            response.sendRedirect("my-reports.jsp?msg=reported");
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("report.jsp?error=true");
        }
    }
}
