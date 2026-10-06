import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Update report.jsp to include File Upload and Reward
report_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<% if(session.getAttribute("user") == null) { response.sendRedirect("login.jsp"); return; } %>
<!DOCTYPE html>
<html>
<head>
    <title>Report Item - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=7">
    <script>
        // HTML5 Canvas Image Resizer (Client-side compression)
        function processImage(event) {
            const file = event.target.files[0];
            if(!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    const canvas = document.createElement('canvas');
                    const MAX_WIDTH = 500;
                    const scaleSize = MAX_WIDTH / img.width;
                    canvas.width = MAX_WIDTH;
                    canvas.height = img.height * scaleSize;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    
                    const base64 = canvas.toDataURL('image/jpeg', 0.6); // Compress to 60%
                    document.getElementById('imageBase64').value = base64;
                    
                    const preview = document.getElementById('imgPreview');
                    preview.src = base64;
                    preview.style.display = 'block';
                }
                img.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }

        // Smart Template Generator
        function generateTemplate() {
            const category = document.querySelector('select[name="category"]').value;
            let template = "";
            if(category === 'Electronics') template = "Brand: \\nColor: \\nModel/Serial No: \\nDistinguishing Marks (Scratches, Stickers): ";
            else if(category === 'Personal') template = "Brand/Material: \\nColor: \\nContents (if bag/wallet): \\nUnique Features: ";
            else if(category === 'Documents') template = "Type of Document (ID, Notes): \\nName on Document: \\nDepartment/Year: ";
            else template = "Detailed Description: \\nColor: \\nWhere was it last seen: ";
            
            document.querySelector('textarea[name="description"]').value = template;
        }

        function toggleReward() {
            const type = document.querySelector('select[name="type"]').value;
            document.getElementById('rewardGroup').style.display = (type === 'LOST') ? 'block' : 'none';
        }
    </script>
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="dashboard.jsp">Back to Dashboard</a></nav>
    <div class="container">
        <div class="card" style="max-width: 700px; margin: auto;">
            <h1 style="text-align:center;">Report an Item</h1>
            <p style="text-align:center; color:#7A6F66; margin-bottom:20px;">Provide detailed information or a photo to help identify it.</p>
            
            <form action="ReportItemServlet" method="POST" style="margin-top:20px;">
                <div class="form-group" style="display:flex; gap:15px;">
                    <div style="flex:1;">
                        <label>Item Name</label>
                        <input type="text" name="itemName" required placeholder="e.g. Blue Dell Laptop">
                    </div>
                    <div style="flex:1;">
                        <label>Type</label>
                        <select name="type" onchange="toggleReward()">
                            <option value="LOST">I Lost Something</option>
                            <option value="FOUND">I Found Something</option>
                        </select>
                    </div>
                </div>

                <div class="form-group" style="display:flex; gap:15px;">
                    <div style="flex:1;">
                        <label>Category</label>
                        <select name="category" onchange="generateTemplate()">
                            <option value="Electronics">Electronics 💻</option>
                            <option value="Personal">Personal Items 🎒</option>
                            <option value="Documents">Documents 📚</option>
                            <option value="Other">Other ✨</option>
                        </select>
                    </div>
                    <div style="flex:1;">
                        <label>Location (Lost/Found at)</label>
                        <input type="text" name="location" required placeholder="e.g. Main Canteen">
                    </div>
                </div>

                <!-- Reward Section -->
                <div class="form-group" id="rewardGroup">
                    <label>Reward Offered (Optional)</label>
                    <input type="text" name="reward" placeholder="e.g. ₹500 or Coffee treat!">
                </div>

                <!-- Photo Section -->
                <div class="form-group" style="background:#FDF9F2; padding:20px; border:2px dashed #D8D0C1; border-radius:8px; text-align:center;">
                    <label style="font-size:18px; color:#943A29;">📸 Upload a Photo (Crucial for Identification)</label>
                    <input type="file" accept="image/*" onchange="processImage(event)" style="border:none; background:transparent; margin-top:10px;">
                    <input type="hidden" name="imageBase64" id="imageBase64">
                    <img id="imgPreview" src="" style="display:none; max-width:100%; max-height:300px; margin-top:15px; border-radius:8px; border:5px solid #FFF; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
                </div>

                <div class="form-group">
                    <label style="display:flex; justify-content:space-between; align-items:center;">
                        Description
                        <button type="button" onclick="generateTemplate()" style="background:transparent; border:1px solid #943A29; color:#943A29; border-radius:20px; padding:4px 10px; cursor:pointer; font-size:12px;">✨ Auto-Fill Template</button>
                    </label>
                    <textarea name="description" rows="5" required placeholder="Provide as much detail as possible..."></textarea>
                </div>

                <button type="submit" class="btn" style="width: 100%; font-size:18px; padding:15px;">Submit Report</button>
            </form>
        </div>
    </div>
    <script>generateTemplate(); toggleReward();</script>
