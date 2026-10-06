package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import com.campusfind.model.User;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;

@WebServlet("/ClaimItemServlet")
public class ClaimItemServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect("login.jsp");
            return;
        }
        
        User user = (User) session.getAttribute("user");
        int itemId = Integer.parseInt(request.getParameter("itemId"));
        String message = request.getParameter("message");
        
        try (Connection conn = DBConnection.getConnection()) {
            String sql = "INSERT INTO claims (item_id, user_id, message) VALUES (?, ?, ?)";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setInt(1, itemId);
            ps.setInt(2, user.getId());
            ps.setString(3, message);
            ps.executeUpdate();
            
            response.sendRedirect("item-details.jsp?id=" + itemId + "&msg=claimed");
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("item-details.jsp?id=" + itemId + "&error=true");
        }
    }
}
