<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    String rememberedEmail = "";
    Cookie[] cookies = request.getCookies();
    if(cookies != null) {
        for(Cookie c : cookies) {
            if("rememberedUser".equals(c.getName())) {
                rememberedEmail = c.getValue();
            }
        }
    }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Login - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <div class="card" style="max-width: 500px; margin: auto;">
            <h2>Login</h2>
            <% if(request.getParameter("msg") != null) { %>
                <p style="color:green;">Registration successful! Please login.</p>
            <% } %>
            <% if(request.getParameter("error") != null) { %>
                <p style="color:red;">Invalid email or password.</p>
            <% } %>
            <form action="LoginServlet" method="POST">
                <div class="form-group">
                    <label>Email ID:</label>
                    <input type="email" name="email" value="<%= rememberedEmail %>" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" required>
                </div>
                <div class="form-group">
                    <input type="checkbox" name="remember" id="remember" <%= rememberedEmail.isEmpty() ? "" : "checked" %>>
                    <label for="remember" style="display:inline;">Remember me</label>
                </div>
                <button type="submit" class="btn">Login</button>
                <p>New user? <a href="register.jsp">Register here</a></p>
            </form>
        </div>
    </div>
</body>
</html>
