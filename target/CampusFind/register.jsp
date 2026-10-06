<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>Register - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=2">
    <script src="js/script.js"></script>
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <div class="card" style="max-width: 500px; margin: auto;">
            <h2>Student Registration</h2>
            <% if(request.getParameter("error") != null) { %>
                <p style="color:red;">Error in registration. Email might exist.</p>
            <% } %>
            <form action="RegisterServlet" method="POST" onsubmit="return validateRegistration()">
                <div class="form-group">
                    <label>Full Name:</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Email ID:</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" id="password" required>
                </div>
                <div class="form-group">
                    <label>Confirm Password:</label>
                    <input type="password" id="confirmPassword" required>
                </div>
                <button type="submit" class="btn">Register</button>
                <p>Already have an account? <a href="login.jsp">Login here</a></p>
            </form>
        </div>
    </div>
</body>
</html>
