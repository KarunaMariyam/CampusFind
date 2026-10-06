<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="com.campusfind.model.User" %>
<%
    User user = (User) session.getAttribute("user");
    if(user == null) {
        response.sendRedirect("login.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
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
        <div class="card">
            <h3>CIT Student Dashboard</h3>
            <p>Select an action below:</p>
            <br>
            <a href="report.jsp" class="btn">Report Lost/Found Item</a>
            <a href="my-reports.jsp" class="btn">My Reports & Claims</a>
            <a href="ecommerce.jsp" class="btn">Campus Essentials Store</a>
        </div>
    </div>
</body>
</html>
