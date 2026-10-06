package com.campusfind.servlet;
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
        String category = request.getParameter("cat");
        if (query == null) query = "";
        if (category == null) category = "";
        
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        JSONArray itemsArray = new JSONArray();
        
        try (Connection conn = DBConnection.getConnection()) {
            String sql = "SELECT * FROM items WHERE item_name LIKE ? AND status='ACTIVE'";
            if (!category.isEmpty()) {
                sql += " AND category = ?";
            }
            sql += " ORDER BY date_reported DESC";
            
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, "%" + query + "%");
            if (!category.isEmpty()) {
                ps.setString(2, category);
            }
            
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                JSONObject obj = new JSONObject();
                obj.put("id", rs.getInt("id"));
                obj.put("item_name", rs.getString("item_name"));
                obj.put("type", rs.getString("type"));
                obj.put("category", rs.getString("category"));
                obj.put("location", rs.getString("location"));
                obj.put("date_reported", rs.getString("date_reported"));
                itemsArray.put(obj);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        out.print(itemsArray.toString());
        out.flush();
    }
}
