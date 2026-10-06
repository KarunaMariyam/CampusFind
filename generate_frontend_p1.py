import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

web_files = {
    r"src\main\webapp\css\style.css": """
:root {
    --primary-color: #0056b3;
    --background: #f4f7f6;
    --text-color: #333;
    --card-bg: #fff;
}
* { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
body { margin: 0; padding: 0; background: var(--background); color: var(--text-color); }
nav { background: var(--primary-color); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; color: white; }
nav a { color: white; text-decoration: none; margin: 0 10px; font-weight: 500; }
nav a:hover { text-decoration: underline; }
.container { max-width: 1000px; margin: 30px auto; padding: 20px; }
.card { background: var(--card-bg); padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
.btn { display: inline-block; padding: 10px 15px; background: var(--primary-color); color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; }
.btn:hover { opacity: 0.9; }
.btn-danger { background: #dc3545; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
table { width: 100%; border-collapse: collapse; margin-top: 15px; }
table, th, td { border: 1px solid #ddd; }
th, td { padding: 12px; text-align: left; }
th { background-color: var(--primary-color); color: white; }
.badge-lost { background: #dc3545; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
.badge-found { background: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
#searchResults { margin-top: 15px; display: grid; gap: 15px; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
.item-card { border: 1px solid #ddd; padding: 15px; border-radius: 5px; background: white; }
""",
    r"src\main\webapp\js\script.js": """
function validateRegistration() {
    let pwd = document.getElementById("password").value;
    let cpwd = document.getElementById("confirmPassword").value;
    if (pwd !== cpwd) {
        alert("Passwords do not match!");
        return false;
    }
    return true;
}

function searchItems(query) {
    if (query.length < 2) {
        document.getElementById("searchResults").innerHTML = "";
        return;
    }
    fetch('SearchItemServlet?q=' + encodeURIComponent(query))
        .then(response => response.json())
        .then(data => {
            let html = "";
            if(data.length === 0) {
                html = "<p>No items found.</p>";
            } else {
                data.forEach(item => {
                    let typeClass = item.type === 'LOST' ? 'badge-lost' : 'badge-found';
                    html += `<div class="item-card">
                        <h4>${item.item_name} <span class="${typeClass}">${item.type}</span></h4>
                        <p><strong>Category:</strong> ${item.category}</p>
                        <p><strong>Location:</strong> ${item.location}</p>
                        <a href="item-details.jsp?id=${item.id}" class="btn">View Details</a>
                    </div>`;
                });
            }
            document.getElementById("searchResults").innerHTML = html;
        });
}

function loadXMLData() {
    fetch('data/items.xml')
        .then(response => response.text())
        .then(str => (new window.DOMParser()).parseFromString(str, "text/xml"))
        .then(data => {
            let items = data.getElementsByTagName("item");
            let table = "<table><tr><th>Name</th><th>Category</th><th>Location</th><th>Status</th></tr>";
            for (let i = 0; i < items.length; i++) {
                table += "<tr><td>" + items[i].getElementsByTagName("name")[0].childNodes[0].nodeValue +
                         "</td><td>" + items[i].getElementsByTagName("category")[0].childNodes[0].nodeValue +
                         "</td><td>" + items[i].getElementsByTagName("location")[0].childNodes[0].nodeValue +
                         "</td><td>" + items[i].getElementsByTagName("status")[0].childNodes[0].nodeValue +
                         "</td></tr>";
            }
            table += "</table>";
            document.getElementById("xmlTableContainer").innerHTML = table;
        });
}
""",
    r"src\main\webapp\data\items.xml": """<?xml version="1.0" encoding="UTF-8"?>
<items>
    <item>
        <name>Black Wallet</name>
        <category>Personal</category>
        <location>Library</location>
        <status>Found</status>
    </item>
    <item>
        <name>Room Keys</name>
        <category>Keys</category>
        <location>Block A</location>
        <status>Lost</status>
    </item>
    <item>
        <name>White Earphones</name>
        <category>Electronics</category>
        <location>Cafeteria</location>
        <status>Found</status>
    </item>
</items>
""",
    r"src\main\webapp\index.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>CampusFind - Home</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav>
        <h2>CampusFind</h2>
        <div>
            <a href="items.jsp">Browse Items</a>
            <a href="ecommerce.jsp">Campus Essentials</a>
            <% if(session.getAttribute("user") != null) { %>
                <a href="dashboard.jsp">Dashboard</a>
                <a href="LogoutServlet">Logout</a>
            <% } else { %>
                <a href="login.jsp">Login</a>
                <a href="register.jsp">Register</a>
            <% } %>
        </div>
    </nav>
    <div class="container">
        <div class="card" style="text-align: center;">
            <h1>Welcome to CampusFind</h1>
            <p>Lost something on campus? Found something that belongs to someone?</p>
            <br>
            <a href="report.jsp" class="btn">Report Lost/Found</a>
            <a href="items.jsp" class="btn">Browse Items</a>
            <hr style="margin:30px 0;">
            <h3>Lab Demonstrations</h3>
            <a href="ajax-demo.jsp" class="btn">AJAX Search Demo</a>
            <a href="xml-demo.html" class="btn">XML Demo</a>
            <a href="php-demo.php" class="btn">PHP Demo</a>
        </div>
    </div>
</body>
</html>
""",
    r"src\main\webapp\register.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>Register - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/script.js"></script>
</head>
<body>
    <nav><h2>CampusFind</h2><a href="index.jsp">Home</a></nav>
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
""",
    r"src\main\webapp\login.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
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
    <title>Login - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CampusFind</h2><a href="index.jsp">Home</a></nav>
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
""",
    r"src\main\webapp\dashboard.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
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
    <title>Dashboard - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav>
        <h2>CampusFind</h2>
        <div>
            <a href="report.jsp">Report Item</a>
            <a href="items.jsp">Browse Items</a>
            <a href="LogoutServlet">Logout</a>
        </div>
    </nav>
    <div class="container">
        <h2>Welcome, <%= user.getName() %>!</h2>
        <div class="card">
            <h3>Student Dashboard</h3>
            <p>Select an action below:</p>
            <br>
            <a href="report.jsp" class="btn">Report Lost/Found Item</a>
            <a href="my-reports.jsp" class="btn">My Reports & Claims</a>
            <a href="ecommerce.jsp" class="btn">Campus Essentials Store</a>
        </div>
    </div>
</body>
</html>
""",
    r"src\main\webapp\report.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    if(session.getAttribute("user") == null) {
        response.sendRedirect("login.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <title>Report Item - CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <nav><h2>CampusFind</h2><a href="dashboard.jsp">Dashboard</a></nav>
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
"""
}

for rel_path, content in web_files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend Files Part 1 written successfully.")
