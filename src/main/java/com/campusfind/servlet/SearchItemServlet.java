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
        if (query == null) query = "";
        
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        JSONArray itemsArray = new JSONArray();
        
        try (Connection conn = DBConnection.getConnection()) {
            String sql = "SELECT * FROM items WHERE item_name LIKE ? AND status='ACTIVE' ORDER BY date_reported DESC";
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
