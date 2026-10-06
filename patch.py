import os

base_dir = r"C:\Users\Karuna\Documents\Codex\CampusFind\src\main\webapp"

def replace_in_file(filepath, replacements):
    full_path = os.path.join(base_dir, filepath)
    if not os.path.exists(full_path):
        return
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Update index.jsp
replace_in_file("index.jsp", {
    "CampusFind": "CIT CampusFind",
    "Welcome to CIT CampusFind": "Welcome to Coimbatore Institute of Technology - Lost & Found",
})

# Update ecommerce.jsp
replace_in_file("ecommerce.jsp", {
    "CampusFind": "CIT CampusFind",
    "$20.00": "₹1,500",
    "$15.00": "₹600",
    "$3.00": "₹100"
})

# Update other JSPs to say CIT CampusFind
for jsp in ["login.jsp", "register.jsp", "dashboard.jsp", "report.jsp", "items.jsp", "item-details.jsp", "my-reports.jsp", "admin.jsp", "ajax-demo.jsp", "xml-demo.html", "php-demo.php"]:
    replace_in_file(jsp, {
        "CampusFind": "CIT CampusFind",
        "Student Dashboard": "CIT Student Dashboard"
    })

print("Patched all references to CIT and Indian Rupees.")
