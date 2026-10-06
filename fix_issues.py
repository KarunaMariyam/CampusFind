import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Update CSS for Butter Yellow + Professional Typography & Shadows
css_content = """@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:opsz,wght@9..144,300..700&display=swap');

:root {
    --bg-color: #FFFDE7; /* Butter Yellow */
    --card-bg: #FFFFFF;
    --primary: #C56B46; /* Terracotta Accent */
    --text-main: #333333;
    --font-serif: 'Fraunces', serif;
    --font-sans: 'DM Sans', sans-serif;
}

* { box-sizing: border-box; }

body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: var(--font-sans);
    margin: 0; padding: 0;
    line-height: 1.6;
}

h1, h2, h3, h4 {
    font-family: var(--font-serif);
    color: var(--text-main);
    font-weight: 600;
}

nav {
    background: #FFFFFF;
    padding: 15px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

nav h2 {
    margin: 0;
    color: var(--primary);
    font-size: 26px;
    letter-spacing: -0.5px;
}

nav a {
    color: var(--text-main);
    text-decoration: none;
    margin: 0 15px;
    font-weight: 500;
    font-size: 15px;
    transition: color 0.2s;
}

nav a:hover { color: var(--primary); }

.container {
    max-width: 1000px;
    margin: 40px auto;
    padding: 0 20px;
}

.card {
    background: var(--card-bg);
    padding: 35px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    margin-bottom: 25px;
    border: 1px solid rgba(0,0,0,0.02);
}

.btn {
    background: var(--primary);
    color: #fff;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    text-decoration: none;
    font-weight: 500;
    font-family: var(--font-sans);
    display: inline-block;
    transition: all 0.2s ease;
    text-align: center;
}

.btn:hover { background: #a85634; transform: translateY(-1px); }

.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 500; font-size: 14px; }
.form-group input, .form-group select, .form-group textarea {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    font-family: var(--font-sans);
    font-size: 15px;
    transition: all 0.2s;
    background: #FAFAFA;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
    outline: none;
    border-color: var(--primary);
    background: #FFFFFF;
    box-shadow: 0 0 0 4px rgba(197, 107, 70, 0.1);
}

.item-card {
    border: 1px solid #EAEAEA;
    padding: 20px;
    border-radius: 12px;
    background: #FAFAFA;
    transition: transform 0.2s;
}
.item-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.03); }
.item-card h4 { margin-top: 0; font-size: 20px; display: flex; justify-content: space-between; align-items: center; }

.badge-lost { background: #EED9E9; color: #8A4B75; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-family: var(--font-sans); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;}
.badge-found { background: #D5E8D4; color: #4B7552; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-family: var(--font-sans); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;}

table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 15px; }
table, th, td { border: 1px solid #EAEAEA; }
th, td { padding: 15px; text-align: left; }
th { background-color: #FAFAFA; font-weight: 600; color: var(--text-main); }
"""
with open(os.path.join(base_dir, r"src\main\webapp\css\style.css"), "w") as f:
    f.write(css_content)

# 2. Fix GuidelinesServlet XML DTD resolution crash
servlet_content = """package com.campusfind.servlet;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.InputStream;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Element;

@WebServlet("/GuidelinesServlet")
public class GuidelinesServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        
        try (InputStream xmlStream = getServletContext().getResourceAsStream("/data/guidelines.xml")) {
            if (xmlStream == null) {
                out.println("<li>Error: Cannot find guidelines.xml</li>");
                return;
            }
            
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            // IMPORTANT FIX: Prevent Java from trying to resolve the DTD file over network/filesystem which causes crashes
            factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
            
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(xmlStream);
            
            XPathFactory xPathfactory = XPathFactory.newInstance();
            XPath xpath = xPathfactory.newXPath();
            String expression = "/guidelines/rule[@type='Important']";
            NodeList nodeList = (NodeList) xpath.compile(expression).evaluate(doc, XPathConstants.NODESET);
            
            for (int i = 0; i < nodeList.getLength(); i++) {
                Element el = (Element) nodeList.item(i);
                out.println("<li style='margin-bottom:10px;'><strong>Important:</strong> " + el.getTextContent() + "</li>");
            }
        } catch (Exception e) {
            e.printStackTrace();
            out.println("<li style='color:red;'>XML Parsing Error: " + e.getMessage() + "</li>");
        }
    }
}
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\GuidelinesServlet.java"), "w") as f:
    f.write(servlet_content)

# 3. Fix LoginServlet to output DB errors directly to the page so the user knows if DB is disconnected
login_servlet = """package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import com.campusfind.model.User;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.net.URLEncoder;

@WebServlet("/LoginServlet")
public class LoginServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String email = request.getParameter("email");
        String password = request.getParameter("password");
        String remember = request.getParameter("remember");
        
        try (Connection conn = DBConnection.getConnection()) {
            if (conn == null) {
                response.sendRedirect("login.jsp?error=exception&msg=" + URLEncoder.encode("Database connection failed. Please check MySQL is running and DBConnection.java has correct username/password.", "UTF-8"));
                return;
            }
            
            String sql = "SELECT * FROM users WHERE email=? AND password=?";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, email);
            ps.setString(2, password);
            ResultSet rs = ps.executeQuery();
            
            if (rs.next()) {
                User user = new User(rs.getInt("id"), rs.getString("name"), rs.getString("email"), rs.getString("role"));
                HttpSession session = request.getSession();
                session.setAttribute("user", user);
                
                if ("on".equals(remember)) {
                    Cookie cookie = new Cookie("rememberedUser", email);
                    cookie.setMaxAge(60 * 60 * 24 * 30);
                    response.addCookie(cookie);
                }
                
                if ("ADMIN".equals(user.getRole())) {
                    response.sendRedirect("admin.jsp");
                } else {
                    response.sendRedirect("dashboard.jsp");
                }
            } else {
                response.sendRedirect("login.jsp?error=invalid");
            }
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("login.jsp?error=exception&msg=" + URLEncoder.encode(e.getMessage(), "UTF-8"));
        }
    }
}
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\LoginServlet.java"), "w") as f:
    f.write(login_servlet)

# 4. Update login.jsp to display the exact DB error message
login_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
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
"""
with open(os.path.join(base_dir, r"src\main\webapp\login.jsp"), "w") as f:
    f.write(login_jsp)

print("Fixes applied: Butter Yellow CSS, XML DTD bug fixed, Login DB error reporting added.")
