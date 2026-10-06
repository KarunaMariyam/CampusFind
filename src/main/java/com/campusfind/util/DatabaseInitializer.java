package com.campusfind.util;

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
