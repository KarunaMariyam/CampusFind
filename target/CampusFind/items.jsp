<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>Browse Items - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=3">
    <script src="js/script.js"></script>
</head>
<body onload="searchItems('')">
    <nav><h2>CIT CampusFind</h2><div><a href="index.jsp">Home</a></div></nav>
    <div class="container">
        <h2>Explore Reports</h2>
        
        <!-- Category Filters -->
        <div class="category-pills">
            <button class="pill active" onclick="setCategory(this, '')">All</button>
            <button class="pill" onclick="setCategory(this, 'Electronics')">💻 Electronics</button>
            <button class="pill" onclick="setCategory(this, 'Personal')">🎒 Personal</button>
            <button class="pill" onclick="setCategory(this, 'Documents')">📚 Documents</button>
            <button class="pill" onclick="setCategory(this, 'Other')">✨ Other</button>
        </div>

        <div class="form-group">
            <input type="text" id="searchInput" onkeyup="triggerSearch()" placeholder="Search items (e.g., Wallet, Calculator)...">
        </div>

        <!-- Pinterest Masonry Grid -->
        <div id="searchResults">
            <!-- Filled via AJAX -->
        </div>
    </div>
</body>
</html>
