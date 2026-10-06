<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>CIT CampusFind - Home</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=2">
    <script src="js/script.js"></script>
</head>
<body onload="loadGuidelines()">
    <nav>
        <h2>CIT CampusFind</h2>
        <div>
            <a href="items.jsp">Browse Items</a>
            <% com.campusfind.model.User user = (com.campusfind.model.User) session.getAttribute("user");
               if(user != null) { 
                   if("ADMIN".equals(user.getRole())) { %>
                       <a href="admin.jsp">Admin Dashboard</a>
                   <% } else { %>
                       <a href="dashboard.jsp">Dashboard</a>
                   <% } %>
                <a href="LogoutServlet">Logout</a>
            <% } else { %>
                <a href="login.jsp">Login</a>
                <a href="register.jsp">Register</a>
            <% } %>
        </div>
    </nav>
    <div class="container">
        <div class="card" style="text-align: center;">
            <h1>Welcome to Coimbatore Institute of Technology - Lost & Found</h1>
            <p>Lost something on campus? Found something that belongs to someone?</p>
            <br>
            <a href="report.jsp" class="btn">Report Lost/Found</a>
            <a href="items.jsp" class="btn">Browse Items</a>
        </div>
        
        <!-- Seamless XML Integration -->
        <div class="card">
            <h3>Campus Guidelines</h3>
            <ul id="guidelines-list" style="color: #555;">
                <!-- Filled via AJAX + XML DOM Parser -->
            </ul>
        </div>
    </div>
</body>
</html>
