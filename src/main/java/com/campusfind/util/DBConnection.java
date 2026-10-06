package com.campusfind.util;

import java.sql.Connection;
import java.sql.DriverManager;

public class DBConnection {
    public static Connection getConnection() {
        Connection conn = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            // Use Cloud Environment Variables if on Render, otherwise use Localhost
            String url = System.getenv("DB_URL");
            String user = System.getenv("DB_USER");
            String password = System.getenv("DB_PASSWORD");
            
            if (url == null || url.trim().isEmpty()) {
                url = "jdbc:mysql://localhost:3306/campusfind";
                user = "root";
                password = "1234";
            }
            
            conn = DriverManager.getConnection(url, user, password);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Database connection failed.");
        }
        return conn;
    }
}
