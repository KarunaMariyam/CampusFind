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
    <link rel="stylesheet" type="text/css" href="css/style.css?v=8">
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <div class="card" style="max-width: 500px; margin: auto;">
            <h2>Welcome Back.</h2>
            <p style="color:#666;">Pick up where you left off.</p>
            
            <% if(request.getParameter("msg") != null && request.getParameter("error") == null) { %>
                <div style="background:#d4edda; color:#155724; padding:10px; border-radius:5px; margin-bottom:15px;">Registration successful! Please login.</div>
            <% } %>
            <% if("invalid".equals(request.getParameter("error"))) { %>
                <div style="background:#f8d7da; color:#721c24; padding:10px; border-radius:5px; margin-bottom:15px;">Invalid email or password.</div>
            <% } %>
            <% if("exception".equals(request.getParameter("error"))) { %>
                <div style="background:#f8d7da; color:#721c24; padding:10px; border-radius:5px; margin-bottom:15px;">
                    <strong>System Error:</strong> <%= request.getParameter("msg") %>
                </div>
            <% } %>
            
            <form action="LoginServlet" method="POST">
                <div class="form-group">
                    <label>Email address</label>
                    <input type="email" name="email" value="<%= rememberedEmail %>" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <div class="form-group" style="display:flex; align-items:center;">
                    <input type="checkbox" name="remember" id="remember" <%= rememberedEmail.isEmpty() ? "" : "checked" %> style="width:auto; margin-right:8px; margin-top:0;">
                    <label for="remember" style="margin-bottom:0;">Remember me</label>
                </div>
                <button type="submit" class="btn" style="width:100%; margin-top:10px;">Sign In</button>
                <p style="text-align:center; margin-top:20px; font-size:14px;">New to CampusFind? <a href="register.jsp" style="color:var(--primary); text-decoration:none; font-weight:600;">Create an account</a></p>
            </form>
        </div>
    </div>
</body>
</html>
