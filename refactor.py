import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Delete Demo Files
files_to_delete = [
    r"src\main\webapp\ajax-demo.jsp",
    r"src\main\webapp\xml-demo.html",
    r"src\main\webapp\php-demo.php",
    r"src\main\webapp\ecommerce.jsp",
    r"src\main\webapp\data\items.xml",
    r"src\main\webapp\data\items.dtd",
    r"src\main\webapp\data\items.xsd"
]
for f in files_to_delete:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        os.remove(path)

# 2. Create Guidelines XML (DTD, XSD, XML)
dtd = """<!ELEMENT guidelines (rule+)>
<!ELEMENT rule (#PCDATA)>
<!ATTLIST rule type CDATA #REQUIRED>
"""
xsd = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="guidelines">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="rule" maxOccurs="unbounded">
          <xs:complexType>
            <xs:simpleContent>
              <xs:extension base="xs:string">
                <xs:attribute name="type" type="xs:string" use="required"/>
              </xs:extension>
            </xs:simpleContent>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""
xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE guidelines SYSTEM "guidelines.dtd">
<guidelines xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="guidelines.xsd">
    <rule type="Important">Turn in found items to the administration within 24 hours.</rule>
    <rule type="General">Provide accurate descriptions when reporting a lost item.</rule>
    <rule type="Important">Fraudulent claims will lead to immediate disciplinary action.</rule>
    <rule type="General">You can view your reports in the dashboard.</rule>
</guidelines>
"""
os.makedirs(os.path.join(base_dir, r"src\main\webapp\data"), exist_ok=True)
with open(os.path.join(base_dir, r"src\main\webapp\data\guidelines.dtd"), "w") as f: f.write(dtd)
with open(os.path.join(base_dir, r"src\main\webapp\data\guidelines.xsd"), "w") as f: f.write(xsd)
with open(os.path.join(base_dir, r"src\main\webapp\data\guidelines.xml"), "w") as f: f.write(xml)

# 3. Update XmlParserServlet to read Guidelines (DOM + XPath)
servlet = """package com.campusfind.servlet;
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
        
        try {
            // 18. XML DOM Parser
            InputStream xmlStream = getServletContext().getResourceAsStream("/data/guidelines.xml");
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(xmlStream);
            
            // 19. XPath - Fetch only 'Important' rules
            XPathFactory xPathfactory = XPathFactory.newInstance();
            XPath xpath = xPathfactory.newXPath();
            String expression = "/guidelines/rule[@type='Important']";
            NodeList nodeList = (NodeList) xpath.compile(expression).evaluate(doc, XPathConstants.NODESET);
            
            for (int i = 0; i < nodeList.getLength(); i++) {
                Element el = (Element) nodeList.item(i);
                out.println("<li><strong>Important:</strong> " + el.getTextContent() + "</li>");
            }
        } catch (Exception e) {
            e.printStackTrace();
            out.println("<li>Error loading guidelines.</li>");
        }
    }
}
"""
old_servlet = os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\XmlParserServlet.java")
if os.path.exists(old_servlet): os.remove(old_servlet)
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\GuidelinesServlet.java"), "w") as f: f.write(servlet)

# 4. Update index.jsp to show Guidelines seamlessly
index_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>CIT CampusFind - Home</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/script.js"></script>
</head>
<body onload="loadGuidelines()">
    <nav>
        <h2>CIT CampusFind</h2>
        <div>
            <a href="items.jsp">Browse Items</a>
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
"""
with open(os.path.join(base_dir, r"src\main\webapp\index.jsp"), "w") as f: f.write(index_jsp)

# 5. Update items.jsp to include seamless AJAX Live Search
items_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, com.campusfind.util.DBConnection" %>
<!DOCTYPE html>
<html>
<head>
    <title>Browse Items - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/script.js"></script>
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <h2>Reported Items</h2>
        
        <!-- Seamless AJAX Integration -->
        <div class="form-group">
            <input type="text" id="searchInput" onkeyup="searchItems(this.value)" placeholder="Live search (e.g., Wallet, Calculator)..." style="width:100%; padding:12px; font-size:16px; border-radius:8px; border:1px solid #ccc;">
        </div>

        <div id="searchResults" style="display: grid; gap: 15px; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));">
        <%
            try (Connection conn = DBConnection.getConnection()) {
                String sql = "SELECT * FROM items WHERE status='ACTIVE' ORDER BY date_reported DESC";
                PreparedStatement ps = conn.prepareStatement(sql);
                ResultSet rs = ps.executeQuery();
                while(rs.next()) {
                    String badgeClass = "LOST".equals(rs.getString("type")) ? "badge-lost" : "badge-found";
        %>
            <div class="item-card card">
                <h4><%= rs.getString("item_name") %> <span class="<%= badgeClass %>"><%= rs.getString("type") %></span></h4>
                <p><strong>Category:</strong> <%= rs.getString("category") %></p>
                <p><strong>Location:</strong> <%= rs.getString("location") %></p>
                <p><strong>Date:</strong> <%= rs.getString("date_reported") %></p>
                <a href="item-details.jsp?id=<%= rs.getInt("id") %>" class="btn">View Details</a>
            </div>
        <%
                }
            } catch(Exception e) { e.printStackTrace(); }
        %>
        </div>
    </div>
