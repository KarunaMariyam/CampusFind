# Web Technology Lab Record: CampusFind Project

## Technologies & Implementation Mapping

### Frontend Technologies
1. **HTML:** Used to create the structural skeleton of the web application. E.g., forms in `report.jsp` and tables in `admin.jsp`.
2. **CSS:** Used in `style.css` to create the "Aesthetic Modern" UI, utilizing custom variables (`:root`), Flexbox, CSS Grid (`.dashboard-grid`), and responsive design media queries.
3. **JavaScript:** Used in `script.js` to handle client-side logic, such as the HTML5 Canvas image resizing for photo uploads and the dynamic category filter switching.
4. **DOM (Document Object Model):** Used heavily in `script.js` (e.g., `document.getElementById`, `innerHTML`) to dynamically inject new search results and image previews into the HTML without refreshing the page.
5. **AJAX:** Used to provide a seamless user experience. On `items.jsp`, typing in the search bar triggers an asynchronous AJAX request to the backend.
6. **Fetch API (for AJAX requests):** The modern JavaScript API (`fetch(...)`) is used in `script.js` to execute the AJAX calls to the `SearchItemServlet` and handle the JSON responses.

### Java & Backend Framework
7. **Java:** The core object-oriented language used for backend business logic, specifically in the models (e.g., `User.java`) and database utilities.
8. **Java Servlets:** Used as the server-side controllers. For example, `ReportItemServlet.java` handles POST requests from the report form, processes the parameters, and interacts with the database.
9. **JSP (JavaServer Pages):** Used as the view layer (e.g., `dashboard.jsp`, `items.jsp`). JSPs allow the dynamic embedding of Java logic (like `session.getAttribute`) directly inside the HTML via scriptlets (`<% %>`).

### Database & State Management
10. **MySQL:** The relational database management system used to persistently store tables for `users`, `items`, and `claims`.
11. **JDBC (Java Database Connectivity):** Used in `DBConnection.java` and all servlets (via `PreparedStatement`, `ResultSet`) to establish a connection to MySQL and execute secure SQL queries (CRUD operations).
12. **HTTP Session:** Used in `LoginServlet.java` (`request.getSession()`) to securely store the authenticated `User` object across different pages, enabling the dashboard authorization.
13. **Cookies:** Implemented in `LoginServlet.java` for the "Remember Me" functionality. An authentication token is saved to the user's browser via `new Cookie()`.

### XML Technologies (Campus Guidelines feature)
14. **XML:** Used in `guidelines.xml` to store the official university policies for lost and found items in a structured text format.
15. **DTD (Document Type Definition):** Implemented in `guidelines.dtd` to strictly define the legal building blocks (elements and attributes) of the XML file.
16. **XSD (XML Schema Definition):** Implemented in `guidelines.xsd` as a richer, XML-based alternative to DTD for validating the data types in the XML document.
17. **XML DOM Parser:** Used in `GuidelinesServlet.java` (`DocumentBuilderFactory`) to parse the physical XML file from the disk into a manipulatable tree structure in Java memory.
18. **XPath:** Used in `GuidelinesServlet.java` (`XPathFactory.newInstance()`) to directly query and extract specific rule text nodes from the XML DOM tree without writing loops.

### Build & Deployment Server
19. **Maven:** Used via the `pom.xml` file to automatically resolve and download project dependencies (like the MySQL JDBC driver and JSON libraries) and package the source code into a `.war` file.
20. **Apache Tomcat:** The Servlet Container / Web Server used to host, compile, and run the deployed `.war` application locally and in production.
