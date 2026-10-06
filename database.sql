-- CampusFind Database Setup

CREATE DATABASE IF NOT EXISTS campusfind;
USE campusfind;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'STUDENT'
);

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    type VARCHAR(20), -- 'LOST' or 'FOUND'
    location VARCHAR(100),
    date_reported DATE,
    description TEXT,
    status VARCHAR(20) DEFAULT 'ACTIVE', -- 'ACTIVE', 'RETURNED'
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    user_id INT,
    message TEXT,
    claim_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'PENDING',
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert a sample admin account
INSERT INTO users (name, email, password, role) VALUES ('Admin', 'admin@campusfind.com', 'admin123', 'ADMIN');

-- Insert a sample student account
INSERT INTO users (name, email, password, role) VALUES ('John Doe', 'john@student.com', 'john123', 'STUDENT');

-- Insert some sample items
INSERT INTO items (user_id, item_name, category, type, location, date_reported, description, status) 
VALUES (2, 'Casio Calculator', 'Electronics', 'LOST', 'Library 2nd Floor', '2023-10-15', 'Black scientific calculator', 'ACTIVE');

INSERT INTO items (user_id, item_name, category, type, location, date_reported, description, status) 
VALUES (2, 'Blue Water Bottle', 'Personal', 'FOUND', 'Cafeteria', '2023-10-16', 'Milton blue bottle', 'ACTIVE');
