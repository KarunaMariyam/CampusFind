package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import com.campusfind.model.User;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.net.URLEncoder;

@WebServlet("/LoginServlet")
public class LoginServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String email = request.getParameter("email");
        String password = request.getParameter("password");
        String remember = request.getParameter("remember");
        
        try (Connection conn = DBConnection.getConnection()) {
            if (conn == null) {
                response.sendRedirect("login.jsp?error=exception&msg=" + URLEncoder.encode("Database connection failed. Please check MySQL is running and DBConnection.java has correct username/password.", "UTF-8"));
                return;
            }
            
            String sql = "SELECT * FROM users WHERE email=? AND password=?";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, email);
            ps.setString(2, password);
            ResultSet rs = ps.executeQuery();
            
            if (rs.next()) {
                User user = new User(rs.getInt("id"), rs.getString("name"), rs.getString("email"), rs.getString("role"));
                HttpSession session = request.getSession();
                session.setAttribute("user", user);
                
                if ("on".equals(remember)) {
                    Cookie cookie = new Cookie("rememberedUser", email);
                    cookie.setMaxAge(60 * 60 * 24 * 30);
                    response.addCookie(cookie);
                }
                
                if ("ADMIN".equals(user.getRole())) {
                    response.sendRedirect("admin.jsp");
                } else {
                    response.sendRedirect("dashboard.jsp");
                }
            } else {
                response.sendRedirect("login.jsp?error=invalid");
            }
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("login.jsp?error=exception&msg=" + URLEncoder.encode(e.getMessage(), "UTF-8"));
        }
    }
}
