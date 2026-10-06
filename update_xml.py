import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Add DTD
dtd_content = """<!ELEMENT items (item+)>
<!ELEMENT item (name, category, location, status)>
<!ELEMENT name (#PCDATA)>
<!ELEMENT category (#PCDATA)>
<!ELEMENT location (#PCDATA)>
<!ELEMENT status (#PCDATA)>
"""
with open(os.path.join(base_dir, "src/main/webapp/data/items.dtd"), "w") as f:
    f.write(dtd_content)

# 2. Add XSD
xsd_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="items">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="item" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="name" type="xs:string"/>
              <xs:element name="category" type="xs:string"/>
              <xs:element name="location" type="xs:string"/>
              <xs:element name="status" type="xs:string"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""
with open(os.path.join(base_dir, "src/main/webapp/data/items.xsd"), "w") as f:
    f.write(xsd_content)

# 3. Update XML to reference DTD
xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE items SYSTEM "items.dtd">
<items xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="items.xsd">
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
"""
with open(os.path.join(base_dir, "src/main/webapp/data/items.xml"), "w") as f:
    f.write(xml_content)

# 4. Create XmlParserServlet.java to demonstrate Java XML DOM & XPath
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

@WebServlet("/XmlParserServlet")
public class XmlParserServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        String searchStatus = request.getParameter("status"); // e.g. 'Lost' or 'Found'
        if (searchStatus == null) searchStatus = "Found";

        try {
            // Demonstrate XML DOM Parser
            InputStream xmlStream = getServletContext().getResourceAsStream("/data/items.xml");
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(xmlStream);
            
            // Demonstrate XPath
            XPathFactory xPathfactory = XPathFactory.newInstance();
            XPath xpath = xPathfactory.newXPath();
            String expression = "/items/item[status='" + searchStatus + "']";
            NodeList nodeList = (NodeList) xpath.compile(expression).evaluate(doc, XPathConstants.NODESET);
            
            out.println("<h3>Filtered XML Results (using XPath for status='" + searchStatus + "'):</h3><ul>");
            for (int i = 0; i < nodeList.getLength(); i++) {
                Element el = (Element) nodeList.item(i);
                String name = el.getElementsByTagName("name").item(0).getTextContent();
                String loc = el.getElementsByTagName("location").item(0).getTextContent();
                out.println("<li>" + name + " located at " + loc + "</li>");
            }
            out.println("</ul>");
        } catch (Exception e) {
            e.printStackTrace();
            out.println("<p>Error parsing XML</p>");
        }
    }
}
"""
os.makedirs(os.path.join(base_dir, "src/main/java/com/campusfind/servlet"), exist_ok=True)
with open(os.path.join(base_dir, "src/main/java/com/campusfind/servlet/XmlParserServlet.java"), "w") as f:
    f.write(servlet_content)

# 5. Update xml-demo.html to link to the new servlet
xml_demo_html = """<!DOCTYPE html>
<html>
<head>
    <title>XML Demo - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/script.js"></script>
</head>
<body onload="loadXMLData()">
    <nav><h2>CIT CampusFind</h2><a href="index.jsp">Home</a></nav>
    <div class="container">
        <div class="card">
            <h2>1. Client-side XML DOM Parsing</h2>
            <p>JavaScript reads the XML file, validates elements, and maps to the DOM.</p>
            <div id="xmlTableContainer"></div>
        </div>
        <div class="card">
            <h2>2. Server-side XML DOM Parser & XPath</h2>
            <p>Java Servlet parses the XML file using XPath to find only "Lost" items.</p>
            <iframe src="XmlParserServlet?status=Lost" style="width:100%; border:none; height:150px;"></iframe>
        </div>
    </div>
</body>
</html>
"""
with open(os.path.join(base_dir, "src/main/webapp/xml-demo.html"), "w") as f:
    f.write(xml_demo_html)

print("Added DTD, XSD, XPath, and XML DOM Parser to the project.")
