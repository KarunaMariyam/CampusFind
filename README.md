# CampusFind – A College Lost & Found Portal

## Problem Statement
Students frequently lose personal belongings on campus, while found items may not easily reach their owners. CampusFind provides a simple centralized portal for reporting, searching, and claiming lost and found items.

## Objectives
- Report lost/found items
- Search reported items
- Allow users to submit claims
- Track item status
- Demonstrate Web Technology concepts (HTML, CSS, JS, JSP, Servlets, DB, AJAX, XML, PHP)

## Technologies Used
- Frontend: HTML5, CSS3, JavaScript (Vanilla)
- Backend: Java Servlets, JSP (Jakarta EE / Tomcat 10)
- Database: MySQL
- Data Formats: XML, JSON (via AJAX)
- Misc: PHP

## Database Setup
1. Open MySQL Workbench or your terminal.
2. Run the `database.sql` script provided in the root folder.
   This will:
   - Create a database called `campusfind`
   - Create `users`, `items`, and `claims` tables
   - Insert sample user and admin accounts
3. Open `src/main/java/com/campusfind/util/DBConnection.java`
4. Update the `USER` and `PASSWORD` to match your local MySQL credentials.

## How to Run (Visual Studio Code)
1. Ensure you have the **Extension Pack for Java** and **Community Server Connectors** (or Tomcat for Java) extensions installed in VS Code.
2. Ensure you have **Apache Tomcat 10** downloaded and extracted on your PC.
3. Open the `CampusFind` folder in VS Code.
4. VS Code should recognize the `pom.xml` and configure the Java project. 
5. Right-click on your Tomcat server in the "Servers" tab (bottom left), add the CampusFind app, and click **Start**.
6. Alternatively, copy the project into the Tomcat `webapps` folder, or build a `.war` file via Maven (`mvn clean install`) and deploy.
7. Open your browser and navigate to: `http://localhost:8080/CampusFind/` (or the respective port you configure).
8. For the **PHP Demo**, since Tomcat does not natively run PHP, you must host `php-demo.php` using a PHP server (like XAMPP/WAMP/LAMP). Simply copy `php-demo.php` to your `htdocs` folder to test that particular page.

## Sample Login Credentials
- **Student Account:**
  - Email: `john@student.com`
  - Password: `john123`
- **Admin Account:**
  - Email: `admin@campusfind.com`
  - Password: `admin123`

## Web Technology Concepts Demonstrated
Here is a breakdown of how the lab syllabus requirements were met:

| Concept | Project Feature | File Reference |
|---------|-----------------|----------------|
| **HTML/CSS** | All user interfaces, structured forms, and clean stylesheet | `style.css`, all `.jsp` and `.html` files |
| **JavaScript** | Client-side validation for passwords on Registration | `script.js` -> `validateRegistration()` |
| **Java Servlets** | Backend controllers handling form submissions and logic | `LoginServlet.java`, `ReportItemServlet.java`, etc. |
| **JSP** | Dynamic web pages pulling session/DB data into views | `dashboard.jsp`, `items.jsp`, `my-reports.jsp` |
| **Cookies** | "Remember Me" functionality on the Login page | `LoginServlet.java`, `login.jsp` |
| **Session Management** | Restricting access to dashboard, tracking logged-in user | `LoginServlet.java`, `dashboard.jsp`, `LogoutServlet.java` |
| **Database Connectivity** | Connecting to MySQL via JDBC, CRUD operations | `DBConnection.java`, `database.sql` |
| **AJAX** | Live search demonstration for finding items instantly | `ajax-demo.jsp`, `script.js`, `SearchItemServlet.java` |
| **XML** | Parsing a sample `items.xml` using JavaScript DOM into a table | `xml-demo.html`, `data/items.xml`, `script.js` |
| **PHP** | A standalone demo processing a PHP array for a mock view | `php-demo.php` |
| **E-commerce** | "Campus Essentials" demo with Add to Cart / Order session | `ecommerce.jsp` |

## Testing Checklist
- [x] Registration
- [x] Duplicate registration error handling
- [x] Login & Session creation
- [x] Cookie ("Remember Me") creation
- [x] Report Lost / Found item
- [x] Browse items & View details
- [x] Submit claim
- [x] Admin Login -> Mark Returned & Delete
- [x] AJAX Search demo
- [x] XML Table generation demo
- [x] PHP standalone demo
- [x] Campus Essentials cart demonstration
- [x] Logout (Invalidates session)
