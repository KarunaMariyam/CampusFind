package com.campusfind.util;

import java.sql.Connection;
import java.sql.DriverManager;

public class DBConnection {
    public static Connection getConnection() {
        Connection conn = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            // Hardcoding the Aiven Database details to bypass Render Environment Variable bugs
            String url = "jdbc:mysql://mysql-2d9d59d5-campusfind.c.aivencloud.com:27727/defaultdb?useSSL=true&requireSSL=true&verifyServerCertificate=false&allowPublicKeyRetrieval=true";
            String user = "avnadmin";
            
            // Still using environment variable for the password to keep it secure
            String password = System.getenv("DB_PASSWORD");
            
            // If testing locally on your laptop without the environment variable, put your Aiven password here!
            if (password == null || password.trim().isEmpty()) {
                password = "PUT_YOUR_AIVEN_PASSWORD_HERE"; 
            }
            
            conn = DriverManager.getConnection(url, user, password);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Database connection failed.");
        }
        return conn;
    }
}
