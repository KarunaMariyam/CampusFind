# 🏫 CampusFind - College Lost & Found Portal

CampusFind is a smart, aesthetically pleasing, and fully functional web application designed to help college students quickly report, track, and claim lost or found items on campus. 

This project was built from scratch utilizing a strict **Java EE** technology stack, demonstrating the seamless integration of frontend design with complex backend database operations, without relying on external UI frameworks or third-party cloud APIs.

## ✨ Key Features

- 📸 **Smart Photo Uploads:** Uses HTML5 Canvas and JavaScript to instantly compress images client-side into Base64 format before securely saving them in the database.
- 🔍 **Live AJAX Search & Filtering:** Instantly filter lost and found items by category or keyword using the Fetch API and DOM manipulation—no page reloads required.
- 💡 **Smart Connect (Auto-Match):** The backend leverages complex `JOIN` SQL queries to automatically cross-reference lost items with found items in the same category, alerting students of possible matches on their dashboard.
- 📳 **Secure Handover System (Pairing Code):** Generates a mathematically hashed 4-digit secret "Handover Code" for found items. The owner must type this code into the portal when meeting in person to officially resolve and pair the transaction.
- 🖨️ **Printable Missing Posters:** Uses CSS `@media print` rules to auto-generate a beautiful, printable A4 missing poster for any lost item directly from the browser.
- 📍 **Meetup Location Pinpointing:** Dynamically generates map coordinates based on text input to help students find each other on campus.
- 👑 **Admin God-Mode:** A comprehensive Admin Dashboard to monitor live campus statistics, enforce rules, securely ban spam accounts (cascading deletes), and manage all reports.

## 🛠️ Technology Stack (20-Point Checklist)

This project strictly adheres to standard Web Technologies:

### Frontend
* **HTML5** & **CSS3** (Modern variables, grids, flexbox)
* **JavaScript** & **DOM Manipulation**
* **AJAX** & **Fetch API**

### Backend & Database
* **Java** & **Java Servlets**
* **JSP (JavaServer Pages)**
* **MySQL** (Relational Database)
* **JDBC (Java Database Connectivity)**
* **HTTP Session** & **Cookies** (State Management & Auth)

### XML Processing
* **XML** (Campus Guidelines storage)
* **DTD** & **XSD** (Data Validation)
* **XML DOM Parser** & **XPath** (Data Extraction)

### Build & Deployment
* **Maven** (Dependency Management & Packaging)
* **Apache Tomcat** (Web Server Container)
* **Docker** (Cloud Deployment ready)

## 🚀 How to Run Locally

1. **Database Setup:** 
   Ensure MySQL is running. Create a database named `campusfind`.
2. **Configure Credentials:** 
   Update `src/main/java/com/campusfind/util/DBConnection.java` with your local MySQL `root` password.
3. **Build the Project:** 
   Run `mvn clean package` in the project root directory.
4. **Deploy:** 
   Copy the generated `CampusFind.war` from the `target/` directory to your Apache Tomcat `webapps/` folder.
5. **Start Server:** 
   Start Tomcat and visit `http://localhost:8080/CampusFind`.
