import os
import re

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind"

# 1. Update DBConnection.java to support Cloud Environment Variables
db_conn = """package com.campusfind.util;

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
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\util\DBConnection.java"), "w", encoding="utf-8") as f:
    f.write(db_conn)

# 2. Create a Database Initializer (Runs on startup to auto-create tables in the Cloud)
db_init = """package com.campusfind.util;

import jakarta.servlet.ServletContextEvent;
import jakarta.servlet.ServletContextListener;
import jakarta.servlet.annotation.WebListener;
import java.sql.Connection;
import java.sql.Statement;

@WebListener
public class DatabaseInitializer implements ServletContextListener {
    @Override
    public void contextInitialized(ServletContextEvent sce) {
        try (Connection conn = DBConnection.getConnection(); Statement stmt = conn.createStatement()) {
            if (conn != null) {
                // Auto-create users table
                stmt.execute("CREATE TABLE IF NOT EXISTS users (" +
                        "id INT AUTO_INCREMENT PRIMARY KEY," +
                        "name VARCHAR(100) NOT NULL," +
                        "email VARCHAR(100) NOT NULL UNIQUE," +
                        "password VARCHAR(100) NOT NULL," +
                        "role VARCHAR(20) DEFAULT 'STUDENT'" +
                        ")");

                // Auto-create items table
                stmt.execute("CREATE TABLE IF NOT EXISTS items (" +
                        "id INT AUTO_INCREMENT PRIMARY KEY," +
                        "user_id INT," +
                        "item_name VARCHAR(100) NOT NULL," +
                        "category VARCHAR(50)," +
                        "type VARCHAR(20)," +
                        "location VARCHAR(100)," +
                        "date_reported DATE," +
                        "description TEXT," +
                        "status VARCHAR(20) DEFAULT 'ACTIVE'," +
                        "image_base64 LONGTEXT," +
                        "reward VARCHAR(100)," +
                        "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE" +
                        ")");

                // Auto-create claims table
                stmt.execute("CREATE TABLE IF NOT EXISTS claims (" +
                        "id INT AUTO_INCREMENT PRIMARY KEY," +
                        "item_id INT," +
                        "user_id INT," +
                        "message TEXT," +
                        "status VARCHAR(20) DEFAULT 'PENDING'," +
                        "FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE," +
                        "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE" +
                        ")");
                        
                // Insert a default Admin if one doesn't exist
                stmt.execute("INSERT IGNORE INTO users (id, name, email, password, role) VALUES (1, 'Admin', 'admin@campusfind.com', 'admin123', 'ADMIN')");
            }
        } catch (Exception e) {
            System.out.println("Could not auto-initialize tables. They might already exist.");
        }
    }
}
"""
with open(os.path.join(base_dir, r"src\main\java\com\campusfind\util\DatabaseInitializer.java"), "w", encoding="utf-8") as f:
    f.write(db_init)

print("Cloud-ready DB Connection and Auto-Initializer added.")
