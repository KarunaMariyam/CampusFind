<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    if(session.getAttribute("user") == null) {
        response.sendRedirect("login.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Report Item - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=2">
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="dashboard.jsp">Dashboard</a></nav>
    <div class="container">
        <div class="card" style="max-width: 600px; margin: auto;">
            <h2>Report a Lost or Found Item</h2>
            <form action="ReportItemServlet" method="POST">
                <div class="form-group">
                    <label>Report Type:</label>
                    <select name="type" required>
                        <option value="LOST">I Lost Something</option>
                        <option value="FOUND">I Found Something</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Item Name:</label>
                    <input type="text" name="itemName" required>
                </div>
                <div class="form-group">
                    <label>Category:</label>
                    <select name="category" required>
                        <option value="Electronics">Electronics</option>
                        <option value="Personal">Personal Items (Wallet, ID, etc)</option>
                        <option value="Stationery">Stationery / Books</option>
                        <option value="Keys">Keys</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Location (Where was it lost/found?):</label>
                    <input type="text" name="location" required>
                </div>
                <div class="form-group">
                    <label>Date:</label>
                    <input type="date" name="date" required>
                </div>
                <div class="form-group">
                    <label>Description / Identifying marks:</label>
                    <textarea name="description" rows="4" required></textarea>
                </div>
                <button type="submit" class="btn">Submit Report</button>
            </form>
        </div>
    </div>
</body>
</html>