</body>
</html>
"""
with open(os.path.join(base_dir, r"src\main\webapp\report.jsp"), "w", encoding="utf-8") as f:
    f.write(report_jsp)


# 2. Update ReportItemServlet.java to handle imageBase64 and reward
report_servlet = """package com.campusfind.servlet;
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
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\ReportItemServlet.java"), "w", encoding="utf-8") as f:
    f.write(report_servlet)


# 3. Update SearchItemServlet.java to send Image and Reward
search_servlet = """package com.campusfind.servlet;
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
            if (!category.isEmpty()) { sql += " AND category = ?"; }
            sql += " ORDER BY id DESC";
            
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, "%" + query + "%");
            if (!category.isEmpty()) { ps.setString(2, category); }
            
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                JSONObject obj = new JSONObject();
                obj.put("id", rs.getInt("id"));
                obj.put("item_name", rs.getString("item_name"));
                obj.put("type", rs.getString("type"));
                obj.put("category", rs.getString("category"));
                obj.put("location", rs.getString("location"));
                obj.put("date_reported", rs.getString("date_reported"));
                
                String img = rs.getString("image_base64");
                obj.put("has_image", img != null && !img.isEmpty());
                if(img != null && !img.isEmpty()) obj.put("image_url", img);
                
                String rew = rs.getString("reward");
                obj.put("reward", rew != null ? rew : "");
                
                itemsArray.put(obj);
            }
        } catch (Exception e) { e.printStackTrace(); }
        
        out.print(itemsArray.toString());
        out.flush();
    }
}
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\SearchItemServlet.java"), "w", encoding="utf-8") as f:
    f.write(search_servlet)


# 4. Update script.js to render Images and Rewards
script_js_path = os.path.join(base_dir, r"src\main\webapp\js\script.js")
with open(script_js_path, "r", encoding="utf-8") as f:
    script_content = f.read()

new_card_html = """
                    let visual = obj.has_image ? `<img src="${obj.image_url}" style="width:100%; height:200px; object-fit:cover; border-radius:4px; margin-bottom:15px; border:1px solid #EFEADD;">` : `<div class="item-card-emoji" style="background:#F1ECE1; border-radius:4px;">${emoji}</div>`;
                    let rewardBadge = obj.reward !== "" ? `<p style="color:#C92A2A; font-weight:bold; font-family:'Fraunces', serif; margin:10px 0;"><span style="font-size:18px;">💰</span> Reward: ${obj.reward}</p>` : "";
                    
                    html += `<div class="item-card">
                        ${visual}
                        <h4>${obj.item_name} <span class="${typeClass}">${obj.type}</span></h4>
                        <p><strong>📍</strong> ${obj.location}</p>
                        <p><strong>🕒</strong> ${obj.date_reported}</p>
                        ${rewardBadge}
                        <div class="action-bar" style="margin-top:15px;">
                            <a href="item-details.jsp?id=${obj.id}" class="btn" style="padding: 8px 16px;">View</a>
                            <button onclick="copyShareLink(${obj.id})" class="share-btn" style="background:transparent; border:1px solid #7A6F66; padding:6px 12px; border-radius:4px; cursor:pointer;">🔗 Share</button>
                        </div>
                    </div>`;
"""
script_content = script_content.replace('let emoji = getEmojiForCategory(item.category);', 'let emoji = getEmojiForCategory(item.category);\nlet obj = item;')
import re
script_content = re.sub(r'html \+= `<div class="item-card">.*?</div>`;', new_card_html, script_content, flags=re.DOTALL)

with open(script_js_path, "w", encoding="utf-8") as f:
    f.write(script_content)


# 5. Update item-details.jsp to show the image and reward
item_details_path = os.path.join(base_dir, r"src\main\webapp\item-details.jsp")
with open(item_details_path, "r", encoding="utf-8") as f:
    details_content = f.read()

# Replace the poster-emoji with the actual image if available
poster_emoji_html = """
            <% 
                String b64 = rs.getString("image_base64");
                String rewardStr = rs.getString("reward");
                if(b64 != null && !b64.isEmpty()) { 
            %>
                <img src="<%= b64 %>" style="max-width:100%; max-height:350px; object-fit:contain; border-radius:4px; border:10px solid #FFF; box-shadow:0 5px 15px rgba(0,0,0,0.1); margin:20px 0;" class="poster-emoji">
            <% } else { %>
                <div class="poster-emoji">🔍</div>
            <% } %>
"""
details_content = details_content.replace('<div class="poster-emoji">🔍</div>', poster_emoji_html)

# Add reward tag
reward_html = """
            <div style="margin: 20px 0; font-size: 20px;" class="poster-text">
                <% if(rewardStr != null && !rewardStr.isEmpty()) { %>
                    <div style="background:#FFE8E8; color:#C92A2A; padding:15px; border-radius:8px; border:2px dashed #C92A2A; margin-bottom:20px; font-weight:bold;">
                        💰 REWARD OFFERED: <%= rewardStr %>
                    </div>
                <% } %>
"""
details_content = details_content.replace('<div style="margin: 20px 0; font-size: 20px;" class="poster-text">', reward_html)

with open(item_details_path, "w", encoding="utf-8") as f:
    f.write(details_content)

print("Added Photo Upload (Canvas Base64) and Reward/Auto-Template features.")
