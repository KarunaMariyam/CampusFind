import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

java_files = {
    r"src\main\java\com\campusfind\model\User.java": """package com.campusfind.model;
public class User {
    private int id;
    private String name;
    private String email;
    private String role;
    
    public User() {}
    public User(int id, String name, String email, String role) {
        this.id = id; this.name = name; this.email = email; this.role = role;
    }
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
}
""",
    r"src\main\java\com\campusfind\model\Item.java": """package com.campusfind.model;
public class Item {
    private int id;
    private int userId;
    private String itemName;
    private String category;
    private String type;
    private String location;
    private String dateReported;
    private String description;
    private String status;
    
    public Item() {}
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public int getUserId() { return userId; }
    public void setUserId(int userId) { this.userId = userId; }
    public String getItemName() { return itemName; }
    public void setItemName(String itemName) { this.itemName = itemName; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    public String getDateReported() { return dateReported; }
    public void setDateReported(String dateReported) { this.dateReported = dateReported; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
""",
    r"src\main\java\com\campusfind\servlet\RegisterServlet.java": """package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;

@WebServlet("/RegisterServlet")
public class RegisterServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name = request.getParameter("name");
        String email = request.getParameter("email");
        String password = request.getParameter("password");
        
        try (Connection conn = DBConnection.getConnection()) {
            String sql = "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'STUDENT')";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, name);
            ps.setString(2, email);
            ps.setString(3, password);
            ps.executeUpdate();
            
            response.sendRedirect("login.jsp?msg=registered");
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("register.jsp?error=true");
        }
    }
}
""",
    r"src\main\java\com\campusfind\servlet\LoginServlet.java": """package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import com.campusfind.model.User;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

@WebServlet("/LoginServlet")
public class LoginServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String email = request.getParameter("email");
        String password = request.getParameter("password");
        String remember = request.getParameter("remember");
        
        try (Connection conn = DBConnection.getConnection()) {
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
                    cookie.setMaxAge(60 * 60 * 24 * 30); // 30 days
                    response.addCookie(cookie);
                } else {
                    Cookie cookie = new Cookie("rememberedUser", "");
                    cookie.setMaxAge(0);
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
            response.sendRedirect("login.jsp?error=exception");
        }
    }
}
""",
    r"src\main\java\com\campusfind\servlet\LogoutServlet.java": """package com.campusfind.servlet;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;

@WebServlet("/LogoutServlet")
public class LogoutServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session != null) {
            session.invalidate();
        }
        response.sendRedirect("index.jsp");
    }
}
""",
    r"src\main\java\com\campusfind\servlet\ReportItemServlet.java": """package com.campusfind.servlet;
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
""",
    r"src\main\java\com\campusfind\servlet\SearchItemServlet.java": """package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import org.json.JSONArray;
import org.json.JSONObject;

@WebServlet("/SearchItemServlet")
public class SearchItemServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String query = request.getParameter("q");
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        
        JSONArray itemsArray = new JSONArray();
        
        try (Connection conn = DBConnection.getConnection()) {
            String sql = "SELECT * FROM items WHERE item_name LIKE ? AND status='ACTIVE'";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, "%" + query + "%");
            ResultSet rs = ps.executeQuery();
            
            while (rs.next()) {
                JSONObject obj = new JSONObject();
                obj.put("id", rs.getInt("id"));
                obj.put("item_name", rs.getString("item_name"));
                obj.put("type", rs.getString("type"));
                obj.put("category", rs.getString("category"));
                obj.put("location", rs.getString("location"));
                itemsArray.put(obj);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        out.print(itemsArray.toString());
        out.flush();
    }
}
""",
    r"src\main\java\com\campusfind\servlet\ClaimItemServlet.java": """package com.campusfind.servlet;
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
""",
    r"src\main\java\com\campusfind\servlet\AdminServlet.java": """package com.campusfind.servlet;
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
"""
}

for rel_path, content in java_files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Java Backend Files written successfully.")
