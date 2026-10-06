<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null) {
        response.sendRedirect("login.jsp");
        return;
    }
    if("ADMIN".equals(user.getRole())) {
        response.sendRedirect("admin.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=2">
</head>
<body>
    <nav>
        <h2>CIT CampusFind</h2>
        <div>
            <a href="report.jsp">Report Item</a>
            <a href="items.jsp">Browse Items</a>
            <a href="LogoutServlet">Logout</a>
        </div>
    </nav>
    <div class="container">
        <h2>Welcome, <%= user.getName() %>!</h2>
        <div class="dashboard-grid">
            <a href="report.jsp" class="dash-card">
                <div class="dash-icon">📝</div>
                <h4>Report Item</h4>
                <p>Report a lost or found item</p>
            </a>
            <a href="items.jsp" class="dash-card">
                <div class="dash-icon">🔍</div>
                <h4>Browse Items</h4>
                <p>Search all reported items</p>
            </a>
            <a href="my-reports.jsp" class="dash-card">
                <div class="dash-icon">📋</div>
                <h4>My Reports</h4>
                <p>View your submitted reports</p>
            </a>
        </div>
    </div>
</body>
</html>
