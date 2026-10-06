package com.campusfind.util;

import java.sql.Connection;
import java.sql.DriverManager;

public class DBConnection {
    // IMPORTANT: Change these values to match your local MySQL setup
    private static final String URL = "jdbc:mysql://localhost:3306/campusfind";
    private static final String USER = "root";
    private static final String PASSWORD = "1234"; 

    public static Connection getConnection() {
        Connection conn = null;
        try {
            // Load the MySQL JDBC Driver
            Class.forName("com.mysql.cj.jdbc.Driver");
            // Establish the connection
            conn = DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Database connection failed. Check credentials in DBConnection.java");
        }
        return conn;
    }
}
