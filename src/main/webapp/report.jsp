<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<% if(session.getAttribute("user") == null) { response.sendRedirect("login.jsp"); return; } %>
<!DOCTYPE html>
<html>
<head>
    <title>Report Item - CIT CampusFind</title>
    <link rel="stylesheet" type="text/css" href="css/style.css?v=8">
    <script>
        // HTML5 Canvas Image Resizer (Client-side compression)
        function processImage(event) {
            const file = event.target.files[0];
            if(!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    const canvas = document.createElement('canvas');
                    const MAX_WIDTH = 500;
                    const scaleSize = MAX_WIDTH / img.width;
                    canvas.width = MAX_WIDTH;
                    canvas.height = img.height * scaleSize;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    
                    const base64 = canvas.toDataURL('image/jpeg', 0.6); // Compress to 60%
                    document.getElementById('imageBase64').value = base64;
                    
                    const preview = document.getElementById('imgPreview');
                    preview.src = base64;
                    preview.style.display = 'block';
                }
                img.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }

        // Smart Template Generator
        function generateTemplate() {
            const category = document.querySelector('select[name="category"]').value;
            let template = "";
            if(category === 'Electronics') template = "Brand: \nColor: \nModel/Serial No: \nDistinguishing Marks (Scratches, Stickers): ";
            else if(category === 'Personal') template = "Brand/Material: \nColor: \nContents (if bag/wallet): \nUnique Features: ";
            else if(category === 'Documents') template = "Type of Document (ID, Notes): \nName on Document: \nDepartment/Year: ";
            else template = "Detailed Description: \nColor: \nWhere was it last seen: ";
            
            document.querySelector('textarea[name="description"]').value = template;
        }

        function toggleReward() {
            const type = document.querySelector('select[name="type"]').value;
            document.getElementById('rewardGroup').style.display = (type === 'LOST') ? 'block' : 'none';
        }
    </script>
</head>
<body>
    <nav><h2>CIT CampusFind</h2><a href="dashboard.jsp">Back to Dashboard</a></nav>
    <div class="container">
        <div class="card" style="max-width: 700px; margin: auto;">
            <h1 style="text-align:center;">Report an Item</h1>
            <p style="text-align:center; color:#7A6F66; margin-bottom:20px;">Provide detailed information or a photo to help identify it.</p>
            
            <form action="ReportItemServlet" method="POST" style="margin-top:20px;">
                <div class="form-group" style="display:flex; gap:15px;">
                    <div style="flex:1;">
                        <label>Item Name</label>
                        <input type="text" name="itemName" required placeholder="e.g. Blue Dell Laptop">
                    </div>
                    <div style="flex:1;">
                        <label>Type</label>
                        <select name="type" onchange="toggleReward()">
                            <option value="LOST">I Lost Something</option>
                            <option value="FOUND">I Found Something</option>
                        </select>
                    </div>
                </div>

                <div class="form-group" style="display:flex; gap:15px;">
                    <div style="flex:1;">
                        <label>Category</label>
                        <select name="category" onchange="generateTemplate()">
                            <option value="Electronics">Electronics 💻</option>
                            <option value="Personal">Personal Items 🎒</option>
                            <option value="Documents">Documents 📚</option>
                            <option value="Other">Other ✨</option>
                        </select>
                    </div>
                    <div style="flex:1;">
                        <label>Location (Lost/Found at)</label>
                        <input type="text" name="location" required placeholder="e.g. Main Canteen">
                    </div>
                </div>

                <!-- Reward Section -->
                <div class="form-group" id="rewardGroup">
                    <label>Reward Offered (Optional)</label>
                    <input type="text" name="reward" placeholder="e.g. ₹500 or Coffee treat!">
                </div>

                <!-- Photo Section -->
                <div class="form-group" style="background:#FDF9F2; padding:20px; border:2px dashed #D8D0C1; border-radius:8px; text-align:center;">
                    <label style="font-size:18px; color:#943A29;">📸 Upload a Photo (Crucial for Identification)</label>
                    <input type="file" accept="image/*" onchange="processImage(event)" style="border:none; background:transparent; margin-top:10px;">
                    <input type="hidden" name="imageBase64" id="imageBase64">
                    <img id="imgPreview" src="" style="display:none; max-width:100%; max-height:300px; margin-top:15px; border-radius:8px; border:5px solid #FFF; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
                </div>

                <div class="form-group">
                    <label style="display:flex; justify-content:space-between; align-items:center;">
                        Description
                        <button type="button" onclick="generateTemplate()" style="background:transparent; border:1px solid #943A29; color:#943A29; border-radius:20px; padding:4px 10px; cursor:pointer; font-size:12px;">✨ Auto-Fill Template</button>
                    </label>
                    <textarea name="description" rows="5" required placeholder="Provide as much detail as possible..."></textarea>
                </div>

                <button type="submit" class="btn" style="width: 100%; font-size:18px; padding:15px;">Submit Report</button>
            </form>
        </div>
    </div>
    <script>generateTemplate(); toggleReward();</script>
</body>
</html>