</body>
</html>
"""
with open(os.path.join(base_dir, r"src\main\webapp\items.jsp"), "w") as f: f.write(items_jsp)

# 6. Update script.js for seamless DOM Manipulation
script_js = """
// 3. JavaScript & 4. DOM Manipulation
function validateRegistration() {
    let pwd = document.getElementById("password").value;
    let cpwd = document.getElementById("confirmPassword").value;
    if (pwd !== cpwd) {
        alert("Passwords do not match!");
        return false;
    }
    return true;
}

// 5. AJAX & 20. Fetch API
function searchItems(query) {
    if (query.length < 2 && query.length > 0) return; // Wait for at least 2 chars
    
    let url = query.length === 0 ? 'SearchItemServlet?q=' : 'SearchItemServlet?q=' + encodeURIComponent(query);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let html = "";
            if(data.length === 0) {
                html = "<p>No items found.</p>";
            } else {
                data.forEach(item => {
                    let typeClass = item.type === 'LOST' ? 'badge-lost' : 'badge-found';
                    html += `<div class="item-card card">
                        <h4>${item.item_name} <span class="${typeClass}">${item.type}</span></h4>
                        <p><strong>Category:</strong> ${item.category}</p>
                        <p><strong>Location:</strong> ${item.location}</p>
                        <a href="item-details.jsp?id=${item.id}" class="btn">View Details</a>
                    </div>`;
                });
            }
            document.getElementById("searchResults").innerHTML = html; // DOM Manipulation
        });
}

// 20. Fetch API reading from our XML parser servlet
function loadGuidelines() {
    fetch('GuidelinesServlet')
        .then(response => response.text())
        .then(html => {
            document.getElementById('guidelines-list').innerHTML = html; // DOM Manipulation
        });
}
"""
with open(os.path.join(base_dir, r"src\main\webapp\js\script.js"), "w") as f: f.write(script_js)

# 7. Update SearchItemServlet to handle empty queries (return all)
search_servlet = """package com.campusfind.servlet;
import com.campusfind.util.DBConnection;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import org.json.JSONArray;
import org.json.JSONObject;

@WebServlet("/SearchItemServlet")
public class SearchItemServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String query = request.getParameter("q");
        if (query == null) query = "";
        
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        JSONArray itemsArray = new JSONArray();
        
        try (Connection conn = DBConnection.getConnection()) {
            String sql = "SELECT * FROM items WHERE item_name LIKE ? AND status='ACTIVE' ORDER BY date_reported DESC";
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, "%" + query + "%");
            ResultSet rs = ps.executeQuery();
            
            while (rs.next()) {
                JSONObject obj = new JSONObject();
                obj.put("id", rs.getInt("id"));
                obj.put("item_name", rs.getString("item_name"));
                obj.put("type", rs.getString("type"));
                obj.put("category", rs.getString("category"));
                obj.put("location", rs.getString("location"));
                itemsArray.put(obj);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        out.print(itemsArray.toString());
        out.flush();
    }
}
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\servlet\SearchItemServlet.java"), "w") as f: f.write(search_servlet)

# 8. Create Dockerfile for Render deployment
dockerfile = """# Use official Tomcat 10 image with JDK 17
FROM tomcat:10.1-jdk17

# Remove default ROOT application
RUN rm -rf /usr/local/tomcat/webapps/ROOT

# Copy our compiled .war file to be the ROOT web application
COPY target/CampusFind.war /usr/local/tomcat/webapps/ROOT.war

# Expose port 8080
EXPOSE 8080

# Run Tomcat
CMD ["catalina.sh", "run"]
"""
with open(os.path.join(base_dir, "Dockerfile"), "w") as f: f.write(dockerfile)

print("Refactoring complete: Removed demos, integrated features seamlessly, added Dockerfile.")
