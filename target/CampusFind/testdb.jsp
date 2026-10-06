<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, java.io.*" %>
<!DOCTYPE html>
<html>
<head><title>Database Diagnostic Tool</title></head>
<body style="font-family: monospace; padding: 20px;">
    <h2>Database Diagnostic Tool</h2>
    <%
        String url = System.getenv("DB_URL");
        String user = System.getenv("DB_USER");
        String pass = System.getenv("DB_PASSWORD");
        
        out.println("<strong>Environment Variables Detected:</strong><br>");
        out.println("DB_URL: " + (url != null ? url : "NULL") + "<br>");
        out.println("DB_USER: " + (user != null ? user : "NULL") + "<br>");
        out.println("DB_PASSWORD: " + (pass != null ? "***[HIDDEN]***" : "NULL") + "<br><br>");
        
        if (url == null || url.isEmpty()) {
            out.println("<span style='color:red;'>ERROR: Environment variables are not reaching the application!</span>");
        } else {
            out.println("<strong>Attempting Connection...</strong><br>");
            try {
                Class.forName("com.mysql.cj.jdbc.Driver");
                try (Connection conn = DriverManager.getConnection(url, user, pass)) {
                    out.println("<h3 style='color:green;'>✅ CONNECTION SUCCESSFUL!</h3>");
                    out.println("MySQL Server Version: " + conn.getMetaData().getDatabaseProductVersion());
                }
            } catch (Exception e) {
                out.println("<h3 style='color:red;'>❌ CONNECTION FAILED!</h3>");
                out.println("<strong>Error Message:</strong> " + e.getMessage() + "<br><br>");
                
                StringWriter sw = new StringWriter();
                e.printStackTrace(new PrintWriter(sw));
                out.println("<strong>Full Stack Trace:</strong><br>");
                out.println("<pre style='background:#f4f4f4; padding:10px; border:1px solid #ddd;'>" + sw.toString() + "</pre>");
            }
        }
    %>
</body>
</html>
