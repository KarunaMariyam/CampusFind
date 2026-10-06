package com.campusfind.servlet;
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
