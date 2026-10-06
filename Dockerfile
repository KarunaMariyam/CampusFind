# Use official Tomcat 10 image with JDK 17
FROM tomcat:10.1-jdk17

# Remove default ROOT application
RUN rm -rf /usr/local/tomcat/webapps/ROOT

# Copy our compiled .war file to be the ROOT web application
COPY target/CampusFind.war /usr/local/tomcat/webapps/ROOT.war

# Expose port 8080
EXPOSE 8080

# Run Tomcat
CMD ["catalina.sh", "run"]
