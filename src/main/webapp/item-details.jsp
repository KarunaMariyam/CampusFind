<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection, com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    String idParam = request.getParameter("id");
    if(idParam == null) { response.sendRedirect("items.jsp"); return; }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Item Details - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=8">
    <style>
    @media print {
        body * { visibility: hidden; }
        #poster-area, #poster-area * { visibility: visible; }
        #poster-area {
            position: absolute; left: 0; top: 0; width: 100%; height: 100%; text-align: center;
            padding: 50px; border: 15px solid #C56B46; background: #FFFDE7;
        }
        .no-print { display: none !important; }
        .poster-title { font-size: 80px !important; color: #C56B46; margin-bottom: 20px; text-transform: uppercase;}
        .poster-emoji { font-size: 120px !important; margin: 30px 0; }
        .poster-text { font-size: 30px !important; margin-bottom: 20px; }
    }
    </style>
</head>
<body>
    <nav class="no-print"><h2>CIT CampusFind</h2><a href="items.jsp">Back to Items</a></nav>
    <div class="container">
        <%
            try (Connection conn = DBConnection.getConnection()) {
                String sql = "SELECT * FROM items WHERE id=?";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setInt(1, Integer.parseInt(idParam));
                ResultSet rs = ps.executeQuery();
                if(rs.next()) {
                    boolean isLost = "LOST".equals(rs.getString("type"));
        %>
        
        <% if("paired".equals(request.getParameter("success"))) { %>
            <div style="background:#EBFBEE; color:#2B8A3E; padding:15px; border-radius:4px; margin-bottom:20px; font-family:var(--font-heading);">✅ Bluetooth Connection Paired Successfully! Item marked as RETURNED.</div>
        <% } else if("invalidcode".equals(request.getParameter("error"))) { %>
            <div style="background:#FFE8E8; color:#C92A2A; padding:15px; border-radius:4px; margin-bottom:20px; font-family:var(--font-heading);">❌ Pairing Failed. Invalid Handover Code.</div>
        <% } %>
        
        <div class="card" id="poster-area">

            <h1 class="poster-title"><%= isLost ? "MISSING" : "FOUND" %></h1>
            
            <% 
                String b64 = rs.getString("image_base64");
                String rewardStr = rs.getString("reward");
                if(b64 != null && !b64.isEmpty()) { 
            %>
                <img src="<%= b64 %>" style="max-width:100%; max-height:350px; object-fit:contain; border-radius:4px; border:10px solid #FFF; box-shadow:0 5px 15px rgba(0,0,0,0.1); margin:20px 0;" class="poster-emoji">
            <% } else { %>
                <div class="poster-emoji">🔍</div>
            <% } %>

            <h2 style="font-size: 36px;"><%= rs.getString("item_name") %></h2>
            
            
            <div style="margin: 20px 0; font-size: 20px;" class="poster-text">
                <% if(rewardStr != null && !rewardStr.isEmpty()) { %>
                    <div style="background:#FFE8E8; color:#C92A2A; padding:15px; border-radius:8px; border:2px dashed #C92A2A; margin-bottom:20px; font-weight:bold;">
                        💰 REWARD OFFERED: <%= rewardStr %>
                    </div>
                <% } %>

                <p><strong>Category:</strong> <%= rs.getString("category") %></p>
                <p><strong><%= isLost ? "Lost at:" : "Found at:" %></strong> <%= rs.getString("location") %></p>
                <p><strong>Date:</strong> <%= rs.getString("date_reported") %></p>
            </div>
            
            
            <div style="background:#FFF; padding:25px; border-radius:4px; border:1px solid #D8D0C1; margin-top:20px; text-align:left;">
                <p style="font-size: 18px; color:#666;"><strong>Description:</strong></p>
                <p style="font-size: 20px; margin-top:10px;"><%= rs.getString("description") %></p>
                <hr style="border:0; border-top:1px solid #EEE; margin: 15px 0;">
                <a href="https://www.google.com/maps/search/?api=1&query=Coimbatore+Institute+of+Technology+<%= rs.getString("location").replace(" ", "+") %>" target="_blank" class="btn" style="background:#FFF; color:#943A29; font-size:14px; padding:8px 16px;">📍 Pinpoint Location on Map</a>
            </div>

            
            <% if(isLost) { %>
                <p class="poster-text" style="margin-top:30px; font-weight:bold; color:#C56B46;">If found, please hand it over to the CIT Administration Office immediately.</p>
            <% } else { %>
                <p class="poster-text" style="margin-top:30px; font-weight:bold; color:#2B8A3E;">If this is yours, please claim it via the CampusFind portal.</p>
            <% } %>
        </div>
        
        <div class="no-print" style="margin-top: 20px; display:flex; gap:15px;">
            <% if(user != null && rs.getInt("user_id") != user.getId()) { %>
                <form action="ClaimItemServlet" method="POST" style="margin:0;">
                    <input type="hidden" name="itemId" value="<%= rs.getInt("id") %>">
                    <input type="text" name="message" placeholder="Message to owner..." required style="padding:12px; border-radius:8px; border:1px solid #ccc; width:300px; margin-right:10px;">
                    <button type="submit" class="btn">Claim / Contact</button>
                </form>
            <% } else if(user == null) { %>
                <p style="color:#666;"><em><a href="login.jsp" style="color:#C56B46; font-weight:bold;">Log in</a> to claim this item or contact the finder.</em></p>
            <% } %>
            
            
            <% if(isLost) { %>
                <button onclick="window.print()" class="btn" style="background:#333;">🖨️ Print Missing Poster</button>
            <% } %>
            
            <% if("ACTIVE".equals(rs.getString("status")) && user != null) { %>
                <form action="ResolveItemServlet" method="POST" style="margin-left:auto; display:flex; gap:10px; align-items:center; background:#FAFAFA; padding:10px; border-radius:4px; border:1px solid #D8D0C1;">
                    <span style="font-size:24px;">📳</span>
                    <div>
                        <p style="margin:0; font-size:12px; font-weight:bold;">Pairing Connection</p>
                        <input type="hidden" name="itemId" value="<%= rs.getInt("id") %>">
                        <input type="text" name="code" placeholder="4-Digit Handover Code" required pattern="\d{4}" style="padding:8px; width:180px; text-align:center; letter-spacing:3px; font-weight:bold;">
                    </div>
                    <button type="submit" class="btn" style="background:#2B8A3E;">Pair & Resolve</button>
                </form>
            <% } %>

        </div>
        
        <%
                } else {
                    out.println("<p>Item not found.</p>");
                }
            } catch(Exception e) { e.printStackTrace(); }
        %>
    </div>
</body>
</html>
