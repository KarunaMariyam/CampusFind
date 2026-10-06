package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;

@WebServlet("/ResolveItemServlet")
public class ResolveItemServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        int itemId = Integer.parseInt(request.getParameter("itemId"));
        String inputCode = request.getParameter("code");
        
        // Generate the secret code hash expected
        String expectedCode = String.format("%04d", (itemId * 9876) % 10000);
        
        if(expectedCode.equals(inputCode)) {
            try (Connection conn = DBConnection.getConnection()) {
                String sql = "UPDATE items SET status='RETURNED' WHERE id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, itemId);
                ps.executeUpdate();
                response.sendRedirect("item-details.jsp?id=" + itemId + "&success=paired");
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            response.sendRedirect("item-details.jsp?id=" + itemId + "&error=invalidcode");
        }
    }
}
